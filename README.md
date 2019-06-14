# 静态站定生成器
## 环境
django 2.1
python 3.6

## 关键技术点
1. 将pages（非template目录）下的文件读取，再将之生成Template(), 传入基本布局页面page.html模板的context中去渲染。
```python
from django.utils._os import safe_join
def get_page_or_404(name):
    try:
        file_path = safe_join(settings.SITE_PAGES_DIRECTORY, name)## 找到pagex下的文件
    except ValueError:
        raise Http404('Page not found!')
    else:
        if not os.path.exists(file_path):
            raise Http404('Page not found!')

    with open(file_path, 'r') as f:
        page = Template(f.read())
    return page


def page(request, slug='index'):
    """ render th request page if found."""
    file_name = '{}.html'.format(slug)
    page = get_page_or_404(file_name)
    context = {'slug': slug, 'page': page}
    return render(request, 'page.html', context)
```

2. 自定义管理命令 build, 位于 sitebuilder/managements/commands/build.py
```bash
   python prototypes.py build
```
   将自动执行build.py中的自定义命令， 该命令将 django模板，url等动态技术生成的内容转换成真正的静态
    
3. [django-compressor 压缩静态文件](https://github.com/ShawSpring/sitebuilder/blob/master/django-compressor%20%E5%8E%8B%E7%BC%A9%E9%9D%99%E6%80%81%E6%96%87%E4%BB%B6.md)

4. 缓存 和 哈希化 css 和 js文件
    setting中：
```python
   STATICFILES_STORAGE='django.contrib.staticfiles.storage.CachedStaticFilesStorage'
```
    当debug=False时， 静态文件的文件名自动哈希化，文件名因此独一无二，这样一来，一但文件有丁点改动，就会不再使用浏览器缓存。
5. 将 html中BlockNode节点内的 json数据 自动转换成 context去渲染。
   ```python
    from django.template import Template, Context

    from django.template.loader_tags import BlockNode

    import logging
    logging.basicConfig(
        level=logging.INFO,
        filename='a.log',
        filemode='w',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


    def get_page_or_404(name):
       ...
        """
        将 html中的{% block context %}这种BlockNode数据先pop出来,再用render,序列化后填加到context中
        本来是在python代码中 context词典中写的数据，现在可以用json形式写到html中了。
        """
        meta = None
        for i, node in enumerate(list(page.nodelist)):
            if isinstance(node, BlockNode) and node.name == "context":
                meta = page.nodelist.pop(i)
                break
        page._meta = meta
        return page

    def page(request, slug='index'):
        """ render th request page if found."""
        file_name = '{}.html'.format(slug)
        page = get_page_or_404(file_name)
        context = {'slug': slug, 'page': page}
        if page._meta is not None:
            meta = page._meta.render(Context())
            logging.info(meta)
            extra_context = json.loads(meta)
            context.update(extra_context)
        return render(request, 'page.html', context)

   ``` 