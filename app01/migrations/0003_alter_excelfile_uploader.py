# Generated by Django 5.0.6 on 2024-06-07 07:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_alter_excelfile_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excelfile',
            name='uploader',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app01.admin', verbose_name='上传者'),
        ),
    ]