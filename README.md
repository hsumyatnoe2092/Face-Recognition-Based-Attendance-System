

---

# Face Recognition Based Attendance System

## Project Overview

The **Face Recognition Based Attendance System** automates the attendance tracking process using advanced face recognition technology. The system captures real-time student images, compares them with pre-stored reference images, and automatically records attendance. This solution reduces administrative overhead, improves accuracy, and ensures efficient management of student attendance.

## Key Features

* **Real-time Face Recognition**: Uses advanced computer vision algorithms for fast face detection and identity verification.
* **Automated Attendance Tracking**: Automates attendance logging, eliminating the need for manual entries.
* **Scalable Architecture**: Easily scalable to accommodate a growing number of students by adding new student images to the system.
* **Data Management**: Stores student information and attendance records in CSV files, allowing for easy retrieval and analysis.
* **Error Handling**: Robust error management ensures smooth operation under diverse conditions.

## Technologies

* **Python 3**: Core language for developing the system.
* **OpenCV**: Used for face detection and recognition.
* **dlib**: Enhances face recognition accuracy by providing facial landmarks detection.
* **NumPy**: Handles numerical operations necessary for image processing.
* **pandas**: Used for managing data, specifically student and attendance records.
* **CSV**: A simple and efficient file format for storing and retrieving data.

## Installation

To get started with the project, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/hsumyatnoe2092/face-recognition-attendance.git
   ```

2. **Install Dependencies**:
   Navigate to the project directory and install the required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare Student Images**:
   Collect student images for training the face recognition model. Ensure these images are placed in the `student_images/` folder.

4. **Run the System**:
   Launch the system by running the following command:

   ```bash
   python attendance_system.py
   ```

## System Workflow

1. **Training Phase**: The system first trains a face recognition model using the images in the `student_images/` directory.
2. **Face Recognition**: As students enter the frame, the system captures their faces and matches them with stored reference images to verify their identity.
3. **Attendance Recording**: Once a student is successfully identified, the system records their attendance in real-time in the `student_database.csv` file.
4. **Data Logging**: The attendance records are stored in the `student_database.csv` file, and subject-specific data is saved in `subjects_database.csv` for easy access.

## Folder Structure

* `attendance_system.py`: The main script for running the attendance system.
* `student_images/`: Directory where student images are stored for training the face recognition model.
* `student_database.csv`: CSV file containing student information (e.g., name, ID).
* `subjects_database.csv`: CSV file for tracking attendance for various subjects.
* `trainer/`: Contains model files and configuration related to face recognition training.

## Usage

Once the system is set up, run the `attendance_system.py` script to begin recording attendance. The system will automatically detect students' faces, verify their identities, and log attendance in real-time.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for more details.

## Acknowledgements

* **OpenCV**: For providing face detection and recognition functionalities.
* **dlib**: Used for facial landmark detection, improving face recognition accuracy.
* **NumPy** and **pandas**: Help with efficient data processing and management.
* **Python**: The core programming language for system development.

---

