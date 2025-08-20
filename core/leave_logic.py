
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



def add_student(roll_no, name, email):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = "INSERT INTO students (roll_no, name, email, math, physics, chemistry, bio) VALUES (%s, %s, %s, 0, 0, 0, 0)"
        cursor.execute(query, (roll_no, name, email))
        conn.commit()

        send_mail(email,
                f"Enrollment Confirmation - Welcome to the [XYZ Program]",
                f"We are pleased to inform you that you have been successfully enrolled in the [XYZ Program / Course Name / Batch Name].\n\nYour enrollment details are as follows:\n    📌 Roll No   : [{roll_no}]\n    📌 Name: [{name}]\n    📌 Email: [{email}]\n    📌 Subjects: [Math, Physics, Chemistry, Bio]\n Please ensure that you attend the orientation session. Further details and class schedules will be shared soon.\n If you have any questions or need assistance, feel free to reply to this email.\n Once again, welcome aboard!\nBest regards,\nRegistrar Office\n")

        return True, "Student added successfully"
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

#----------------------  This method was changed [testing_branch] --------------------------------
def update_student_email(roll_no, new_email):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name FROM students WHERE roll_no = %s LIMIT 1", (roll_no,))
        result = cursor.fetchone()

        if not result:
            print("!! Student Not Found !!")
            return False, "!! Student Not Found !!"

        name = result[0]

        cursor.execute("UPDATE students SET email = %s WHERE roll_no = %s", (new_email, roll_no))
        conn.commit()

        print(f"----[ Email Updated for {name} (Roll No: {roll_no}) ]-----")
        return True, f"Email Updated for {name} (Roll No: {roll_no}"

    except Exception as e:
        print(f"[ERROR] Failed to update email: {e}")
        return False, f"[ERROR] Failed to update email: {e}"

    finally:
        cursor.close()
        conn.close()

#----------------------  This method was changed [testing_branch] --------------------------------
def view_leave_count(roll_no):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name, math, physics, chemistry, bio FROM students WHERE roll_no = %s", (roll_no,))
        result = cursor.fetchone()

        if not result:
            print("!! Student Not Found !!")
            return False, "!! Student Not Found !!"
        
        name, math, physics, chemistry, bio = result

        return True, (
            f"Leave Count for {name} (Roll No: {roll_no}):\n"
            f"Math: {math} leaves\n"
            f"Physics: {physics} leaves\n"
            f"Chemistry: {chemistry} leaves\n"
            f"Biology: {bio} leaves"
        )
    except Exception as e:
        print(f"[ERROR] Could not fetch leave data: {e}")
        return False, f"[ERROR] Could not fetch leave data: {e}"
    finally:
        cursor.close()
        conn.close()

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


def reset_leaves(roll_no):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name FROM students WHERE roll_no = %s", (roll_no,))
        result = cursor.fetchone()
        print(result)
        if not result:
            print("!! Student not found !!")
            return False, "!! Student not found !!"
        
        name = result[0]

        cursor.execute("""
            UPDATE students
            SET math = 0, physics = 0, chemistry = 0, bio = 0
            WHERE roll_no = %s
        """, (roll_no,))
        conn.commit()

        print(f"------ Leaves are reset for student: {name}, Roll No: {roll_no} ------")

    except Exception as e:
        print(f"[ERROR] Could not reset leaves: {e}")
        return False, f"[ERROR] Could not reset leaves: {e}"

    finally:
        cursor.close()
        conn.close()

#------- here the last night i have done--------------------!!!!!!!!!!!!!!!!!
# need to commit !!



#----------------------  This method was changed [testing_branch] --------------------------------
def delete_student(roll_no):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name, email FROM students WHERE roll_no = %s LIMIT 1", (roll_no,))
        result = cursor.fetchone()

        if not result:
            return False, f"Student with Roll No {roll_no} does not exist."

        name, email = result

        cursor.execute("DELETE FROM students WHERE roll_no = %s", (roll_no,))
        conn.commit()

        send_mail(
            email,
            f"Removal Notification - [XYZ Program]",
            f"Dear {name},\n\nWe wish to inform you that your enrollment with Roll No {roll_no} has been removed from our records for the [XYZ Program].\n"
            "If you believe this is a mistake or have any questions, please contact the administration.\n\n"
            "Best regards,\nRegistrar Office"
        )

        return True, f"Student with Roll No {roll_no} deleted successfully."

    except Exception as e:
        return False, str(e)

    finally:
        cursor.close()
        conn.close()



# --------------- [marking leave + email triggers] ---------------


def mark_leave(roll_no, subject):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name, email FROM students WHERE roll_no = %s LIMIT 1", (roll_no,))
        result = cursor.fetchone()

        if not result:
            return False, f"Student with Roll No {roll_no} does not exist."
        
        name, email = result


        if subject not in {"math", "physics", "chemistry", "bio"}:
            return False, f"Invalid subject: {subject}"

        cursor.execute(f"UPDATE students SET {subject} = {subject} + 1 WHERE roll_no = %s", (roll_no,))

        cursor.execute(f"SELECT {subject} FROM students WHERE roll_no = %s LIMIT 1", (roll_no,))
        leaves = cursor.fetchone()[0]

        conn.commit()

        print(f"Student: {name}, Roll no: {roll_no}, Marked Leave in {subject}.")

        # email trigering on basic of the leaves
        try:
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
                
        except Exception as e:
            print(f"Error in Email sending: {e}")

        finally:
            return True, f"Student: {name}, Roll no: {roll_no}, Marked Leave in {subject}."
    
    except Exception as e:
        print(f"[ERROR] Could not Mark as leaves: {e}")
        return False, f"[ERROR] Could not reset leaves: {e}"
    
    finally:
        cursor.close()
        conn.close()