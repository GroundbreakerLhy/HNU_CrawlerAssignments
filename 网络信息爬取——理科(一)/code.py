# 代码来自Groundbreaker 
# 想联系我的话花点心思不难找到我的联系方式
# 如果今年题目变了代码用不了了，可以在Github上找到我，我会尽快更新代码

import requests
import re
import time
import csv
import matplotlib.pyplot as plt
import csv
import pandas as pd
import os 

# 用黑体显示中文
# mac用户这里自己注意, 你们的电脑可能没有这个字体, 可以换成你有的中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

message = []

# 由于需要爬取的数据过于庞大，有899页，不做处理的话会被网站拦截，因此做了判断
# 当发现被拦截后就从断点继续开始爬取

def fetchUrlWithRetry(url, maxRetries=3, retryDelay=5):# 判断有无被拦截
    retries = 0
    while retries < maxRetries:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch {url}. Retrying...")
            retries += 1
            time.sleep(retryDelay)
    return None

# 从断点处继续爬取数据
startI = 0
startJ = 0
filename = "content.csv"
path = os.getcwd()
filename = path + "/" + filename

try:
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        message = [row for row in reader]
    startI = len(message) // 100
    startJ = len(message) % 100
except FileNotFoundError:
    pass

for i in range(startI, 9):
    for j in range(startJ, 100):
        cnt = i * 100 + j
        if cnt == 0:
            url = "https://top.chinaz.com/gongsi/index_zhuce.html"
        else:
            url = "https://top.chinaz.com/gongsi/index_zhuce_{}.html".format(cnt + 1)
        html = fetchUrlWithRetry(url)
        if html:
            company = re.findall('<a.*?target="_blank">(.+?)</a></h3>', html)
            capital = re.findall('<em>(.+?)</em>', html)
            page = list(zip(company, capital))
            message.extend(page)
            print(f"Page {cnt} has been recorded.")
            if len(message) % 100 == 0:
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(message)
        else:
            print(f"Failed to fetch page {cnt} after multiple retries.")



with open("content.csv", "w", encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerows(message)

df = pd.read_csv(path + "/content.csv", names=["company", "capital"])

# 定义函数将字符串转换为数字
def strToNum(s):
    if '亿' in s:
        return float(s.replace('亿', '')) * 100000000
    elif '万' in s:
        return float(s.replace('万', '')) * 10000
    else:
        return float(s)
    
# 将capital列中的字符串转换为数字
df["capitalNum"] = df["capital"].apply(strToNum)

# 按capitalNum列从大到小排序并取前20名
df_sorted = df.sort_values(by="capitalNum", ascending=False).head(20)

print(df_sorted)

# 按capitalNum列从小到大排序
df_sorted = df_sorted.sort_values(by="capitalNum", ascending=True)

plt.figure(figsize=(8, 6))

# 绘制折线图
plt.plot(df_sorted["company"], df_sorted["capital"], marker='*', linestyle='-', color="red", label="注册资金")

# 绘制柱状图
plt.bar(df_sorted["company"], df_sorted["capital"], alpha=0.5, color="gold", label="注册资金")

plt.title("注册资金最多的公司 top20")
plt.xlabel("公司")
plt.xticks(rotation=90)
plt.ylabel("注册资金")
plt.legend()
plt.tight_layout()

plt.savefig('注册资金最多的公司 top20.png', format='png')

plt.show()