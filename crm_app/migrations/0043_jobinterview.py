# Generated by Django 5.1.2 on 2024-11-12 06:41

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0042_jobinterviewtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobInterview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_secured_enum_id', models.CharField(blank=True, choices=[('INTR_RATNG_A', 'A (above 75%)'), ('INTR_RATNG_B', 'B (60-75%)'), ('INTR_RATNG_C', 'C (45-60%)'), ('INTR_RATNG_D', 'D (below 40%)')], max_length=20)),
                ('job_interview_result', models.CharField(choices=[('Pass', 'Pass'), ('Fail', 'Fail')], max_length=10)),
                ('job_interview_date', models.DateField(default=datetime.date.today)),
                ('job_interview_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_app.jobinterviewtype', to_field='jobinterviewType')),
                ('job_interviewee_party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interviews_as_interviewee', to='crm_app.hr_employee', to_field='employee_id')),
                ('job_interviewer_party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interviews_as_interviewer', to='crm_app.hr_employee', to_field='employee_id')),
                ('job_requisition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_app.jobrequisition')),
            ],
            options={
                'verbose_name': 'Job Interview',
                'verbose_name_plural': 'Job Interviews',
                'db_table': 'job_interview',
            },
        ),
    ]
