import matplotlib.pyplot as plt

# 1. 读取 .file 文件（记事本）
file_path = '11.txt'  # 请替换为实际文件路径

# 初始化年份和均分列表
years = []
avg_scores = []

# 读取文件并处理每一行
with open(file_path, 'r') as f:
    for line in f:
        # 去除多余的空格并去掉括号
        line = line.strip().strip('()')  # 去除括号
        if line:  # 确保不处理空行
            # 分割年份和评分
            year, avg_score = line.split(',')
            
            try:
                # 转换为数字类型
                year = int(year)
                avg_score = float(avg_score)
                
                # 将年份和均分添加到列表中
                years.append(year)
                avg_scores.append(avg_score)
            except ValueError:
                continue  # 如果转换失败，则跳过该行

# 2. 数据排序（确保年份升序）
sorted_years, sorted_avg_scores = zip(*sorted(zip(years, avg_scores)))

# 3. 绘制折线图
plt.figure(figsize=(10, 6))

# 绘制折线图
plt.plot(sorted_years, sorted_avg_scores, marker='o', linestyle='-', color='b', label='Avg_Rating')

# 4. 添加标题和标签
plt.title('The Relationship between Year and Avg_Rating', fontsize=16, fontweight='bold')
plt.xlabel('Year', fontsize=14)
plt.ylabel('Avg_Rating', fontsize=14)

# 5. 设置网格、字体以及显示图例
plt.grid(True)
plt.xticks(rotation=45)  # 旋转横坐标，使年份更清晰
plt.legend(loc='upper right')

# 6. 调整图形布局以避免重叠
plt.tight_layout()

# 7. 显示图形
plt.show()
