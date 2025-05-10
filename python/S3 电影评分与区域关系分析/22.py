import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# 读取数据并预处理
def preprocess_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            # 解析评分和地区
            rating, regions = line.strip('()').split(',')
            rating = float(rating)
            regions = [r.strip() for r in regions.split('/')]
            # 将多地区数据拆分为多条
            for region in regions:
                data.append((rating, region))
    return data

# 统计每个国家的均分、标准差和电影数量
def calculate_statistics(data):
    country_ratings = defaultdict(list)
    for rating, region in data:
        country_ratings[region].append(rating)
    
    country_stats = {}
    for country, ratings in country_ratings.items():
        mean = np.mean(ratings)
        std = np.std(ratings)
        count = len(ratings)
        country_stats[country] = (mean, std, count)
    return country_stats

# 将统计结果保存到txt文件（按均分降序）
def save_statistics_to_txt(country_stats, output_file):
    # 按均分降序排序
    sorted_countries = sorted(country_stats.items(), key=lambda x: x[1][0], reverse=True)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        # 写入表头
        file.write("Country\tMean Rating\tStandard Deviation\tNumber of Movies\n")
        # 写入每个国家的数据
        for country, stats in sorted_countries:
            mean, std, count = stats
            file.write(f"{country}\t{mean:.2f}\t{std:.2f}\t{count}\n")

# 第一张图：绘制柱状图（不显示国家名称）
def visualize_statistics(country_stats):
    # 按均分降序排序
    sorted_countries = sorted(country_stats.items(), key=lambda x: x[1][0], reverse=True)
    countries = [item[0] for item in sorted_countries]
    means = [item[1][0] for item in sorted_countries]
    stds = [item[1][1] for item in sorted_countries]

    # 创建柱状图
    plt.figure(figsize=(12, 6))
    x = np.arange(len(countries))
    plt.bar(x, means, yerr=stds, color='#1f77b4', alpha=0.7, capsize=5, label='Mean Rating ± Std Dev')
    plt.title('Movie Ratings by Country (Mean ± Standard Deviation)', fontsize=16, pad=20)
    plt.xlabel('Country', fontsize=14)
    plt.ylabel('Rating', fontsize=14)
    plt.xticks(x, [])  # 不显示横轴国家名称
    plt.ylim(0, 10)  # 评分范围一般为0-10
    plt.legend(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 调整布局
    plt.tight_layout()

    # 显示图表
    plt.show()

# 第二张图：绘制均分前十的国家的均分、电影数量和标准差
def visualize_top_countries(country_stats):
    # 按均分降序排序
    sorted_countries = sorted(country_stats.items(), key=lambda x: x[1][0], reverse=True)
    top_countries = sorted_countries[:10]  # 取均分前十的国家

    # 提取数据
    countries = [item[0] for item in top_countries]
    means = [item[1][0] for item in top_countries]
    stds = [item[1][1] for item in top_countries]
    counts = [item[1][2] for item in top_countries]

    # 创建表格图
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')  # 隐藏坐标轴
    table_data = [
        ['Country', 'Mean Rating', 'Standard Deviation', 'Number of Movies']
    ]
    for i in range(len(countries)):
        table_data.append([
            countries[i], f'{means[i]:.2f}', f'{stds[i]:.2f}', counts[i]
        ])
    
    # 绘制表格
    table = ax.table(cellText=table_data, loc='center', cellLoc='center', colLabels=None)
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)

    # 设置标题
    plt.title('Top 10 Countries by Mean Rating', fontsize=16, pad=20)

    # 调整布局
    plt.tight_layout()

    # 显示图表
    plt.show()

# 主程序
if __name__ == '__main__':
    # 数据文件路径
    file_path = '2.txt'
    # 输出文件路径
    output_file = 'country_stats.txt'
    
    # 数据预处理
    data = preprocess_data(file_path)
    
    # 统计每个国家的均分、标准差和电影数量
    country_stats = calculate_statistics(data)
    
    # 将统计结果保存到txt文件（按均分降序）
    save_statistics_to_txt(country_stats, output_file)
    print(f"Statistics saved to {output_file}")
    
    # 第一张图：绘制柱状图（不显示国家名称）
    visualize_statistics(country_stats)
    
    # 第二张图：绘制均分前十的国家的均分、电影数量和标准差
    visualize_top_countries(country_stats)