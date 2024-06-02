import requests
from bs4 import BeautifulSoup
import jieba.posseg as pseg
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from snownlp import SnowNLP
import networkx as nx
from pylab import mpl
from matplotlib.ticker import FuncFormatter

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']

# 初始化一个空列表，用于存储所有的标题
total_title=[]

# 创建一个空的文本文件，用于存储抓取的小说内容
with open('noval.txt','w',encoding='utf-8') as f:
    f.write('')

# 从指定的网址范围内抓取小说内容
for i in range(178295,178231,-1):
    url="http://m.sbkk8.com/waiguo/dawei_kebofeier/{}.html".format(i)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    flag=1
    # 由于网址访问过于频繁返回502错误，需要重新访问
    while(flag):
        try:
            print(url)
            r=requests.get(url,headers=headers)
            r.raise_for_status()#如果状态不是200，引发HTTPError异常
            r.encoding=r.apparent_encoding#解决乱码问题
            flag=0
        except:
            flag=1
    html = r.text    
    soup = BeautifulSoup(html,'html.parser')#解析网页
    title=soup.find('h1').text#获取标题
    total_title.append(title)
    # 将标题写入文本文件
    with open('noval.txt','a+',encoding='utf-8') as f:
        f.write(title+'\n')
    content=soup.find('div',class_='articleContent').text
    # 将内容写入文本文件
    with open('noval.txt','a+',encoding='utf-8') as f:
        f.write(content+'\n')

# 读取存储小说内容的文本文件
with open('noval.txt', 'r', encoding='utf-8') as file:
    novel_text = file.readlines()

# 创建一个新的文本文件，用于存储去除空行后的小说内容
with open('noval_copy.txt','w',encoding='utf-8') as f:
    f.write('')

# 去除空行
for i in range(len(novel_text)):
    if novel_text[i]!='\n':
        with open('noval_copy.txt','a+',encoding='utf-8') as f:
            f.write(novel_text[i])

# 读取去除空行后的小说内容
with open('noval_copy.txt', 'r', encoding='utf-8') as file:
    novel_text = file.readlines()

# 对小说内容进行情感分析
text=''
for i in range(len(novel_text)):
    novel_text[i]=novel_text[i].replace('\n','')
    if novel_text[i] in total_title:
        if i!=0:
            # 使用SnowNLP进行情感分析
            s = SnowNLP(text)
            # 获取整体情感分数（越接近1表示正面情感，越接近0表示负面情感）
            sentiment_score = s.sentiments
            # 打印结果
            print(f'{title }Sentiment Score: {sentiment_score}')
        text=''
        title=novel_text[i]
    text=text+novel_text[i]

# 读取小说内容
with open('noval.txt','r',encoding='utf-8') as f:
    txt=f.read()

# 去除特殊字符
for i in '!"#$%&()*+,-./:;<=>?@[\\]^_‘“”{|}~，。：！；？、':
    txt=txt.replace(i,' ')

# 使用jieba进行中文分词和词性标注
words_with_pos = pseg.lcut(txt)
# 过滤出名词
words = [word for word, pos in words_with_pos if pos.startswith('n') and len(word) >= 2]
# 使用Counter进行词频统计
word_count = Counter(words)
top_words = word_count.most_common(100)

# 打印词频统计结果
plt.figure(figsize=(10, 6))#创建一个图形对象，设置图形的大小为宽度 10 英寸，高度 6 英寸。
plt.bar([word for word, count in top_words[:20]], [count for word, count in top_words[:20]], color='red')
plt.xlabel('词语')  # 设置 x 轴标签
plt.ylabel('词频')  # 设置 y 轴标签
plt.title('大卫·科波菲尔小说中出现频率最高的 20 个名词')  # 设置图表标题
plt.savefig('大卫·科波菲尔小说中出现频率最高的 20 个名词.png')
plt.show()

# 将词频统计结果写入文本文件
for word, count in top_words:
    print(f'{word}: {count}')
for word, count in top_words:
    with open('word.txt','a+',encoding='utf-8') as f:
        f.write(word+'\n')
f.close()

# 读取词频统计结果
with open('word.txt', 'r', encoding='utf-8') as file:
    novel_text = file.read()

# 创建WordCloud对象
wordcloud = WordCloud(width=800, height=400, background_color='white', font_path='C:\Windows\Fonts\STZHONGS.TTF').generate(novel_text)

# 显示词云图
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()  #显示图

# 读取小说内容
with open('noval.txt', 'r', encoding='utf-8') as file:
    novel_text = file.readlines()

# 定义小说中的主要人物
characters = ["大卫",'贝西小姐','科波菲尔先生','皮果提先生','爱米丽','汉姆','特洛伍德小姐','妮丝','尤来亚', '朵拉', '詹姆斯'
                ,'斯梯福兹','狄克','大卫·科波菲尔','威克费尔德先生','尤来亚·希普','克里克尔先生','斯宾罗','姨奶奶','苏菲','特拉德尔','我']

# 统计人物共现次数
relation={}
for line in novel_text:
    for i in range(len(characters)):
        for j in range(i + 1, len(characters)):
            if characters[i] in line and characters[j] in line:
                names=characters[i]+'-'+characters[j]
                if names in relation:
                    relation[names]+=1
                else:
                    relation[names]=1

# 过滤出共现次数大于5的人物对
lsa = []
dic={}
for k,v in relation.items():
    k1,k2 = k.split('-')
    if v > 5:   # 选共同出现30次以上的人物对
        if k1 in ['大卫','我','大卫·科波菲尔']:
            k1 = '大卫·科波菲尔'
        if k2 in ['大卫','我','大卫·科波菲尔']:
            k2 = '大卫·科波菲尔'
        if k1==k2:
            continue
        dic[k]=v
        lsa.append([k1,k2,v])   #k1,k2为人物，v为两人共现次数

# 绘制人物共现次数的柱状图
plt.figure(figsize=(10, 6))#创建一个图形对象，设置图形的大小为宽度 10 英寸，高度 6 英寸。
plt.bar([k for k,v in dic.items()], [v for k,v in dic.items()], color='red')
plt.xlabel('人物')  # 设置 x 轴标签
plt.ylabel('共现次数')  # 设置 y 轴标签
plt.xticks(rotation=45, ha='right')
plt.title('大卫·科波菲尔小说中人物共现次数')  # 设置图表标题
plt.show()  #显示图

# 绘制人物关系网络
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体
mpl.rcParams['axes.unicode_minus']   # 正常显示负号
G = nx.Graph()
G.add_weighted_edges_from(lsa)   #添加节点（带权重）
nx.draw(G,with_labels=True,font_size=9,node_size=1200,node_color='#FF9999')
plt.savefig('大卫科波菲尔人物网络.png')   #保存图到文件
plt.show()   #显示图