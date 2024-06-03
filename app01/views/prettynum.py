from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import UserModelForm, PrettyModelForm, PrettyEditModelForm


def prettynum_list(request):
    """靓号管理"""

    # for i in range(300):
    #     models.PrettyNumber.objects.create(mobile=str(13879795727 + i), price=199 + i, level=2)

    # import copy
    # get_query_dict = copy.deepcopy(request.GET)
    # get_query_dict._mutable = True
    #
    # get_query_dict.setlist('page')

    data_dict = {}
    search_data = request.GET.get('search', '')
    if search_data:
        data_dict["mobile__contains"] = search_data

    queryset = models.PrettyNumber.objects.filter(**data_dict).order_by('-level')
    from app01.utils.pagination import Pagination
    page_object = Pagination(request, queryset)
    # 1.根据用户想要访问的页码,计算出起止位置
    # page_size = 10
    # page = int(request.GET.get('page', 1))
    # start = (page - 1) * page_size
    # end = start + page_size

    # 2.生成页码
    """
    <li><a href="#">1</a></li>
    <li><a href="#">2</a></li>
    <li><a href="#">3</a></li>
    <li><a href="#">4</a></li>
    <li><a href="#">5</a></li>
    """
    # 计算总页码
    # total_count = models.PrettyNumber.objects.filter(**data_dict).order_by('-level').count()
    # total_page_count, div = divmod(total_count, page_object.page_size)
    # if div:
    #     total_page_count += 1
    #
    # 计算当前页的前5页和后5页
    # plus = 5
    # start_page = page_object.page - plus
    # end_page = page_object.page + plus

    # page_str_list = []
    # for i in range(start_page, end_page + 1):
    #     if i <= 0 or i > page_object.total_page_count:
    #         continue
    #     elif i == page_object.page:
    #         ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
    #     else:
    #         ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
    #     page_str_list.append(ele)
    #     page_string = mark_safe("".join(page_str_list))
    context = {
        'queryset': page_object.page_queryset,
        'search_data': search_data,
        'page_string': page_object.html(),
        'page': page_object.page,
    }
    return render(request, 'prettynum_list.html', context)


def prettynum_add(request):
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, 'prettynum_add.html', {'form': form})
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/prettynum/list/')
    else:
        return render(request, 'prettynum_add.html', {'form': form})


def prettynum_edit(request, nid):
    """编辑靓号(ModelForm)"""
    row_object = models.PrettyNumber.objects.filter(id=nid).first()
    if request.method == "GET":
        # 根据id去数据库获取需要编辑的数据信息
        # row_object = models.UserInfo.objects.filter(id=nid).first()
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'prettynum_edit.html', {'form': form})

    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据,如果想要在用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/prettynum/list/')
    else:
        return render(request, 'prettynum_edit.html', {'form': form})


def prettynum_delete(request, nid):
    models.PrettyNumber.objects.filter(id=nid).delete()
    return redirect('/prettynum/list/')
