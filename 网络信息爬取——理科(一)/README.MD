# 网络信息爬取——理科(一)

## 注意注意注意

这个文件夹可能因为名字中有括号（不想改了，因为题目是这个命名），我自己的电脑会因为符号问题运行不了，需要把代码放别的地方跑

## 文件

* code_easy_verion  —— 去除了反爬虫的部分
* code.ipynb —— 就是jupyter版本，看要求和code.py随便交一个就行
* code.py —— 完整的爬虫代码
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
