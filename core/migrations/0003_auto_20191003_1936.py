# Generated by Django 2.2.5 on 2019-10-03 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20191003_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='immobile',
            name='mutuo',
            field=models.CharField(default=3, max_length=2),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Mutuo',
        ),
    ]
