# Generated by Django 4.2.16 on 2024-11-04 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0023_remove_partyskill_ofbiz_installation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partyskill',
            name='years_of_experience',
            field=models.FloatField(),
        ),
    ]
