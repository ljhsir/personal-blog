# Generated by Django 2.0.4 on 2018-07-24 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_readnums'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['created_time']},
        ),
    ]
