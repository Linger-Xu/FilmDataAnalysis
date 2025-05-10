import matplotlib.pyplot as plt
import numpy as np

# 读取数据
data = []
with open('3.txt', 'r') as file:
    for line in file:
        line = line.strip()  # 去除首尾空白字符
        if ',' in line:
            # 分割时根据第一个逗号进行切割，以防万一有多余的逗号
            time, ratings = line.split(',', 1)
            time = int(time.strip('()'))  # 处理时间
            ratings = tuple(map(int, ratings.strip('()').split(',')))  # 处理评价数据
            data.append((time, ratings))

# 提取时间和对应的评级数据
times = [item[0] for item in data]
ratings_data = np.array([item[1] for item in data])

# 每个评级的用户数量
rating_1 = ratings_data[:, 0]
rating_2 = ratings_data[:, 1]
rating_3 = ratings_data[:, 2]
rating_4 = ratings_data[:, 3]
rating_5 = ratings_data[:, 4]

# 计算每个小时的总用户数
total_users = rating_1 + rating_2 + rating_3 + rating_4 + rating_5

# 计算每个星级的占比
percentage_1 = rating_1 / total_users
percentage_2 = rating_2 / total_users
percentage_3 = rating_3 / total_users
percentage_4 = rating_4 / total_users
percentage_5 = rating_5 / total_users

# 绘制堆叠柱状图
fig, ax = plt.subplots(figsize=(10, 6))

# 使用比例数据绘制堆叠柱状图
ax.bar(times, percentage_1, label='1 Star', color='#d62728')
ax.bar(times, percentage_2, bottom=percentage_1, label='2 Stars', color='#ff7f0e')
ax.bar(times, percentage_3, bottom=percentage_1 + percentage_2, label='3 Stars', color='#2ca02c')
ax.bar(times, percentage_4, bottom=percentage_1 + percentage_2 + percentage_3, label='4 Stars', color='#1f77b4')
ax.bar(times, percentage_5, bottom=percentage_1 + percentage_2 + percentage_3 + percentage_4, label='5 Stars', color='#9467bd')

# 设置标题和标签
ax.set_title('User Ratings Proportion by Hour', fontsize=16, fontweight='bold')
ax.set_xlabel('Time of Day (Hour)', fontsize=12)
ax.set_ylabel('Proportion of Users', fontsize=12)

# 添加图例
ax.legend(title='Rating', fontsize=10, title_fontsize=12)

# 美化图形
plt.xticks(times, fontsize=10)
plt.yticks(np.arange(0, 1.1, 0.1), fontsize=10)  # y轴刻度显示比例
plt.tight_layout()

# 显示图形
plt.show()
