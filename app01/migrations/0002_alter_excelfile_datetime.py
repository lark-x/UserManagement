# Generated by Django 5.0.6 on 2024-06-07 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excelfile',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='上传时间'),
        ),
    ]
