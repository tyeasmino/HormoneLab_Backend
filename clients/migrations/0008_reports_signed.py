# Generated by Django 5.1.2 on 2025-04-07 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_delete_hospital'),
    ]

    operations = [
        migrations.AddField(
            model_name='reports',
            name='signed',
            field=models.BooleanField(default=False),
        ),
    ]
