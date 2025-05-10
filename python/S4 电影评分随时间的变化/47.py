import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 数据
seasons = [1, 2, 3, 4]  # 春-夏依次标记为1, 2, 3, 4
mean_ratings = [3.3168794899625986, 3.3011268634841735, 3.338779210562589, 3.3693824770655114]
rating_counts = [
    [78601, 133858, 351810, 312503, 152329],  # Spring
    [78325, 127845, 330516, 288144, 144054],  # Winter
    [67661, 113276, 299440, 273050, 138930],  # Autumn
    [93735, 154565, 422254, 402544, 205980]   # Summer
]

# 将数据转换为DataFrame
data = {
    'Season': seasons,
    'Mean Rating': mean_ratings,
    '1 Star': [counts[0] for counts in rating_counts],
    '2 Stars': [counts[1] for counts in rating_counts],
    '3 Stars': [counts[2] for counts in rating_counts],
    '4 Stars': [counts[3] for counts in rating_counts],
    '5 Stars': [counts[4] for counts in rating_counts]
}
df = pd.DataFrame(data)

# 计算相关系数矩阵
correlation_matrix = df.corr()

# 可视化相关系数热力图
plt.figure(figsize=(10, 8))
heatmap = plt.imshow(correlation_matrix, cmap='coolwarm', vmin=-1, vmax=1)

# 添加颜色条
cbar = plt.colorbar(heatmap)
cbar.set_label('Correlation Coefficient', fontsize=12)

# 设置标题和标签
plt.title('Correlation Heatmap of Season, Mean Rating, and Rating Counts', fontsize=16, pad=20)
plt.xlabel('Variables', fontsize=14)
plt.ylabel('Variables', fontsize=14)

# 设置横轴和纵轴刻度
variables = ['Season', 'Mean Rating', '1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars']
plt.xticks(np.arange(len(variables)), variables, fontsize=12, rotation=45)
plt.yticks(np.arange(len(variables)), variables, fontsize=12)

# 在热力图中显示相关系数值
for i in range(len(variables)):
    for j in range(len(variables)):
        plt.text(j, i, f'{correlation_matrix.iloc[i, j]:.2f}', ha='center', va='center', color='black', fontsize=10)

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()