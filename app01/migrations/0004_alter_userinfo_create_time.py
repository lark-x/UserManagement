# Generated by Django 5.0.6 on 2024-05-20 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_alter_userinfo_create_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='create_time',
            field=models.DateField(verbose_name='入职时间'),
        ),
    ]
