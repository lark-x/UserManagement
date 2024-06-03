import os
from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from app01 import models

from app01.utils.form import UploadForm, UploadModelForm


def upload_list(request):
    if request.method == 'GET':
        return render(request, 'upload_list.html')
    if request.method == 'POST':
        file = request.FILES.get('avatar')
        f = open('avatar.jpg', 'wb')
        for chunk in file.chunks():
            f.write(chunk)
        f.close()
        return render(request, 'upload_list.html')


def upload_form(request):
    title = 'form上传'
    if request.method == 'GET':
        form = UploadForm()
        context = {
            'title': title, 'form': form
        }
        return render(request, 'upload_form.html', context)
    if request.method == 'POST':
        form = UploadForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # 1.读取图片内容,写入到文件夹中并获取文件的路径
            image_object = form.cleaned_data.get('img')

            media_path = os.path.join("media", image_object.name)

            f = open(media_path, mode='wb')
            for chunk in image_object.chunks():
                f.write(chunk)
            f.close()
            # 2.将图片文件路径写入到数据库
            models.Boss.objects.create(
                name=form.cleaned_data.get('name'),
                age=form.cleaned_data.get('age'),
                img=media_path
            )
            return HttpResponse("...")
        return render(request, 'upload_form.html', {'form': form, 'title': title})


def upload_model_form(request):
    if request.method == 'GET':
        form = UploadModelForm()
        context = {
            'form': form,
            'title': 'ModelForm上传文件'
        }
        print()
        return render(request, 'upload_form.html', context)
    if request.method == 'POST':
        form = UploadModelForm(data=request.POST, files=request.FILES)
        print(request.FILES)
        context = {
            'form': form,
            'title': 'ModelForm上传文件'
        }
        if form.is_valid():
            # 自动保存数据
            form.save()
            redirect('/upload/modelform/')
        return render(request, 'upload_form.html', context)
