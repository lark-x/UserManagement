# Generated by Django 5.0.6 on 2024-05-20 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_prettynumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='create_time',
            field=models.DateField(default=-28800, verbose_name='入职时间'),
        ),
    ]