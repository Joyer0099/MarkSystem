# Generated by Django 2.1.2 on 2019-01-22 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MarkManagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='pointNumber',
            field=models.FloatField(default=0, verbose_name='分数'),
        ),
    ]