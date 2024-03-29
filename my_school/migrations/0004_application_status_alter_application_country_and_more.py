# Generated by Django 5.0.2 on 2024-03-10 21:21

import django.core.validators
import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_school', '0003_remove_student_report_student_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('received', 'Received'), ('review', 'Under Review'), ('admitted', 'Admitted')], default='received', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
        migrations.AlterField(
            model_name='application',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='phone_number',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$')]),
        ),
    ]
