#！/usr/bin/env python
#  -*- coding:utf-8 -*-
#  author:dabai time:2019/3/7

import requests
import pygal
from pygal.style import LightColorizedStyle as LCS,LightenStyle as LS
# 执行API调用并存储响应

url='https://api.github.com/search/repositories?q=language:python&sort=stars'
r=requests.get(url)
print("Status code:",r.status_code)

# 将API响应存储在一个变量中
response_dict=r.json()
# 打印了与 'total_count' 相关联的值，它指出了GitHub总共包含多少个Python仓库
print("Total repositories:", response_dict['total_count'])

# 探索有关仓库的信息
repo_dicts=response_dict['items']
# print("Repositories returned:",len(repo_dicts))

# 研究第一个仓库
# repo_dict= repo_dicts[0]
# print("\nKeys:",len(repo_dict)) # 打印这个字典包含的键数，看看其中有多少信息
# for key in sorted(repo_dict.keys()): # 打印这个字典的所有键，看看其中包含哪些信息
#     print(key)

# print("\nSelected information about first repository")
# print('Name:',repo_dict['name'])                # 打印项目名称
# print('Owner:',repo_dict['owner']['login'])     # 使用键 owner 来访问表示所有者的字典，再使用键 key 来获取所有者的登录名
# print('Stars:',repo_dict['stargazers_count'])   # 打印项目获得了多少个星的评级
# print('Repository:', repo_dict['html_url'])     # 打印项目在GitHub仓库的URL
# print('Created:', repo_dict['created_at'])      # 显示项目的创建时间
# print('Updated:', repo_dict['updated_at'])      # 最后一次更新的时间
# print('Description:', repo_dict['description']) # 打印仓库的描述

# 概述最受欢迎的仓库
# print("\nSelected information about each repository")
# for repo_dict in repo_dicts:
#     print('\nName:', repo_dict['name'])  # 打印项目名称
#     print('Owner:', repo_dict['owner']['login'])  # 使用键 owner 来访问表示所有者的字典，再使用键 key 来获取所有者的登录名
#     print('Stars:', repo_dict['stargazers_count'])  # 打印项目获得了多少个星的评级
#     print('Repository:', repo_dict['html_url'])  # 打印项目在GitHub仓库的URL
#     print('Description:', repo_dict['description'])  # 打印仓库的描述

names,plot_dicts=[],[] # 创建两个空列表 names 和 plot_dicts 。为生成x轴上的标签，我们依然需要列表 names
for repo_dict in repo_dicts:
    names.append(repo_dict['name'])

    # 循环内部，对于每个项目，我们都创建了字典 plot_dict
    # 使用键 'value' 存储了星数，并使用键 'label' 存储了项目描述
    plot_dict={
        'value':repo_dict['stargazers_count'],
        'label':str(repo_dict['description']),
        'xlink': repo_dict['html_url']
    }
    plot_dicts.append(plot_dict) # 将字典 plot_dict 附加到 plot_dicts 末尾


# 可视化
my_style=LS('#333366',base_style=LCS)

my_config=pygal.Config()  # 创建一个Pygal类Config 的实例，并将其命名为 my_config 。通过修改my_config的属性，可定制图表的外观
my_config.x_label_rotation=45
my_config.show_legend=False
my_config.title_font_size=24       # 设置了图表标题,副标签和主标签的字体大小
my_config.label_font_size=14       # 副标签是x轴上的项目名以及y轴上的大部分数字
my_config.major_label_font_size=18 # 主标签是y轴上为5000整数倍的刻度；这些标签应更大，以与副标签区分开来
my_config.truncate_label=15        # 使用truncate_label 将较长的项目名缩短为15个字符（如果你将鼠标指向屏幕上被截短的项目名，将显示完整的项目名）
my_config.show_y_guides=False      # 将 show_y_guides 设置为 False ，以隐藏图表中的水平线
my_config.width=1000               # 设置了自定义宽度，让图表更充分地利用浏览器中的可用空间

chart=pygal.Bar(my_config,style=my_style) # 创建 Bar 实例时，我们将 my_config 作为第一个实参，从而通过一个实参传递了所有的配置设置
                                          # 可以通过 my_config 做任意数量的样式和配置修改，而此处的代码行将保持不变
chart.title='Most-Starred Python Projects on GitHub'
chart.x_labels=names

chart.add('',plot_dicts) # 将列表 plot_dicts 传递给了 add()
chart.render_to_file('python_repos.svg')