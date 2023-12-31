# Generated by Django 4.2.6 on 2023-10-15 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_alter_membership_create_by_and_more'),
        ('patient', '0003_remove_patient_date_exam'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientexam',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='company.company', verbose_name='Empresa'),
            preserve_default=False,
        ),
    ]
