# Generated by Django 5.0.6 on 2024-06-15 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_remove_lecture_description_remove_lecture_title_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecture',
            name='date',
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='time',
        ),
        migrations.AddField(
            model_name='lecture',
            name='course',
            field=models.CharField(default='Unknown Course', max_length=255),
        ),
        migrations.AddField(
            model_name='lecture',
            name='department',
            field=models.CharField(default='Unknown Department', max_length=255),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
