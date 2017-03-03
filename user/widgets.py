#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: alishtory
@site: https://github.com/alishtory/xsadmin
@time: 2017/3/3 9:56
'''

from django.forms import widgets
from django.conf import settings
import os,re
from django.utils.html import format_html

allow_avatar_prex = re.compile(r'.*(\.(jpg|jpeg|png|gif|bmp))$',re.IGNORECASE)

class AvatarRadioSelect(widgets.Input):

    @staticmethod
    def avatars():
        # Override the default choices.
        avatar_dir = os.path.join(settings.BASE_DIR, 'static/images/avatars')
        avatar_list = os.listdir(avatar_dir)
        avatars = []
        for avat in avatar_list:
            if allow_avatar_prex.match(avat) and os.path.isfile(os.path.join(avatar_dir, avat)):
                avatars.append(avat)
        return avatars


    def render(self, name, value, attrs= None):
        html = ''
        avatars = AvatarRadioSelect.avatars()
        for avat in avatars:
            checked = ' checked="checked"' if avat== value  else ''
            html+= format_html("""<label style="margin-right:14px"><input type="radio" name="{}" value='{}'{}>
        <img alt='{}' src='{}' class='avatar avatar-32 photo' height='96'></label> """, name, avat, checked, avat, settings.STATIC_URL+'images/avatars/'+avat)
        return html
