from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from trainings.models import Training, Exercise, TrainingPlan
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

def signup(request):
    if (request.method == 'GET'):
        return render(request, 'signup.html')
    else:
        if (request.POST['password1'] == request.POST['password2']):
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], email=request.POST['email'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('trainings')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'errorSignup': 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
            'error': 'Las contraseñas no coinciden'
        })

def signout(request):
    logout(request)
    return redirect('signup')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signup.html', {
                'error': 'Usuario o contraseña incorrecta'
            })
        else:
            login(request, user)
            return redirect('home')

def trainings_view(request):
    all_trainings = Training.objects.all()
    all_trainings = all_trainings[::-1]
    return render(
        request, 
        'trainings.html', 
        {'all_trainings': all_trainings}
        )
    

def single_training_view(request, training_id):
    training = Training.objects.get(id=training_id)
    exercises = Exercise.objects.filter(training__id=training_id)
    return render(
        request, 
        'single-training.html', 
        {'training': training, 'exercises': exercises}
        )


def record_training(request):
    new_training = Training()
    new_training.save()
    return HttpResponseRedirect(f'/edit-training/{new_training.id}/')


def edit_training_view(request, training_id):
    training = Training.objects.get(id=training_id)
    exercises = Exercise.objects.filter(training__id=training_id)
    training_plans = TrainingPlan.objects.all()
    return render(
        request,
        'edit-training.html',
        {'training': training, 'exercises': exercises, 'training_plans': training_plans}
    )


def start_training(request, training_id):
    training = Training.objects.get(id=training_id)
    training.time_start = timezone.now()
    training.save()
    return HttpResponseRedirect(f'/edit-training/{training_id}/')
    

def stop_training(request, training_id):
    # save the end time
    training = Training.objects.get(id=training_id)
    training.time_end = timezone.now()
    training.duration = training.time_end - training.time_start
    training.save()

    exercises = Exercise.objects.filter(training__id=training_id)
    for exercise in exercises:
        exercise.name = request.POST[f'name_{exercise.id}']
        exercise.weight_kg = request.POST[f'weight_kg_{exercise.id}']
        exercise.weight_per = request.POST[f'weight_per_{exercise.id}']

        for s in exercise.reps:
            exercise.reps[s] = request.POST[f'rep_{s}']

        exercise.save()

    return HttpResponseRedirect(f'/edit-training/{training_id}/')


def save_training(request, training_id):
    training = Training.objects.get(id=training_id)
    training.name = request.POST['name']
    training.save()  

    if training.plan:

        training_plan = training.plan
        training_plan = training_to_training_plan(training_id, training_plan)
        training_plan.save()

    return HttpResponseRedirect(f'/trainings/{training_id}/')


def delete_training(request, training_id):
    training = Training.objects.get(id=training_id)
    training.delete()

    return HttpResponseRedirect('/trainings/')


def cancel_training(request, training_id):
    return delete_training(request, training_id)


def add_exercise_to_training(request, training_id):
    training = Training.objects.get(id=training_id)
    exercise = Exercise()

    exercise.training = training
    exercise.name = request.POST['name']
    exercise.weight_kg = request.POST['weight_kg']
    exercise.weight_per = request.POST['weight_per']
    exercise.series = request.POST['series']
    exercise.reps = dict()

    this_training_exercises = Exercise.objects.filter(training__id=training_id)
    series_count = this_training_exercises.aggregate(Sum('series'))['series__sum']
    series_count = series_count if series_count else 0
    for s in range(series_count, series_count+int(exercise.series)):
        exercise.reps[s] = 0

    exercise.save()

    return HttpResponseRedirect(f'/edit-training/{training_id}/')


def save_training_plan(request, training_id):
    training_plan = TrainingPlan()
    training_plan.name = request.POST['name']
    training = Training.objects.get(id=training_id)
    training.plan = training_plan

    training_plan = training_to_training_plan(training_id, training_plan)

    training_plan.save()
    training.save()

    return HttpResponseRedirect(f'/edit-training/{training_id}/')


def load_training_plan(request, training_id):
    training = Training.objects.get(id=training_id)
    plan_id = request.POST['selected_plan_id']
    training_plan = TrainingPlan.objects.get(id=plan_id)
    training.plan = training_plan
    training.save()

    series_count = 0

    for plan_exercise in training_plan.exercises:
        new_exercise = Exercise()
        new_exercise.training = training
        new_exercise.name = plan_exercise['name']
        new_exercise.weight_kg = plan_exercise['weight_kg']
        new_exercise.weight_per = plan_exercise['weight_per']
        new_exercise.series = plan_exercise['series']
        new_exercise.reps = dict()

        new_series_count = series_count + int(new_exercise.series)
        for s in range(series_count, new_series_count):
            new_exercise.reps[s] = 0
        series_count = new_series_count

        new_exercise.save()

    return HttpResponseRedirect(f'/edit-training/{training_id}/')


def training_to_training_plan(training_id, training_plan):
    exercises = Exercise.objects.filter(training__id=training_id)
    plan_table = []
    
    for exercise in exercises:
        plan_table.append(
            {
                'name': exercise.name,
                'weight_kg': exercise.weight_kg,
                'weight_per': exercise.weight_per,
                'series': exercise.series
            }
        )

    training_plan.exercises = plan_table

    return training_plan
