# Generated by Django 5.0 on 2023-12-08 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0002_alter_task_note_alter_task_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='note',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
