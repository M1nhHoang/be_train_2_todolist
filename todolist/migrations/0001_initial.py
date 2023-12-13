# Generated by Django 5.0 on 2023-12-08 02:51

import django_lifecycle
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(null=True)),
                ('delete_at', models.DateTimeField(null=True)),
                ('task_name', models.TextField(max_length=250)),
                ('note', models.TextField(max_length=500)),
                ('is_completed', models.BooleanField(default=False)),
                ('completed_on', models.DateTimeField(null=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
            bases=(django_lifecycle.LifecycleModelMixin, models.Model),
        ),
    ]
