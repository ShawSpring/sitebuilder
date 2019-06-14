import os
import json

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.template import Template, Context
from django.utils._os import safe_join
from django.template.loader_tags import BlockNode

import logging
logging.basicConfig(
    level=logging.INFO,
    filename='a.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_page_or_404(name):
    try:
        file_path = safe_join(settings.SITE_PAGES_DIRECTORY, name)
    except ValueError:
        raise Http404('Page not found!')
    else:
        if not os.path.exists(file_path):
            raise Http404('Page not found!')

    with open(file_path, 'r') as f:
        page = Template(f.read())

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
