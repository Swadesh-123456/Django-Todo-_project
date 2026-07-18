from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('delete/<int:id>/', views.delete_todo, name='delete'),
    path('update/<int:id>/', views.update_todo, name='update'),
    path('toggle/<int:id>/', views.toggle_complete, name='toggle'),
    path('signup/', views.signup, name='signup'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("api/todos/", views.todo_api, name="todo_api"),
    path("api/create/", views.create_todo, name="create_todo"),
    path("api/update/<int:id>/", views.update_todo_api, name="update_todo_api"),path("api/delete/<int:id>/", views.delete_todo_api, name="delete_todo_api"),
]