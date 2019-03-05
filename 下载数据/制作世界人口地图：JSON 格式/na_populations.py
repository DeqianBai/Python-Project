#！/usr/bin/env python
#  -*- coding:utf-8 -*-
#  author:dabai time:2019/3/4

import pygal_maps_world.maps

wm = pygal_maps_world.maps.World()

wm.title = 'Populations of Countries in North America'
wm.add('North America', {'ca': 34126000, 'us': 309349000, 'mx': 113423000})
wm.render_to_file('na_populations.svg')