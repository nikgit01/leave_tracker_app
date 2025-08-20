import os 
import pandas as pd
from fpdf import FPDF
from .db_service import get_connection


def generate_unique_filename(base_path, base_name, ext):
    i=1

    file_path = os.path.join(base_path, f"{base_name}.{ext}")

    while os.path.exists(file_path):
        file_path = os.path.join(base_path, f"{base_name}{i}.{ext}")
        i+=1
    return file_path


def export_to_excel():
    folder = "data/excel_files"
    os.makedirs(folder, exist_ok=True)

    file_path = generate_unique_filename(folder, "leave_records", "xlsx")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT roll_no, name, email, math, physics, chemistry, bio FROM students")
        row = cursor.fetchall()

        columns = ["Roll No", "Name", "Email", "Math", "Physics", "Chemistry", "Biology"]
        df = pd.DataFrame(row, columns=columns)

        df.to_excel(file_path, index=False)
        print(f"Excel file imported to: {file_path}, Successfully.")
        return True, f"Excel file imported to: {file_path}, Successfully."

    except Exception as e:
        print(e)
        return False, f"Error exporting to Excel: {e}"
    
    finally:
        cursor.close()
        conn.close()


def export_pdf():
    folder = "data/pdf_files"
    os.makedirs(folder, exist_ok=True)

    file_path = generate_unique_filename(folder, "leave_records", "pdf")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT roll_no, name, email, math, physics, chemistry, bio FROM students")
        row = cursor.fetchall()

        columns = ["Roll No", "Name", "Email", "Math", "Physics", "Chemistry", "Biology"]
        df = pd.DataFrame(row, columns=columns)

        if df.empty:
            return False, "No student records available to export."
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, "Student Leave Records", ln=True, align='C')
        pdf.ln(10)

        # Define custom column widths
        col_widths = {
            "Roll No": 20,
            "Name": 40,
            "Email": 50,
            "Math": 20,
            "Physics": 20,
            "Chemistry": 20,
            "Biology": 20
        }

        # Table Header
        pdf.set_font("Arial", 'B', 10)
        for col in columns:
            pdf.cell(col_widths[col], 10, col, border=1, align='C')
        pdf.ln()

        # Table Rows
        pdf.set_font("Arial", size=10)
        for _, row in df.iterrows():
            pdf.cell(20, 10, str(row["Roll No"]), border=1)
            pdf.cell(40, 10, str(row["Name"]), border=1)
            pdf.cell(50, 10, str(row["Email"]), border=1)
            pdf.cell(20, 10, str(row["Math"]), border=1, align='C')
            pdf.cell(20, 10, str(row["Physics"]), border=1, align='C')
            pdf.cell(20, 10, str(row["Chemistry"]), border=1, align='C')
            pdf.cell(20, 10, str(row["Biology"]), border=1, align='C')
            pdf.ln()

        # Save PDF
        pdf.output(file_path)
        print(f"PDF file exported to: {file_path}, Successfully.")
        return True, f"PDF file exported to: {file_path}, Successfully."

    except Exception as e:
        print(e)
        return False, f"Error exporting to PDF: {e}"

    finally:
        cursor.close()
        conn.close()
