#!/usr/bin/Python
# -*- coding: utf-8 -*-
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud, STOPWORDS
from scipy.misc import imread

###当前文件路径
d = path.dirname("D:\yanjiusheng\自然语言处理\数据")

# Read the whole text.
file = open(path.join(d, '华师简介.txt'),encoding='utf-8',errors='ignore').read()
##进行分词

default_mode =jieba.cut(file)
text = " ".join(default_mode)
stopwords = set(STOPWORDS)
stopwords.add("said")
myfont = r'C:\Windows\Fonts\simhei.ttf'
wc = WordCloud(font_path = myfont,
    mask = imread("D:\yanjiusheng\自然语言处理\Python数据分析系列视频课程--玩转文本挖掘\TMData190320-01\PythonData\射雕背景1.png"),
    mode = "RGBA", background_color = None
    )
# generate word cloud
wc.generate(text)

# store to file
wc.to_file(path.join(d, "ccnuwordcloud.png"))

# show
plt.imshow(wc)
plt.axis("off")
plt.show()