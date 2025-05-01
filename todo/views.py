from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SharedList, Task
from django.utils.dateparse import parse_date

@login_required
def task_list(request):
    shared_lists = SharedList.objects.filter(users=request.user)
    if not shared_lists:
        return render(request, 'todo/no_list.html')
    shared_list = shared_lists.first()
    tasks = Task.objects.filter(shared_list=shared_list).order_by('-created_at')
    return render(request, 'todo/task_list.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        priority = request.POST.get('priority', 'M')
        finish_by_raw = request.POST.get('finish_by', '')
        finish_by = parse_date(finish_by_raw) if finish_by_raw else None

        shared_list = SharedList.objects.filter(users=request.user).first()
        Task.objects.create(
            title=title,
            priority=priority,
            finish_by=finish_by,
            created_by=request.user,
            shared_list=shared_list
        )
        return redirect('task_list')
    return render(request, 'todo/add_task.html')

@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_done = not task.is_done
    task.save()
    return redirect('task_list')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')
