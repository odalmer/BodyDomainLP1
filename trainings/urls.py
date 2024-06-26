from django.urls import path
from .views import trainings_view, single_training_view, \
    edit_training_view, start_training, stop_training, save_training, \
    delete_training,    cancel_training, record_training, add_exercise_to_training, \
    save_training_plan, load_training_plan, signin, signout, signup, progress_analysis_view

urlpatterns = [
    path('', trainings_view, name='home'),
    path('signin/', signin, name='signin'),
    path('logout/', signout, name='logout'),
    path('signup/', signup, name='signup'),
    path('trainings/', trainings_view, name='trainings'),
    path('trainings/<int:training_id>/', single_training_view),
    path('edit-training/<int:training_id>/', edit_training_view),
    path('record-training/', record_training),
    path('start-training/<int:training_id>/', start_training),
    path('stop-training/<int:training_id>/', stop_training),
    path('save-training/<int:training_id>/', save_training),
    path('delete-training/<int:training_id>/', delete_training),
    path('cancel-training/<int:training_id>/', cancel_training),
    path('add-exercise/<int:training_id>/', add_exercise_to_training),
    path('save-training-plan/<int:training_id>/', save_training_plan),
    path('load-training-plan/<int:training_id>/', load_training_plan),
    path('progress-analysis/', progress_analysis_view),

]
