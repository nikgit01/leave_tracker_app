
import pandas as pd
from .email_service import send_mail
from .db_service import get_connection



EXCEL_PATH = "data/leave_records.xlsx"


# ---------- temprory credentials and Thresholds

WARNING_LEVEL = 2
MAX_LEAVES = 3


# -----------------[ helper functions ]--------------------------
def load_data():
    return pd.read_excel(EXCEL_PATH)

def save_data(df):
    df.to_excel(EXCEL_PATH, index=False)

def subjects_in_file(df):
    return [ c for c in df.columns if c not in ["RollNo", "Name", "Email"]]






def update_student_email(roll_no, new_email):
    df = load_data()
    if roll_no not in df["RollNo"].values:
        print(f"!!  Student Not Found !!")
        return False
    df.loc[df["RollNo"]== roll_no, "Email"] = new_email
    save_data(df)
    print("----[ Email Updated !! ]-----")


def view_leave_count(roll_no, subject):
    df = load_data()
    if roll_no not in df["RollNo"].values:
        print(f"!!  Student Not Found !!")
        return
    leaves = int(df.loc[df["RollNo"]== roll_no, subject].iloc[0])
    name = df.loc[df["RollNo"] == roll_no, "Name"].iloc[0]
    return f"{name} RollNo: ({roll_no}) has {leaves} leaves in {subject}"

def reset_leaves(roll_no):
    df = load_data()
    if roll_no not in df["RollNo"].values:
        print("!! Student not found !!")
        return
    
    subs = subjects_in_file(df)
    df.loc[df["RollNo"] == roll_no, subs] = 0
    student = df.loc[df["RollNo"] == roll_no, "Name"].iloc[0]
    save_data(df)
    print(f"------ leave are reset for Student: {student}, RollNo: {roll_no}---------")



def delete_student(roll_no):
    df = load_data()
    if roll_no not in df["RollNo"].values:
        print("!! Student not found !!")
        return

    index_to_del = df[df["RollNo"] == roll_no].index
    df = df.drop(index_to_del)
    save_data(df)
    print(f"Roll No: {roll_no} was deleted successfully")


# --------------- [marking leave + email triggers] ---------------


def mark_leave(roll_no, subject):
    df = load_data()
    if roll_no not in df["RollNo"].values:
        print("!! student not found !!")
        return
    if subject not in df.columns:
        print("!! subject not found !!")
        return
    df.loc[df["RollNo"] == roll_no, subject] += 1
    leaves = int(df.loc[df["RollNo"] == roll_no, subject].iloc[0])
    name   = df.loc[df["RollNo"] == roll_no, "Name"].iloc[0]
    email  = df.loc[df["RollNo"] == roll_no, "Email"].iloc[0]
    save_data(df)
    print(f" Mark leave --> {name} | RollNo: {roll_no} | Subject: {subject}, Total leave: {leaves}")

    if leaves < WARNING_LEVEL:
        send_mail(email,
                f"Regarding to Leave (Subject-{subject})",
                f"Dear {name}, \n\nYou have taken leave in Subject-{subject}, \n[Subject- {subject}, Remaining leave- {MAX_LEAVES - leaves}].\n\n Kind Regards, Registrar Office.",)

    if leaves == WARNING_LEVEL or leaves == MAX_LEAVES:
        send_mail(email,
                f"Attendence Warning - {subject}",
                f"Dear {name},\n\nYou have taken {leaves} leaves in {subject}.\n\n You are allowed only {MAX_LEAVES}.\nPlease attend the upcoming classes to avoid being barred from exams.\n\n Kind Regards, Registrar Office. ")


    if leaves > MAX_LEAVES:
        send_mail(email,
                f"Attendance Alert - {subject}",
                f"Dear {name},\n\nYou have exceeded the maximum allowed leaves ({MAX_LEAVES}) in {subject}. You may not be allowed to appear for the exam.")
        
    
        


