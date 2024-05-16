# 网络信息爬取——理科(一)

## 文件

* 注册资金最多的公司 top20.png —— 结果展示图
* code_easy_verion  —— 去除了反爬虫的部分
* code.ipynb —— 就是jupyter版本，看要求和code.py随便交一个就行
* code.py —— 完整的爬虫代码
* content.csv —— 爬取的信息
* requirements.txt —— 环境依赖

## 如何使用

我的电脑装的是conda所以使用的是conda管理虚拟环境，源是清华源

首先创建虚拟环境

```powershell
conda creat -n crawler_venv python=3.10
```

然后安装依赖

```powershell
conda activate crawler_venv
pip install -r requirements.txt
```

接着你运行就行了
