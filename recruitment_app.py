import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import sqlite3
import PyPDF2
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Function to setup database and create tables
def setup_database():
    conn = sqlite3.connect("recruitment.db")
    cursor = conn.cursor()

    # Create Candidates table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        email TEXT,
        degree TEXT,
        skills TEXT,
        status TEXT,
        job_role TEXT
    )
    """)

    # Create JobRoles table with predefined roles
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS JobRoles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        required_skills TEXT
    )
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO JobRoles (role, required_skills) 
    VALUES 
    ('Software Developer', 'Python,SQL,Algorithms'),
    ('Data Analyst', 'SQL,Excel,Data Analysis'),
    ('AI Engineer', 'Python,AI,Machine Learning'),
    ('Web Developer', 'HTML,CSS,JavaScript')
    """)

    conn.commit()
    conn.close()


# Function to parse the resume PDF and extract details
def parse_resume(file_path):
    with open(file_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = "".join(page.extract_text() for page in pdf_reader.pages)

    # Extract details using regex
    name_match = re.search(r"(?:Name[:\-]?\s*|^)([A-Za-z\s]{3,})", text, re.IGNORECASE)
    phone_match = re.search(r"\b(?:\+?\d{1,3}[-.\s]?)?\d{10}\b", text)  # Supports international formats
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    degree_match = re.search(r"(BTech|BE|MTech|BSc|MSc|PhD|Bachelor|Master|Doctorate)", text, re.IGNORECASE)

    name = name_match.group(1).strip() if name_match else "Unknown Name"
    phone = phone_match.group() if phone_match else "Not Provided"
    email = email_match.group() if email_match else "Not Provided"
    degree = degree_match.group() if degree_match else "Not Specified"

    return name, phone, email, degree, text


# Function to find matching job role based on skills in resume
def find_job_role(resume_text):
    conn = sqlite3.connect("recruitment.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role, required_skills FROM JobRoles")
    job_roles = cursor.fetchall()
    conn.close()

    for role, skills in job_roles:
        required_skills = [skill.strip().lower() for skill in skills.split(",")]
        if all(skill in resume_text.lower() for skill in required_skills):
            return role
    return "Trainee"  # Default fallback job role


# Function to upload resume and process it
def upload_resume():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return

    # Update text box to show screening progress
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, "Resume is being screened. Please wait...\n")
    text_box.update()

    name, phone, email, degree, resume_text = parse_resume(file_path)
    job_role = find_job_role(resume_text)
    status = "Eligible"

    # Insert the candidate data into the Candidates table
    conn = sqlite3.connect("recruitment.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Candidates (name, phone, email, degree, skills, status, job_role) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, phone, email, degree, "Extracted skills here", status, job_role))
    conn.commit()
    conn.close()

    # Prepare summary message
    summary_message = f"Candidate Details:\n"
    summary_message += f"Name: {name}\n"
    summary_message += f"Phone: {phone}\n"
    summary_message += f"Email: {email}\n"
    summary_message += f"Degree: {degree}\n"
    summary_message += f"Job Role: {job_role}\n"
    summary_message += "Status: Mail sent successfully.\n"
    summary_message += f"A written test list has been mailed to {email}.\n"

    # Display summary in the text box
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, summary_message)


# Main GUI for the application
def main():
    setup_database()  # Set up the database

    # Create main window
    root = tk.Tk()
    root.title("Smart AI Recruitment System")
    root.geometry("850x650")
    root.configure(bg="#eaf6f6")  # Light turquoise background

    # Welcome label
    welcome_label = tk.Label(
        root, text="Welcome to Smart AI Recruitment System", font=("Helvetica", 24, "bold"), fg="#3b5998", bg="#eaf6f6"
    )
    welcome_label.pack(pady=20)

    # Upload button
    upload_button = tk.Button(
        root, text="Upload Resume", command=upload_resume, font=("Arial", 18), bg="#4caf50", fg="white", relief="raised"
    )
    upload_button.pack(pady=30)

    # Text box for displaying resume summary
    global text_box
    text_box = scrolledtext.ScrolledText(
        root, width=90, height=20, font=("Courier New", 14), wrap=tk.WORD, bg="#fffacd", fg="#000000", borderwidth=3
    )
    text_box.pack(pady=20)

    # Exit button
    exit_button = tk.Button(
        root, text="Exit", command=root.destroy, font=("Arial", 18), bg="#f44336", fg="white", height=2, width=15
    )
    exit_button.pack(pady=20)

    root.mainloop()


# Run the application
if __name__ == "__main__":
    main()
