import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="IntelliSQL",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Session State
# --------------------------------------------------
if "query_history" not in st.session_state:
    st.session_state.query_history = []

# --------------------------------------------------
# Advanced UI Styling
# --------------------------------------------------
st.markdown("""
<style>
body { background-color: #0b0f19; }

.main-title {
    font-size: 56px;
    font-weight: 900;
    background: linear-gradient(90deg, #00FF7F, #00C9FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
}

.sub-title {
    text-align: center;
    font-size: 22px;
    color: #b3b3b3;
    margin-bottom: 40px;
}

.hero {
    background: linear-gradient(135deg, #111827, #1f2937);
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.4);
}

.card {
    background: linear-gradient(145deg, #1a1f2e, #11141f);
    padding: 26px;
    border-radius: 18px;
    margin-bottom: 20px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.35);
}

.footer {
    text-align: center;
    color: #777;
    margin-top: 50px;
}
.sidebar-title {
    font-size: 22px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Load API Key
# --------------------------------------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("Google API Key not found. Check .env file.")
    st.stop()

genai.configure(api_key=API_KEY)

# --------------------------------------------------
# Prompt
# --------------------------------------------------
PROMPT = """
You are an expert in converting English questions to SQL queries.

Database:
Table name: STUDENTS
Columns: NAME, CLASS, MARKS, COMPANY

Rules:
- Return ONLY SQL query
- No explanation
- No markdown
- No backticks
"""

# --------------------------------------------------
# Gemini Function
# --------------------------------------------------
def get_response(question):
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content(PROMPT + "\nQuestion: " + question)
    return response.text.strip()

# --------------------------------------------------
# SQL Execution
# --------------------------------------------------
def read_query(sql, db="data.db"):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return rows, columns

# --------------------------------------------------
# Get overall stats (for Home page)
# --------------------------------------------------
def get_dashboard_stats():
    conn = sqlite3.connect("data.db")
    df = pd.read_sql_query("SELECT * FROM STUDENTS", conn)
    conn.close()
    return len(df), df["MARKS"].max(), round(df["MARKS"].mean(), 2)

# --------------------------------------------------
# Pages
# --------------------------------------------------
def page_home():
    st.markdown('<div class="main-title">IntelliSQL</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">AI-Powered Natural Language Database Analytics</div>', unsafe_allow_html=True)

    total, max_marks, avg_marks = get_dashboard_stats()

    st.markdown('<div class="hero"><h2>Ask Questions. Get Insights. Instantly.</h2><p>Powered by Gemini AI for intelligent database querying.</p></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Students", total)
    c2.metric("Highest Marks", max_marks)
    c3.metric("Average Marks", avg_marks)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="card"><h3>🤖 Intelligent Querying</h3><p>Ask questions in English and let AI generate SQL automatically.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h3>📊 Data Exploration</h3><p>Analyze performance, trends, and insights visually.</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="card"><h3>⚡ Real-Time Analytics</h3><p>Instant execution and visualization from SQLite database.</p></div>', unsafe_allow_html=True)

def page_about():
    st.markdown('<div class="main-title">About IntelliSQL</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>Project Overview</h3>
    IntelliSQL is an AI-powered database querying system that enables users to interact with structured data using natural language. 
    Instead of writing complex SQL queries manually, users can simply ask questions in plain English, and the system automatically 
    converts them into SQL using Google’s Gemini Large Language Model.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>Key Features</h3>
    • Natural Language to SQL conversion using Gemini AI  
    • Interactive dashboard with metrics and visual analytics  
    • Query history with quick re-execution  
    • Real-time database interaction using SQLite  
    • Data insights through charts and summary statistics  
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>Technologies Used</h3>
    Python • Streamlit • Google Gemini API • SQLite • Pandas
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>Use Case</h3>
    IntelliSQL helps students, analysts, and beginners explore data without prior SQL knowledge, making data analysis faster, easier, and more accessible.
    </div>
    """, unsafe_allow_html=True)

def page_query():
    st.markdown('<div class="main-title">Intelligent Query Assistance</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <b>Try these queries:</b><br>
    • Show all students<br>
    • Students working at INFOSYS<br>
    • Average marks<br>
    • Highest marks<br>
    • How many students are there
    </div>
    """, unsafe_allow_html=True)

    question = st.text_input("💬 Ask a question about student records")

    if st.button("🚀 Generate & Execute"):
        if not question:
            st.warning("Please enter a question.")
            return

        with st.spinner("Thinking with Gemini AI..."):
            sql_query = get_response(question)

            st.session_state.query_history.insert(
                0, {"question": question, "sql": sql_query}
            )

            st.subheader("Generated SQL")
            st.code(sql_query, language="sql")

            rows, columns = read_query(sql_query)
            df = pd.DataFrame(rows, columns=columns)

            upper_sql = sql_query.upper()
            m1, m2, m3 = st.columns(3)

            if "COUNT" in upper_sql:
                m1.metric("Total Students", int(df.iloc[0, 0]))
            if "MAX" in upper_sql:
                m2.metric("Highest Marks", int(df.iloc[0, 0]))
            if "AVG" in upper_sql:
                m3.metric("Average Marks", round(float(df.iloc[0, 0]), 2))

            st.subheader("Results")
            st.dataframe(df, use_container_width=True)

            if "AVG" in upper_sql or "MAX" in upper_sql:
                st.subheader("Visual Analytics")
                chart_df = df.T
                chart_df.columns = ["Marks"]
                st.bar_chart(chart_df)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
def sidebar():
    st.sidebar.markdown('<div class="sidebar-title">Navigation</div>', unsafe_allow_html=True)
    page = st.sidebar.radio("", ["Home", "About", "Intelligent Query Assistance"])

    st.sidebar.markdown("---")
    st.sidebar.subheader("Query History")

    if st.session_state.query_history:
        for i, item in enumerate(st.session_state.query_history[:5]):
            if st.sidebar.button(item["question"], key=f"history_{i}"):
                rows, columns = read_query(item["sql"])
                df = pd.DataFrame(rows, columns=columns)
                st.sidebar.success("Executed")
                st.dataframe(df)
    else:
        st.sidebar.info("No queries yet")

    return page

# --------------------------------------------------
# Main
# --------------------------------------------------
def main():
    page = sidebar()

    if page == "Home":
        page_home()
    elif page == "About":
        page_about()
    else:
        page_query()

    st.markdown('<div class="footer">© 2026 IntelliSQL | AI-Powered Analytics</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
