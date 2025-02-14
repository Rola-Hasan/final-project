# Generated by Django 5.1.4 on 2025-02-13 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_alter_doctor_governorate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
