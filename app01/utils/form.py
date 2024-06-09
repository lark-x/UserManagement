from django.core.exceptions import ValidationError
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm, BootStrapForm
from django.core.validators import RegexValidator
from django import forms
from app01.utils.encrypt import md5


class PrettyModelForm(BootStrapModelForm):
    # 格式验证: 方式1
    # mobile = forms.CharField(
    #     label="手机",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误')],
    # )
    class Meta:
        model = models.PrettyNumber
        fields = '__all__'

    # 格式验证: 方式二
    def clean_mobile(self):

        txt_mobile = self.cleaned_data["mobile"]
        if models.PrettyNumber.objects.filter(mobile=txt_mobile).exists():
            # 验证不通过
            raise ValidationError("手机号已存在")
        elif len(txt_mobile) != 11:
            raise ValidationError("手机号格式错误")
        # 验证通过 返回用户输入的数据
        return txt_mobile


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(min_length=2, label="用户名")
    password = forms.CharField(min_length=6, label='密码')

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'account', 'gender', 'depart', 'create_time']
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'age': forms.TextInput(attrs={'class': 'form-control'}),
        #     'account': forms.TextInput(attrs={'class': 'form-control'}),
        #     'gender': forms.Select(attrs={'class': 'form-control'}),
        #     'depart': forms.Select(attrs={'class': 'form-control'}),
        #     'create_time': forms.TextInput(attrs={'class': 'form-control'}),
        # }
        # widgets = {
        #     'create_time': forms.DateTimeInput(attrs={'type': 'date'}),
        # }
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # 循环找到所有的插件,添加class
    #     for name, field in self.fields.items():
    #         # if name in ['create_time']:
    #         #     continue
    #         field.widget.attrs = {'class': 'form-control', 'placeholder': '请输入' + field.label}


class PrettyEditModelForm(BootStrapModelForm):
    # 格式验证: 方式1
    # mobile = forms.CharField(
    #     label="手机",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误')],
    # )
    # mobile = forms.CharField(disabled=True, label="手机号")

    class Meta:
        model = models.PrettyNumber
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # 循环找到所有的插件,添加class
    #     for name, field in self.fields.items():
    #         field.widget.attrs = {'class': 'form-control', 'placeholder': '请输入' + field.label}

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        if models.PrettyNumber.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists():
            # 验证不通过
            raise ValidationError("手机号已存在")
        elif len(txt_mobile) != 11:
            raise ValidationError("手机号格式错误")
        # 验证通过 返回用户输入的数据
        return txt_mobile


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        password = self.cleaned_data["password"]
        return md5(password)

    def clean_confirm_password(self):
        password = self.cleaned_data["password"]
        confirm_password = md5(self.cleaned_data["confirm_password"])
        if password != confirm_password:
            raise ValidationError("密码不一致")
        # 返回什么,此字段以后保存到数据库就是什么
        return confirm_password


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        md5_password = md5(password)
        # 去数据库校验当前密码和新输入的密码是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_password).exists()
        if exists:
            raise ValidationError("不能与以前的密码相同")
        return md5_password

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = md5(self.cleaned_data.get("confirm_password"))
        if password != confirm_password:
            raise ValidationError("密码不一致")
        # 返回什么,此字段以后保存到数据库就是什么
        return confirm_password


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        password = self.cleaned_data.get("password")
        md5_password = md5(password)
        return md5_password


class LoginModelForm(forms.ModelForm):
    class Meta:
        model = models.Admin
        fields = ['username', 'password']


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = ['title', 'level', 'detail', 'user']
        widgets = {
            'detail': forms.TextInput,
        }


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = '__all__'
        exclude = ['oid', 'admin']


class UploadForm(BootStrapForm):
    bootstrap_exclude_fields = ['img']
    name = forms.CharField(label='姓名')
    age = forms.IntegerField(label='年龄')
    img = forms.FileField(label='头像')


class UploadModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.City
        fields = '__all__'


class RecordModelForm(BootStrapModelForm):
    class Meta:
        model = models.Record
        # fields = '__all__'
        exclude = ['data', 'recorder']


class BillModelForm(BootStrapModelForm):
    class Meta:
        model = models.Bill
        fields = '__all__'
        exclude = ['recorder']


class ExcelFileModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['filePath']

    class Meta:
        model = models.ExcelFile
        fields = ['filePath']
