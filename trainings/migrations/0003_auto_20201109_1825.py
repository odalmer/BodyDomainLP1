# Generated by Django 3.1.3 on 2020-11-09 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0002_auto_20201109_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='reps_s1',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='reps_s2',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='reps_s3',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='reps_s4',
            field=models.IntegerField(blank=True),
        ),
    ]