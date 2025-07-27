from django.shortcuts import render

# Create your views here.
# teacher_dashboard/views.py
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UploadFileForm
from .forms import AddStudentForm
from .models import Student
from .ml_model.predictor import StudentPerformancePredictor
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from .forms import ProfileForm
from .models import Profile

import pandas as pd
import csv

@login_required
def upload_data_view(request):
    if request.method == 'POST':
        print("🟢 Form submitted.")
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("Processing file and saving student data...")
            file = request.FILES['file']
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file, sep=';')
                else:
                    df = pd.read_excel(file)
                
                predictor = StudentPerformancePredictor()
                
                for _, row in df.iterrows():
                    # Prepare student data for prediction
                    student_data = {
                        'age': row['age'],
                        'Medu': row['Medu'],
                        'Fedu': row['Fedu'],
                        'traveltime': row['traveltime'],
                        'studytime': row['studytime'],
                        'failures': row['failures'],
                        'famrel': row['famrel'],
                        'freetime': row['freetime'],
                        'goout': row['goout'],
                        'Dalc': row['Dalc'],
                        'Walc': row['Walc'],
                        'health': row['health'],
                        'absences': row['absences'],
                        'G1': row['G1'],
                        'G2': row['G2'],
                        'G3': row.get('G3', None),
                        # Add categorical variables
                        'school': row['school'],
                        'sex': row['sex'],
                        'address': row['address'],
                        # ... add other categorical columns as needed
                    }
                    
                    prediction = predictor.predict_performance(student_data)
                    first = row.get('firstname', '')
                    last = row.get('lastname', '')
                    name = f"{first} {last}".strip() or f"Student {row.name}"

                    Student.objects.create(
                        teacher=request.user,
                        name=name,
                        age=row['age'],
                        studytime=row['studytime'],
                        failures=row['failures'],
                        absences=row['absences'],
                        g1=row['G1'],
                        g2=row['G2'],
                        g3=row.get('G3', None),
                        prediction=prediction
                    )

                    print(f"Saving: {name}, Prediction: {prediction}")
                return redirect('teacher_dashboard:dashboard')
            except Exception as e:
                form.add_error(None, f"Error processing file: {str(e)}")
    else:
        form = UploadFileForm()
    return render(request, 'upload_data.html', {'form': form})


# Authentication

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  # ✅ correct way
            login(request, user)
            return redirect('teacher_dashboard:dashboard')  # ✅ ensure this URL name exists
        else:
            messages.error(request, "Invalid username or password")  # ✅ feedback to user
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# Dashboard
@login_required
def dashboard_view(request):
    students = Student.objects.filter(teacher=request.user)
    high_performers = students.filter(prediction__in=["Excellent", "Good"])
    medium_performers = students.filter(prediction="Average")
    low_performers = students.filter(prediction="Poor")

    avg_marks = students.aggregate(avg_marks=Avg('g3'))['avg_marks'] or 0
    avg_attendance = 100 - (students.aggregate(avg_absences=Avg('absences'))['avg_absences'] or 0)  # example logic
    total_students = students.count()

    return render(request, 'dashboard.html', {
        'students': students,
        'high_performers': high_performers,
        'medium_performers': medium_performers,
        'low_performers': low_performers,
        'avg_marks': round(avg_marks, 2),
        'avg_attendance': round(avg_attendance, 2),
        'total_students': total_students
    })


@login_required
def predictions_view(request):
    students = Student.objects.filter(teacher=request.user)  # show only logged-in teacher's students
    return render(request, 'predictions.html', {'students': students})


@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard:profile')  # make sure this name matches your URL
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {
        'form': form,
        'profile': profile
    })

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('teacher_dashboard:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})



# Student Management
@login_required
def student_list_view(request):
    pass

@login_required
def add_student_view(request):
    if request.method == 'POST':
        form = AddStudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.teacher = request.user

            # Predict performance
            predictor = StudentPerformancePredictor()
            student_data = {
                'age': student.age,
                'Medu': 2,  # or collect from form if needed
                'Fedu': 2,
                'traveltime': 1,
                'studytime': student.studytime,
                'failures': student.failures,
                'famrel': 4,
                'freetime': 3,
                'goout': 3,
                'Dalc': 1,
                'Walc': 1,
                'health': 4,
                'absences': student.absences,
                'G1': student.g1,
                'G2': student.g2,
                'G3': student.g3,
                'school': 'GP',
                'sex': 'F',
                'address': 'U'
            }
            prediction = predictor.predict_performance(student_data)
            student.prediction = prediction
            student.save()

            messages.success(request, f"Student '{student.name}' added with prediction: {prediction}")
            return redirect('teacher_dashboard:dashboard')
    else:
        form = AddStudentForm()

    return render(request, 'add_student.html', {'form': form})


@login_required
def student_detail_view(request, pk):
    pass

@login_required
def edit_student_view(request, pk):
    pass

@login_required
def delete_student_view(request, student_id):
    student = get_object_or_404(Student, id=student_id, teacher=request.user)
    if request.method == 'POST':
        student.delete()
    return redirect('teacher_dashboard:dashboard')

@login_required
def delete_all_students_view(request):
    if request.method == 'POST':
        Student.objects.filter(teacher=request.user).delete()
    return redirect('teacher_dashboard:dashboard')


# Reports
@login_required
def reports_view(request):
    pass

@login_required
def export_reports_view(request):
    students = Student.objects.filter(teacher=request.user)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Age', 'Study Time', 'Failures', 'Absences', 'G1', 'G2', 'G3', 'Prediction'])
    
    for student in students:
        writer.writerow([
            student.name,
            student.age,
            student.studytime,
            student.failures,
            student.absences,
            student.g1,
            student.g2,
            student.g3,
            student.prediction
        ])
    
    return response

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('teacher_dashboard:dashboard')
        else:
            messages.error(request, "Registration failed. Please try again.")
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})