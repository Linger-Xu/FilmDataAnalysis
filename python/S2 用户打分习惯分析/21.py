import matplotlib.pyplot as plt

# 数据
ratings = ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars']
counts = [318322, 529544, 1404020, 1276241, 641293]

# 颜色设置（使用渐变色）
colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd']

# 创建柱状图
plt.figure(figsize=(10, 6))
bars = plt.bar(ratings, counts, color=colors)

# 添加数据标签
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:,}', 
             ha='center', va='bottom', fontsize=12)

# 添加标题和标签
plt.title('Distribution of User Ratings', fontsize=16, pad=20)
plt.xlabel('Rating', fontsize=14)
plt.ylabel('Number of Ratings', fontsize=14)

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()