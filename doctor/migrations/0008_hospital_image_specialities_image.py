# Generated by Django 5.0.4 on 2024-11-20 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0007_alter_doctor_education_alter_doctor_experience_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='doctor/images/'),
        ),
        migrations.AddField(
            model_name='specialities',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='doctor/images/'),
        ),
    ]
