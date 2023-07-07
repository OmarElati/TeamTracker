from django.shortcuts import render
from .models import Task
from .models import Link
from gantt.serializers import TaskSerializer
from gantt.serializers import LinkSerializer
 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
 
 
def create_gantt_view(request):
    return render(request, 'gantt/create_gantt.html')
 
def index(request):
    return render(request, 'gantt/gantt.html')
 
@api_view(['GET'])
def data_list(request, offset): # returns the serialized data in a JSON response
    if request.method == 'GET':
        tasks = Task.objects.all()
        links = Link.objects.all()
        taskData = TaskSerializer(tasks, many=True)
        linkData = LinkSerializer(links, many=True)
        return Response({
            "tasks": taskData.data,
            "links": linkData.data
        })
 
 
@api_view(['POST'])
def task_add(request): # request for adding a new task
    print("aa")
    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        print(serializer)
 
        if serializer.is_valid():
            task = serializer.save()
            return JsonResponse({'action':'inserted', 'tid': task.id})
        return JsonResponse({'action':'error'})
 
@api_view(['PUT', 'DELETE'])
def task_update(request, pk): # PUT and DELETE requests for updating || deleting a task with the specified primary key pk
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return JsonResponse({'action':'error2'})
 
    if request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'action':'updated'})
        return JsonResponse({'action':'error'})
 
    if request.method == 'DELETE':
        task.delete()
        return JsonResponse({'action':'deleted'})
 
 
@api_view(['POST'])
def link_add(request): # POST request for adding a new link
    if request.method == 'POST':
        serializer = LinkSerializer(data=request.data)
        print(serializer)
 
        if serializer.is_valid():
            link = serializer.save()
            return JsonResponse({'action':'inserted', 'tid': link.id})
        return JsonResponse({'action':'error'})
 
@api_view(['PUT', 'DELETE'])
def link_update(request, pk): #  PUT and DELETE requests for updating || deleting a link with the specified primary key pk
    try:
        link = Link.objects.get(pk=pk)
    except Link.DoesNotExist:
        return JsonResponse({'action':'error'})
 
    if request.method == 'PUT':
        serializer = LinkSerializer(link, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'action':'updated'})
        return JsonResponse({'action':'error'})
 
    if request.method == 'DELETE':
        link.delete()
        return JsonResponse({'action':'deleted'})
