from django.shortcuts import render, redirect

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm


def admin_list(request):
    """ 管理员列表 """
    # 检查用户是否已登录
    # 未登录时访问该页面则跳转回登陆页面
    info = request.session.get('info')
    if not info:
        return redirect('/login/')

    # 获取搜索条件
    data_dict = {}
    search_data = request.GET.get('search', '')
    if search_data:
        data_dict["username__contains"] = search_data

    # 根据搜索条件去数据库获取
    queryset = models.Admin.objects.filter(**data_dict)

    # 对数据进行分页
    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        'search_data': search_data,
    }

    return render(request, 'admin_list.html', context)


def admin_add(request):
    """ 添加管理员 """

    if request.method == 'GET':
        form = AdminModelForm()
        context = {
            "title": "新增管理员",
            "form": form,
        }
        return render(request, 'change.html', context)
    if request.method == 'POST':
        form = AdminModelForm(data=request.POST)
        context = {
            "title": "新增管理员",
            "form": form,
        }
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')
        return render(request, 'change.html', context)


def admin_edit(request, nid):
    """ 编辑管理员 """

    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        context = {
            "msg": "数据不存在",
        }
        return render(request, 'error.html', context)
    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_object)
        context = {
            "title": "编辑管理员",
            "form": form,
        }
        return render(request, 'change.html', context)
    if request.method == 'POST':
        form = AdminEditModelForm(data=request.POST, instance=row_object)
        context = {
            "title": "编辑管理员",
            "form": form,
        }
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')
        return render(request, 'change.html', context)


def admin_delete(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        context = {
            "msg": "数据不存在",
        }
        return render(request, 'error.html', context)
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


def admin_reset(request, nid):
    """ 重置密码 """
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        context = {
            "msg": "数据不存在",
        }
        return render(request, 'error.html', context)
    if request.method == 'GET':
        form = AdminResetModelForm()
        context = {
            "title": "重置密码",
            "form": form,
        }
        return render(request, 'change.html', context)
    if request.method == 'POST':
        form = AdminResetModelForm(data=request.POST, instance=row_object)
        context = {
            "title": "重置密码",
            "form": form,
        }
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')
        return render(request, 'change.html', context)
