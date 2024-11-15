# Generated by Django 5.1.2 on 2024-10-23 07:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0014_company_department_departmentbudget'),
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('budget_name', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('allocated_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(default='Pending', max_length=50)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_app.company')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_app.department')),
            ],
        ),
    ]
