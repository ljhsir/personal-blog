# Generated by Django 2.0.4 on 2018-07-24 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20180724_1733'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ('-created_time',)},
        ),
    ]
