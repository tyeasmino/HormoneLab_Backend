# Generated by Django 5.1.2 on 2025-03-18 04:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_reports'),
        ('hospital_authorities', '0003_alter_hospitalauthority_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reports',
            name='location',
        ),
        migrations.AlterField(
            model_name='reports',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='hospital_authorities.hospitalauthority'),
        ),
    ]
