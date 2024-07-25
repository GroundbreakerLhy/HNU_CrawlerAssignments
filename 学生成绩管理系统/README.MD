# 学生成绩管理系统

是什么垃圾教程……不知道几年前写的，pandas类已经没有append方法了都，已经换成了concat方法……真的难绷

## 文件

* grade.ipynb —— 代码
* requirements.txt —— 环境依赖
* stu.csv —— 数据（头歌扒下来的，万一今年变了要注意）

这个题很奇怪，会有要用户输入的部分，不知道助教是怎么评阅的，反正放注释里了

## 如何使用

我的电脑装的是conda所以使用的是conda管理虚拟环境，源是清华源

首先创建虚拟环境

```powershell
conda create -n data_venv python=3.10
```

然后安装依赖

```powershell
conda activate data_venv
pip install -r requirements.txt
```

接着你运行就行了
