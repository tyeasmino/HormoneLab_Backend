# Generated by Django 5.1.7 on 2025-03-10 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_authorities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospitalauthority',
            name='hospital_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='hospitalauthority',
            name='phone',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
