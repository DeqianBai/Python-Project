#！/usr/bin/env python
#  -*- coding:utf-8 -*-
#  author:dabai time:2019/3/4

from pygal_maps_world.i18n import COUNTRIES
for country_code in sorted(COUNTRIES.keys()):
    print(country_code, COUNTRIES[country_code])