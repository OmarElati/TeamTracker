from django.urls import path

from create.views import (
	create_task,
    complete_task,
    task_list,
    notification_list,
    create_account_view,
)


app_name = 'create'


urlpatterns = [
    path('create-account/', create_account_view, name='create_account'),
    path('create-task/', create_task, name='create_task'),
    path('complete-task/<int:task_id>/', complete_task, name='complete_task'),
    path('tasks/', task_list, name='task_list'),
    path('notifications/', notification_list, name='notification_list'),
]
