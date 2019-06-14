# django-compressor 压缩静态文件

1. pip install django-compressor

2. INSTALLED_APPS 中添加 compressor

```python
INSTALLED_APPS=[
        ...
        'django.contrib.staticfiles',
        'compressor',  # 添加compressor moudle
    ],
```

3.设置中添加 STAITCFILES_FINDERS

```python
    STATIC_URL='/static/',
    STATIC_ROOT=os.path.join(BASE_DIR, 'static'),
    STAITCFILES_FINDERS=(
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder',
    ),

```

4. html 模板文件中添加 compress 标记, 压缩 css 和 js

```html
{% load staticfiles compress%}
<!DOCTYPE html>
<html lang="en">
  <head>
    {% compress css %}
    <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}" />
    <link rel="stylesheet" href="{% static 'css/site.css' %}" />
    {% endcompress %}
  </head>

  <body>
    {% compress js %}
    <script src="{% static 'js/jquery.min.js' %}"></script>
    <script src="{% static 'js/bootstrap.min.js' %}"></script>
    {% endcompress %}
  </body>
</html>
```

5. 相关设置，及运行 compress 命令
   自定义管理命令中

```python
from django.conf import settings
from django.core.management import call_command
...

settings.DEBUG = False
settings.COMPRESS_ENABLED = True

...
call_command('collectstatic', interactive=False, clear=True, verbosity=0)
call_command('compress', force=True)
```

执行命令,先满足 settings.COMPRESS_ENABLED = True

```bash
python xxx.py collectstatic
python xxx.py compress --force
```

## 结果

可以在 STATIC_ROOT 目录下看到生成了一个 CACHE 文件夹，存放着压缩过的 css 和 js, html 里的 css,js 引用也会对应的更新，
甚至是多个 css 变为一个
