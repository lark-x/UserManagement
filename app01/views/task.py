import json
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app01.utils.form import TaskModelForm
from app01 import models
from app01.utils.pagination import Pagination


def task_list(request):
    """ 任务列表 """
    # 去数据库中获取所有的任务
    queryset = models.Task.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)
    form = TaskModelForm()
    context = {
        'form': form,
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
    }
    return render(request, 'task_list.html', context)


@csrf_exempt
def task_ajax(request):
    print(request.GET)
    print(request.POST)
    data_dict = {"status": True, "data": [11, 22, 33, 44]}
    return JsonResponse(data_dict)


@csrf_exempt
def task_add(request):
    # print(request.POST)
    # 1.对用户发送过来的数据进行校验(ModelForm进行校验)
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return JsonResponse(data_dict)
    data_dict = {"status": False, 'error': form.errors}
    return JsonResponse(data_dict)
