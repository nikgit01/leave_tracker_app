import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from core import leave_logic


class LeaveTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Leave Tracker System")
        self.root.geometry("500x400")
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="Leave Tracker", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        # Buttons for operations
        btn_add_student = tk.Button(self.root, text="Add Student", width=30, command=self.add_student)
        btn_add_student.pack(pady=5)

        btn_update_email = tk.Button(self.root, text="Update Student Email", width=30, command=self.update_email)
        btn_update_email.pack(pady=5)

        btn_view_leave = tk.Button(self.root, text="View Leave Count", width=30, command=self.view_leave_count)
        btn_view_leave.pack(pady=5)

        btn_reset_leaves = tk.Button(self.root, text="Reset Leaves", width=30, command=self.reset_leaves)
        btn_reset_leaves.pack(pady=5)

        btn_mark_leave = tk.Button(self.root, text="Mark Leave", width=30, command=self.mark_leave)
        btn_mark_leave.pack(pady=5)

        btn_exit = tk.Button(self.root, text="Exit", width=30, command=self.root.quit)
        btn_exit.pack(pady=20)

    # ---------------- Functions mapped to leave_logic ----------------

    def add_student(self):
        roll_no = simpledialog.askinteger("Add Student", "Enter Roll No:")
        if roll_no is None:
            return
        name = simpledialog.askstring("Add Student", "Enter Name:")
        email = simpledialog.askstring("Add Student", "Enter Email:")
        subjects = simpledialog.askstring(
            "Add Student",
            "Enter Subjects (comma-separated, e.g., Math,Physics,Chemistry):"
        )

        if "" in (name, email, subjects):
            messagebox.showerror("Error","All field must have filled ")
            return

        subjects_list = [s.strip() for s in subjects.split(",")]
        df = leave_logic.load_data()
        if roll_no in df["RollNo"].values:
            messagebox.showerror("Erorr", "RollNo is Already exists ")
        else:
            leave_logic.add_student(roll_no, name, email, subjects_list)
            messagebox.showinfo("Success", f"Student {name} added successfully.")

    def update_email(self):
        roll_no = simpledialog.askinteger("Update Email", "Enter Roll No:")
        if roll_no is None:
            return
        email = simpledialog.askstring("Update Email", "Enter New Email:")
        if None in (roll_no, email):
            return
        
        leave_logic.update_student_email(roll_no, email)
        messagebox.showinfo("Success", "Email updated successfully.")

    def view_leave_count(self):
        roll_no = simpledialog.askinteger("View Leave Count", "Enter Roll No:")
        subject = simpledialog.askstring("View Leave Count", "Enter Subject (case-sensitive):")
        if None in (roll_no, subject):
            return
        result = leave_logic.view_leave_count(roll_no, subject)
        messagebox.showinfo("Leave Count", result)

    def reset_leaves(self):
        roll_no = simpledialog.askinteger("Reset Leaves", "Enter Roll No:")
        if roll_no is None:
            return
        df = leave_logic.load_data()
        if roll_no in df["RollNo"].values:
            name = df.loc[df["RollNo"]== roll_no, "Name"].iloc[0]
            leave_logic.reset_leaves(roll_no)
            messagebox.showinfo("Success", f"Leaves reset for Roll No {roll_no} Student name: {name}")
        else:
            messagebox.showwarning("Invalid RollNo", "RollNo does not exists")

    def mark_leave(self):
        roll_no = simpledialog.askinteger("Mark Leave", "Enter Roll No:")
        if roll_no is None:
            return
        subject = simpledialog.askstring("Mark Leave", "Enter Subject (case-sensitive):")
        if None in (roll_no, subject):
            return
        leave_logic.mark_leave(roll_no, subject)
        df = leave_logic.load_data()


        messagebox.showinfo("Success", f"Leave marked for Roll No {roll_no} in {subject}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LeaveTrackerGUI(root)
    root.mainloop()
