# Generated by Django 2.0.2 on 2018-04-18 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0002_auto_20180418_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pipeline',
            name='description',
            field=models.TextField(max_length=200),
        ),
    ]