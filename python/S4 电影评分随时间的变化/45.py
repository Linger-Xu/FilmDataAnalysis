import matplotlib.pyplot as plt
import numpy as np

# 数据
seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
mean_ratings = [3.3168794899625986,3.3693824770655114, 3.338779210562589,  3.3011268634841735]
rating_counts = [
    [78601, 133858, 351810, 312503, 152329],  # Spring
    [93735, 154565, 422254, 402544, 205980],   # Summer
    [67661, 113276, 299440, 273050, 138930],  # Autumn
    [78325, 127845, 330516, 288144, 144054],  # Winter
]

# 设置颜色
colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd']
labels = ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars']

# 创建画布
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# 子图1：柱状堆叠图
bottom = np.zeros(len(seasons))  # 用于堆叠的初始值
for i in range(5):
    ax1.bar(seasons, [counts[i] for counts in rating_counts], bottom=bottom, color=colors[i], label=labels[i], alpha=0.8)
    bottom += [counts[i] for counts in rating_counts]  # 更新堆叠的初始值
ax1.set_title('Seasonal Distribution of User Ratings (Stacked Bar Chart)', fontsize=16, pad=20)
ax1.set_ylabel('Number of Users', fontsize=14)
ax1.legend(title='Rating', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# 子图2：均分柱状图
ax2.bar(seasons, mean_ratings, color='#1f77b4', alpha=0.8)
ax2.set_title('Mean Ratings by Season', fontsize=16, pad=20)
ax2.set_ylabel('Mean Rating', fontsize=14)
ax2.set_ylim(3.2, 3.4)  # 评分范围一般为0-5
ax2.grid(axis='y', linestyle='--', alpha=0.7)

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()