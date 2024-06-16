import pandas as pd
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler

# 设置matplotlib的字体和符号，以便正确显示中文和负号
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 从Excel文件中读取CPI数据
cpi = pd.read_excel("CPI.xlsx")

# 去掉首列（指标分类）和首行（总CPI），并将数据转换为numpy数组
data = cpi.iloc[1:, 1:].to_numpy()

# 获取CPI类别和采样时间
d = cpi["指标"][1:]
t = cpi.columns[1:]

# 使用StandardScaler进行数据标准化
scaler = StandardScaler()
y = scaler.fit_transform(data).T  # y第一维为时间，第二维为类别

# 使用PCA进行主成分分析，保留4个主成分
pca = PCA(n_components=4)
pca.fit(y)

# 打印解释的方差比例的总和
print(pca.explained_variance_ratio_.sum())

# 创建一个新的图形，设置dpi和大小
plt.figure(dpi=300, figsize=(12, 12))

# 对每个主成分进行绘图
for i, c in enumerate(pca.components_):
    plt.subplot(220 + i + 1)  # 两行两列布局的第i+1个图
    plt.grid()
    plt.bar(d, c, alpha=0.8**i)  # 绘制条形图
    plt.xticks(rotation=90)  # x轴标签竖放
    plt.title(f"component{i+1}, explain ratio {pca.explained_variance_ratio_[i]:.2f}")  # 设置标题
plt.tight_layout()  # 排版
# plt.show()  # 显示图形
plt.savefig('figure_1.png')

# 对数据进行PCA转换
y_transformed = pca.transform(y)

# 创建一个新的图形，设置dpi
plt.figure(dpi=300)

# 对每个主成分的得分进行绘图
for i, s in enumerate(y_transformed.T):
    plt.subplot(220 + i + 1)
    plt.grid()
    plt.plot(t, s)  # 绘制折线图
    plt.xticks(rotation=30)
    plt.title(f"component {i+1}")  # 设置标题
    plt.ylim(-3, 3)
plt.tight_layout()
# plt.show()  # 显示图形
plt.savefig('figure_2.png')