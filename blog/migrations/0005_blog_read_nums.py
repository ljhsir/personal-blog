# Generated by Django 2.0.4 on 2018-07-24 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20180722_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='read_nums',
            field=models.IntegerField(default=0),
        ),
    ]