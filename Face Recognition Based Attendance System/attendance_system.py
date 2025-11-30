import cv2
import os
import numpy as np
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import ttkthemes  # You'll need to install this: pip install ttkthemes

class AttendanceSystem:
    def __init__(self):
        # Initialize face recognition components
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Setup directories and database
        self.setup_directories()
        self.db_file = "student_database.csv"
        if not os.path.exists(self.db_file):
            pd.DataFrame(columns=['ID', 'Name']).to_csv(self.db_file, index=False)
        
        self.student_db = self.load_student_database()
        
        # Initialize GUI
        self.setup_gui()
        
    def setup_directories(self):
        """Create necessary directories if they don't exist"""
        for dir_name in ["student_images", "attendance", "trainer"]:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
        
        # Load trained model if exists
        self.model_path = "trainer/face_model.yml"
        if os.path.exists(self.model_path):
            try:
                self.recognizer.read(self.model_path)
                # Retrain the model when starting the program to ensure accuracy
                self.train_recognizer()
            except:
                # If there's any error loading the model, retrain it
                self.train_recognizer()
    
    def load_student_database(self):
        """Load student information from CSV"""
        student_db = {}
        if os.path.exists(self.db_file):
            df = pd.read_csv(self.db_file)
            for _, row in df.iterrows():
                student_db[str(row['ID'])] = row['Name']
        return student_db

    def setup_gui(self):
        """Setup the main GUI window with modern styling"""
        self.root = ttkthemes.ThemedTk(theme="arc")
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1024x768")
        self.root.configure(bg='#EDF2F7')

        # Create main header
        header_frame = ttk.Frame(self.root, style='Header.TFrame')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = ttk.Label(
            header_frame, 
            text="Face Recognition Attendance System",
            font=('Helvetica', 26, 'bold'),
            foreground='#1a73e8',
            style='Header.TLabel'
        )
        title_label.pack(pady=10)

        # Configure styles
        self.style = ttk.Style()
        
        # Button styling
        self.style.configure('Accent.TButton', 
                            font=('Helvetica', 12, 'bold'),
                            padding=10)
        
        # Other style configurations remain the same
        self.style.configure('TNotebook.Tab', 
                            padding=[12, 8], 
                            font=('Helvetica', 11, 'bold'))
        
        self.style.configure('Header.TFrame', background='#EDF2F7')
        self.style.configure('Header.TLabel', background='#EDF2F7')
        self.style.configure('Camera.TLabelframe', background='#FFFFFF')
        
        # Label styling
        self.style.configure('TLabel', 
                           font=('Helvetica', 11),
                           foreground='#2C3E50')  # Darker text color
        
        # Entry styling
        self.style.configure('TEntry', 
                           font=('Helvetica', 11))

        # LabelFrame styling
        self.style.configure('Info.TLabelframe.Label', 
                           font=('Helvetica', 12, 'bold'),
                           foreground='#2B6CB0')  # Darker blue
        
        self.style.configure('Info.TLabelframe', 
                           background='#FFFFFF',
                           foreground='#2B6CB0')

        # Create tabs with custom styling
        self.style.configure('TNotebook.Tab', padding=[12, 8], font=('Helvetica', 10))
        self.style.configure('Header.TFrame', background='#EDF2F7')
        self.style.configure('Header.TLabel', background='#EDF2F7')
        self.style.configure('Camera.TLabelframe', background='#FFFFFF')
        
        # Initialize subjects database BEFORE setting up tabs
        self.subjects_file = "subjects_database.csv"
        if not os.path.exists(self.subjects_file):
            pd.DataFrame(columns=['Subject Code', 'Subject Name']).to_csv(self.subjects_file, index=False)
        self.subjects_db = self.load_subjects_database()

        # Initialize admin credentials
        self.admin_credentials = {
            "admin": "password123"  # You can change this default username/password
        }

        # Create tabs
        self.tab_control = ttk.Notebook(self.root)
        self.attendance_tab = ttk.Frame(self.tab_control, style='Tab.TFrame')
        self.admin_tab = ttk.Frame(self.tab_control, style='Tab.TFrame')
        
        # Create admin section tabs (initially hidden)
        self.register_tab = ttk.Frame(self.tab_control, style='Tab.TFrame')
        self.subjects_tab = ttk.Frame(self.tab_control, style='Tab.TFrame')
        self.students_tab = ttk.Frame(self.tab_control, style='Tab.TFrame')
        self.records_tab = ttk.Frame(self.tab_control, style='Tab.TFrame')
        self.logout_tab = ttk.Frame(self.tab_control, style='Tab.TFrame')  # New logout tab
        
        # Add only attendance and admin tabs initially
        self.tab_control.add(self.attendance_tab, text='Take Attendance')
        self.tab_control.add(self.admin_tab, text='Admin')
        
        # Bind tab change event
        self.tab_control.bind('<<NotebookTabChanged>>', self.on_tab_change)
        
        self.tab_control.pack(expand=1, fill='both', padx=20, pady=10)
        
        # Setup all tabs
        self.setup_attendance_tab()
        self.setup_admin_tab()
        self.setup_register_tab()
        self.setup_subjects_tab()
        self.setup_records_tab()
        self.setup_students_tab()
        self.setup_logout_tab()  # Add setup for logout tab

    def setup_register_tab(self):
        """Setup the registration tab with improved layout"""
        # Create left panel for inputs
        input_frame = ttk.Frame(self.register_tab)
        input_frame.pack(side='left', padx=20, pady=20, fill='y')

        # Student ID input with label frame
        id_frame = ttk.LabelFrame(
            input_frame, 
            text="Student Information", 
            padding=15,
            style='Info.TLabelframe'
        )
        id_frame.pack(fill='x', pady=5)

        ttk.Label(
            id_frame, 
            text="Student ID:", 
            font=('Helvetica', 11, 'bold'),
            foreground='#2C3E50'
        ).pack(anchor='w', pady=5)
        self.student_id_var = tk.StringVar()
        ttk.Entry(id_frame, textvariable=self.student_id_var, width=30).pack(fill='x', pady=5)

        ttk.Label(
            id_frame, 
            text="Name:", 
            font=('Helvetica', 11, 'bold'),
            foreground='#2C3E50'
        ).pack(anchor='w', pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(id_frame, textvariable=self.name_var, width=30).pack(fill='x', pady=5)

        # Add buttons frame
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(fill='x', pady=20)
        
        # Create button container for side-by-side buttons
        button_container = ttk.Frame(btn_frame)
        button_container.pack(fill='x')
        
        # Register button
        register_btn = ttk.Button(
            button_container, 
            text="Register Student",
            command=self.start_registration,
            style='Accent.TButton'
        )
        register_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))

        # Retrain button
        retrain_btn = ttk.Button(
            button_container,
            text="Retrain Student",
            command=self.start_retraining,
            style='Accent.TButton'
        )
        retrain_btn.pack(side='left', fill='x', expand=True, padx=(5, 0))

        # Camera feed frame with white background - matching attendance tab
        camera_frame = ttk.LabelFrame(
            self.register_tab, 
            text="Camera Feed", 
            padding=10,
            style='Camera.TLabelframe'
        )
        camera_frame.pack(side='right', padx=20, pady=20, fill='both', expand=True)

        self.register_canvas = tk.Canvas(
            camera_frame,
            width=640,
            height=480,
            bg='#F7FAFC',  # Very light blue-gray
            highlightthickness=1,
            highlightbackground='#E2E8F0'  # Light gray border
        )
        self.register_canvas.pack(padx=10, pady=10)

        # Status label with custom styling
        self.register_status_label = ttk.Label(
            camera_frame,
            text="Waiting to start registration...",
            font=('Helvetica', 11, 'bold'),
            foreground='#2C3E50',
            anchor='center'
        )
        self.register_status_label.pack(pady=10)

    def setup_attendance_tab(self):
        """Setup the attendance tab with improved layout"""
        # Similar styling as register tab
        input_frame = ttk.Frame(self.attendance_tab)
        input_frame.pack(side='left', padx=20, pady=20, fill='y')

        subject_frame = ttk.LabelFrame(
            input_frame, 
            text="Attendance Details", 
            padding=15,
            style='Info.TLabelframe'
        )
        subject_frame.pack(fill='x', pady=5)

        ttk.Label(
            subject_frame, 
            text="Subject:", 
            font=('Helvetica', 11, 'bold'),
            foreground='#2C3E50'
        ).pack(anchor='w', pady=5)
        
        # Modified Combobox for subject selection with increased width and height
        self.subject_var = tk.StringVar()
        self.subject_combo = ttk.Combobox(
            subject_frame,
            textvariable=self.subject_var,
            width=40,  # Increased width
            state='readonly',
            font=('Helvetica', 12),  # Increased font size
            height=10  # Show up to 10 items in dropdown
        )
        self.subject_combo.pack(fill='x', pady=10)  # Increased padding

        # Configure style for combobox
        self.style.configure(
            'TCombobox',
            padding=5,
            selectbackground='#1a73e8',
            selectforeground='white'
        )

        # Configure dropdown list style
        self.root.option_add('*TCombobox*Listbox.font', ('Helvetica', 12))  # Dropdown font
        self.root.option_add('*TCombobox*Listbox.selectBackground', '#1a73e8')  # Selection background
        self.root.option_add('*TCombobox*Listbox.selectForeground', 'white')  # Selection text color
        self.root.option_add('*TCombobox*Listbox.background', 'white')  # Background color
        self.root.option_add('*TCombobox*Listbox.foreground', '#2C3E50')  # Text color
        self.root.option_add('*TCombobox*Listbox.selectMode', 'browse')
        self.root.option_add('*TCombobox*Listbox.relief', 'flat')
        # Add spacing between items
        self.root.option_add('*TCombobox*Listbox.spacing', 2)
        
        # Bind tab selection to update subjects
        self.tab_control.bind('<<NotebookTabChanged>>', self.on_tab_change)
        
        # Update subject choices initially
        self.update_subject_choices()

        # Start attendance button with ttk styling
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(fill='x', pady=20)
        
        start_btn = ttk.Button(
            btn_frame,
            text="Start Attendance",
            command=self.start_attendance,
            style='Accent.TButton'
        )
        start_btn.pack(fill='x')

        # Camera feed frame with white background
        camera_frame = ttk.LabelFrame(
            self.attendance_tab, 
            text="Camera Feed", 
            padding=10,
            style='Camera.TLabelframe'
        )
        camera_frame.pack(side='right', padx=20, pady=20, fill='both', expand=True)

        self.attendance_canvas = tk.Canvas(
            camera_frame,
            width=640,
            height=480,
            bg='#F7FAFC',  # Very light blue-gray
            highlightthickness=1,
            highlightbackground='#E2E8F0'  # Light gray border
        )
        self.attendance_canvas.pack(padx=10, pady=10)

        # Status label with custom styling
        self.status_label = ttk.Label(
            camera_frame,
            text="Waiting to start...",
            font=('Helvetica', 11, 'bold'),
            foreground='#2C3E50',
            anchor='center'
        )
        self.status_label.pack(pady=10)

    def setup_subjects_tab(self):
        """Setup the subjects management tab"""
        # Create left panel for inputs
        input_frame = ttk.Frame(self.subjects_tab)
        input_frame.pack(side='left', padx=20, pady=20, fill='y')

        # Subject input frame
        subject_input_frame = ttk.LabelFrame(
            input_frame,
            text="Add New Subject",
            padding=15,
            style='Info.TLabelframe'
        )
        subject_input_frame.pack(fill='x', pady=5)

        # Subject Code input
        ttk.Label(
            subject_input_frame,
            text="Subject Code:",
            font=('Helvetica', 11, 'bold'),
            foreground='#2C3E50'
        ).pack(anchor='w', pady=5)
        self.subject_code_var = tk.StringVar()
        ttk.Entry(subject_input_frame, textvariable=self.subject_code_var, width=30).pack(fill='x', pady=5)

        # Subject Name input
        ttk.Label(
            subject_input_frame,
            text="Subject Name:",
            font=('Helvetica', 11, 'bold'),
            foreground='#2C3E50'
        ).pack(anchor='w', pady=5)
        self.subject_name_var = tk.StringVar()
        ttk.Entry(subject_input_frame, textvariable=self.subject_name_var, width=30).pack(fill='x', pady=5)

        # Add Subject button
        add_btn = ttk.Button(
            subject_input_frame,
            text="Add Subject",
            command=self.add_subject,
            style='Accent.TButton'
        )
        add_btn.pack(fill='x', pady=10)

        # Subjects List
        list_frame = ttk.LabelFrame(
            self.subjects_tab,
            text="Subjects List",
            padding=15,
            style='Info.TLabelframe'
        )
        list_frame.pack(side='right', padx=20, pady=20, fill='both', expand=True)

        # Create Treeview for subjects list
        columns = ('Subject Code', 'Subject Name')
        self.subjects_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Set column headings
        for col in columns:
            self.subjects_tree.heading(col, text=col)
            self.subjects_tree.column(col, width=150)

        self.subjects_tree.pack(fill='both', expand=True)

        # Delete button
        delete_btn = ttk.Button(
            list_frame,
            text="Delete Selected Subject",
            command=self.delete_subject,
            style='Accent.TButton'
        )
        delete_btn.pack(pady=10)

        # Load existing subjects
        self.refresh_subjects_list()

    def setup_records_tab(self):
        """Setup the attendance records tab"""
        # Create split view
        left_frame = ttk.Frame(self.records_tab)
        left_frame.pack(side='left', fill='y', padx=20, pady=20)

        right_frame = ttk.Frame(self.records_tab)
        right_frame.pack(side='right', fill='both', expand=True, padx=20, pady=20)

        # Subjects list on the left
        subjects_frame = ttk.LabelFrame(
            left_frame,
            text="Subjects",
            padding=15,
            style='Info.TLabelframe'
        )
        subjects_frame.pack(fill='both', expand=True)

        # Create subjects listbox with increased width and custom font
        self.subjects_listbox = tk.Listbox(
            subjects_frame,
            font=('Helvetica', 11),
            width=40,  # Increased width
            selectmode='single',
            activestyle='none',
            bg='white',
            highlightthickness=1,
            highlightbackground='#E2E8F0',
            selectbackground='#1a73e8',  # Blue selection color
            selectforeground='white',
            relief='flat'
        )
        self.subjects_listbox.pack(fill='both', expand=True, pady=5)

        # Bind selection event
        self.subjects_listbox.bind('<<ListboxSelect>>', self.on_subject_select)

        # Title label for subject name and date - centered
        self.records_title = ttk.Label(
            right_frame,
            text="",
            font=('Helvetica', 14, 'bold'),
            foreground='#2C3E50'
        )
        self.records_title.pack(fill='x', pady=(0, 10))  # Changed to fill='x' for center alignment

        # Attendance records on the right
        records_frame = ttk.LabelFrame(
            right_frame,
            text="Attendance Records",
            padding=15,
            style='Info.TLabelframe'
        )
        records_frame.pack(fill='both', expand=True)

        # Create Treeview for attendance records
        columns = ('No', 'Student ID', 'Name', 'Time')
        self.records_tree = ttk.Treeview(records_frame, columns=columns, show='headings')
        
        # Set column headings and widths
        self.records_tree.heading('No', text='No.')
        self.records_tree.column('No', width=50, anchor='center')
        
        self.records_tree.heading('Student ID', text='Student ID')
        self.records_tree.column('Student ID', width=100)
        
        self.records_tree.heading('Name', text='Name')
        self.records_tree.column('Name', width=200)
        
        self.records_tree.heading('Time', text='Time')
        self.records_tree.column('Time', width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(records_frame, orient='vertical', command=self.records_tree.yview)
        self.records_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.records_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Update subjects list
        self.update_subjects_list()

    def load_subjects_database(self):
        """Load subjects from CSV"""
        subjects_db = {}
        if os.path.exists(self.subjects_file):
            df = pd.read_csv(self.subjects_file)
            for _, row in df.iterrows():
                subjects_db[str(row['Subject Code'])] = row['Subject Name']
        return subjects_db

    def add_subject(self):
        """Add a new subject to the database"""
        code = self.subject_code_var.get().strip()
        name = self.subject_name_var.get().strip()

        if not code or not name:
            messagebox.showerror("Error", "Please enter both Subject Code and Name")
            return

        if code in self.subjects_db:
            messagebox.showerror("Error", "Subject Code already exists")
            return

        # Update database
        df = pd.read_csv(self.subjects_file)
        new_row = pd.DataFrame([{'Subject Code': code, 'Subject Name': name}])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.subjects_file, index=False)

        self.subjects_db[code] = name
        self.refresh_subjects_list()
        self.update_subject_choices()
        self.update_subjects_list()

        # Clear inputs
        self.subject_code_var.set("")
        self.subject_name_var.set("")

        messagebox.showinfo("Success", "Subject added successfully!")

    def delete_subject(self):
        """Delete selected subject"""
        selected_item = self.subjects_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a subject to delete")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this subject?"):
            subject_code = self.subjects_tree.item(selected_item)['values'][0]
            
            # Update database
            df = pd.read_csv(self.subjects_file)
            df = df[df['Subject Code'] != str(subject_code)]
            df.to_csv(self.subjects_file, index=False)

            del self.subjects_db[str(subject_code)]
            self.refresh_subjects_list()
            self.update_subject_choices()
            self.update_subjects_list()
            messagebox.showinfo("Success", "Subject deleted successfully!")

    def refresh_subjects_list(self):
        """Refresh the subjects list in the treeview"""
        for item in self.subjects_tree.get_children():
            self.subjects_tree.delete(item)
        
        df = pd.read_csv(self.subjects_file)
        for _, row in df.iterrows():
            self.subjects_tree.insert('', 'end', values=(row['Subject Code'], row['Subject Name']))

    def update_subject_choices(self):
        """Update the subject choices in the attendance tab"""
        subjects = [f"{code} - {name}" for code, name in self.subjects_db.items()]
        # Add extra spaces to create visual separation between items
        formatted_subjects = ["Please Choose Subject"] + [f"{subject}\n" for subject in subjects]
        self.subject_combo['values'] = formatted_subjects
        self.subject_combo.set("Please Choose Subject")

    def start_registration(self):
        """Start the registration process"""
        student_id = self.student_id_var.get().strip()
        name = self.name_var.get().strip()

        if not student_id or not name:
            messagebox.showerror("Error", "Please enter both Student ID and Name")
            return

        self.register_student(student_id, name)

    def register_student(self, student_id, name):
        """Register a new student"""
        cap = cv2.VideoCapture(0)
        face_samples = 0
        max_samples = 20  # Changed from 5 to 20 photos

        self.register_status_label.config(text="Please move your face in different positions and angles...")

        while face_samples < max_samples:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, (200, 200))
                
                # Save face image
                img_name = f"student_images/{student_id}_{name}_{face_samples}.jpg"
                cv2.imwrite(img_name, face)
                
                face_samples += 1
                
                # Draw rectangle around face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"Captured: {face_samples}/{max_samples}", 
                          (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Add a small delay to allow time for position changes
                cv2.waitKey(100)

            # Update GUI
            self.update_camera_feed(frame, self.register_canvas)
            self.register_status_label.config(text=f"Capturing images: {face_samples}/{max_samples}")
            self.root.update()

        cap.release()

        # Update database
        df = pd.read_csv(self.db_file) if os.path.exists(self.db_file) else pd.DataFrame(columns=['ID', 'Name'])
        new_row = pd.DataFrame([{'ID': student_id, 'Name': name}])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.db_file, index=False)
        
        self.student_db[student_id] = name
        self.train_recognizer()
        self.refresh_students_list()
        
        self.register_status_label.config(text="Registration completed successfully!")
        messagebox.showinfo("Success", "Registration completed successfully!")

    def start_attendance(self):
        """Start taking attendance"""
        subject = self.subject_var.get().strip()  # Strip removes newline characters
        if not subject or subject == "Please Choose Subject":
            messagebox.showerror("Error", "Please select a subject")
            return

        # Extract subject code from the selection
        subject_code = subject.split(' - ')[0]

        if not os.path.exists(self.model_path):
            messagebox.showerror("Error", "No trained model found. Please register students first.")
            return

        self.take_attendance(subject_code)

    def take_attendance(self, subject):
        """Take attendance for a subject"""
        # Retrain the model before taking attendance to ensure accuracy
        self.train_recognizer()
        
        cap = cv2.VideoCapture(0)
        recognition_counts = {}
        attendance_marked = set()
        required_recognitions = 20  # Increased from 5 to 20 for better accuracy
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    face = gray[y:y+h, x:x+w]
                    face = cv2.resize(face, (200, 200))

                    try:
                        student_id, confidence = self.recognizer.predict(face)
                        student_id = str(student_id)

                        if confidence < 65:  # Decreased threshold for stricter matching
                            name = self.student_db.get(student_id, "Unknown")
                            
                            if student_id not in recognition_counts:
                                recognition_counts[student_id] = 0
                            recognition_counts[student_id] += 1
                            
                            if recognition_counts[student_id] >= required_recognitions and student_id not in attendance_marked:
                                self.mark_attendance(subject, student_id, name)
                                attendance_marked.add(student_id)
                                color = (0, 255, 0)  # Green for marked
                                label = f"{name} (Marked)"
                                
                                # Show success message and break the loop
                                messagebox.showinfo("Success", f"Attendance marked for {name}")
                                return
                            else:
                                color = (255, 165, 0)  # Orange for recognizing
                                label = f"{name} [{recognition_counts[student_id]}/{required_recognitions}]"
                        else:
                            color = (0, 0, 255)  # Red for unknown
                            label = "Unknown"

                        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                        cv2.putText(frame, label, (x, y-10),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                    except:
                        continue

                # Update GUI
                self.update_camera_feed(frame, self.attendance_canvas)
                self.root.update()

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            cap.release()
            self.attendance_canvas.delete("all")

    def mark_attendance(self, subject, student_id, name):
        """Record attendance in CSV file"""
        try:
            if not os.path.exists('attendance'):
                os.makedirs('attendance')
                
            date = datetime.now().strftime("%Y-%m-%d")
            time = datetime.now().strftime("%H:%M:%S")
            
            filename = f"attendance/{subject}_{date}.csv"
            
            if not os.path.exists(filename):
                df = pd.DataFrame(columns=['Student ID', 'Name', 'Time'])
            else:
                df = pd.read_csv(filename)
            
            if not df[(df['Student ID'] == str(student_id))].empty:
                return
            
            new_row = pd.DataFrame([{
                'Student ID': str(student_id),
                'Name': name,
                'Time': time
            }])
            
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(filename, index=False)
            
        except Exception as e:
            print(f"Error marking attendance: {e}")

    def train_recognizer(self):
        """Train the face recognizer"""
        faces = []
        ids = []
        
        # Load all training images
        for img_file in os.listdir("student_images"):
            if img_file.endswith(".jpg"):
                img_path = os.path.join("student_images", img_file)
                face_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                student_id = int(img_file.split("_")[0])
                
                if face_img is not None:  # Check if image was loaded successfully
                    face_img = cv2.resize(face_img, (200, 200))
                    faces.append(face_img)
                    ids.append(student_id)
        
        if faces:  # Only train if there are faces
            try:
                # Convert ids to numpy array
                ids = np.array(ids)
                
                # Train the recognizer
                self.recognizer.train(faces, ids)
                
                # Save the model
                self.recognizer.save(self.model_path)
                print("Model trained and saved successfully")
            except Exception as e:
                print(f"Error training model: {e}")
                # If training fails, try to delete the model file and train again
                if os.path.exists(self.model_path):
                    os.remove(self.model_path)
                self.recognizer = cv2.face.LBPHFaceRecognizer_create()
                self.recognizer.train(faces, ids)
                self.recognizer.save(self.model_path)

    def update_camera_feed(self, frame, canvas):
        """Update camera feed with improved scaling"""
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        
        # Scale to fit canvas while maintaining aspect ratio
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        # Calculate scaling factor
        scale_w = canvas_width / frame.width
        scale_h = canvas_height / frame.height
        scale = min(scale_w, scale_h)
        
        # Resize frame
        new_width = int(frame.width * scale)
        new_height = int(frame.height * scale)
        frame = frame.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        frame = ImageTk.PhotoImage(image=frame)
        canvas.create_image(
            canvas_width//2,
            canvas_height//2,
            anchor=tk.CENTER,
            image=frame
        )
        canvas.image = frame

    def start_retraining(self):
        """Start the retraining process"""
        student_id = self.student_id_var.get().strip()
        name = self.name_var.get().strip()

        if not student_id or not name:
            messagebox.showerror("Error", "Please enter both Student ID and Name")
            return

        # Verify student exists in database
        if student_id not in self.student_db:
            messagebox.showerror("Error", "Student ID not found. Please register the student first.")
            return

        # Delete existing training images for this student
        for img_file in os.listdir("student_images"):
            if img_file.startswith(f"{student_id}_"):
                os.remove(os.path.join("student_images", img_file))

        self.retrain_student(student_id, name)

    def retrain_student(self, student_id, name):
        """Retrain a student with new photos"""
        cap = cv2.VideoCapture(0)
        face_samples = 0
        max_samples = 20  # Increased to 20 samples for better accuracy

        self.register_status_label.config(text="Please move your face in different positions and angles...")

        while face_samples < max_samples:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, (200, 200))
                
                # Save face image
                img_name = f"student_images/{student_id}_{name}_{face_samples}.jpg"
                cv2.imwrite(img_name, face)
                
                face_samples += 1
                
                # Draw rectangle around face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"Captured: {face_samples}/{max_samples}", 
                          (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Update GUI
            self.update_camera_feed(frame, self.register_canvas)
            self.register_status_label.config(text=f"Capturing images: {face_samples}/{max_samples}")
            self.root.update()

            # Add a small delay to allow time for position changes
            cv2.waitKey(100)

        cap.release()

        # Retrain the recognizer
        self.train_recognizer()
        
        self.register_status_label.config(text="Retraining completed successfully!")
        messagebox.showinfo("Success", "Student retraining completed successfully!")

    def on_tab_change(self, event):
        """Handle tab change events"""
        current_tab = self.tab_control.select()
        
        # If admin tab is selected, show login dialog
        if current_tab == self.admin_tab:
            self.show_admin_sections()
            # If login failed, switch back to attendance tab
            if not self.tab_control.index(current_tab) > 1:
                self.tab_control.select(0)
        # If logout tab is selected, perform logout
        elif current_tab == self.logout_tab:
            self.logout_admin()
        
        # Update subject choices if on attendance tab
        if current_tab == self.attendance_tab:
            self.update_subject_choices()

    def update_subjects_list(self):
        """Update the subjects list in the records tab"""
        self.subjects_listbox.delete(0, tk.END)
        for code, name in self.subjects_db.items():
            # Add the subject with a blank line after it for spacing
            self.subjects_listbox.insert(tk.END, f"{code} - {name}")
            self.subjects_listbox.insert(tk.END, "")  # Add empty line for spacing

    def on_subject_select(self, event):
        """Handle subject selection in records tab"""
        selection = self.subjects_listbox.curselection()
        if not selection:
            return
        
        # Get selected subject code
        subject_text = self.subjects_listbox.get(selection[0])
        subject_code = subject_text.split(' - ')[0]
        
        # Clear current records
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        
        # Load attendance records for selected subject
        self.load_attendance_records(subject_code)

    def load_attendance_records(self, subject_code):
        """Load attendance records for a specific subject"""
        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Create filename for current date
        filename = f"attendance/{subject_code}_{current_date}.csv"
        
        # Update title with subject name and current date
        subject_name = self.subjects_db.get(subject_code, "Unknown Subject")
        
        # Format date for display (DD/MM/YYYY)
        try:
            date_obj = datetime.strptime(current_date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%d/%m/%Y")
        except:
            formatted_date = current_date
        
        # Update title
        self.records_title.config(
            text=f"{subject_name} - {formatted_date}",
            anchor='center'
        )
        
        # Clear previous records
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        
        # Load and display today's records if file exists
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            
            # Add records with row numbers
            for idx, row in enumerate(df.iterrows(), 1):
                values = (
                    idx,  # Row number
                    row[1]['Student ID'],
                    row[1]['Name'],
                    row[1]['Time']
                )
                self.records_tree.insert('', 'end', values=values)
        else:
            # If no attendance file exists for today
            self.records_title.config(
                text=f"No attendance records for {subject_name} on {formatted_date}",
                anchor='center'
            )

    def show_login_dialog(self):
        """Show login dialog and return True if authentication successful"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Admin Login")
        dialog.geometry("300x250")  # Made slightly taller for buttons
        dialog.transient(self.root)  # Make dialog modal
        dialog.grab_set()  # Make dialog modal
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        # Style
        dialog_frame = ttk.Frame(dialog, padding="20")
        dialog_frame.pack(fill='both', expand=True)

        ttk.Label(
            dialog_frame,
            text="Admin Login",
            font=('Helvetica', 14, 'bold'),
            foreground='#2C3E50'
        ).pack(pady=(0, 20))

        # Username
        ttk.Label(
            dialog_frame,
            text="Username:",
            font=('Helvetica', 11)
        ).pack(anchor='w')
        username_var = tk.StringVar()
        username_entry = ttk.Entry(dialog_frame, textvariable=username_var)
        username_entry.pack(fill='x', pady=(0, 10))

        # Password
        ttk.Label(
            dialog_frame,
            text="Password:",
            font=('Helvetica', 11)
        ).pack(anchor='w')
        password_var = tk.StringVar()
        password_entry = ttk.Entry(dialog_frame, textvariable=password_var, show='*')
        password_entry.pack(fill='x', pady=(0, 20))

        # Result variable
        result = {'success': False}

        def on_login():
            username = username_var.get().strip()
            password = password_var.get().strip()
            
            if username in self.admin_credentials and self.admin_credentials[username] == password:
                result['success'] = True
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Invalid username or password")
                username_entry.focus()

        def on_cancel():
            dialog.destroy()

        # Button frame for side-by-side buttons
        button_frame = ttk.Frame(dialog_frame)
        button_frame.pack(fill='x', pady=(0, 10))

        # Submit button
        submit_btn = ttk.Button(
            button_frame,
            text="Submit",
            command=on_login,
            style='Accent.TButton'
        )
        submit_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))

        # Cancel button
        cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            command=on_cancel,
            style='Accent.TButton'
        )
        cancel_btn.pack(side='left', fill='x', expand=True, padx=(5, 0))

        # Set focus to username entry
        username_entry.focus()
        
        # Bind Enter key to submit button
        dialog.bind('<Return>', lambda e: submit_btn.invoke())
        # Bind Escape key to cancel button
        dialog.bind('<Escape>', lambda e: cancel_btn.invoke())

        # Wait for dialog to close
        dialog.wait_window()
        return result['success']

    def show_admin_sections(self):
        """Show admin sections after successful login"""
        if self.show_login_dialog():
            # Hide attendance tab
            self.tab_control.hide(self.attendance_tab)
            
            # Add admin section tabs
            self.tab_control.add(self.register_tab, text='Register Student')
            self.tab_control.add(self.subjects_tab, text='Manage Subjects')
            self.tab_control.add(self.students_tab, text='View Students')
            self.tab_control.add(self.records_tab, text='Check Records')
            self.tab_control.add(self.logout_tab, text='Log out')  # Add logout tab
            
            # Remove the admin tab
            self.tab_control.hide(self.admin_tab)
            
            # Switch to register tab
            self.tab_control.select(self.register_tab)

    def setup_admin_tab(self):
        """Setup the admin tab with login functionality"""
        frame = ttk.Frame(self.admin_tab, padding="20")
        frame.pack(expand=True, fill='both')

        ttk.Label(
            frame,
            text="Admin Login Required",
            font=('Helvetica', 16, 'bold'),
            foreground='#2C3E50'
        ).pack(pady=(0, 20))

        ttk.Label(
            frame,
            text="Please login to access admin features:",
            font=('Helvetica', 11)
        ).pack(pady=(0, 10))

        login_btn = ttk.Button(
            frame,
            text="Login",
            command=self.show_admin_sections,
            style='Accent.TButton'
        )
        login_btn.pack(pady=10)

    def logout_admin(self):
        """Logout admin and hide admin sections"""
        # Remove admin section tabs
        for tab in [self.register_tab, self.subjects_tab, self.students_tab, 
                    self.records_tab, self.logout_tab]:  # Added logout_tab
            self.tab_control.hide(tab)
        
        # Show attendance and admin tabs again
        self.tab_control.add(self.attendance_tab, text='Take Attendance')
        self.tab_control.add(self.admin_tab, text='Admin')
        
        # Switch to attendance tab
        self.tab_control.select(0)

    def setup_students_tab(self):
        """Setup the students view tab"""
        # Create main frame
        main_frame = ttk.Frame(self.students_tab, padding="20")
        main_frame.pack(fill='both', expand=True)

        # Only keep the total count label
        self.student_count_label = ttk.Label(
            main_frame,
            text="Total: 0 students",
            font=('Helvetica', 12),
            foreground='#2C3E50'
        )
        self.student_count_label.pack(anchor='e', pady=(0, 10))  # Align right, add bottom padding

        # Create Treeview for students list
        columns = ('No', 'Student ID', 'Name')
        self.students_tree = ttk.Treeview(main_frame, columns=columns, show='headings')
        
        # Set column headings and widths
        self.students_tree.heading('No', text='No.', anchor='center')
        self.students_tree.column('No', width=50, anchor='center')
        
        self.students_tree.heading('Student ID', text='Student ID', anchor='center')
        self.students_tree.column('Student ID', width=150, anchor='center')
        
        self.students_tree.heading('Name', text='Name', anchor='center')
        self.students_tree.column('Name', width=300, anchor='w')  # 'w' for west/left alignment

        # Configure tags for different alignments
        self.students_tree.tag_configure('centered', anchor='center')
        self.students_tree.tag_configure('left_aligned', anchor='w')

        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=self.students_tree.yview)
        self.students_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.students_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Load students
        self.refresh_students_list()

    def refresh_students_list(self):
        """Refresh the students list in the treeview"""
        # Clear current items
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        # Load students from database
        if os.path.exists(self.db_file):
            df = pd.read_csv(self.db_file)
            
            # Add students with row numbers
            for idx, row in enumerate(df.iterrows(), 1):
                item = self.students_tree.insert('', 'end', values=(
                    idx,  # Row number
                    row[1]['ID'],
                    row[1]['Name']
                ))
                
                # Apply different alignments to each column
                self.students_tree.set(item, 'No', idx)  # Center aligned by column
                self.students_tree.set(item, 'Student ID', row[1]['ID'])  # Center aligned by column
                self.students_tree.set(item, 'Name', f" {row[1]['Name']}")  # Added space for left padding
            
            # Update total count
            self.student_count_label.config(text=f"Total: {len(df)} students")

    def setup_logout_tab(self):
        """Setup the logout tab"""
        frame = ttk.Frame(self.logout_tab, padding="20")
        frame.pack(expand=True, fill='both')

        ttk.Label(
            frame,
            text="Are you sure you want to logout?",
            font=('Helvetica', 14, 'bold'),
            foreground='#2C3E50'
        ).pack(pady=(0, 20))

        logout_btn = ttk.Button(
            frame,
            text="Logout",
            command=self.logout_admin,
            style='Accent.TButton'
        )
        logout_btn.pack(pady=10)

    def run(self):
        """Start the GUI application"""
        # Center window on screen
        self.root.update()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1024) // 2
        y = (screen_height - 768) // 2
        self.root.geometry(f"1024x768+{x}+{y}")
        
        self.root.mainloop()

if __name__ == "__main__":
    app = AttendanceSystem()
    app.run() 