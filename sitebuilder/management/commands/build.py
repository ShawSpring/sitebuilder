import os
import shutil

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import reverse
from django.test.client import Client


def get_pages():
    for name in os.listdir(settings.SITE_PAGES_DIRECTORY):
        if name.endswith('.html'):
            yield name[:-5]


class Command(BaseCommand):
    help = "Build static site output"
    leave_locale_alone = True
    """
    自定义管理命令 build 
    将内容转换成静态内容，不再是模板，生成静态站点
    输出到静态站点输出目录 STIE_OUTPUT_DIRECTORY，即根目录下的 _build
    1. output目录是否存在，存在则删除
    2. 创建output目录
    3. 创建 STATIC_ROOT目录，并call_command 'collectstatic' 将站点中所有的static文件收集到STATIC_ROOT
    4. 使用django.test.client,创建模拟客户端
    5. 遍历pages目录下的所有 .html文件，reverse()反转出url,再用client.get(url)得到html页面
    6. 将得到的response写入output目录下
    7. 运行该 自定义的管理命令： python prototypes.py build
       或者python prototypes.py build index
    8. 测试静态站点：cd _build, python -m http.server 9000
    """

    def add_arguments(self, parser):  #build命令后带参数
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        """request pages and build output"""
        settings.DEBUG = False

        if args:  # pages 有参数决定
            pages = args
            available = list(get_pages())
            invaild = []
            for page in pages:
                if page not in available:
                    invaild.append(page)
            if invaild:
                msg = "Invalid pass :{}".format(",".join(pages))
                raise CommandError(msg)
        else:  # 没有参数 pages指全部文件
            pages = get_pages()
            if os.path.exists(settings.STIE_OUTPUT_DIRECTORY):
                shutil.rmtree(settings.STIE_OUTPUT_DIRECTORY)
            os.mkdir(settings.STIE_OUTPUT_DIRECTORY)

        os.makedirs(settings.STATIC_ROOT, exist_ok=True)
        call_command(
            'collectstatic', interactive=False, clear=True, verbosity=0)
        client = Client()
        for page in pages:
            url = reverse('page', kwargs={'slug': page})
            response = client.get(url)
            if page == "index":
                output_dir = settings.STIE_OUTPUT_DIRECTORY
            else:
                output_dir = os.path.join(settings.STIE_OUTPUT_DIRECTORY, page)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
            with open(os.path.join(output_dir, 'index.html'), 'wb') as f:
                f.write(response.content)