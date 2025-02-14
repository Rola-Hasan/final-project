# Generated by Django 5.1.4 on 2025-02-10 07:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_alter_insurancecompany_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='insurancecompany',
            name='governorate',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.governorate'),
            preserve_default=False,
        ),
    ]
