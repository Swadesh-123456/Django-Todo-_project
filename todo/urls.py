from django.urls import path
from . import views


urlpatterns = [

    # =========================
    # HOME
    # =========================

    path(
        "",
        views.home,
        name="home"
    ),


    # =========================
    # TODO
    # =========================

    path(
        "delete/<int:id>/",
        views.delete_todo,
        name="delete"
    ),

    path(
        "update/<int:id>/",
        views.update_todo,
        name="update"
    ),

    path(
        "toggle/<int:id>/",
        views.toggle_complete,
        name="toggle"
    ),


    # =========================
    # AUTHENTICATION
    # =========================

    path(
        "signup/",
        views.signup,
        name="signup"
    ),


    # =========================
    # DASHBOARD
    # =========================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),


    # =========================
    # PROFILE
    # =========================

    path(
        "profile/",
        views.profile,
        name="profile"
    ),


    # =========================
    # API
    # =========================

    path(
        "api/todos/",
        views.todo_api,
        name="todo_api"
    ),

    path(
        "api/create/",
        views.create_todo,
        name="create_todo"
    ),

    path(
        "api/update/<int:id>/",
        views.update_todo_api,
        name="update_todo_api"
    ),

    path(
        "api/delete/<int:id>/",
        views.delete_todo_api,
        name="delete_todo_api"
    ),

]