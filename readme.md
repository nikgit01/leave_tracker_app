# Leave Tracker Application

A simple **Leave Tracking System** with a **Tkinter GUI** and **Excel backend** for managing student leave records.  
This project allows teachers/admins to mark leaves, update student emails, and send email notification easily.

---

##  Features

- **Mark Leave** → Select roll number & subject, and mark a student’s leave.  
- **Show Student Name** → Displays the student’s name along with roll number when marking leave.  
- **View Leave Count** → Check how many leaves a student has taken in a specific subject.  
- **Update Student Email** → Modify student email addresses directly from the app.  
- **Reset Leaves** → Reset all leave records.  
- **Excel Backend** → All records are stored in `data/leave_records.xlsx`.  
- **Email Reports** → Send leave reports to students via email.  

---

## Project Structure
    leave_tracker/
    ├── 
    ├── config/ # Configuration (email credentials, settings)
    ├── core/
    │ ├── email_service.py # Handles sending emails
    │ └── leave_logic.py # Main logic for leave tracking (Excel operations)
    ├── data/
    │ └── leave_records.xlsx # Excel sheet storing student records
    ├── main.py # TCL for terminal based 
    ├── gui.py # Tkinter GUI for the application
    ├── README.md # Project documentation
    └── requirements.txt # use pip install requirements.txt 


## Data Storage

### Student records are stored in Excel format at:
    data/leave_records.xlsx
**Columns in the Excel file:**
- Roll No
- Name
- Email
- Subject1, Subject2, … (Leave counts per subject)

# Author

## Nikhil Maddheshiya  
**nikhilside72@gmail.com**  
Instagram: **@nik.py.09**
