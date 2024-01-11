import tkinter as tk
from tkinter import ttk, messagebox
import requests

class GradeBookManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Grade Book Manager")

        # Variables
        self.roll_no = tk.StringVar()
        self.student_name = tk.StringVar()
        self.course_code = tk.StringVar()
        self.semester_session = tk.StringVar()
        self.instructor_name = tk.StringVar()
        self.credit_hours = tk.StringVar()
        self.department = tk.StringVar()
        self.result_approved = tk.BooleanVar(value=False)

        # Data for Treeview
        self.data = []

        # UI Components
        self.create_widgets()
        self.fetch_data_from_api()  # Fetch initial data from the API

    def create_widgets(self):
        # Main Frame
        main_frame = ttk.LabelFrame(self.master)
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # Labels
        label = ttk.Label(main_frame, text="Grade Book Manager", font=("Helvetica", 16))
        label.grid(row=0, column=0, columnspan=2, pady=10)

        # Student Details Frame
        student_frame = ttk.LabelFrame(main_frame, text="Student Info")
        student_frame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        roll_no_label = ttk.Label(student_frame, text="Roll No:")
        roll_no_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        roll_no_entry = ttk.Entry(student_frame, textvariable=self.roll_no)
        roll_no_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

        student_label = ttk.Label(student_frame, text="Student Name:")
        student_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        student_entry = ttk.Entry(student_frame, textvariable=self.student_name)
        student_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

        # Course Details Frame
        course_frame = ttk.LabelFrame(main_frame, text="Course Info")
        course_frame.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        course_label = ttk.Label(course_frame, text="Course Code:")
        course_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        course_entry = ttk.Entry(course_frame, textvariable=self.course_code)
        course_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

        semester_label = ttk.Label(course_frame, text="Semester/Session:")
        semester_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        semester_entry = ttk.Entry(course_frame, textvariable=self.semester_session)
        semester_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

        instructor_label = ttk.Label(course_frame, text="Instructor Name:")
        instructor_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        instructor_entry = ttk.Entry(course_frame, textvariable=self.instructor_name)
        instructor_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

        credit_hours_label = ttk.Label(course_frame, text="Credit Hours:")
        credit_hours_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        credit_hours_entry = ttk.Entry(course_frame, textvariable=self.credit_hours)
        credit_hours_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

        department_label = ttk.Label(course_frame, text="Department:")
        department_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        department_entry = ttk.Entry(course_frame, textvariable=self.department)
        department_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

        approval_checkbox = ttk.Checkbutton(main_frame, text="Result Approved", variable=self.result_approved)
        approval_checkbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

        # Buttons
        submit_button = ttk.Button(main_frame, text="Submit", command=self.submit_result_to_api)
        submit_button.grid(row=4, column=0, pady=10, padx=10, sticky=tk.W)

        confirm_button = ttk.Button(main_frame, text="Confirm Result", command=self.confirm_result)
        confirm_button.grid(row=5, column=0, pady=10, padx=10, sticky=tk.W)

        acknowledge_button = ttk.Button(main_frame, text="Acknowledge Result", command=self.acknowledge_result)
        acknowledge_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

        # Treeview Frame
        treeview_frame = ttk.LabelFrame(self.master)
        treeview_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W + tk.N)

        # Treeview
        columns = ("Roll No", "Student Name", "Course Code", "Semester/Session", "Instructor Name", "Credit Hours",
                   "Department", "Result Approved")
        self.treeview = ttk.Treeview(treeview_frame, columns=columns, show="headings", selectmode="browse")

        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100)  # Adjust the width as needed

        self.treeview.grid(row=0, column=0, padx=10, pady=10)
        self.treeview.bind("<ButtonRelease-1>", self.populate_entry_fields)  # Bind click event to populate fields

        # CRUD Buttons
        update_button = ttk.Button(treeview_frame, text="Update", command=self.update_data_to_api)
        update_button.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        delete_button = ttk.Button(treeview_frame, text="Delete", command=self.delete_data_from_api)
        delete_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        # Populate Treeview with data
        self.update_treeview()

    def fetch_data_from_api(self):
        api_url = "http://localhost:5000/results"  # Update with your API endpoint
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Check for errors
            data = response.json().get("results", [])
            self.data = data
            self.update_treeview()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"Error fetching data from API: {e}")

    def submit_result_to_api(self):
        if self.result_approved.get():
            data = {
                "roll_no": self.roll_no.get(),
                "student_name": self.student_name.get(),
                "course_code": self.course_code.get(),
                "semester_session": self.semester_session.get(),
                "instructor_name": self.instructor_name.get(),
                "credit_hours": self.credit_hours.get(),
                "department": self.department.get(),
                "result_approved": self.result_approved.get()
            }
            api_url = "http://localhost:5000/results"  # Update with your API endpoint
            try:
                response = requests.post(api_url, json=data)
                response.raise_for_status()  # Check for errors
                self.fetch_data_from_api()  # Refresh data from the API
                self.clear_entries()
                messagebox.showinfo("Submission", "Result submitted successfully!")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("API Error", f"Error submitting result to API: {e}")
        else:
            messagebox.showwarning("Submission Warning", "Please approve the result before submitting.")

    def confirm_result(self):
        if self.result_approved.get():
            message = (
                f"Result for {self.student_name.get()} (Roll No: {self.roll_no.get()}) "
                f"in {self.course_code.get()} ({self.semester_session.get()}) "
                f"confirmed!"
            )
            messagebox.showinfo("Confirmation", message)
        else:
            messagebox.showwarning("Confirmation Warning", "Please approve the result before confirming.")

    def acknowledge_result(self):
        if self.result_approved.get():
            message = (
                f"Result for {self.student_name.get()} (Roll No: {self.roll_no.get()}) "
                f"in {self.course_code.get()} ({self.semester_session.get()}) "
                f"acknowledged!"
            )
            messagebox.showinfo("Acknowledgment", message)
        else:
            messagebox.showwarning("Acknowledgment Warning", "Please approve the result before acknowledging.")

    def populate_entry_fields(self, event):
        selected_item = self.treeview.selection()
        if selected_item:
            values = self.treeview.item(selected_item, "values")
            if values and len(values) == 8:
                self.roll_no.set(values[0])
                self.student_name.set(values[1])
                self.course_code.set(values[2])
                self.semester_session.set(values[3])
                self.instructor_name.set(values[4])
                self.credit_hours.set(values[5])
                self.department.set(values[6])
                self.result_approved.set(values[7])

    def update_data_to_api(self):
        selected_item = self.treeview.selection()
        if selected_item:
            if self.validate_input():
                data = {
                    "roll_no": self.roll_no.get(),
                    "student_name": self.student_name.get(),
                    "course_code": self.course_code.get(),
                    "semester_session": self.semester_session.get(),
                    "instructor_name": self.instructor_name.get(),
                    "credit_hours": self.credit_hours.get(),
                    "department": self.department.get(),
                    "result_approved": self.result_approved.get()
                }
                roll_no = self.roll_no.get()
                api_url = f"http://localhost:5000/results/{roll_no}"  # Update with your API endpoint
                try:
                    response = requests.put(api_url, json=data)
                    response.raise_for_status()  # Check for errors
                    self.fetch_data_from_api()  # Refresh data from the API
                    self.clear_entries()
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("API Error", f"Error updating data to API: {e}")

    def delete_data_from_api(self):
        selected_item = self.treeview.selection()
        if selected_item:
            roll_no = self.roll_no.get()
            api_url = f"http://localhost:5000/results/{roll_no}"  # Update with your API endpoint
            try:
                response = requests.delete(api_url)
                response.raise_for_status()  # Check for errors
                self.fetch_data_from_api()  # Refresh data from the API
            except requests.exceptions.RequestException as e:
                messagebox.showerror("API Error", f"Error deleting data from API: {e}")

    def update_treeview(self):
        self.treeview.delete(*self.treeview.get_children())
        for item in self.data:
            self.treeview.insert("", "end", values=(
                item.get("roll_no", ""),
                item.get("student_name", ""),
                item.get("course_code", ""),
                item.get("semester_session", ""),
                item.get("instructor_name", ""),
                item.get("credit_hours", ""),
                item.get("department", ""),
                item.get("result_approved", "")
            ))

    def clear_entries(self):
        self.roll_no.set("")
        self.student_name.set("")
        self.course_code.set("")
        self.semester_session.set("")
        self.instructor_name.set("")
        self.credit_hours.set("")
        self.department.set("")
        self.result_approved.set(False)

    def validate_input(self):
        if not self.roll_no.get() or not self.student_name.get() or not self.course_code.get():
            messagebox.showwarning("Input Error", "Roll No, Student Name, and Course Code are required.")
            return False
        return True


def main():
    root = tk.Tk()
    app = GradeBookManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
