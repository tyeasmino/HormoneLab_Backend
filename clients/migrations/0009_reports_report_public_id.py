# Generated by Django 5.1.2 on 2025-04-07 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_reports_signed'),
    ]

    operations = [
        migrations.AddField(
            model_name='reports',
            name='report_public_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
