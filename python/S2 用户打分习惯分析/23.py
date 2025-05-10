import matplotlib.pyplot as plt
import numpy as np
import ast

# 读取数据
user_ratings = []
with open('1.txt', 'r') as file:
    for line in file:
        # 分割用户ID和评分数据
        user_id, rating_map = line.strip().split(',Map(')
        rating_map = rating_map.rstrip(')')
        # 将 "->" 替换为 ":"
        rating_map = rating_map.replace("->", ":")
        # 解析为字典
        rating_map = ast.literal_eval("{" + rating_map + "}")
        user_ratings.append((user_id, rating_map))

# 计算每个用户的评分均值和标准差
def calculate_mean_std(rating_map):
    ratings = []
    for star, count in rating_map.items():
        ratings.extend([star] * count)
    if not ratings:
        return 0, 0
    return np.mean(ratings), np.std(ratings)

# 计算所有用户的评分均值和标准差
means = []
std_devs = []
for _, rating_map in user_ratings:
    mean, std = calculate_mean_std(rating_map)
    means.append(mean)
    std_devs.append(std)

# 绘制评分均值的分布直方图
plt.figure(figsize=(14, 6))

# 直方图：评分均值分布
plt.subplot(1, 2, 1)
plt.hist(means, bins=30, color='#1f77b4', edgecolor='black', alpha=0.7)
plt.title('Distribution of User Rating Means', fontsize=14, pad=10)
plt.xlabel('Mean Rating', fontsize=12)
plt.ylabel('Number of Users', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 散点图：评分均值与标准差的关系
plt.subplot(1, 2, 2)
plt.scatter(means, std_devs, color='#d62728', alpha=0.5)
plt.title('Mean Rating vs Standard Deviation', fontsize=14, pad=10)
plt.xlabel('Mean Rating', fontsize=12)
plt.ylabel('Standard Deviation', fontsize=12)
plt.grid(linestyle='--', alpha=0.7)

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()