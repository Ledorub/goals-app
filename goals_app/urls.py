from django.contrib.auth import views as auth_views
from django.urls import path

from goals_app import views

task_list = views.TaskViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

AUTH_PREFIX = 'auth/'

app_name = 'goals-app'
urlpatterns = [
    path(
        f'{AUTH_PREFIX}sign-in/',  # TODO: fix redirect to /accounts/profile
        views.LoginView.as_view(),
        name='sign-in'
    ),
    path(
        f'{AUTH_PREFIX}sign-up/',
        views.RegistrationView.as_view(),
        name='sign-up'
    ),
    path(
        f'{AUTH_PREFIX}refresh-token/',
        views.TokenRefreshView.as_view(),
        name='refresh-token'
    ),
    path(
        'task-list/',
        task_list,
        name='task-list'
    ),
    path(
        'user/',
        views.UserRetrieveUpdateView.as_view(),
        name='user-detail'
    )
]
