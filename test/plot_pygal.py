#!/usr/bin/env python

import pygal

def run():
    tid_list = [1,2,3,4]
    ans = [10, 20, 30, 40]
    total = 100
    plot(tid_list, ans, total)

def plot(tid_list, ans, total):
    garph = pygal.StackedBar()    # 创建图（叠加柱状图）

    ans = [10,0,0,0]
    apple_data = [20,0,0,0]
    data3 = [30,0,0,0]

    garph.add('香蕉的历年销量', ans)
    garph.add('苹果的历年销量', apple_data)
    garph.add('苹果的历年销量', data3)

    garph.x_labels = [1]            # 设置 X 轴刻度
    garph.y_label_rotation = 45           # 设置Y轴的标签旋转多少度

    garph.title = '香蕉与苹果历年的销量分析'  # 设置图标题
    garph.x_title = '年份'                 # 设置 X 轴标题
    garph.y_title = '销量（吨）'            # 设置 Y 轴标题

    garph.legend_at_bottom = True         # 设置图例位置（下面）

    garph.margin = 35    # 设置页边距（margin_bottom、margin_top、margin_left、margin_right）

    garph.show_x_guides = True    # 显示X轴的网格线
    garph.show_y_guides = True    # 显示Y轴的网格线

    garph.render_to_file('fruit.svg')    # 输出到图片文件

run()
