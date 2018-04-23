#!/usr/bin/env python
# encoding: utf-8
"""
@version: 1.0
@author: Pis
@license: Apache Licence 
@software: PyCharm
@file: excel.py
@time: 2018/3/13 14:33
"""
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader


class ListImportExeclPlugin(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    def block_top_toolbar(self, context, nodes):
        nodes.append(loader.render_to_string('model_list.top_toolbar.importexport.import.html', context_instance=context))


xadmin.site.register_plugin(ListImportExeclPlugin, ListAdminView)
