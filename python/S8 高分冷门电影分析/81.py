import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 读取数据
def load_data(file_path):
    movies = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            # 解析数据，例如：(行骗天下 剧场版,8.5,1941)
            name, rating, count = line.strip('()').split(',')
            movies.append({
                'name': name.strip(),
                'rating': float(rating),
                'count': int(count)
            })
    return pd.DataFrame(movies)

# 计算冷门指数
def calculate_cold_index(df, count_threshold=1000):
    max_rating = df['rating'].max()
    max_count = df['count'].max()
    # 归一化均分和评分人数
    df['rating_norm'] = df['rating'] / max_rating
    df['count_norm'] = 1 - np.log(df['count']) / np.log(max_count)
    # 评分人数惩罚因子（低于阈值的电影冷门指数降低）
    df['count_penalty'] = np.where(df['count'] < count_threshold, 
                                   df['count'] / count_threshold, 1)
    # 冷门指数公式
    df['cold_index'] = df['rating_norm'] * df['count_norm'] * df['count_penalty'] * 100
    return df

# 保存结果
def save_results(df, output_file):
    df_sorted = df.sort_values(by='cold_index', ascending=False)
    df_sorted.to_csv(output_file, sep='\t', index=False, 
                     columns=['name', 'rating', 'count', 'cold_index'],
                     header=['Movie', 'Mean Rating', 'Rating Count', 'Cold Index'])

# 可视化
def visualize_data(df):
    plt.figure(figsize=(12, 8))
    # 绘制散点图
    scatter = plt.scatter(df['count'], df['rating'], 
                          c=df['cold_index'], cmap='viridis', alpha=0.6,
                          s=50, edgecolor='black')
    plt.colorbar(label='Cold Index')
    plt.title('High Rating vs. Low Popularity Movies', fontsize=16)
    plt.xlabel('Rating Count (Log Scale)', fontsize=12)
    plt.ylabel('Mean Rating', fontsize=12)
    plt.xscale('log')  # 横轴取对数
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# 主程序
if __name__ == '__main__':
    # 数据文件路径
    file_path = '10.txt'
    output_file = 'movie_cold_index.tsv'
    
    # 加载数据
    df = load_data(file_path)
    
    # 计算冷门指数
    df = calculate_cold_index(df, count_threshold=1000)
    
    # 保存结果
    save_results(df, output_file)
    print(f"Results saved to {output_file}")
    
    # 可视化
    visualize_data(df)