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

def plot_grouped_boxplot(director_ratings):
    """
    绘制分组箱线图：按评分均分分组，展示每组导演的评分分布
    """
    # 计算每位导演的均分
    statistics = {director: (np.mean(ratings), np.std(ratings), len(ratings))
                  for director, ratings in director_ratings.items()}

    # 将导演按均分分组
    bins = [0, 2, 4, 6, 8, 10]  # 分组区间
    labels = ['0-2', '2-4', '4-6', '6-8', '8-10']  # 分组标签
    grouped_data = {label: [] for label in labels}

    for director, (mean_rating, _, _) in statistics.items():
        for i, bin_edge in enumerate(bins[:-1]):
            if bin_edge <= mean_rating < bins[i + 1]:
                grouped_data[labels[i]].extend(director_ratings[director])
                break

    # 创建画布
    plt.figure(figsize=(12, 8))

    # 设置背景颜色
    plt.gca().set_facecolor('#f7f7f7')
    plt.grid(axis='y', linestyle='--', alpha=0.6, color='white')

    # 定义颜色
    box_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    # 绘制分组箱线图
    boxes = plt.boxplot([grouped_data[label] for label in labels], labels=labels, showmeans=True, patch_artist=True,
                        boxprops={'facecolor': None, 'edgecolor': 'black', 'linewidth': 1.5},
                        medianprops={'color': 'red', 'linewidth': 2},
                        meanprops={'marker': 'D', 'markerfacecolor': 'yellow', 'markersize': 8},
                        whiskerprops={'color': 'black', 'linewidth': 1.5},
                        capprops={'color': 'black', 'linewidth': 1.5},
                        flierprops={'marker': 'o', 'markerfacecolor': 'black', 'markersize': 5, 'alpha': 0.5})

    # 为每个箱子填充颜色
    for box, color in zip(boxes['boxes'], box_colors):
        box.set_facecolor(color)

    # 设置标题和标注
    plt.title('Distribution of Ratings by Mean Rating Group', fontsize=18, pad=20, fontweight='bold')
    plt.xlabel('Mean Rating Group', fontsize=14, labelpad=10)
    plt.ylabel('Rating', fontsize=14, labelpad=10)

    # 设置纵轴范围
    plt.ylim(0, 10)  # 评分范围为 0 到 10

    # 添加副标题
    plt.text(0.5, -0.15, 'Grouped by the mean rating of each director', transform=plt.gca().transAxes,
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
    plot_grouped_boxplot(director_ratings)

if __name__ == '__main__':
    main()