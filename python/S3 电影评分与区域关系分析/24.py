import matplotlib.pyplot as plt
import numpy as np

# 读取数据
def load_data(file_path):
    countries = []
    means = []
    stds = []
    composite_scores = []
    with open(file_path, 'r', encoding='utf-8') as file:
        next(file)  # 跳过表头
        for line in file:
            parts = line.strip().split('\t')
            countries.append(parts[0])
            means.append(float(parts[1]))
            stds.append(float(parts[2]))
            composite_scores.append(float(parts[5]))
    return countries, means, stds, composite_scores

# 可视化
def visualize_data(countries, means, stds, composite_scores):
    # 设置颜色
    bar_color = '#1f77b4'
    error_color = '#d62728'

    # 创建柱状图
    plt.figure(figsize=(12, 6))
    x = np.arange(len(countries))
    bars = plt.bar(x, composite_scores, color=bar_color, alpha=0.7, label='Composite Score')
    plt.errorbar(x, composite_scores, yerr=stds, fmt='none', color=error_color, capsize=5, label='Standard Deviation')

    # 添加标题和标签
    plt.title('Composite Scores and Standard Deviations by Country', fontsize=16, pad=20)
    plt.ylabel('Composite Score', fontsize=14)
    plt.xticks(x, [])  # 不显示横轴国家名称
    plt.ylim(0, 25)  # 假设综合评分为0-100
    plt.legend(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 调整布局
    plt.tight_layout()

    # 显示图表
    plt.show()

# 主程序
if __name__ == '__main__':
    # 数据文件路径
    file_path = 'country_stats_composite_updated.txt'
    
    # 加载数据
    countries, means, stds, composite_scores = load_data(file_path)
    
    # 可视化
    visualize_data(countries, means, stds, composite_scores)