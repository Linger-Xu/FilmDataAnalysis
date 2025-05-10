import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 读取数据并预处理
def load_data(file_path):
    hour_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            # 解析小时段和评分分布
            hour, ratings = line.strip('()').split(',(')
            hour = int(hour)
            ratings = list(map(int, ratings.strip(')').split(',')))
            hour_data[hour] = [hour] + ratings  # 将小时段和评分合并为一个列表
    # 按小时顺序排列
    sorted_hours = sorted(hour_data.keys())
    sorted_data = [hour_data[hour] for hour in sorted_hours]
    return sorted_data

# 计算相关系数矩阵
def calculate_correlation(data):
    # 将数据转换为DataFrame
    df = pd.DataFrame(data, columns=['Hour', '1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars'])
    # 计算相关系数矩阵
    correlation_matrix = df.corr()
    return correlation_matrix

# 可视化相关系数热力图
def visualize_correlation_heatmap(correlation_matrix):
    # 创建热力图
    plt.figure(figsize=(10, 8))
    heatmap = plt.imshow(correlation_matrix, cmap='coolwarm', vmin=-1, vmax=1)

    # 添加颜色条
    cbar = plt.colorbar(heatmap)
    cbar.set_label('Correlation Coefficient', fontsize=12)

    # 设置标题和标签
    plt.title('Correlation Heatmap of Hour and Rating Distributions', fontsize=16, pad=20)
    plt.xlabel('Variables', fontsize=14)
    plt.ylabel('Variables', fontsize=14)

    # 设置横轴和纵轴刻度
    variables = ['Hour', '1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars']
    plt.xticks(np.arange(len(variables)), variables, fontsize=12, rotation=45)
    plt.yticks(np.arange(len(variables)), variables, fontsize=12)

    # 在热力图中显示相关系数值
    for i in range(len(variables)):
        for j in range(len(variables)):
            plt.text(j, i, f'{correlation_matrix.iloc[i, j]:.2f}', ha='center', va='center', color='black', fontsize=10)

    # 调整布局
    plt.tight_layout()

    # 显示图表
    plt.show()

# 主程序
if __name__ == '__main__':
    # 数据文件路径
    file_path = '3.txt'
    
    # 加载数据
    data = load_data(file_path)
    
    # 计算相关系数矩阵
    correlation_matrix = calculate_correlation(data)
    
    # 可视化相关系数热力图
    visualize_correlation_heatmap(correlation_matrix)