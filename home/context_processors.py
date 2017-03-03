#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: alishtory
@site: https://github.com/alishtory/xsadmin
@time: 2017/2/26 18:10
'''
from django.conf import settings
from user.urls import menus
import copy

def site_config(request):
    siteconf =  settings.SITE_CONFIG
    siteconf['USER_MENUS'] = get_menus(request)
    return siteconf

def get_menus(request):
    path = request.path
    temp_menus = copy.deepcopy(menus)
    for menu in temp_menus:
        if path == menu.get('url', ''):
            menu['open'] = 'open'
            return temp_menus
        menu_subs = menu.get('children', ())
        for menu_sub in menu_subs:
            if path == menu_sub.get('url', ''):
                menu['open'] = 'open'
                menu_sub['active'] = 'active'
                return temp_menus
            menu_subs_subs = menu_sub.get('children', ())
            for menu_sub_sub in menu_subs_subs:
                if path == menu_sub_sub.get('url', ''):
                    menu['open'] = 'open'
                    menu_sub['active'] = 'active'
                    return temp_menus