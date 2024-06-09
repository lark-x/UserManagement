import asyncio

from django.test import TestCase
# Create your tests here.
import asyncio


async def process_item(item):
    # 异步任务，例如数据库查询、网络请求等
    await asyncio.sleep(1)
    print(item)


async def main():
    my_list = [1, 2, 3, 4, 5]
    # 使用异步函数处理列表中的每个项目
    await asyncio.gather(*(process_item(item) for item in my_list))


asyncio.run(main())
