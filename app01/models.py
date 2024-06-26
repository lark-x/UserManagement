from time import timezone

from django.db import models


class Admin(models.Model):
    """ 管理员 """
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=32, verbose_name="密码")

    def __str__(self):
        return self.username


class Department(models.Model):
    """ 部门表 """
    # id = models.BigAutoField(verbose_name="ID", primary_key=True)
    title = models.CharField(verbose_name="标题", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)

    # create_time = models.DateTimeField(verbose_name="入职时间")
    create_time = models.DateField(verbose_name="入职时间")

    # 无约束
    # did = models.BigIntegerField(verbose_name="部门ID")

    # 1. 有约束
    # - to, 与哪张表关联
    # - to_field, 表中的哪一列关联
    # 2. django自动
    # - 写的depart
    # - 生成数据列 depart_id
    # 3. 部门表被删除
    # 3.1 级联删除

    # depart = models.ForeignKey(to="Department",to_field="id",on_delete=models.CASCADE)
    # 3.2 置空
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", null=True, blank=True,
                               on_delete=models.SET_NULL)

    # 在django中做的约束
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class PrettyNumber(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    price = models.IntegerField(verbose_name="价格")
    level_choices = (
        (1, "一级"),
        (2, "二级"),
        (3, "三级"),
        (4, "四级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    status_choices = (
        (1, "已使用"),
        (2, "未使用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)


class Task(models.Model):
    """ 任务 """
    level_choices = (
        (1, '紧急'),
        (2, '重要'),
        (3, '临时'),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详细信息")
    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)


class Order(models.Model):
    """ 订单 """
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")
    status_choices = (
        (1, "待支付"),
        (2, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    admin = models.ForeignKey(verbose_name="管理员", to="Admin", on_delete=models.CASCADE)


class Boss(models.Model):
    """ 老板 """
    name = models.CharField(verbose_name='姓名', max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    img = models.CharField(verbose_name="头像", max_length=128)


class City(models.Model):
    """ 城市 """
    name = models.CharField(verbose_name='名称', max_length=32)
    count = models.IntegerField(verbose_name='人口')
    # 本质上数据库也是CharField
    img = models.FileField(verbose_name="Logo", max_length=128, upload_to="cityLogo")


class Record(models.Model):
    """ 账本 """
    data = models.DateField(verbose_name='记账日期', max_length=64)
    type_choices = (
        (1, '支出'),
        (2, '收入'),
    )
    type = models.SmallIntegerField(verbose_name='类型', choices=type_choices, default=1)
    money = models.DecimalField(verbose_name='记账金额', max_digits=10, decimal_places=2, default=0)
    state = models.CharField(verbose_name='说明', max_length=64)
    recorder = models.ForeignKey(verbose_name='记账人', to='Admin', on_delete=models.CASCADE)


class Bill(models.Model):
    """ 账单 """
    data = models.DateTimeField(verbose_name='交易时间')
    type = models.CharField(verbose_name='收/支', max_length=64)
    amount = models.DecimalField(verbose_name='金额', max_digits=10, decimal_places=2, default=0)
    description = models.CharField(verbose_name='说明', max_length=128)
    recorder = models.ForeignKey(verbose_name='记账人', to='Admin', on_delete=models.CASCADE)


class ExcelFile(models.Model):
    """ Excel文件 """
    datetime = models.DateTimeField(verbose_name='上传时间', auto_now_add=True)
    filePath = models.FileField(verbose_name='Excel文件', upload_to='excel', max_length=128)
    uploader = models.ForeignKey(verbose_name='上传者', to='Admin', on_delete=models.CASCADE, default=None)
