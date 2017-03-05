#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: alishtory
@site: https://github.com/alishtory/xsadmin
@time: 2017/2/26 18:10
'''
from django.conf import settings
from user.urls import menus
from django.urls import resolve
import copy

def site_config(request):
    siteconf =  settings.SITE_CONFIG
    path_resovle = resolve(request.path)
    #print('path_resovle:',path_resovle)
    if 'user' in path_resovle.app_names:
        siteconf['USER_MENUS'], siteconf['USER_BREADCRUMBS'] = get_menus_breadcrumbs('user:'+path_resovle.url_name)
        now_bread = siteconf['USER_BREADCRUMBS'][-1]
        siteconf['USER_BREADCRUMBS_TITLE'] = now_bread.get('title','')+' | '+now_bread.get('title_en','')
        siteconf['USER_DASHBOARD_TITLE'] = now_bread.get('title','无标题')
    #print('siteconf',siteconf)
    return siteconf

def get_menus_breadcrumbs(url_name ):
    temp_menus = copy.deepcopy(menus)
    for menu in temp_menus:
        if url_name == menu.get('url_name', ''):
            menu['open'] = 'open'
            return temp_menus, (menu,)
        menu_subs = menu.get('children', ())
        for menu_sub in menu_subs:
            if url_name == menu_sub.get('url_name', ''):
                menu['open'] = 'open'
                menu_sub['active'] = 'active'
                return temp_menus, (menu, menu_sub)
            menu_subs_subs = menu_sub.get('children', ())
            for menu_sub_sub in menu_subs_subs:
                if url_name == menu_sub_sub.get('url_name', ''):
                    menu['open'] = 'open'
                    menu_sub['active'] = 'active'
                    return temp_menus, (menu, menu_sub, menu_sub_sub)
    else:
        return temp_menus, (temp_menus[0],)
