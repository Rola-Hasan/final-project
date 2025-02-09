# Generated by Django 5.1.4 on 2024-12-26 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InsuranceCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=200)),
                ('lastname', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=1, null=True)),
                ('phone_number', models.CharField(max_length=10)),
                ('address', models.TextField(blank=True, null=True)),
                ('rate', models.DecimalField(decimal_places=1, default=0.0, max_digits=4)),
                ('insurancecompany', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.insurancecompany')),
                ('specialization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.specialization')),
            ],
        ),
    ]
