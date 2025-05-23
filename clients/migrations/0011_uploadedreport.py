# Generated by Django 5.1.2 on 2025-04-09 21:06

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0010_remove_reports_report_public_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', cloudinary.models.CloudinaryField(max_length=255, verbose_name='file')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
