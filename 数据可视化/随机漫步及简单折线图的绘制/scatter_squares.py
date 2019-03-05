#！/usr/bin/env python
#  -*- coding:utf-8 -*-
#  author:dabai time:2019/2/28

import matplotlib.pyplot as plt

# x_values = [1, 2, 3, 4, 5]
# y_values = [1, 4, 9, 16, 25]

x_values = list(range(1, 1001))
y_values = [x**2 for x in x_values]

# plt.scatter(x_values, y_values,c='red',edgecolor='none', s=20)

# 使用RGB颜色模式自定义颜色。要指定自定义颜色，可传递参数 c ，并将其设置为一个元组，
# 其中包含三个0~1之间的小数值，它们分别表示红色、绿色和蓝色分量
plt.scatter(x_values, y_values, c=(0, 0, 0.8), edgecolor='none', s=40)

# 颜色映射:这些代码将y值较小的点显示为浅蓝色，并将y值较大的点显示为深蓝色
plt.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Blues,edgecolor='none', s=40)


# 设置图表标题并给坐标轴加上标签
plt.title("Square Numbers", fontsize=24)
plt.xlabel("Value", fontsize=14)
plt.ylabel("Square of Value", fontsize=14)

# 设置刻度标记的大小
plt.tick_params(axis='both', which='major', labelsize=14)

# 设置每个坐标轴的取值范围
plt.axis([0, 1100, 0, 1100000])

# 自动保存图表
# 第一个实参指定要以什么样的文件名保存图表,这个文件将存储到scatter_squares.py所在的
# 目录中;第二个实参指定将图表多余的空白区域裁剪掉。如果要保留图表周围多余的空白区域,可省略这个实参

plt.savefig('squares_plot.png', bbox_inches='tight')
plt.show()