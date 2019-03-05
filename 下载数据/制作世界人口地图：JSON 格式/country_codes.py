#！/usr/bin/env python
#  -*- coding:utf-8 -*-
#  author:dabai time:2019/3/4

from pygal_maps_world.i18n import COUNTRIES

def get_country_code(country_name):
    """根据指定的国家，返回Pygal使用的两个字母的国别码"""
    for code, name in COUNTRIES.items():
        if name == country_name:
            return code
     # 如果没有找到指定的国家，就返回None
    return None
