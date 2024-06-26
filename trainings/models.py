from django.db import models


class Training(models.Model):
    name = models.TextField(default='My weight training')
    time_start = models.DateTimeField(blank=True, null=True)
    time_end = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    plan = models.ForeignKey('TrainingPlan', null=True, on_delete=models.SET_NULL)


class Exercise(models.Model):
    training = models.ForeignKey('Training', on_delete=models.CASCADE)
    name = models.TextField(default='Exercise')
    weight_kg = models.FloatField(blank=True, null=True)
    weight_per = models.TextField(blank=True, null=True)
    series = models.IntegerField(blank=True, null=True)
    reps = models.JSONField(blank=True, null=True)

class TrainingPlan(models.Model):
    name = models.TextField()
    exercises = models.JSONField()
    """ exercises es una table de diccionario por ejemplo:,
        exercises = [{'name': 'pushup', 'weight_kg': 5, 
                      'weight_per': 'total', 'series': 3},
                      {'name': 'hammer', 'weight_kg': 5, 
                      'weight_per': 'per hand', 'series': 3}]
    """
