import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS STUDENTS (
    NAME TEXT,
    CLASS TEXT,
    MARKS INTEGER,
    COMPANY TEXT
)
""")

cursor.execute("DELETE FROM STUDENTS")

students = [
    ("Rahul Sharma", "BTech", 78, "TCS"),
    ("Priya Reddy", "MCom", 85, "INFOSYS"),
    ("Amit Kumar", "BSc", 67, "WIPRO"),
    ("Sneha Patel", "BTech", 92, "INFOSYS"),
    ("Arjun Verma", "BCom", 74, "HCL"),
    ("Neha Gupta", "MCom", 88, "TCS"),
    ("Rohit Singh", "BTech", 81, "ACCENTURE"),
    ("Anjali Mehta", "BSc", 69, "WIPRO"),
    ("Karan Malhotra", "BTech", 95, "GOOGLE"),
    ("Pooja Nair", "MCom", 84, "INFOSYS"),
    ("Vikram Das", "BCom", 72, "TCS"),
    ("Deepika Joshi", "BTech", 90, "AMAZON"),
    ("Manish Yadav", "BSc", 65, "HCL"),
    ("Kavya Iyer", "MCom", 87, "INFOSYS"),
    ("Sandeep Rao", "BTech", 79, "WIPRO")
]

cursor.executemany("INSERT INTO STUDENTS VALUES (?, ?, ?, ?)", students)

conn.commit()
conn.close()

print("Database created with updated student records.")
