from django.apps import AppConfig


class TeacherDashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'teacher_dashboard'

def ready(self):
    import teacher_dashboard.signals
