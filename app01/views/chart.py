from django.http import JsonResponse
from django.shortcuts import render


def chart_list(request):
    """ 数据统计页面 """
    context = {
        'title': '数据统计',
    }
    return render(request, 'chart_list.html', context)


def chart_bar(request):
    """ 构造柱状图的数据 """

    # 数据可以去数据库中获取

    legend = ["原神", "崩坏:星穹铁道"]
    series_list = [
        {
            "name": '原神',
            "type": 'bar',
            "data": [5, 20, 35, 10, 10, 110]
        },
        {
            "name": '崩坏:星穹铁道',
            "type": 'bar',
            "data": [15, 32, 36, 17, 50, 10]
        }
    ]
    x_axis = ['一月', '二月', '三月', '四月', '五月', '六月']

    result = {
        "status": True,
        "data": {
            "series_list": series_list,
            "legend": legend,
            "x_axis": x_axis
        }
    }
    return JsonResponse(result)


def chart_pie(request):
    """ 构造饼状图的数据"""
    # 数据可以去数据库中获取
    series_list = [
        {"value": 2048, "name": '原神'},
        {"value": 735, "name": '崩坏:星穹铁道'},
        {"value": 580, "name": '未定事件簿'},
        {"value": 484, "name": '崩坏学院2'},
        {"value": 300, "name": '崩坏三'}
    ]
    result = {
        "status": True,
        "data": series_list
    }
    return JsonResponse(result)


def chart_line(request):
    """ 构造折线图的数据"""
    # 数据可以去数据库中获取
    series_list = [
        {
            "data": [150, 230, 224, 218, 135, 147, 260],
            "type": 'line',
            "smooth": True
        },
        {
            "data": [50, 130, 424, 218, 135, 147, 260],
            "type": 'line',
            "smooth": True
        },
        {
            "data": [250, 330, 124, 218, 135, 147, 260],
            "type": 'line',
            "smooth": False
        }
    ]

    result = {
        "status": True,
        "data": series_list,
    }
    return JsonResponse(result)
