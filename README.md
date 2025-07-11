# 🎓 EduPredict

**EduPredict** is a full-stack web application built with Django to help educators manage student records and predict academic performance using machine learning. It provides an intuitive dashboard for uploading and managing student data, along with predictive insights into performance categories like *Excellent*, *Good*, *Average*, and *Poor*.

---

## 🔍 Features

- ✅ Teacher dashboard to upload and manage student records
- 📂 Export functionality for generating reports
- 🧠 ML model for performance prediction using academic and behavioral data
- 🛠️ Built with Django, scikit-learn, pandas, and joblib
- 📄 SQLite database for easy local setup

---

## 🏗️ Tech Stack

- **Frontend**: HTML, CSS (via Django templates)
- **Backend**: Django
- **ML Tools**: scikit-learn, pandas, joblib
- **Database**: SQLite (default Django DB)

---

## 📁 Project Structure

edupredict/
│
├── edupredict/ # Django project settings
│ ├── init.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── teacher_dashboard/ # Main Django app
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── forms.py
│ ├── models.py
│ ├── signals.py
│ ├── tests.py
│ ├── urls.py
│ ├── views.py
│ ├── migrations/ # Database migrations
│ ├── ml_model/ # ML logic and model files
│ └── templates/ # HTML templates
│
├── media/ # Uploaded files (excluded from Git)
├── static/ # Static files (CSS, JS)
├── venv/ # Python virtual environment (excluded from Git)
├── .gitignore # Git ignore file
├── db.sqlite3 # SQLite database (excluded from Git)
├── manage.py # Django management script
└── requirements.txt # Python dependencies


---

## 🚀 Getting Started

## 🚀 Getting Started

1. Clone the repository  
```bash
git clone https://github.com/your-username/edupredict.git
cd edupredict
```

2. Set up a virtual environment  
```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

3. Install dependencies  
```bash
pip install -r requirements.txt
```

4. Apply migrations  
```bash
python manage.py migrate
```

5. Run the server  
```bash
python manage.py runserver
```

Then open your browser and go to:  
👉 **http://127.0.0.1:8000/**

---

## 🤖 Machine Learning Component

The `ml_model/` folder contains:

- Preprocessing scripts  
- A trained model saved using `joblib`  
- Logic for loading the model and predicting performance categories  

The ML model predicts one of the following categories:

- **Excellent**  
- **Good**  
- **Average**  
- **Poor**

These predictions are based on student academic and behavioral input features.

---

## 📤 Export Feature

Teachers can export student performance reports in **CSV** or **PDF** format (depending on implementation) for offline analysis and documentation.
