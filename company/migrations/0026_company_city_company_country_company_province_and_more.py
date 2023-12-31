# Generated by Django 4.2.6 on 2024-01-01 03:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0025_rename_provincie_city_province_alter_country_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='Ciudad', to='company.city', verbose_name='Ciudad'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='country',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='Pais', to='company.country', verbose_name='Pais'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='province',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='Provincia', to='company.province', verbose_name='Provincia'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Nombre Ciudad'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nombre Pais'),
        ),
        migrations.AlterField(
            model_name='province',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Nombre Provincia'),
        ),
        migrations.AddConstraint(
            model_name='city',
            constraint=models.UniqueConstraint(fields=('country', 'province', 'name'), name='unique_country_province_ciudad'),
        ),
        migrations.AddConstraint(
            model_name='province',
            constraint=models.UniqueConstraint(fields=('country', 'name'), name='unique_country_province'),
        ),
    ]
