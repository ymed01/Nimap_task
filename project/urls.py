# urls.py

from django.urls import path
from .views import client_list, client_detail, project_create, user_projects

urlpatterns = [
    path('clients/', client_list, name='client-list'),
    path('clients/<int:id>/', client_detail, name='client-detail'),
    path('clients/<int:client_id>/projects/', project_create, name='create-project'),
    path('projects/', user_projects, name='user-projects'),
]
