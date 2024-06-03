from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm, PrettyModelForm, PrettyEditModelForm


def user_list(request):
    """ 用户管理"""

    queryset = models.UserInfo.objects.all()

    page_object = Pagination(request, queryset)
    context = {
        'page_string': page_object.html(),
        'queryset': page_object.page_queryset,
    }

    return render(request, 'user_list.html', context)


def user_add(request):
    """添加用户"""
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all(),
        }
        return render(request, 'user_add.html', context)
    # 获取用户提交的数据
    name = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender = request.POST.get('gd')
    depart_id = request.POST.get('dp')
    models.UserInfo.objects.create(name=name, password=pwd, age=age, account=account, create_time=ctime, gender=gender,
                                   depart_id=depart_id)
    return redirect('/user/list/')


def user_model_form_add(request):
    """添加用户(ModelForm)"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {'form': form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    else:
        return render(request, 'user_model_form_add.html', {'form': form})


def user_model_form_edit(request, nid):
    """编辑用户(ModelForm)"""
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        # 根据id去数据库获取需要编辑的数据信息
        # row_object = models.UserInfo.objects.filter(id=nid).first()
        form = UserModelForm(instance=row_object)
        return render(request, 'user_model_form_edit.html', {'form': form})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据,如果想要在用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')
    else:
        return render(request, 'user_model_form_edit.html', {'form': form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')
