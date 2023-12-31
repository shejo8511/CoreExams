# Generated by Django 4.2.6 on 2023-10-14 22:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeexam',
            name='create_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tyexm_create_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='typeexam',
            name='update_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tyexm_update_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
