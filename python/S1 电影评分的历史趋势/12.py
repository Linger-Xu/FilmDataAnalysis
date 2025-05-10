import matplotlib.pyplot as plt
import numpy as np

# 读取数据
data = []
with open('12.txt', 'r') as file:
    for line in file:
        year, counts = eval(line)
        data.append((year, counts))

# 提取年份和各分数段数量
years = [item[0] for item in data]
scores_0_2 = [item[1][0] for item in data]
scores_2_4 = [item[1][1] for item in data]
scores_4_6 = [item[1][2] for item in data]
scores_6_8 = [item[1][3] for item in data]
scores_8_10 = [item[1][4] for item in data]

# 设置颜色
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# 创建堆叠柱状图
plt.figure(figsize=(12, 6))
plt.bar(years, scores_0_2, color=colors[0], label='0-2')
plt.bar(years, scores_2_4, bottom=scores_0_2, color=colors[1], label='2-4')
plt.bar(years, scores_4_6, bottom=np.array(scores_0_2)+np.array(scores_2_4), color=colors[2], label='4-6')
plt.bar(years, scores_6_8, bottom=np.array(scores_0_2)+np.array(scores_2_4)+np.array(scores_4_6), color=colors[3], label='6-8')
plt.bar(years, scores_8_10, bottom=np.array(scores_0_2)+np.array(scores_2_4)+np.array(scores_4_6)+np.array(scores_6_8), color=colors[4], label='8-10')

# 添加标题和标签
plt.title('Movie Score Distribution by Year', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Number of Movies', fontsize=14)
plt.legend(title='Score Range', bbox_to_anchor=(1.05, 1), loc='upper left')

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()