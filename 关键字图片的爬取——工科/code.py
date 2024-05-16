# 代码来自Groundbreaker 
# 想联系我的话花点心思不难找到我的联系方式
# 如果今年题目变了代码用不了了，可以在Github上找到我，我会尽快更新代码
import re
import requests
import os
import time
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'Cookie': '',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

url = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111110&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E5%B7%A5%E7%A8%8B%E5%B8%88&oq=%E5%B7%A5%E7%A8%8B%E5%B8%88&rsp=-1'

html = requests.get(url, headers=header)
html.encoding = 'utf8'
html = html.text

# 获取当前工作目录
scriptDir = os.getcwd()
imgsPath = os.path.join(scriptDir, 'Img')

# 如果路径不存在则创建
if not os.path.exists(imgsPath):
    os.mkdir(imgsPath)

res = re.findall('"objURL":"(.*?)"', html)
num = 0
for imgUrl in res:
    num += 1
    try:
        imgResponse = requests.get(imgUrl, headers=header)
        imgResponse.raise_for_status()
    except requests.exceptions.RequestException as e:
        continue

    imgFileName = os.path.join(imgsPath, f'Img_{num}.jpg')

    with open(imgFileName, 'wb') as imgFile:
        imgFile.write(imgResponse.content)

    time.sleep(1)

print("下载完成。")
