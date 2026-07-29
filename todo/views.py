from django.contrib import messages


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import TodoSerializer

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Todo
from .forms import TodoForm


@login_required
def home(request):
    search = request.GET.get('search')

    todos = Todo.objects.filter(user=request.user)

    if search:
        todos = todos.filter(title__icontains=search)

    if request.method == "POST":
        form = TodoForm(request.POST, request.FILES)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
             
            return redirect('/')
    else:
        form = TodoForm()

    context = {
        'todos': todos,
        'form': form,
        'total': todos.count(),
        'completed': todos.filter(completed=True).count(),
        'pending': todos.filter(completed=False).count(),
    }

    return render(request, 'index.html', context)


@login_required
def delete_todo(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)
    todo.delete()
    return redirect('/')


@login_required
def update_todo(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)

    if request.method == "POST":
        form = TodoForm(request.POST, request.FILES, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = TodoForm(instance=todo)

    return render(request, "update.html", {"form": form})


@login_required
def toggle_complete(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('/')


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})



@login_required
def dashboard(request):

    todos = Todo.objects.filter(user=request.user)

    context = {
        "total": todos.count(),
        "completed": todos.filter(completed=True).count(),
        "pending": todos.filter(completed=False).count(),
        "completion_rate": (
            (todos.filter(completed=True).count() * 100) // todos.count()
            if todos.exists() else 0
        )
    }

    return render(request, "dashboard.html", context)

@api_view(['GET'])
def todo_api(request):
    todos = Todo.objects.filter(user=request.user)
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_todo(request):
    serializer = TodoSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

@api_view(['GET'])
def todo_api(request):
    todos = Todo.objects.all()
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def update_todo_api(request, id):
    todo = get_object_or_404(Todo, id=id)

    serializer = TodoSerializer(todo, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_todo_api(request, id):
    todo = get_object_or_404(Todo, id=id)
    todo.delete()

    return Response(
        {"message": "Todo deleted successfully"},
        status=200
    )