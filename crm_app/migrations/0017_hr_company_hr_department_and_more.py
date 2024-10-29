# Generated by Django 5.1.2 on 2024-10-29 05:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0016_paygrade_salarystepgrade_hr_employee_employment'),
    ]

    operations = [
        migrations.CreateModel(
            name='HR_Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='HR_Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_app.hr_company')),
            ],
        ),
        migrations.AlterField(
            model_name='employment',
            name='internal_organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_app.hr_department'),
        ),
        migrations.AlterField(
            model_name='hr_employee',
            name='internal_organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_app.hr_department'),
        ),
    ]
