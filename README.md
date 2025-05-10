
# 🎬 FilmDataAnalysis

基于 Hadoop 与 Spark 的电影大数据分析项目，探索电影历史趋势、观众评分行为和多维影响因素，服务于学术研究、内容制作与市场策略制定。

---

## 📁 项目结构

```
FilmDataAnalysis/
├── FilmDataAnalysis/     # Scala 实现的各阶段数据处理与分析文件
├── python/               # Python 可视化模块及结果图（含分类子文件夹）
│   ├── S1~S8/            # 不同主题的可视化脚本（如 S1 历史趋势）
│   └── Fxx.png           # 可视化结果图像
```

---

## 🚀 技术栈

- Hadoop HDFS, Apache Spark, Scala
- pandas, numpy, matplotlib, seaborn
- 项目使用 IntelliJ IDEA + Maven + Python 环境部署

---

## ▶️ 快速开始

1. 上传数据至 HDFS：

```bash
hdfs dfs -mkdir /filmdata
hdfs dfs -put movies.csv /filmdata/
hdfs dfs -put ratings.csv /filmdata/
```

2. 编译并运行 Scala 分析脚本：

```bash
spark-submit --class S11_dataProcess target/FilmDataAnalysis.jar
```

3. 进入 python 目录运行可视化脚本：

```bash
cd python/S1_电影评分的历史趋势
python s1_plot.py
```

---

## 📈 数据分析亮点（含部分结论与可视化展示）

### 📌 S1. 电影评分历史趋势

- **分析目标**：按年份分析均分与分布变化。
- **结论**：评分整体波动下降，评分两极化趋势明显。

**插图位置 1（年度均分图）：**
![示例图1](./python/F11.png)

---

### 📌 S2. 评分时间分布分析

- **分析目标**：研究评分的时间维度（年、季节、小时）影响。
- **结论**：夏季及晚间评分偏高，深夜低评分集中。

**插图位置 2（时间段评分分布）：**
![示例图2](./python/F27.png)

---

### 📌 S3. 不同地区评分表现

- **分析目标**：分析国家与评分关系，构建“电影质量”指标。
- **结论**：苏联、捷克等地评分质量高；印度波动大。

**插图位置 3（国家评分柱状图）：**
![示例图3](./python/F32.png)

---

## 🧠 更多分析维度

- S4. 类型与评分关系（剧情、武侠、灾难等）
- S5. 时长与评分关系（采用对数坐标）
- S6. 导演影响力（均分与执导数量）
- S7. 用户打分习惯（评分标准差与偏好）
- S8. 冷门佳作分析（冷门指数）

可前往 `python/` 各子目录查看完整图表与脚本。

---

## 📜 致谢

本项目由吉林大学《企业实训-大数据》课程支持，特别感谢指导教师王大瑞与邹淑雪的悉心指导。

---

> 如需插入更多图像，请将图片文件放入 `python/` 目录并在上述“插图位置”添加 Markdown 图片链接：  
> `![图片说明](./python/你的图片名.png)`
