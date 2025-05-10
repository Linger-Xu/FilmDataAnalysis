import matplotlib.pyplot as plt
import numpy as np

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
            hour_data[hour] = ratings
    # 按小时顺序排列
    sorted_hours = sorted(hour_data.keys())
    sorted_ratings = [hour_data[hour] for hour in sorted_hours]
    return sorted_hours, sorted_ratings

# 可视化柱状堆叠图
def visualize_stacked_bar(hours, ratings):
    # 将数据转换为二维数组
    ratings = np.array(ratings).T  # 转置，使得每行对应一个评分

    # 设置颜色
    colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd']
    labels = ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars']

    # 创建柱状堆叠图
    plt.figure(figsize=(14, 8))
    bottom = np.zeros(len(hours))  # 用于堆叠的初始值
    for i in range(5):
        plt.bar(hours, ratings[i], bottom=bottom, color=colors[i], label=labels[i], alpha=0.8)
        bottom += ratings[i]  # 更新堆叠的初始值

    # 添加标题和标签
    plt.title('Hourly Distribution of User Ratings (Stacked Bar Chart)', fontsize=16, pad=20)
    plt.xlabel('Hour of Day', fontsize=14)
    plt.ylabel('Number of Users', fontsize=14)

    # 设置横轴和纵轴刻度
    plt.xticks(hours, fontsize=12)
    plt.yticks(fontsize=12)

    # 添加图注
    plt.legend(title='Rating', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)

    # 调整布局
    plt.tight_layout()

    # 显示图表
    plt.show()

# 主程序
if __name__ == '__main__':
    # 数据文件路径
    file_path = '3.txt'
    
    # 加载数据
    hours, ratings = load_data(file_path)
    
    # 可视化柱状堆叠图
    visualize_stacked_bar(hours, ratings)