# 代码来自Groundbreaker 
# 想联系我的话花点心思不难找到我的联系方式
# 如果今年题目变了代码用不了了，可以在Github上找到我，我会尽快更新代码
import requests
import re
import csv
import matplotlib.pyplot as plt
import csv

# 用黑体显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']  

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

message = []

for i in range(0, 9):
    for j in range(0, 100):# 899页分段处理
        cnt = i * 100 + j
        if cnt == 0:
            url = "https://top.chinaz.com/gongsi/index_zhuce.html"
        else:
            url = "https://top.chinaz.com/gongsi/index_zhuce_{}.html".format(cnt + 1)
            
        response = requests.get(url, headers=headers)
        
        html = response.text

        if html:
            company = re.findall('<a.*?target="_blank">(.+?)</a></h3>', html)
            capital = re.findall('<em>(.+?)</em>', html)
            page = list(zip(company, capital))
            message.extend(page)
            print(f"Page {cnt} has been recorded.")
            if len(message) % 100 == 0:
                with open('content.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(message)
        else:
            print(f"Failed to fetch page {cnt} after multiple retries.")



with open("content.csv", "w") as f:
    w = csv.writer(f)
    w.writerows(message)
    import pandas as pd

df = pd.read_csv("content.csv", names=["company", "capital"])

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