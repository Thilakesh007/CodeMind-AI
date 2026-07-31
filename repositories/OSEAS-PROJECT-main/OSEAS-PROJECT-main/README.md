# 🎓 OSEAS – Online Student Engagement Analysis System

An AI-powered **real-time student engagement monitoring system** built with **Flask**, **MediaPipe FaceMesh**, **OpenCV**, and **JavaScript**. OSEAS analyzes students' attention and engagement during online learning sessions and provides live analytics through a faculty dashboard.

> **Python Version:** 3.10.10

---

## 📌 Features

- 👨‍🎓 Student Login & Authentication
- 🎥 Real-time FaceMesh Detection (Browser-side)
- 👀 Eye Tracking & Head Pose Estimation
- 📊 Live Attention & Engagement Analysis
- 📈 Faculty Dashboard with Analytics
- 📝 Attendance Tracking
- 📄 Session Report Generation
- 💾 CSV-based Data Storage
- 🏗 Modular Flask Architecture

---

## 🛠 Tech Stack

### Backend
- Python 3.10.10
- Flask
- Flask Blueprints
- OpenCV
- NumPy
- Pandas

### Frontend
- HTML5
- CSS3
- JavaScript
- Jinja2 Templates
- MediaPipe FaceMesh

### Database
- CSV Storage

### AI Technologies
- MediaPipe FaceMesh
- Eye Tracking
- Head Pose Estimation
- Attention Score Calculation
- Engagement Score Calculation

---

# 📁 Project Structure

```
OSEAS-PROJECT/
│
├── app.py                         # Flask WSGI Entry Point
├── run.py                         # Local Development Server
├── config.py                      # Application Configuration
├── requirements.txt
├── README.md
├── .gitignore
│
├── ai/
│   ├── calculations/
│   │   ├── attention.py
│   │   ├── engagement.py
│   │   └── grading.py
│   │
│   └── mediapipe/
│       ├── engagement_detector.py
│       ├── eye_tracking.py
│       ├── face_mesh.py
│       └── head_pose.py
│
├── backend/
│   ├── auth/
│   │   └── authentication.py
│   │
│   ├── models/
│   │   ├── runtime_store.py
│   │   ├── session.py
│   │   └── student.py
│   │
│   ├── routes/
│   │   ├── api_routes.py
│   │   ├── auth_routes.py
│   │   ├── faculty_routes.py
│   │   ├── metrics_routes.py
│   │   └── student_routes.py
│   │
│   ├── services/
│   │   ├── attendance_service.py
│   │   ├── attention_service.py
│   │   ├── dashboard_service.py
│   │  ├── engagement_service.py
│   │  ├── metrics_service.py
│   │  ├── report_service.py
│   │  └── student_service.py
│   │
│   └── utils/
│       ├── constants.py
│       ├── helpers.py
│       ├── logger.py
│       └── validators.py
│
├── database/
│   ├── attendance_repository.py
│   ├── csv_repository.py
│   ├── database.py
│   └── session_repository.py
│
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── faculty.html
│       └── login.html
│
├── data/
│   ├── attendance.csv
│   └── session_report.csv
│
├── logs/
│   └── app.log
│
└── tests/
    ├── test_ai.py
    ├── test_database.py
    ├── test_routes.py
    └── test_services.py
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/Thilakesh007/OSEAS-PROJECT.git
```

Move into the project directory

```bash
cd OSEAS-PROJECT
```

Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python run.py
```

The application will start at

```
http://127.0.0.1:5050
```

---

# 🔑 Demo Credentials

### Student

```
Username : student1
Password : student123
```

### Faculty

```
Username : faculty1
Password : faculty123
```

---

# 📊 Available Routes

| Route | Method | Description |
|---------|---------|------------|
| `/login` | GET, POST | Login Page |
| `/logout` | GET | Logout User |
| `/` | GET | Student Dashboard |
| `/start` | GET | Start Session |
| `/stop` | GET | Stop Session |
| `/faculty` | GET | Faculty Dashboard |
| `/data` | GET | Retrieve Student Data |
| `/metrics` | POST | Submit Engagement Metrics |

---

# 🧠 AI Workflow

```
Camera Input
      │
      ▼
MediaPipe FaceMesh
      │
      ▼
Face Landmark Detection
      │
      ▼
Eye Tracking
      │
      ▼
Head Pose Estimation
      │
      ▼
Attention Score
      │
      ▼
Engagement Score
      │
      ▼
Faculty Dashboard
```

---

# 📈 Future Enhancements

- MySQL / PostgreSQL Integration
- JWT Authentication
- Docker Deployment
- REST API Documentation
- Cloud Deployment (AWS / Azure)
- Deep Learning-Based Emotion Detection
- Voice Emotion Recognition
- Student Performance Prediction
- PDF Report Generation
- Real-Time Notifications

---

# 👨‍💻 Developer

**Thilakesh S**

B.Tech – Artificial Intelligence & Data Science

GitHub: https://github.com/Thilakesh007

---

# 📄 License

This project is developed for educational and research purposes.

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.
