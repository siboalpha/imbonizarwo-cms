# Generated by Django 4.0.3 on 2022-03-30 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_rename_desciption_activity_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='desciption',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='desciption',
            new_name='description',
        ),
    ]