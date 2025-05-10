import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def load_data(file_path):
    """
    加载数据文件，返回时长列表和对应的均分列表
    """
    durations = []
    ratings = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 解析数据，例如：(138,(7.246153846153846,52))
            line = line.strip()
            if not line:
                continue
            duration_part, rating_part = line.split('(')[1], line.split('(')[2]
            duration = int(duration_part.split(',')[0])
            rating = float(rating_part.split(',')[0])
            durations.append(duration)
            ratings.append(rating)
    return durations, ratings

def poly_func(x, *coefficients):
    """
    多项式函数
    """
    return np.polyval(coefficients, x)

def plot_movie_duration_vs_rating(durations, ratings):
    """
    绘制电影时长与评分的散点图，并分段拟合（确保在 1.5h 处连续）
    """
    # 将数据转换为 NumPy 数组
    durations = np.array(durations)
    ratings = np.array(ratings)

    # 分段拟合
    # 第一段：0-1.5 小时（0-90 分钟）
    mask1 = durations <= 90
    durations1 = durations[mask1]
    ratings1 = ratings[mask1]

    # 第二段：1.5-8 小时（90-480 分钟）
    mask2 = (durations > 90) & (durations <= 480)
    durations2 = durations[mask2]
    ratings2 = ratings[mask2]

    # 对每一段数据按照时长升序排序
    durations1_sorted = np.sort(durations1)
    ratings1_sorted = ratings1[np.argsort(durations1)]
    durations2_sorted = np.sort(durations2)
    ratings2_sorted = ratings2[np.argsort(durations2)]

    # 创建画布
    plt.figure(figsize=(12, 6))

    # 绘制散点图
    plt.scatter(durations1_sorted, ratings1_sorted, color='#1f77b4', alpha=0.6, edgecolor='black', s=50, label='Movie Data (0-1.5h)')
    plt.scatter(durations2_sorted, ratings2_sorted, color='#2ca02c', alpha=0.6, edgecolor='black', s=50, label='Movie Data (1.5-8h)')

    # 对第一段数据进行多项式拟合
    coefficients1, _ = curve_fit(poly_func, durations1_sorted, ratings1_sorted, p0=[1, 1, 1, 1])  # 3 次多项式拟合
    poly1 = np.poly1d(coefficients1)  # 创建多项式函数
    x_fit1 = np.linspace(min(durations1_sorted), 90, 500)  # 生成拟合曲线的 x 值
    y_fit1 = poly1(x_fit1)  # 计算拟合曲线的 y 值

    # 对第二段数据进行多项式拟合，并添加约束条件
    def constrained_poly_func(x, *coefficients):
        """
        约束多项式函数：在 x=90 处的值等于第一段拟合曲线的值
        """
        return np.polyval(coefficients, x)

    # 初始猜测值
    p0 = [1, 1, 1, 1]

    # 约束条件：在 x=90 处的值等于第一段拟合曲线的值
    def constraint(coefficients):
        return poly1(90) - constrained_poly_func(90, *coefficients)

    # 使用 curve_fit 进行拟合
    coefficients2, _ = curve_fit(constrained_poly_func, durations2_sorted, ratings2_sorted, p0=p0, bounds=(-np.inf, np.inf))
    poly2 = np.poly1d(coefficients2)  # 创建多项式函数
    x_fit2 = np.linspace(90, 480, 500)  # 生成拟合曲线的 x 值
    y_fit2 = poly2(x_fit2)  # 计算拟合曲线的 y 值

    # 绘制拟合曲线
    plt.plot(x_fit1, y_fit1, color='#ff7f0e', linewidth=2, label='Polynomial Fit (0-1.5h)')
    plt.plot(x_fit2, y_fit2, color='#d62728', linewidth=2, label='Polynomial Fit (1.5-8h)')

    # 设置横轴为对数刻度
    plt.xscale('log')
    plt.xlim(1, 14400)  # 设置横轴范围为 1 到 14400 分钟

    # 设置横轴刻度
    plt.xticks([1, 10, 60, 90, 120, 240, 480, 1440, 14400], 
               ['1m', '10m', '1h', '1.5h', '2h', '4h', '8h', '24h', '14400m'], fontsize=12)

    # 设置纵轴范围
    plt.ylim(0, 10)  # 评分范围为 0 到 10
    plt.yticks(np.arange(4, 11, 1), fontsize=12)

    # 添加标题和标注
    plt.title('Relationship Between Movie Duration and Audience Rating (Log Scale)', fontsize=16, pad=20)
    plt.xlabel('Movie Duration (Log Scale)', fontsize=14)
    plt.ylabel('Average Rating', fontsize=14)

    # 设置网格线
    plt.grid(True, linestyle='--', alpha=0.6)

    # 设置图注
    plt.legend(loc='upper right', fontsize=12)

    # 调整布局
    plt.tight_layout()

    # 显示图表
    plt.show()

def main():
    # 数据文件路径
    file_path = '8.txt'

    # 加载数据
    durations, ratings = load_data(file_path)

    # 可视化数据
    plot_movie_duration_vs_rating(durations, ratings)

if __name__ == '__main__':
    main()