# -*- coding: utf-8 -*-
#encoding=utf-8

"""
李运辰 2021-3-11

公众号：python爬虫数据分析挖掘
"""


# 导包
import pandas as pd
import os
# from pyecharts import options as opts
# from pyecharts.globals import ThemeType
# from pyecharts.charts import Bar
# from pyecharts.charts import Pie
from stylecloud import gen_stylecloud
import jieba

#读入数据
df_all = pd.read_csv("笔记本电脑-李运辰.csv",engine="python")
df = df_all.copy()
# 重置索引
df = df.reset_index(drop=True)


#展示每个品牌的数据量
def an1():

    brand_counts = df.groupby('brand')['price'].count().sort_values(ascending=False).reset_index()
    brand_counts.columns = ['品牌', '数据量']
    name = (brand_counts['品牌']).tolist()
    dict_values = (brand_counts['数据量']).tolist()

    ##去掉英文名称
    for i in range(0, len(name)):
        if "（" in name[i]:
            name[i] = name[i][0:int(name[i].index("（"))]

        # 链式调用
        c = (
            Bar(
                init_opts=opts.InitOpts(  # 初始配置项
                    theme=ThemeType.MACARONS,
                    animation_opts=opts.AnimationOpts(
                        animation_delay=1000, animation_easing="cubicOut"  # 初始动画延迟和缓动效果
                    ))
            )
                .add_xaxis(xaxis_data=name)  # x轴
                .add_yaxis(series_name="展示每个品牌的数据量", yaxis_data=dict_values)  # y轴
                .set_global_opts(
                title_opts=opts.TitleOpts(title='', subtitle='',  # 标题配置和调整位置
                                          title_textstyle_opts=opts.TextStyleOpts(
                                              font_family='SimHei', font_size=25, font_weight='bold', color='red',
                                          ), pos_left="90%", pos_top="10",
                                          ),
                xaxis_opts=opts.AxisOpts(name='品牌', axislabel_opts=opts.LabelOpts(rotate=45)),
                # 设置x名称和Label rotate解决标签名字过长使用
                yaxis_opts=opts.AxisOpts(name='数据量'),

            )
                .render("展示每个品牌的数据量.html")
        )

#最高价格对比
def an2():
    brand_maxprice = df.groupby('brand')['price'].agg(['max'])['max'].sort_values(ascending=False).reset_index()
    brand_maxprice.columns = ['品牌', '最高价']
    name = (brand_maxprice['品牌']).tolist()
    dict_values = (brand_maxprice['最高价']).tolist()

    ##去掉英文名称
    for i in range(0, len(name)):
        if "（" in name[i]:
            name[i] = name[i][0:int(name[i].index("（"))]

        # 链式调用
    c = (
        Bar(
            init_opts=opts.InitOpts(  # 初始配置项
                theme=ThemeType.MACARONS,
                animation_opts=opts.AnimationOpts(
                    animation_delay=1000, animation_easing="cubicOut"  # 初始动画延迟和缓动效果
                ))
        )
            .add_xaxis(xaxis_data=name)  # x轴
            .add_yaxis(series_name="最高价格对比", yaxis_data=dict_values)  # y轴
            .set_global_opts(
            title_opts=opts.TitleOpts(title='', subtitle='',  # 标题配置和调整位置
                                      title_textstyle_opts=opts.TextStyleOpts(
                                          font_family='SimHei', font_size=25, font_weight='bold', color='red',
                                      ), pos_left="90%", pos_top="10",
                                      ),
            xaxis_opts=opts.AxisOpts(name='品牌', axislabel_opts=opts.LabelOpts(rotate=45)),
            # 设置x名称和Label rotate解决标签名字过长使用
            yaxis_opts=opts.AxisOpts(name='最高价'),

        )
            .render("最高价格对比.html")
    )

#价格均值
def an3():
    brand_meanprice = df.groupby('brand')['price'].agg(['mean'])['mean'].sort_values(ascending=False).reset_index()
    brand_meanprice.columns = ['品牌', '价格均值']
    name = (brand_meanprice['品牌']).tolist()
    dict_values = (brand_meanprice['价格均值']).tolist()

    ##去掉英文名称
    for i in range(0, len(name)):
        if "（" in name[i]:
            name[i] = name[i][0:int(name[i].index("（"))]

    # 价格转为整数
    for i in range(0, len(dict_values)):
        dict_values[i] = int(dict_values[i])

        # 链式调用
        c = (
            Bar(
                init_opts=opts.InitOpts(  # 初始配置项
                    theme=ThemeType.MACARONS,
                    animation_opts=opts.AnimationOpts(
                        animation_delay=1000, animation_easing="cubicOut"  # 初始动画延迟和缓动效果
                    ))
            )
                .add_xaxis(xaxis_data=name)  # x轴
                .add_yaxis(series_name="价格均值对比", yaxis_data=dict_values)  # y轴
                .set_global_opts(
                title_opts=opts.TitleOpts(title='', subtitle='',  # 标题配置和调整位置
                                          title_textstyle_opts=opts.TextStyleOpts(
                                              font_family='SimHei', font_size=25, font_weight='bold', color='red',
                                          ), pos_left="90%", pos_top="10",
                                          ),
                xaxis_opts=opts.AxisOpts(name='品牌', axislabel_opts=opts.LabelOpts(rotate=45)),
                # 设置x名称和Label rotate解决标签名字过长使用
                yaxis_opts=opts.AxisOpts(name='价格均值'),

            )
                .render("价格均值对比.html")
        )

#各大品牌标题词云
def an4():
    brand_title = df.groupby('brand')['title']
    brand_title = list(brand_title)

    for z in range(0, len(brand_title)):
        brandname = brand_title[z][0]
        print(brandname)
        if "（" in brandname:
            brandname = brandname[0:int(brandname.index("（"))]
        brandname = str(brandname).encode("utf-8").decode('utf8')
        print(brandname)

        text = "".join((brand_title[z][1]).tolist())
        text = text.replace(brand_title[z][0], "").replace(brandname, "").replace("\n\r", "").replace("\t", "").replace(
            "\n", "").replace("\r", "").replace("【", "").replace("】", "").replace(" ", "")

        with open("text1/"+str(brandname)+".txt","a+") as f:
            f.write(text)

def an4_pic():
    ###词云图标
    fa_list = ['fas fa-play', 'fas fa-audio-description', 'fas fa-circle', 'fas fa-eject', 'fas fa-stop',
               'fas fa-video', 'fas fa-volume-off', 'fas fa-truck', 'fas fa-apple-alt', 'fas fa-mountain',
               'fas fa-tree', 'fas fa-database', 'fas fa-wifi', 'fas fa-mobile', 'fas fa-plug']
    z = 0
    ##开始绘图
    for filename in os.listdir("text"):
        print(filename)
        with open("text/" + filename, "r") as f:
            text = (f.readlines())[0]

        with open("stopword.txt", "r", encoding='UTF-8') as f:
            stopword = f.readlines()

        for i in stopword:
            print(i)
            i = str(i).replace("\r\n", "").replace("\r", "").replace("\n", "")
            text = text.replace(i, "")
        word_list = jieba.cut(text)
        result = " ".join(word_list)  # 分词用 隔开

        # 制作中文云词
        icon_name = str(fa_list[z])
        gen_stylecloud(text=result, icon_name=icon_name, font_path='simsun.ttc',
                       output_name=str(filename.replace(".txt", "")) + "词云图.png")  # 必须加中文字体，否则格式错误
        z = z + 1

#展示每个品牌的数据量
#an1()
#最高价格对比
#an2()
#价格均值
#an3()
#各大品牌标题词云
#an4()
an4_pic()


""":cvar
1.爬取各大品牌笔记本数据
2.对数据到到excel
3.数据统计
4.可视化

公众号：python爬虫数据分析挖掘

公众号回复：笔记本分析




"""

