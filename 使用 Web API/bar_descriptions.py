#！/usr/bin/env python
#  -*- coding:utf-8 -*-
#  author:dabai time:2019/3/11

import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS
my_style = LS('#333366', base_style=LCS)
chart=pygal.Bar(style=my_style,x_label_rotation=45,show_legend=False)

chart.title='Python project'
chart.x_labels=['httpie','django','flask']

# 定义了一个名为 plot_dicts 的列表，其中包含三个字典，分别针对项目HTTPie、
# Django和Flask。每个字典都包含两个键： 'value' 和 'label' 。Pygal根据与键 'value' 相关联的
# 数字来确定条形的高度，并使用与 'label' 相关联的字符串给条形创建工具提示
plot_dicts=[
    {'value': 16101, 'label': 'Description of httpie.','xlink':'html_url'},
    {'value': 15028, 'label': 'Description of django.','xlink':'html_url'},
    {'value': 14798, 'label': 'Description of flask.','xlink':'html_url'}
]

chart.add('',plot_dicts) # 方法 add() 接受一个字符串和一个列表 这里调用 add() 时，我们传入了一个由表示条形的字典组成的列表(plot_dicts)
chart.render_to_file('bar_description.svg')