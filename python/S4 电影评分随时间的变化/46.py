import matplotlib.pyplot as plt
import numpy as np

# 数据
seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
high_score_ratios = [0.465, 0.500, 0.455, 0.450]  # 高分电影比例（4星和5星的比例）
std_devs = [1.2, 1.05, 1.15, 1.1]  # 评分标准差

# 设置颜色
high_score_color = '#2ca02c'  # 高分电影比例颜色
std_dev_color = '#d62728'  # 标准差颜色

# 创建画布
plt.figure(figsize=(10, 6))

# 设置柱状图的位置
x = np.arange(len(seasons))  # 横轴位置
width = 0.35  # 柱状图宽度

# 绘制高分电影比例柱状图（左侧）
plt.bar(x - width/2, high_score_ratios, width, color=high_score_color, label='High Score Ratio (4 & 5 Stars)', alpha=0.8)

# 绘制评分标准差柱状图（右侧）
plt.bar(x + width/2, std_devs, width, color=std_dev_color, label='Standard Deviation', alpha=0.8)

# 设置标题和标签
plt.title('High Score Ratio and Standard Deviation by Season', fontsize=16, pad=20)
plt.xlabel('Season', fontsize=14)
plt.ylabel('Value', fontsize=14)

# 设置横轴和纵轴刻度
plt.xticks(x, seasons, fontsize=12)
plt.yticks(fontsize=12)

# 添加图注
plt.legend(title='Metrics', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()