# Generated by Django 5.0.2 on 2024-03-11 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_school', '0006_rename_city_or_district_application_city_or_district_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
    ]