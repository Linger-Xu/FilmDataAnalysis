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

# 计算每个用户的评分标准差
def calculate_std(rating_map):
    ratings = []
    for star, count in rating_map.items():
        ratings.extend([star] * count)
    if not ratings:
        return 0
    return np.std(ratings)

std_devs = [calculate_std(rating_map) for _, rating_map in user_ratings]

# 创建直方图
plt.figure(figsize=(10, 6))
plt.hist(std_devs, bins=30, color='#1f77b4', edgecolor='black', alpha=0.7)

# 添加标题和标签
plt.title('Distribution of User Rating Standard Deviations', fontsize=16, pad=20)
plt.xlabel('Standard Deviation of Ratings', fontsize=14)
plt.ylabel('Number of Users', fontsize=14)

# 添加网格
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()