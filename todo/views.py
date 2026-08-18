from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Todo, Profile
from .forms import TodoForm, ProfileForm
from .serializers import TodoSerializer


# =========================================================
# HOME / TODO LIST
# =========================================================

@login_required
def home(request):

    search = request.GET.get("search", "").strip()

    todos = Todo.objects.filter(
        user=request.user
    )

    if search:
        todos = todos.filter(
            title__icontains=search
        )

    if request.method == "POST":

        form = TodoForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            todo = form.save(commit=False)

            todo.user = request.user

            if todo.status == "Completed":
                todo.completed = True
            else:
                todo.completed = False

            todo.save()

            messages.success(
                request,
                "Task added successfully!"
            )

            return redirect("home")

    else:

        form = TodoForm()


    context = {

        "todos": todos,

        "form": form,

        "total": todos.count(),

        "completed": todos.filter(
            completed=True
        ).count(),

        "pending": todos.filter(
            completed=False
        ).count(),

        "todo_count": todos.filter(
            status="Todo"
        ).count(),

        "in_progress_count": todos.filter(
            status="In Progress"
        ).count(),

        "completed_status_count": todos.filter(
            status="Completed"
        ).count(),

    }

    return render(
        request,
        "index.html",
        context
    )


# =========================================================
# DELETE TODO
# =========================================================

@login_required
def delete_todo(request, id):

    todo = get_object_or_404(
        Todo,
        id=id,
        user=request.user
    )

    todo.delete()

    messages.success(
        request,
        "Task deleted successfully!"
    )

    return redirect("home")


# =========================================================
# UPDATE TODO
# =========================================================

@login_required
def update_todo(request, id):

    todo = get_object_or_404(
        Todo,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        form = TodoForm(
            request.POST,
            request.FILES,
            instance=todo
        )

        if form.is_valid():

            todo = form.save(
                commit=False
            )

            if todo.status == "Completed":
                todo.completed = True
            else:
                todo.completed = False

            todo.save()

            messages.success(
                request,
                "Task updated successfully!"
            )

            return redirect("home")

    else:

        form = TodoForm(
            instance=todo
        )

    return render(
        request,
        "update.html",
        {
            "form": form,
            "todo": todo
        }
    )


# =========================================================
# TOGGLE COMPLETE
# =========================================================

@login_required
def toggle_complete(request, id):

    todo = get_object_or_404(
        Todo,
        id=id,
        user=request.user
    )

    todo.completed = not todo.completed

    if todo.completed:

        todo.status = "Completed"

    else:

        todo.status = "Todo"

    todo.save()

    return redirect("home")


# =========================================================
# SIGNUP
# =========================================================

def signup(request):

    if request.method == "POST":

        form = UserCreationForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            login(
                request,
                user
            )

            return redirect("home")

    else:

        form = UserCreationForm()

    return render(
        request,
        "signup.html",
        {
            "form": form
        }
    )


# =========================================================
# PROFILE
# =========================================================

@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully!"
            )

            return redirect("profile")

    else:

        form = ProfileForm(
            instance=profile
        )

    context = {

        "form": form,

        "profile": profile

    }

    return render(
        request,
        "profile.html",
        context
    )


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    todos = Todo.objects.filter(
        user=request.user
    )

    total = todos.count()

    completed = todos.filter(
        completed=True
    ).count()

    pending = todos.filter(
        completed=False
    ).count()


    completion_rate = (

        (completed * 100) // total

        if total > 0

        else 0

    )


    context = {

        "total": total,

        "completed": completed,

        "pending": pending,

        "todo_count": todos.filter(
            status="Todo"
        ).count(),

        "in_progress_count": todos.filter(
            status="In Progress"
        ).count(),

        "completed_status_count": todos.filter(
            status="Completed"
        ).count(),

        "high_priority": todos.filter(
            priority="High"
        ).count(),

        "medium_priority": todos.filter(
            priority="Medium"
        ).count(),

        "low_priority": todos.filter(
            priority="Low"
        ).count(),

        "completion_rate": completion_rate,

    }

    return render(
        request,
        "dashboard.html",
        context
    )


# =========================================================
# API - GET TODOS
# =========================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def todo_api(request):

    todos = Todo.objects.filter(
        user=request.user
    )

    serializer = TodoSerializer(
        todos,
        many=True
    )

    return Response(
        serializer.data
    )


# =========================================================
# API - CREATE TODO
# =========================================================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_todo(request):

    serializer = TodoSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save(
            user=request.user
        )

        return Response(
            serializer.data,
            status=201
        )

    return Response(
        serializer.errors,
        status=400
    )


# =========================================================
# API - UPDATE TODO
# =========================================================

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_todo_api(request, id):

    todo = get_object_or_404(
        Todo,
        id=id,
        user=request.user
    )

    serializer = TodoSerializer(
        todo,
        data=request.data
    )

    if serializer.is_valid():

        serializer.save(
            user=request.user
        )

        return Response(
            serializer.data
        )

    return Response(
        serializer.errors,
        status=400
    )


# =========================================================
# API - DELETE TODO
# =========================================================

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_todo_api(request, id):

    todo = get_object_or_404(
        Todo,
        id=id,
        user=request.user
    )

    todo.delete()

    return Response(
        {
            "message": "Todo deleted successfully"
        },
        status=200
    )