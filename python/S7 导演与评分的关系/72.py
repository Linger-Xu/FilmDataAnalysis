import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import defaultdict

def load_data(file_path):
    """
    加载数据文件，返回导演及其作品评分的字典
    """
    director_ratings = defaultdict(list)
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 解析数据，例如：(4.7,阿卡季·萨赫拉什维利/夏昊)
            line = line.strip()
            if not line:
                continue
            rating_part, directors_part = line.strip('()').split(',')
            rating = float(rating_part)
            directors = directors_part.split('/')
            for director in directors:
                director_ratings[director].append(rating)
    return director_ratings

def save_director_statistics(statistics, output_file):
    """
    按照均分降序将所有导演的名字、均分和电影数量保存到文件
    """
    # 将数据转换为 DataFrame
    df = pd.DataFrame(statistics).T.reset_index()
    df.columns = ['Director', 'Mean Rating', 'Std Rating', 'Movie Count']
    df = df.sort_values(by='Mean Rating', ascending=False)  # 按均分降序排序

    # 保存到文件
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("Director\t\tMean Rating\tMovie Count\n")
        file.write("--------------------------------------------\n")
        for _, row in df.iterrows():
            file.write(f"{row['Director']}\t\t{row['Mean Rating']:.2f}\t\t{row['Movie Count']}\n")

def plot_director_scatter(statistics):
    """
    绘制导演均分和电影数量的散点图
    """
    # 将数据转换为 DataFrame
    df = pd.DataFrame(statistics).T.reset_index()
    df.columns = ['Director', 'Mean Rating', 'Std Rating', 'Movie Count']

    # 创建画布
    plt.figure(figsize=(12, 8))

    # 设置背景颜色
    plt.gca().set_facecolor('#f7f7f7')
    plt.grid(True, linestyle='--', alpha=0.6, color='white')

    # 绘制散点图
    scatter = plt.scatter(df['Movie Count'], df['Mean Rating'], c=df['Mean Rating'], cmap='viridis', alpha=0.8, s=100, edgecolor='black')

    # 添加颜色条
    cbar = plt.colorbar(scatter)
    cbar.set_label('Mean Rating', fontsize=12)

    # 设置标题和标注
    plt.title('Mean Ratings vs. Movie Count by Director', fontsize=18, pad=20, fontweight='bold')
    plt.xlabel('Movie Count', fontsize=14, labelpad=10)
    plt.ylabel('Mean Rating', fontsize=14, labelpad=10)

    # 设置纵轴范围
    plt.ylim(0, 10)  # 评分范围为 0 到 10

    # 添加副标题
    plt.text(0.5, -0.1, 'Each point represents a director, colored by mean rating', transform=plt.gca().transAxes,
             fontsize=12, ha='center', color='gray')

    # 调整布局
    plt.tight_layout()

    # 显示图表
    plt.show()

def main():
    # 数据文件路径
    file_path = '9.txt'
    output_file = 'director_statistics.txt'

    # 加载数据
    director_ratings = load_data(file_path)

    # 计算统计量
    statistics = {director: (np.mean(ratings), np.std(ratings), len(ratings))
                  for director, ratings in director_ratings.items()}

    # 保存导演统计信息到文件
    save_director_statistics(statistics, output_file)
    print(f"Director statistics saved to {output_file}")

    # 可视化数据
    plot_director_scatter(statistics)

if __name__ == '__main__':
    main()