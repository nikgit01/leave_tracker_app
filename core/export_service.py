import os 
import pandas as pd

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


