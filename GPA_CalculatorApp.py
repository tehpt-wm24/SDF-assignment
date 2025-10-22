from tkinter import *
from tkinter import messagebox, ttk

class GPA_CalculatorApp():
    def __init__(self):
        super().__init__()
        self.student_id = None
        self.password = None
        self.courses = []
        self.base_font_size = 16
        self.dynamic_font = ('Arial', self.base_font_size)
        self.bg_colour = '#E0FFFF' # Light Cyan colour
        self.create_login()

    def on_close(self,window):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit the GPA Calculator?"):
            messagebox.showinfo("Quit", "Thanks for using the GPA Calculator!")
            window.destroy()


    # Dynamic font resizing
    def resize_fonts(self, window):
        def adjust(event = None):
            width = window.winfo_width()
            height = window.winfo_height()
            new_font_size = max(self.base_font_size, min(width, height) // 50)
            self.dynamic_font = ('Arial', new_font_size)
            for widget in window.winfo_children():
                if isinstance(widget, (Label, Button, Entry, Radiobutton, ttk.Combobox)):
                    widget.config(font = self.dynamic_font)
        window.bind("<Configure>", adjust)
        adjust()

    def create_login(self):
        # Create a login to set up student ID and password
        self.login_window = Tk()
        self.login_window.title("Student Login")
        self.login_window.geometry("400x600")
        self.login_window.configure(bg = self.bg_colour)

        # Calculate screen dimensions
        screen_height = self.login_window.winfo_screenheight()
        screen_width = self.login_window.winfo_screenwidth()
        window_height = 600
        window_width = 400

        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)

        self.login_window.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')
        self.login_window.state('zoomed')

        self.resize_fonts(self.login_window)
        
        Label(self.login_window, text = "Enter your Student ID: ", font = self.dynamic_font, bg = '#E0FFFF').grid(row = 0, column = 0, pady = 5, sticky = "W")
        self.student_id_var = StringVar()
        student_id_entry = Entry(self.login_window, textvariable = self.student_id_var)
        student_id_entry.grid(row = 0, column = 1, pady = 5)

        Label(self.login_window, text = "Create Password: ", font = self.dynamic_font, bg = '#E0FFFF').grid(row = 1, column = 0, pady = 5, sticky = "W")
        self.password_var = StringVar()
        password_entry = Entry(self.login_window, textvariable = self.password_var, show = "*")
        password_entry.grid(row = 1, column = 1, pady = 5)

        Label(self.login_window, text = "Re-enter Password: ", font = self.dynamic_font, bg = '#E0FFFF').grid(row = 2, column = 0, pady = 5, sticky = "W")
        self.confirm_password_var = StringVar()
        confirm_password_entry = Entry(self.login_window, textvariable = self.confirm_password_var, show = "*")
        confirm_password_entry.grid(row = 2, column = 1, pady = 5)

        Button(self.login_window, text = "Login", font = self.dynamic_font, command = self.validate_credentials, bg = '#00BFFF', fg = '#E0FFFF').grid(row = 3, column = 1, pady = 10)
        self.login_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close(self.login_window)) # closing program
        
        self.login_window.mainloop()

    def validate_credentials(self):
        # Retrieve input values
        student_id_input = self.student_id_var.get()
        password1 = self.password_var.get()
        password2 = self.confirm_password_var.get()

        # Validate student ID
        try: 
            student_id = int(student_id_input)
        except ValueError:
            messagebox.showerror("Error", "Student ID must be numeric.")
            return
            
        condition1 = len(password1) >= 8 and len(password1) <= 12
        condition2 = password1.isalnum()
        condition3 = any(c.isdigit() for c in password1) and any(c.isalpha()for c in password1)

        if not condition1:
            messagebox.showerror("Error","The password must have at least 8 characters and at most 12 characters.")
            return

        if not condition2:
            messagebox.showerror("Error", "The password must consist of only letters and digits.")
            return

        if not condition3:
            messagebox.showerror("Error", "The password must contain at least one letter and one digit.")
            return

        if password1 != password2:
            messagebox.showerror("Error", "The two passwords do not match each other...")
            return

        # Save credentials to a file
        with open("credentials.txt", "w") as file:
            file.write(f"{student_id}, {password1}\n")
            
        # Success
        messagebox.showinfo("Success", "Congratulations! Your password has been created successfully!")
        self.student_id = student_id
        self.password = password1
        self.login_window.destroy()
        self.create_main_window()

    def create_main_window(self):
        # Create a window and set a title
        window = Tk()
        window.title("GPA Calculator")
        window.state('zoomed')
        window.configure(background = '#E0FFFF')

        self.resize_fonts(window)

        # Create and add a frame for year selection
        frame1 = Frame(window)
        frame1.pack()
        frame1.configure(background = '#E0FFFF')

        # Create a variables to associate them with radio buttons for year
        self.year_var = IntVar()

        # Create two radio buttons and add them to frame1
        Label(frame1, text = "Select Year: ", font = self.dynamic_font, bg = '#E0FFFF').grid(row = 1, column = 0, pady = 5, sticky = W)
        rbYear1 = Radiobutton(frame1, text = "Year 1", variable = self.year_var, value = 1, font = self.dynamic_font, bg = '#E0FFFF')
        rbYear2 = Radiobutton(frame1, text = "Year 2", variable = self.year_var, value = 2, font = self.dynamic_font, bg = '#E0FFFF')

        # Organize radio buttons in frame1 using grid manager
        rbYear1.grid(row = 1, column = 1, padx = 5)
        rbYear2.grid(row = 1, column = 2, padx = 5)

        # Create and add another frame for semester selection
        frame2 = Frame(window)
        frame2.pack()
        frame2.configure(background = '#E0FFFF')

        # Create a variables to associate them with radio buttons for semester
        self.semester_var = IntVar()

        # Create three radio buttons and add them to frame2
        Label(frame2, text = "Select Semester: ", font = self.dynamic_font, bg = '#E0FFFF').grid(row = 2, column = 0, pady = 5, sticky = W)
        rbSem1 = Radiobutton(frame2, text = "Semester 1", variable = self.semester_var, value = 1, font = self.dynamic_font, bg = '#E0FFFF')
        rbSem2 = Radiobutton(frame2, text = "Semester 2", variable = self.semester_var, value = 2, font = self.dynamic_font, bg = '#E0FFFF')
        rbSem3 = Radiobutton(frame2, text = "Semester 3", variable = self.semester_var, value = 3, font = self.dynamic_font, bg = '#E0FFFF')

        # Organize radio buttons in frame2 using grid manager
        rbSem1.grid(row = 2, column = 1, padx = 5)
        rbSem2.grid(row = 2, column = 2, padx = 5)
        rbSem3.grid(row = 2, column = 3, padx = 5)

        # Create and add another frame for student ID entry
        frame3 = Frame(window)
        frame3.pack()
        frame3.configure(background = '#E0FFFF')

        # Create a label, an entry and a button and add them to frame3
        label = Label(frame3, text = "Enter your student ID: ", font = self.dynamic_font, bg = '#E0FFFF').grid(row = 1, column = 1, sticky = W)
        self.input_student_id = StringVar()
        Entry(frame3, textvariable = self.input_student_id, font = self.dynamic_font).grid(row = 1, column = 2)

        Label(frame3, text = "Enter your password: ", font = self.dynamic_font, bg = '#E0FFFF').grid(row = 2, column = 1, sticky = W)
        self.input_password = StringVar()
        input_password_entry = Entry(frame3, textvariable = self.input_password, show = "*", font = self.dynamic_font)
        input_password_entry.grid(row = 2, column = 2, padx = 5)

        submit_button = Button(frame3, text = "Submit", font = self.dynamic_font, command = self.validate_submission, bg = '#00BFFF', fg = '#E0FFFF')
        submit_button.grid(row = 3, column = 2, pady = 10)

        self.window.protocol("WM_DELETE_WINDOW", lambda: self.on_close(self.window))
        window.mainloop()
    
    def validate_submission(self):
        try:
            entered_id = int(self.input_student_id.get())
        except ValueError:
            messagebox.showerror("Error", "Student ID must be numeric.")
            return

        if entered_id != self.student_id:
            messagebox.showerror("Error", "Student ID does not match the one used during login.")
            return

        entered_password = self.input_password.get()        
        if entered_password != self.password:
            messagebox.showerror("Error", "Password does not match the one used during login.")
            return
            
        selected_year = self.year_var.get()
        selected_semester=self.semester_var.get()

        if selected_year == 0 or selected_semester == 0:
            messagebox.showwarning("Selection Missing", "Please select both Year and Semester.")
            return

        # Success message
        messagebox.showinfo("Submission Successful", f"Student ID: {self.student_id}\nYear: Year {selected_year}\nSemester: Semester {selected_semester}")

        # Open GPA entry window
        self.openGPAWindow()

    def openGPAWindow(self):
        # Mapping of year and semester to courses
        courses_map = {
            (1, 1): ["AMCS1013 Problem Solving and Programming", "AMCS1113 Computer Architecture", "AMIS1013 Systems Analysis and Design", "AMIS1012 Ethics in Computing", "AMMS1623 Calculus and Algebra", "AJEL1713 English for Tertiary Studies", "MPU-2123 Penghayatan Etika and Peradaban"],
            (1, 2): ["AACS3013 Database Development and Application", "AMCS1034 Software Development Fundamentals", "AAMS2613 Probability and Statistics"],
            (1, 3): ["AACS2034 Fundamentals of Computer Networks", "AACS2303 Introduction to Interface Design", "AACS2204 Object-Oriented Programming Techniques", "AMCS2093 Operating Systems", "AMMS2603 Discrete Mathematics", "AJEL1713 Academic English"],
            (2, 1): ["ECOQ Co-Curicular", "AMCS2034 Introduction to Data Structures and Algorithms", "AMCS2123 Systems and Programming Concepts", "AMCS2104 Fundamentals of Artificial Intelligence", "AACS3353 Mobile Application Dvelopment", "EGU2 Elective Course", "MPU-2302 Integrity and Anti-Corruption"],
            (2, 2): ["AMCS2094 Mini Project", "AMCS2103 Parallel and Distributed Computing", "AMIS1003 Introduction to Cybersecurity"],
            (2, 3): ["AMIT320A Industrial Training"]
        }

        # Get the selected year and semester
        year = self.year_var.get()
        semester = self.semester_var.get()

        if (year, semester) not in courses_map:
            messagebox.showerror("Error", "Invalid year and semester combination.")
            return

        # Create a new window for GPA calculation
        course_list = courses_map[(year, semester)] # Retrieve the course list
        gpa_window = Toplevel()
        gpa_window.title("Enter Grades and Credit Hours")
        gpa_window.configure(background = '#E0FFFF')
        self.resize_fonts(gpa_window)

        # Create a table for courses, grades, and credit hours
        Label(gpa_window, text = "", bg = '#E0FFFF').grid(row = 0, column = 0, padx = 10, pady = 5)
        Label(gpa_window, text = "Course", bg = '#E0FFFF').grid(row = 0, column = 1, padx = 10, pady = 5)
        Label(gpa_window, text = "Grade", bg = '#E0FFFF').grid(row = 0, column = 2, padx = 10, pady = 5)
        Label(gpa_window, text = "Credit Hours", bg = '#E0FFFF').grid(row = 0, column = 3, padx = 10, pady = 5)
        Label(gpa_window, text = "", bg = '#E0FFFF').grid(row = 0, column = 4, padx = 10, pady = 5)

        # Create variables to store courses data
        self.courses = []

        def delete_row(index):
            # Deletes a specific row
            for widget in self.courses[index]:
                widget.destroy() # Remove widgets from the window
            self.courses.pop(index) # Remove from the list

            # Update the remaining rows' numbering and delete buttons
            for i, row_widgets in enumerate(self.courses):
                row_widgets[0].config(text = f"{i + 1}") # Update row numbers
                row_widgets[4].config(command = lambda idx = i: delete_row(idx)) # Update delete button commands

        # Dynamically add rows for the courses
        for i, course_name in enumerate(course_list):
            no_label = Label(gpa_window, text = f"{i + 1}", font = self.dynamic_font, bg = '#E0FFFF')
            no_label.grid(row = i + 1, column = 0, padx = 10, pady = 5)

            # Pre-fill course names
            course_var = StringVar(value = course_name)
            course_label = Label(gpa_window, text = course_name, font = self.dynamic_font, width = 55, anchor = "w", bg = '#E0FFFF')
            course_label.grid(row = i + 1, column = 1, padx = 10, pady = 5, sticky = W)

            grade_var = StringVar()
            grade_dropdown = ttk.Combobox(gpa_window, textvariable = grade_var, values = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "F", "@"])
            grade_dropdown.grid(row = i + 1, column = 2, padx = 10, pady = 5)

            creditHours_var = IntVar()
            creditHours_entry = Entry(gpa_window, textvariable = creditHours_var, font = self.dynamic_font)
            creditHours_entry.grid(row = i + 1, column = 3, padx = 10, pady = 5)

            # Add delete button
            delete_button = Button(gpa_window, text = "×", command = lambda idx = i: delete_row(idx), bg = 'red')
            delete_button.grid(row = i + 1, column = 4, padx = 10, pady = 5)

            self.courses.append((no_label, course_label, grade_dropdown, creditHours_entry, delete_button)) # Store row variables

        next_row_for_buttons = len(course_list) + 1

        Button(gpa_window, text = "Calculate GPA", font = self.dynamic_font, command = self.calculateGPA, bg = 'yellow', fg = 'red').grid(row = next_row_for_buttons, column = 2, pady = 10, columnspan = 2)
        Button(gpa_window, text = "Clear all", font = self.dynamic_font, command = lambda: self.clearAll(gpa_window), bg = 'red', fg = 'yellow').grid(row = next_row_for_buttons, column = 3, pady = 10, columnspan = 2)

        # Add grading notes
        grading_notes = [
            "A+ (4.0000)  → HIGH DISTINCTION\n"
            "A (4.0000)    → HIGH DISTINCTION\n"
            "A- (3.6700)  → DISTINCTION\n"
            "B+ (3.3300) → MERIT\n"
            "B (3.0000)   → MERIT\n"
            "B- (2.6700)  → MERIT\n"
            "C+ (2.3300) → PASS\n"
            "C (2.0000)   → PASS\n"
            "F (0.0000)   → FAIL\n"
            "@ (0.0000)  → BARRED\n"
        ]

        Label(gpa_window, text = "Note on Gradings: ", font = ("Arial", 12, "bold"), bg = '#E0FFFF').grid(row = next_row_for_buttons + 1, column = 0, columnspan = 5, pady = 10, sticky = W)
        for i, note in enumerate(grading_notes):
            Label(gpa_window, text = note, font = ("Arial", 12), anchor = "w", justify = LEFT, bg = '#E0FFFF').grid(row = next_row_for_buttons + 2 + i, column = 0, columnspan = 5, sticky = W, padx = 20)

    def calculateGPA(self):
        total_creditHours = 0
        total_points = 0
    
        grade_points = {"A+": 4.0000, "A": 4.0000, "A-": 3.6700, "B+": 3.3300, "B": 3.0000, "B-": 2.6700, "C+": 2.3300, "C": 2.0000, "F": 0.0000, "@": 0.0000}

        course_details = [] # List to hold course details for the output

        try:
            for no_label, course_label, grade_dropdown, creditHours_entry, delete_button in self.courses:
                course_name = course_label.cget("text")
                grades = grade_dropdown.get().strip().upper()
                credit_hours = creditHours_entry.get().strip()
        
                if not grades or not credit_hours:
                    raise ValueError("Please fill in all grades and credit hours fields.")

                if grades not in grade_points:
                    raise ValueError(f"Invalid grade: {grades}")

                # Ensure that credit_hours is a valid positive integer
                if not credit_hours.isdigit():
                    raise ValueError(f"Credit hours for '{course_name}' must be a valid positive integer.")

                credit_hours = int(credit_hours)
                if credit_hours <= 0:
                    raise ValueError(f"Credit hours for '{course_name}' must be a positive number and cannot be zero or negative.")

                total_creditHours += credit_hours
                total_points += credit_hours * grade_points[grades]

                # Collect course details
                course_details.append(f"{course_name}: Grade = {grades}, Credit Hours = {credit_hours}\n")

            if total_creditHours == 0:
                raise ZeroDivisionError("No credit hours entered.")

            gpa = total_points / total_creditHours

            # Prepare the detailed result
            course_output = "\n".join(course_details)
            with open("gpa_results.txt", "a") as file:
                file.write(f"Student ID: {self.student_id}\nGPA: {gpa:.2f}\nDetails:\n{course_output}\n---\n")

            result_message = f"Your GPA is: {gpa:.2f}\n\nDetails:\n{course_output}"
            messagebox.showinfo("GPA Calculation", result_message)

        except(ValueError, ZeroDivisionError) as e:
            messagebox.showerror("Error", f"Error in GPA calculation: {str(e)}")
            
    def clearAll(self, window):
        for no_label, course_label, grade_dropdown, creditHours_entry, delete_button in self.courses:
            grade_dropdown.set("")
            creditHours_entry.delete(0, END)

# Create GUI
if __name__ == "__main__":
    app = GPA_CalculatorApp()