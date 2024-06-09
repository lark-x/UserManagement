from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from app01.models import City
from app01.utils.form import UploadModelForm


def city_list(request):
    """ 城市列表 """
    queryset = City.objects.all()
    if request.method == 'GET':
        form = UploadModelForm()
        context = {
            'queryset': queryset,
            'title': '城市列表',
            'add_title': '新建城市',
            'form': form,
        }
        return render(request, 'city_list.html', context)
    if request.method == 'POST':
        form = UploadModelForm(request.POST, request.FILES)
        context = {
            'form': form,
            'error': form.errors,
        }
        if form.is_valid():
            form.save()

            redirect('/city/list/')
        return render(request, 'city_list.html', context)


@csrf_exempt
def city_add(request):
    """ 新建城市(Ajax请求) """
    form = UploadModelForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})
