from django.urls import re_path, path
from . import views
from .views import create_gantt_view
from rest_framework.urlpatterns import format_suffix_patterns
 
urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^data/task/(?P<pk>[0-9]+)$', views.task_update),
    re_path(r'^data/task', views.task_add),
    re_path(r'^data/link/(?P<pk>[0-9]+)$', views.link_update),
    re_path(r'^data/link', views.link_add),
    re_path(r'^data/(.*)$', views.data_list),
    path('create-gantt/', create_gantt_view, name='create_gantt'),
]
urlpatterns = format_suffix_patterns(urlpatterns)