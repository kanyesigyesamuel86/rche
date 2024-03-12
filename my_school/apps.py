from django.apps import AppConfig


class MySchoolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_school'

    def ready(self):
        import my_school.models

