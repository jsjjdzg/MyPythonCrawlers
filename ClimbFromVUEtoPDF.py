#! usr/bin/env python3
# -*- coding:UTF-8 -*-
# author DZG 2017-02-15

import requests
from bs4 import BeautifulSoup as bs
import pdfkit
import time
import os

total_url = 'http://cn.vuejs.org/v2/guide/index.html'
ISOTIMEFORMAT = '%Y-%m-%d %X'
file_name_all = "Vue官方中文文档-V2.0+.pdf"

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</html>
</body>
"""

# 将传入的url分析为Html文件
def parse_url_to_html(url, name):
    response = requests.get(url)
    soup = bs(response.content, 'lxml')
    # 有时候图片选取的是服务器本地图片，需要转换
    imgFiles = soup.find_all("img")
    for img in imgFiles:
        src = str(img.get("src"))
        if(src.startswith('/')):
            img.attrs["src"] = "http://cn.vuejs.org" + src
    # 转换图片后的Html才是完整的Html
    # 正文
    body = soup.find_all(class_="content")[0]
    # 标题
    title = soup.find_all("h1")[0].text
    # 标题加入到正文的最前面，居中显示
    center_tag = soup.new_tag("center")
    title_tag = soup.new_tag("h1")
    title_tag.insert(1, title)
    center_tag.insert(1, title_tag)
    body.insert(1, center_tag)
    html = str(body)
    html = html_template.format(content=html)
    html = html.encode("utf-8")
    with open(name, "wb") as f:
        f.write(html)
    return name

# 获取一堆文档Url
def get_url_list(url):
    # 获取该url下的所有目录Url
    response = requests.get(url)
    soup = bs(response.content, 'lxml')
    allmeaus = soup.find_all(class_="menu-root")[0]
    urls = []
    for li in allmeaus.find_all("li"):
	    href = ''
	    if(li.a != None):
	        lihref = li.a.get("href")
	        if(lihref != None):
		        href_1 = str(lihref)
		        if(href_1.startswith('/')):
			        href = "http://cn.vuejs.org" + href_1
			        urls.append(href)
    return urls

# 将Html转换为pdf
def save_pdf(htmls, file_name):
    options = {
        'page-size': 'A4',
        'margin-top': '0',
        'margin-right': '0',
        'margin-bottom': '0',
        'margin-left': '0',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'outline-depth': 10
    }
    pdfkit.from_file(htmls, file_name, options=options)

def main1():
    urls = get_url_list(total_url)
    htmls = [parse_url_to_html(url,str(index)+".html") for index,url in enumerate(urls)]
    save_pdf(htmls,file_name_all)
    return htmls

def main2(htmls):
    for html in htmls:
        os.remove(html)

if __name__ == '__main__':
    print('开始：', time.strftime(ISOTIMEFORMAT, time.localtime()))
    start = time.time()
    hs = main1()
    main2(hs)
    total_time = time.time() -start
    print('结束：', time.strftime(ISOTIMEFORMAT, time.localtime()))
    print("总耗时："+total_time+"秒")
