# Generated by Django 2.0.4 on 2018-07-25 02:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistics', '0003_auto_20180725_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readdetail',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]