# Generated by Django 5.1.4 on 2025-02-10 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_insurancecompany_governorate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='doctors/'),
        ),
    ]
