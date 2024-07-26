# 音乐播放器

这个题出的很不好，虽然跟着一到五学完可以对软件前端开发有个大致了解，但是作业设计太容易，敲几下就做完了(做了附加题又会超过别的题目难度了……).

这道题放头歌上要把所有涉及到文件路径的地方都改成老师示例.ipynb的路径，我这里是方便本地开发才这么写的

## 文件

* fig —— 图标文件夹
* music —— 音乐和歌词文件夹
* player.py —— 代码
* requirements.txt —— 环境依赖

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
