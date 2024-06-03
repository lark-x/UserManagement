from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm, PrettyModelForm, PrettyEditModelForm


def depart_list(request):
    """ 部门列表 """
    # queryset:[对象,对象,对象...]
    queryset = models.Department.objects.all()
    # 去数据库中获取所有的部门列表
    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    """ 添加页面 """
    if request.method == "GET":
        return render(request, 'depart_add.html')
    # 获取用户POST提交过来的数据
    title = request.POST.get('title')
    # 保存到数据库
    models.Department.objects.create(title=title)
    # 重定向回部门列表
    return redirect('/depart/list/')


def depart_delete(request):
    """删除部门"""
    # http://127.0.0.1:8000/depart/delete/?nid=1
    nid = request.GET.get('nid')

    # 删除
    models.Department.objects.filter(id=nid).delete()

    # 重定向回部门列表
    return redirect('/depart/list/')


def depart_edit(request, nid):
    if request.method == "GET":
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {'row_object': row_object})
    title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list/')


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


# class UserModelForm(BootStrapModelForm):
#     name = forms.CharField(min_length=2, label="用户名")
#     password = forms.CharField(min_length=6, label='密码')
#
#     class Meta:
#         model = models.UserInfo
#         fields = ['name', 'password', 'age', 'account', 'gender', 'depart', 'create_time']
#         # widgets = {
#         #     'name': forms.TextInput(attrs={'class': 'form-control'}),
#         #     'password': forms.PasswordInput(attrs={'class': 'form-control'}),
#         #     'age': forms.TextInput(attrs={'class': 'form-control'}),
#         #     'account': forms.TextInput(attrs={'class': 'form-control'}),
#         #     'gender': forms.Select(attrs={'class': 'form-control'}),
#         #     'depart': forms.Select(attrs={'class': 'form-control'}),
#         #     'create_time': forms.TextInput(attrs={'class': 'form-control'}),
#         # }
#         # widgets = {
#         #     'create_time': forms.DateTimeInput(attrs={'type': 'date'}),
#         # }
#     #
#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#     #     # 循环找到所有的插件,添加class
#     #     for name, field in self.fields.items():
#     #         # if name in ['create_time']:
#     #         #     continue
#     #         field.widget.attrs = {'class': 'form-control', 'placeholder': '请输入' + field.label}


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


from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


# class PrettyModelForm(BootStrapModelForm):
#     # 格式验证: 方式1
#     # mobile = forms.CharField(
#     #     label="手机",
#     #     validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误')],
#     # )
#     class Meta:
#         model = models.PrettyNumber
#         fields = '__all__'
#
#     # 格式验证: 方式二
#     def clean_mobile(self):
#
#         txt_mobile = self.cleaned_data["mobile"]
#         if models.PrettyNumber.objects.filter(mobile=txt_mobile).exists():
#             # 验证不通过
#             raise ValidationError("手机号已存在")
#         elif len(txt_mobile) != 11:
#             raise ValidationError("手机号格式错误")
#         # 验证通过 返回用户输入的数据
#         return txt_mobile


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


# class PrettyEditModelForm(BootStrapModelForm):
#     # 格式验证: 方式1
#     # mobile = forms.CharField(
#     #     label="手机",
#     #     validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误')],
#     # )
#     # mobile = forms.CharField(disabled=True, label="手机号")
#
#     class Meta:
#         model = models.PrettyNumber
#         fields = '__all__'
#
#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#     #     # 循环找到所有的插件,添加class
#     #     for name, field in self.fields.items():
#     #         field.widget.attrs = {'class': 'form-control', 'placeholder': '请输入' + field.label}
#
#     def clean_mobile(self):
#         txt_mobile = self.cleaned_data["mobile"]
#         if models.PrettyNumber.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists():
#             # 验证不通过
#             raise ValidationError("手机号已存在")
#         elif len(txt_mobile) != 11:
#             raise ValidationError("手机号格式错误")
#         # 验证通过 返回用户输入的数据
#         return txt_mobile


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
