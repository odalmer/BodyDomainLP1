# Generated by Django 3.1.3 on 2020-11-14 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0013_training_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingplan',
            name='name',
            field=models.TextField(),
        ),
    ]
