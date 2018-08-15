# Generated by Django 2.0.4 on 2018-07-24 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blog_read_nums'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadNums',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_nums', models.IntegerField(default=0)),
                ('blog', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Blog')),
            ],
        ),
    ]