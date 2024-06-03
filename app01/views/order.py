from app01 import models
from django.shortcuts import render
from app01.utils.form import OrderModelForm
from app01.utils.pagination import Pagination
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from datetime import datetime


def order_list(request):
    queryset = models.Order.objects.all().order_by('-id')
    form = OrderModelForm()
    page_object = Pagination(request, queryset)
    context = {
        'form': form,
        'title': '订单列表',
        'modalTitle': '新建订单',
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
    }
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """ 新建订单(Ajax请求) """
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 1.创建基于订单创建时间的随机订单号
        form.instance.oid = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(10000, 99999))
        # 2.为管理员数据赋值,值为提交订单的管理员
        form.instance.admin_id = request.session['info']['id']
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


def order_delete(request):
    """ 删除订单 """
    uid = request.GET.get('uid')
    # print(uid)
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败,数据不存在"})
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


@csrf_exempt
def order_edit(request):
    """ 编辑订单 """
    uid = request.GET.get('uid')
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "编辑失败,数据不存在"})
    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


def order_detail(request):
    """ 根据ID获取订单详细 """
    uid = request.GET.get('uid')
    row_dict = models.Order.objects.filter(id=uid).values('title', 'price', 'status').first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在"})

    return JsonResponse({"status": True, "data": row_dict})
