package FilmDataAnalysis

import org.apache.spark.{SparkConf, SparkContext}

object S61_dataProcess {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local").setAppName("S61_dataProcess")
    val sc = new SparkContext(conf)

    // 读取movies数据
    val moviesPath = "hdfs://master:9000/movie/input/movies"
    val rawMoviesData = sc.textFile(moviesPath)

    // 处理数据：按逗号分割，再去掉双引号，提取豆瓣评分（第7列）和电影时长（第12列）
    val result = rawMoviesData.map { line =>
      val cols = line.split(",")  // 按逗号分割
      // 去掉双引号并提取需要的列
      if (cols.length >= 12) {  // 确保数据列数足够
        val rating = try {
          cols(6).replace("\"", "").trim.toDouble  // 第7列：豆瓣评分
        } catch {
          case _: Exception => -1.0  // 如果评分无法转换为数字，则返回-1.0
        }
        val duration = try {
          cols(11).replace("\"", "").trim.toInt  // 第12列：电影时长
        } catch {
          case _: Exception => 0  // 如果时长无法转换为数字，则返回0
        }
        (rating, duration)
      } else {
        (-1.0, 0)  // 如果数据格式不正确，则返回无效数据
      }
    }

    // 删除评分为空、评分不合理、不是数字的元组
    val validData = result.filter { case (rating, _) => rating > 0 && rating <= 10 }

    // 删除时长为空或为0的元组
    val validMovies = validData.filter { case (_, duration) => duration > 0 }

    // 统计不同电影时长的评分情况
    val lengthRatingStats = validMovies
      .map { case (rating, duration) => (duration, (rating, 1)) }  // 以电影时长为key，评分和计数为value
      .reduceByKey { case ((ratingSum1, count1), (ratingSum2, count2)) =>
        (ratingSum1 + ratingSum2, count1 + count2)  // 累加评分总和和计数
      }
      .mapValues { case (ratingSum, count) =>
        (ratingSum / count, count)  // 计算平均评分和总数
      }

    // 保存结果到指定路径
    val outputPath = "src/main/scala/FilmDataAnalysis/s6/data"
    lengthRatingStats.saveAsTextFile(outputPath)

  }
}
