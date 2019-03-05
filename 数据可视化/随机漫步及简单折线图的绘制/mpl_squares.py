#！/usr/bin/env python
#  -*- coding:utf-8 -*-
#  author:dabai time:2019/2/28

import matplotlib.pyplot as plt

input_values = [1, 2, 3, 4, 5]
squares=[1,4,9,16,25]
plt.plot(input_values,squares,linewidth=5)

# 设置图表标题，并给坐标轴加上标签
plt.title("Square Numbers", fontsize=24)
plt.xlabel("Value", fontsize=14)
plt.ylabel("Square of Value", fontsize=14)

# 设置刻度标记的大小
plt.tick_params(axis='both', labelsize=14)


plt.show()