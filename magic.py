# time: 2022/6/20 15:44
# author:AlwaysLazy21

import time
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    domain = 'https://pic.netbian.com'
    spacing = 3
    count = 0
    zone = {
        "风景": "/4kfengjing/",
        "美女": "/4kmeinv/",
        "游戏": "/4kyouxi/",
        "动漫": "/4kdongman/",
        "影视": "/4kyingshi/",
        "汽车": "/4kqiche/",
        "动物": "/4kdongwu/",
        "人物": "/4krenwu/",
        "美食": "/4kmeishi/",
        "宗教": "/4kzongjiao/",
        "背景": "/4kbeijing/",
        "手机壁纸": "/shoujibizhi/",
    }
    select = {
        "1": "风景",
        "2": "美女",
        "3": "游戏",
        "4": "动漫",
        "5": "影视",
        "6": "汽车",
        "7": "动物",
        "8": "人物",
        "9": "美食",
        "10": "宗教",
        "11": "背景",
        "12": "手机壁纸",
    }
    head = {
        'cookie': '__yjs_duid=1_6edb174479c365ee517ddf5939a367601653921055705; yjs_js_security_passport=aa82f2dadf63030bf06b15ad5cc158d7434b3b2f_1655719081_js',
        'referer': 'https://pic.netbian.com/4kfengjing/index_2.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Content-Type': 'text/html'
    }
    for k in select:
        print(k, select.get(k), end="\t")
    x = int(input("\n请输入你感兴趣的模块前的序号："))
    print("注意：照片数量=数量规模n*20")
    n = int(input("请输入你要要获取的照片数量规模n:"))
    print("现在为您爬取的模块是", select[str(x)])
    print("一共爬取照片数量", n * 20, "张")
    print("该程序会在", int(n * spacing / 3 + 1), "分钟左右完成所有操作")
    print("正在爬取照片请稍后...")
    for i in range(n):
        index = i + 1
        if index > 1:
            part = 'index_' + str(index) + '.html'
            url_main = domain + zone[select[str(x)]] + part
        else:
            url_main = domain + zone[select[str(x)]]
        print(url_main)
        resp_main = requests.get(url_main, headers=head)
        resp_main.encoding = 'gbk'
        time.sleep(spacing)
        if resp_main.status_code != 200:
            print("服务器拒绝了你的连接，请一段时间后重试")
        page_main = BeautifulSoup(resp_main.text, "html.parser")
        if x != 12:
            class_name = 'slist'
        else:
            class_name = 'alist'
        alist_child = page_main.find("div", class_=class_name).find_all("a")
        resp_main.close()
        for a in alist_child:
            href = domain + str(a.get("href"))
            resp_child = requests.get(href, headers=head)
            resp_child.encoding = 'gbk'
            if resp_child.status_code != 200:
                print("服务器拒绝了你的连接，请一段时间后重试")
            time.sleep(spacing)
            page_child = BeautifulSoup(resp_child.text, "html.parser")
            src_img = page_child.find("div", class_="photo-pic").find("img")
            resp_child.close()
            src = domain + src_img.get("src")
            resp_img = requests.get(src, headers=head)
            if resp_img.status_code != 200:
                print("服务器拒绝了你的连接，请一段时间后重试")
            time.sleep(spacing)
            img_path = "img/" + select[str(x)] + "/" + src.split("-")[-1]
            with open(img_path, "wb") as f:
                f.write(resp_img.content)
            count += 1
            print(count, '\t', src.split("-")[-1], "over!")
            resp_img.close()
    print("All Over!")
    time.sleep(5)
