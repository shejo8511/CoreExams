# Generated by Django 4.2.6 on 2023-11-05 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0010_alter_company_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='logo',
        ),
        migrations.AddField(
            model_name='company',
            name='url',
            field=models.ImageField(blank=True, null=True, upload_to='media/logos/'),
        ),
    ]
