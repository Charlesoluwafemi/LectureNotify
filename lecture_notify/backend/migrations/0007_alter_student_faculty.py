# Generated by Django 5.0.6 on 2024-06-17 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_alter_lecture_course_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='faculty',
            field=models.CharField(default='Unknown Faculty', max_length=250),
        ),
    ]
