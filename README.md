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

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Django
- **ML Tools**: scikit-learn, pandas, joblib
- **Database**: SQLite (default Django DB)

---

## 📁 Project Structure

edupredict/
edupredict/ # Project settings
teacher_dashboard/ # Main app (models, views, forms, ML, templates)
 ├── migrations/
 ├── ml_model/
 └── templates/
 media/ # Uploaded files
 static/ # CSS, JS, images
 venv/ # Virtual environment
 manage.py # Django management script
 db.sqlite3 # SQLite DB
 requirements.txt # Python dependencies
.gitignore # Git ignore rules



---

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

Teachers can export student performance reports in **CSV** format for offline analysis and documentation.
