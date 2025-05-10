import matplotlib.pyplot as plt
import numpy as np

def load_genre_ratings(file_path):
    genres = []
    ratings = []
    with open(file_path, 'r', encoding='utf-8') as file:
        next(file)  # 跳过表头
        for line in file:
            parts = line.strip().split('\t')
            genre = parts[0]
            star_counts = list(map(int, parts[1:]))
            genres.append(genre)
            ratings.append(star_counts)
    return genres, ratings

def calculate_mean_ratings(genres, ratings):
    mean_ratings = []
    for genre, counts in zip(genres, ratings):
        total_users = sum(counts)
        mean_rating = (1 * counts[0] + 2 * counts[1] + 3 * counts[2] + 4 * counts[3] + 5 * counts[4]) / total_users if total_users != 0 else 0
        mean_ratings.append(mean_rating)
    return mean_ratings

def save_mean_ratings(genres, ratings, mean_ratings, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        # 写入新表头
        file.write("Genre\t1 Star\t2 Stars\t3 Stars\t4 Stars\t5 Stars\tMean Rating\n")
        # 写入排序后的数据
        for genre, counts, mean_rating in zip(genres, ratings, mean_ratings):
            file.write(f"{genre}\t{counts[0]}\t{counts[1]}\t{counts[2]}\t{counts[3]}\t{counts[4]}\t{mean_rating:.2f}\n")

def plot_mean_ratings(genres, mean_ratings):
    # 创建独立的图表
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(genres)), mean_ratings, color='#1f77b4', alpha=0.8)
    plt.title('Mean Ratings by Genre (Sorted)', fontsize=16)
    plt.ylabel('Mean Rating', fontsize=14)
    plt.xticks(range(len(genres)), [])  # 不显示横轴标签
    plt.ylim(0, 5)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_rating_distribution(genres, ratings):
    colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd']
    labels = ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars']

    # 创建独立的图表
    plt.figure(figsize=(10, 6))
    bottom = np.zeros(len(genres))
    for i in range(5):
        plt.bar(range(len(genres)), 
                [counts[i] for counts in ratings], 
                bottom=bottom, 
                color=colors[i], 
                label=labels[i], 
                alpha=0.8)
        bottom += [counts[i] for counts in ratings]
    plt.title('Rating Distribution by Genre (Sorted)', fontsize=16)
    plt.ylabel('Number of Ratings', fontsize=14)
    plt.xticks(range(len(genres)), [])  # 不显示横轴标签
    plt.legend(title='Rating', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    file_path = 'genre_ratings.txt'
    output_file = 'mean_ratings_by_genre.txt'
    
    genres, ratings = load_genre_ratings(file_path)
    mean_ratings = calculate_mean_ratings(genres, ratings)
    
    # 按均分降序排序所有数据
    sorted_data = sorted(zip(genres, ratings, mean_ratings), 
                        key=lambda x: x[2], 
                        reverse=True)
    genres = [item[0] for item in sorted_data]
    ratings = [item[1] for item in sorted_data]
    mean_ratings = [item[2] for item in sorted_data]
    
    save_mean_ratings(genres, ratings, mean_ratings, output_file)
    print(f"完整数据已保存至 {output_file}")
    
    # 分别绘制两张图
    plot_mean_ratings(genres, mean_ratings)
    plot_rating_distribution(genres, ratings)