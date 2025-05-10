import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# 读取评分均值数据（4.txt）
average_scores = {}
with open('4.txt', 'r') as file:
    for line in file:
        # 去除括号并按逗号分割
        line = line.strip().strip('()')
        year, score = line.split(',')
        year = int(year)  # 处理年份
        score = float(score)  # 处理评分均值
        average_scores[year] = score

# 读取每年各星级评价数量（5.txt）
rating_counts = {}
with open('5.txt', 'r') as file:
    for line in file:
        # 去除括号并按逗号分割
        line = line.strip().strip('()')
        year, ratings = line.split(',', 1)  # 使用split(',', 1)以处理可能的多余逗号
        year = int(year)  # 处理年份
        ratings = tuple(map(int, ratings.strip('()').split(',')))  # 处理每个星级的评价数量
        rating_counts[year] = ratings

# 按年份排序
years = sorted(set(average_scores.keys()).union(rating_counts.keys()))

# 获取每年的评分均值
scores = [average_scores[year] for year in years]

# 获取每年各星级评价的数量
rating_1 = [rating_counts[year][0] for year in years]
rating_2 = [rating_counts[year][1] for year in years]
rating_3 = [rating_counts[year][2] for year in years]
rating_4 = [rating_counts[year][3] for year in years]
rating_5 = [rating_counts[year][4] for year in years]

# 创建一个数据框，包含年份列
data = {
    'Year': years,
    '1 Star': rating_1,
    '2 Stars': rating_2,
    '3 Stars': rating_3,
    '4 Stars': rating_4,
    '5 Stars': rating_5,
    'Average Rating': scores
}

df = pd.DataFrame(data)

# 计算相关系数矩阵
correlation_matrix = df.corr()  # 计算所有列（包括年份和评分）的相关系数

# 创建一个子图，左右排版
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# ---- 左图：折线图 ----

# 绘制左轴（均分）的折线图
ax1.plot(years, scores, marker='o', color='#1f77b4', label='Average Rating', linestyle='-', linewidth=2)
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('Average Rating', fontsize=12, color='black')  # 设置左轴标签颜色为黑色
ax1.tick_params(axis='y', labelcolor='black')  # 设置左轴刻度标签颜色为黑色

# 创建右轴（人数）的折线图
ax2_2 = ax1.twinx()
ax2_2.plot(years, rating_1, marker='o', color='#FF6F61', label='1 Star Count', linestyle='--')
ax2_2.plot(years, rating_2, marker='o', color='#FF9F80', label='2 Stars Count', linestyle='--')
ax2_2.plot(years, rating_3, marker='o', color='#FFD700', label='3 Stars Count', linestyle='--')
ax2_2.plot(years, rating_4, marker='o', color='#A8E6CF', label='4 Stars Count', linestyle='--')
ax2_2.plot(years, rating_5, marker='o', color='#76D7C4', label='5 Stars Count', linestyle='--')
ax2_2.plot(years, [sum(r) for r in zip(rating_1, rating_2, rating_3, rating_4, rating_5)], 
            marker='x', color='#ff7f0e', label='Total Users', linestyle='-', linewidth=2)

# 设置标题
ax1.set_title('Average Rating and Rating Counts per Year', fontsize=16, fontweight='bold')

# 添加图例
ax1.legend(loc='upper left', fontsize=10)
ax2_2.legend(loc='upper right', fontsize=10)

# 美化图形
plt.xticks(years, fontsize=10)

# ---- 右图：相关系数热力图 ----

# 绘制热力图
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax2, cbar=True)

# 设置热力图标题
ax2.set_title('Correlation Heatmap of Rating Counts and Average Rating', fontsize=16)

# 调整右图的轴标签字体大小或角度
ax2.tick_params(axis='both', labelsize=10)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')  # 设置x轴标签倾斜
ax2.set_yticklabels(ax2.get_yticklabels(), rotation=45, ha='right')  # 设置y轴标签倾斜

# 调整子图之间的间距
fig.subplots_adjust(wspace=0.3)  # 增加左右子图之间的间距

# 显示图形
plt.tight_layout()
plt.show()
