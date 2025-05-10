import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 示例数据
countries = ['中国大陆', '美国', '日本', '英国']
means = [7.5, 8.2, 6.8, 7.9]
stds = [0.8, 0.5, 1.2, 0.7]

# 创建柱状图
plt.figure(figsize=(10, 6))
x = np.arange(len(countries))
plt.bar(x, means, yerr=stds, color='#1f77b4', alpha=0.7, capsize=5, label='均分 ± 标准差')
plt.title('各国电影均分及标准差', fontsize=16, pad=20)
plt.xlabel('国家', fontsize=14)
plt.ylabel('均分', fontsize=14)
plt.xticks(x, countries, rotation=45, ha='right', fontsize=12)
plt.ylim(0, 10)  # 评分范围一般为0-10
plt.legend(fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()