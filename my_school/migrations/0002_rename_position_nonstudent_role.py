# Generated by Django 5.0.2 on 2024-03-06 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_school', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nonstudent',
            old_name='position',
            new_name='role',
        ),
    ]
