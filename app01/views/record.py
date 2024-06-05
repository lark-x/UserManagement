from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime
from app01 import models
from app01.models import Record
from app01.utils.form import RecordModelForm
from app01.utils.pagination import Pagination


def record_list(request):
    queryset = models.Record.objects.all()
    form = RecordModelForm()
    pagination = Pagination(request, queryset)
    context = {
        'queryset': queryset,
        'title': '个人账本',
        'form': form,
        'page_string': pagination.html(),
        'modalTitle': '新增账单'
    }
    return render(request, 'record_list.html', context)


@csrf_exempt
def record_add(request):
    """ 新建订单(Ajax请求) """
    form = RecordModelForm(data=request.POST)
    if form.is_valid():
        form.instance.data = datetime.datetime.now().strftime('%Y-%m-%d')
        form.instance.recorder_id = request.session['info']['id']
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


def record_delete(request):
    """ 删除订单 """
    uid = request.GET.get('uid')
    # print(uid)
    exists = models.Record.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败,数据不存在"})
    models.Record.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


@csrf_exempt
def record_edit(request):
    """ 编辑订单 """
    uid = request.GET.get('uid')
    row_object = models.Record.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "编辑失败,数据不存在"})
    form = RecordModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


def record_detail(request):
    """ 根据ID获取订单详细 """
    uid = request.GET.get('uid')
    row_dict = models.Record.objects.filter(id=uid).values('data', 'type', 'recorder', 'money', 'state').first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在"})
    return JsonResponse({"status": True, "data": row_dict})
