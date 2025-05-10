package FilmDataAnalysis

import org.apache.spark.{SparkConf, SparkContext}

object S12_dataAnalysis {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local").setAppName("S12_dataAnalysis")
    val sc = new SparkContext(conf)

    val filePath = "src/main/scala/FilmDataAnalysis/s1/data/part-00000"
    val rawData = sc.textFile(filePath)

    val data = rawData.map(line => {
      val parts = line.stripPrefix("(").stripSuffix(")").split(",") // 去掉括号，并按逗号分割
      val score = parts(0).toDouble
      val year = parts(1).toInt
      (score, year)
    })

    //统计每一年所有电影的平均评分
    val yearlyAvgScore = data
      .map { case (score, year) => (year, score) } // 按年份分组评分
      .groupByKey()
      .mapValues(scores => scores.sum / scores.size) // 计算每年平均评分
      .sortByKey()

    //存储每年平均评分的结果
    val avgOutputPath = "src/main/scala/FilmDataAnalysis/s1/average_scores"
    yearlyAvgScore.saveAsTextFile(avgOutputPath)

    //统计每一年电影评分的区间分布
    val scoreRanges = data
      .map { case (score, year) =>
        val scoreRange = score match {
          case s if s >= 0 && s < 2 => (1, 0, 0, 0, 0)
          case s if s >= 2 && s < 4 => (0, 1, 0, 0, 0)
          case s if s >= 4 && s < 6 => (0, 0, 1, 0, 0)
          case s if s >= 6 && s < 8 => (0, 0, 0, 1, 0)
          case s if s >= 8 && s <= 10 => (0, 0, 0, 0, 1)
        }
        (year, scoreRange)
      }
      .groupByKey()
      .mapValues { ranges =>
        val initial = (0, 0, 0, 0, 0)
        ranges.foldLeft(initial) {
          case ((a, b, c, d, e), (r1, r2, r3, r4, r5)) =>
            (a + r1, b + r2, c + r3, d + r4, e + r5)
        }
      }
      .sortByKey()

    //存储评分区间统计的结果
    val rangeOutputPath = "src/main/scala/FilmDataAnalysis/s1/score_ranges"
    scoreRanges.saveAsTextFile(rangeOutputPath)
  }
}
