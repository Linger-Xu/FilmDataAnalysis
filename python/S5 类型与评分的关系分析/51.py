from collections import defaultdict

# 读取电影数据
def load_movies(file_path):
    movies = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            # 解析电影ID、评分和类型
            movie_id, rating, genres = line.strip('()').split(',')
            movie_id = int(movie_id)
            rating = float(rating)
            genres = [genre.strip() for genre in genres.split('/')]
            movies[movie_id] = (rating, genres)
    return movies

# 读取评价数据
def load_ratings(file_path):
    ratings = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            # 解析电影ID和评分
            movie_id, rating = line.strip('()').split(',')
            movie_id = int(movie_id)
            rating = int(rating)
            ratings.append((movie_id, rating))
    return ratings

# 统计每种类型的评分分布
def count_ratings_by_genre(movies, ratings):
    genre_ratings = defaultdict(lambda: [0, 0, 0, 0, 0])  # 1星到5星的评价数量
    for movie_id, rating in ratings:
        if movie_id in movies:
            _, genres = movies[movie_id]
            for genre in genres:
                genre_ratings[genre][rating - 1] += 1  # 评分从1开始，索引从0开始
    return genre_ratings

# 保存统计结果
def save_results(genre_ratings, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        # 写入表头
        file.write("Genre\t1 Star\t2 Stars\t3 Stars\t4 Stars\t5 Stars\n")
        # 写入每种类型的评分分布
        for genre, counts in genre_ratings.items():
            file.write(f"{genre}\t{counts[0]}\t{counts[1]}\t{counts[2]}\t{counts[3]}\t{counts[4]}\n")

# 主程序
if __name__ == '__main__':
    # 数据文件路径
    movies_file = '6.txt'
    ratings_file = '7.txt'
    output_file = 'genre_ratings.txt'
    
    # 加载数据
    movies = load_movies(movies_file)
    ratings = load_ratings(ratings_file)
    
    # 统计每种类型的评分分布
    genre_ratings = count_ratings_by_genre(movies, ratings)
    
    # 保存统计结果
    save_results(genre_ratings, output_file)
    print(f"Results saved to {output_file}")