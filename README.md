Face Recognition Based Attendance System
Overview

The Face Recognition Based Attendance System automates the process of student attendance using computer vision and face recognition technology. It accurately identifies students and marks their attendance in real-time, eliminating the need for manual entry.

Features

Real-time Face Recognition: Captures and matches student faces with pre-stored images for automated attendance marking.

Efficient Data Management: Stores student details and attendance records in CSV files for easy retrieval.

Scalable: The system can be expanded to add more students by updating the student database and images.

Technologies Used

Python

OpenCV (for face recognition)

NumPy

pandas (for managing data)

CSV (for storing student data and attendance records)

Installation

Clone the repository:

git clone https://github.com/your-username/face-recognition-attendance.git


Install the required dependencies:

pip install -r requirements.txt


Ensure you have a folder of student images for training the face recognition model.

Run the attendance system:

python attendance_system.py

How It Works

Training: The system first trains a model using student images stored in the student_images folder.

Face Recognition: When a student faces the camera, their face is captured, matched with the database, and their attendance is marked.

Data Management: Attendance is recorded in student_database.csv and subjects_database.csv.

Folder Structure

attendance_system.py: Main script for running the attendance system.

student_images/: Folder containing images of students for face recognition.

student_database.csv: Contains student information (name, ID, etc.).

subjects_database.csv: Stores information about subjects for attendance tracking.

trainer/: Contains the trained model and related files.

License

This project is licensed under the MIT License - see the LICENSE
 file for details.
