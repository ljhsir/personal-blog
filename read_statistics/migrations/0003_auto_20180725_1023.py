# Generated by Django 2.0.4 on 2018-07-25 02:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistics', '0002_auto_20180725_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readdetail',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]