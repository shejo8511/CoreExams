# Generated by Django 4.2.6 on 2023-10-24 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0011_examsample_diagnostic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examsample',
            name='sample_url',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Url-Muestra PNG'),
        ),
    ]
