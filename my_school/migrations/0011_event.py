# Generated by Django 5.0.2 on 2024-03-25 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_school', '0010_remove_subject_description_course_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
            ],
        ),
    ]