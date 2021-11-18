from django.contrib.auth import views as auth_views
from django.urls import path

from goals_app import views

task_list = views.TaskViewSet.as_view({
    'get': 'list',
    'post': 'create'
})


app_name = 'goals-app'
urlpatterns = [
    path(
        'auth/sign-in/',  # TODO: fix redirect to /accounts/profile
        views.LoginView.as_view(),
        name='sign-in'
    ),
    path(
        'auth/sign-up/',
        views.RegistrationView.as_view(),
        name='sign-up'
    ),
    path(
        'auth/refresh-token/',
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
