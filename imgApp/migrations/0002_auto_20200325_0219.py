# Generated by Django 3.0.4 on 2020-03-25 02:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imgApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagemodel',
            old_name='preset',
            new_name='preset_gray_or_poster_or_solar_or_none',
        ),
    ]