import matplotlib.pyplot as plt
import numpy as np

# 数据
ratings = ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars']
rating_counts = [318322, 529544, 1404020, 1276241, 641293]

user_categories = [
    'Only 1 or 5 Stars',
    'Mean Rating < 1.5',
    'Mean Rating > 4.0',
    'Other Users'
]
user_counts = [326160, 42786, 242515, 4169420 - 326160 - 42786 - 242515]

# 颜色设置
bar_colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd']
pie_colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4']

# 创建画布
plt.figure(figsize=(14, 6))

# 柱状图：用户评分分布
plt.subplot(1, 2, 1)
bars = plt.bar(ratings, rating_counts, color=bar_colors)
plt.title('Distribution of User Ratings', fontsize=16, pad=20)
plt.xlabel('Rating', fontsize=14)
plt.ylabel('Number of Ratings', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 添加数据标签
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:,}', 
             ha='center', va='bottom', fontsize=12)

# 饼图：用户评分行为分布
plt.subplot(1, 2, 2)
wedges, texts, autotexts = plt.pie(user_counts, labels=user_categories, colors=pie_colors, 
                                   autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12})
plt.title('Distribution of User Rating Behavior', fontsize=16, pad=20)
plt.axis('equal')  # 确保饼图为圆形

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()