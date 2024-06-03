"""
自定义分页组件

def prettynum_list(request):
    # 搜索手机号的功能
    data_dict = {}
    search_data = request.GET.get('search', '')
    if search_data:
        data_dict["mobile__contains"] = search_data

    # 1.根据自己的情况去筛选自己的数据
    queryset = models.PrettyNumber.objects.filter(**data_dict).order_by('-level')

    # 2.实例化分页对象
    from app01.utils.pagination import Pagination
    page_object = Pagination(request, queryset)

    context = {
        'queryset': page_object.page_queryset,  # 分页之后的数据
        'search_data': search_data,             # 查询后的数据
        'page_string': page_object.html(),      # 生成页码
        'page': page_object.page,               #当前页码
    }
    return render(request, 'prettynum_list.html', context)

"""
from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据
        :param page_size: 每页展示多少条数据
        :param page_param: 在URL中传递的获取分页的参数:/user/list/?page=1
        :param plus: 显示当前页的前或后几页(页码)
        """
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        self.page_param = page_param
        page = request.GET.get(page_param, "1")

        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count

        if page.isdecimal():
            page = int(page)
            if page < 1 or page > total_page_count:
                page = 1
        else:
            page = 1
        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        self.plus = plus
        self.start_page = page - plus
        self.end_page = page + plus + 1

    def html(self):
        page_str_list = []
        self.query_dict.setlist(self.page_param, [1])

        head = '<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode())
        self.query_dict.setlist(self.page_param, [self.page - 1])
        prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(head)
        page_str_list.append(prev)
        for i in range(self.start_page, self.end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i <= 0 or i > self.total_page_count:
                continue
            elif i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), self.page)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        tail = '<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(tail)
        jump = """<div style="float: right;width:110px">
                        <form action="" method="get">
                            <div class="input-group">
                                <input type="text" class="form-control" placeholder="页码" name="page"
                                       value="{}">
                                <span class="input-group-btn">
                        <button class="btn btn-default" type="submit">跳转</button>
                        </span>
                            </div>
                        </form>
                    </div>""".format(self.page)
        page_str_list.append(jump)
        page_string = mark_safe("".join(page_str_list))
        return page_string
