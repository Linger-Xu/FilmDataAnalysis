import numpy as np
from collections import defaultdict
import math

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

# 统计每个国家的均分、标准差、电影数量和高分电影比例
def calculate_statistics(data):
    country_ratings = defaultdict(list)
    for rating, region in data:
        country_ratings[region].append(rating)
    
    country_stats = {}
    for country, ratings in country_ratings.items():
        mean = np.mean(ratings)
        std = np.std(ratings)
        count = len(ratings)
        high_score_ratio = sum(1 for r in ratings if r >= 8.0) / count if count > 0 else 0
        country_stats[country] = (mean, std, count, high_score_ratio)
    return country_stats

# 计算综合评分（修改后的方案）
def calculate_composite_score(country_stats, min_movies_threshold=10):
    composite_scores = {}
    for country, stats in country_stats.items():
        mean, std, count, high_score_ratio = stats
        # 使用对数函数减少电影数量的影响
        count_score = math.log(count + 1)  # +1 避免对数为负
        # 标准差转化为正向指标
        std_score = 10 - std if std <= 10 else 0
        # 高分电影比例得分（仅当电影数量超过阈值时计入）
        high_score_ratio_score = 0.2 * high_score_ratio * 100 if count >= min_movies_threshold else 0
        # 综合评分公式
        composite_score = (
            0.5 * mean +  # 均分
            0.3 * count_score +  # 电影数量
            0.2 * std_score +  # 标准差
            high_score_ratio_score  # 高分电影比例得分
        )
        composite_scores[country] = composite_score
    return composite_scores

# 将统计结果保存到txt文件（按综合评分降序）
def save_statistics_to_txt(country_stats, composite_scores, output_file):
    # 按综合评分降序排序
    sorted_countries = sorted(composite_scores.items(), key=lambda x: x[1], reverse=True)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        # 写入表头
        file.write("Country\tMean Rating\tStandard Deviation\tNumber of Movies\tHigh Score Ratio\tComposite Score\n")
        # 写入每个国家的数据
        for country, composite_score in sorted_countries:
            mean, std, count, high_score_ratio = country_stats[country]
            file.write(f"{country}\t{mean:.2f}\t{std:.2f}\t{count}\t{high_score_ratio:.2%}\t{composite_score:.2f}\n")

# 主程序
if __name__ == '__main__':
    # 数据文件路径
    file_path = '2.txt'
    # 输出文件路径
    output_file = 'country_stats_composite_updated.txt'
    
    # 数据预处理
    data = preprocess_data(file_path)
    
    # 统计每个国家的均分、标准差、电影数量和高分电影比例
    country_stats = calculate_statistics(data)
    
    # 计算综合评分（修改后的方案）
    composite_scores = calculate_composite_score(country_stats, min_movies_threshold=10)
    
    # 将统计结果保存到txt文件（按综合评分降序）
    save_statistics_to_txt(country_stats, composite_scores, output_file)
    print(f"Statistics saved to {output_file}")