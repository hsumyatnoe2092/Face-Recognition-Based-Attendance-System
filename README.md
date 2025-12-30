Third Year Ai Project 

# Face Recognition Based Attendance System

## Project Overview

The **Face Recognition Based Attendance System** automates the process of student attendance tracking using advanced face recognition technology. The system captures real-time student images, compares them with pre-stored reference images, and automatically records attendance. This innovation reduces administrative tasks, enhances accuracy, and ensures efficient management of student attendance.

## Key Features

* **Real-time Face Recognition**: Utilizes cutting-edge computer vision algorithms for instant face detection and identity verification.
* **Automated Attendance Tracking**: Streamlines attendance logging by eliminating manual entry.
* **Scalable Architecture**: Designed to scale seamlessly as the student body grows, allowing easy addition of new student images.
* **Data Management**: Stores student information and attendance records in CSV format for simple data analysis and retrieval.
* **Error Handling**: Built-in error management ensures smooth operation even under suboptimal conditions.

## Technologies

* **Python 3**: The primary language for system development.
* **OpenCV**: Powers the face detection and recognition capabilities.
* **dlib**: Used for face recognition, complementing OpenCV.
* **NumPy**: Supports efficient numerical operations, especially for image processing.
* **pandas**: Manages data, storing student and attendance information in CSV files.
* **CSV**: Simplifies data storage for easy access and analysis.

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

1. **Training Phase**: The system trains a face recognition model using the images in the `student_images/` folder.
2. **Face Recognition**: As students enter the frame, the system captures and identifies their faces, matching them with the stored reference images.
3. **Attendance Recording**: After successful identification, the system records attendance in real-time in the `student_database.csv` file.
4. **Data Logging**: Attendance records are stored in `student_database.csv` and subject-specific data is saved in `subjects_database.csv`.

## Folder Structure

* `attendance_system.py`: Main script for running the system.
* `student_images/`: Directory for storing student images used for training.
* `student_database.csv`: CSV file containing student data (e.g., name, ID).
* `subjects_database.csv`: CSV file storing subject-related attendance data.
* `trainer/`: Contains model files and configuration for face recognition.

## Usage

After installation, run the `attendance_system.py` script to begin recording attendance. The system will automatically detect and identify students' faces, recording attendance in real-time.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for more details.

## Acknowledgements

* **OpenCV**: Used for face detection and recognition algorithms.
* **dlib**: Utilized for more accurate facial recognition.
* **NumPy** and **pandas**: Provide efficient data handling and processing.
* **Python**: Powers the entire system’s functionality.

---

Feel free to make further adjustments, or let me know if you'd like to update any additional details!
