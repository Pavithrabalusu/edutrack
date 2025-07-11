from django.db import models

# Create your models here.
# teacher_dashboard/models.py
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    studytime = models.IntegerField()
    failures = models.IntegerField()
    absences = models.IntegerField()
    g1 = models.IntegerField()  # First period grade
    g2 = models.IntegerField()  # Second period grade
    g3 = models.IntegerField(null=True, blank=True)  # Final grade (optional)
    prediction = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"