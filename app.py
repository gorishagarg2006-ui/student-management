import streamlit as st
import sqlite3

# Database connection
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    course TEXT,
    marks REAL
)
""")
conn.commit()

st.title("Student Record Management System")
st.write("Manage Student Records using CRUD Operations")

menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)

# CREATE
if menu == "Add Student":
    st.subheader("Add New Student")

    name = st.text_input("Student Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    course = st.text_input("Course")
    marks = st.number_input("Marks", min_value=0.0, max_value=100.0)

    if st.button("Add Student"):
        cursor.execute(
            "INSERT INTO students(name, age, course, marks) VALUES(?,?,?,?)",
            (name, age, course, marks)
        )
        conn.commit()
        st.success("Student Added Successfully!")

# READ
elif menu == "View Students":
    st.subheader("All Student Records")

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    st.dataframe(data)

# UPDATE
elif menu == "Update Student":
    st.subheader("Update Student Record")

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    if data:
        student_id = st.selectbox(
            "Select Student ID",
            [row[0] for row in data]
        )

        cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
        student = cursor.fetchone()

        name = st.text_input("Name", student[1])
        age = st.number_input("Age", min_value=1, value=student[2])
        course = st.text_input("Course", student[3])
        marks = st.number_input("Marks", min_value=0.0, max_value=100.0,
                                value=float(student[4]))

        if st.button("Update Student"):
            cursor.execute("""
                UPDATE students
                SET name=?, age=?, course=?, marks=?
                WHERE id=?
            """, (name, age, course, marks, student_id))

            conn.commit()
            st.success("Student Updated Successfully!")
    else:
        st.info("No student records found.")

# DELETE
elif menu == "Delete Student":
    st.subheader("Delete Student Record")

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    if data:
        student_id = st.selectbox(
            "Select Student ID",
            [row[0] for row in data]
        )

        if st.button("Delete Student"):
            cursor.execute(
                "DELETE FROM students WHERE id=?",
                (student_id,)
            )
            conn.commit()
            st.success("Student Deleted Successfully!")
    else:
        st.info("No student records found.")

conn.close()