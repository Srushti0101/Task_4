from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Task
from .forms import TaskForm


def task_list(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    status = request.GET.get('status')
    tasks = Task.objects.all()
    if status:
        tasks = tasks.filter(status=status)

    context = {
        'form': form,
        'tasks': tasks,
        'today': timezone.localdate(),
        'active_filter': status,
        'total': Task.objects.count(),
        'pending': Task.objects.filter(status='pending').count(),
        'in_progress': Task.objects.filter(status='in_progress').count(),
        'completed': Task.objects.filter(status='completed').count(),
    }
    return render(request, 'task_list.html', context)


def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = 'completed'
    task.save()
    return redirect('task_list')


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
    return redirect('task_list')