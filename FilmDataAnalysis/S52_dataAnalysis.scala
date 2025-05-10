package FilmDataAnalysis

import org.apache.spark.{SparkConf, SparkContext}

object S52_dataAnalysis {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local").setAppName("S52_dataAnalysis")
    val sc = new SparkContext(conf)

    // 读取 mdata 数据
    val mdataPath = "src/main/scala/FilmDataAnalysis/s5/mdata/part-00000"
    val rawMdata = sc.textFile(mdataPath)

    // 读取 rdata 数据
    val rdataPath = "src/main/scala/FilmDataAnalysis/s5/rdata/part-00000"
    val rawRdata = sc.textFile(rdataPath)

    // 处理 mdata 数据：去掉括号，用逗号分割并提取需要的字段
    val moviesData = rawMdata.map { line =>
      val cols = line.stripPrefix("(").stripSuffix(")").split(",")  // 去掉括号并按逗号分割
      if (cols.length >= 3) {
        val movieId = cols(0).trim
        val rating = try {
          cols(1).trim.toDouble  // 豆瓣评分
        } catch {
          case _: Exception => 0.0  // 如果评分无法转换为数字，则返回0.0
        }
        val genre = cols(2).trim
        (movieId, rating, genre)
      } else {
        ("", 0.0, "")  // 如果数据不完整，则返回空元组
      }
    }

    //处理 rdata 数据：去掉括号，用逗号分割并提取需要的字段
    val ratingsData = rawRdata.map { line =>
      val cols = line.stripPrefix("(").stripSuffix(")").split(",")  // 去掉括号并按逗号分割
      if (cols.length >= 2) {
        val movieId = cols(0).trim
        val rating = try {
          cols(1).trim.toInt  // 评分
        } catch {
          case _: Exception => 0  // 如果评分无法转换为数字，则返回0
        }
        (movieId, rating)
      } else {
        ("", 0)  // 如果数据不完整，则返回空元组
      }
    }

    // 统计每个电影的 1 星到 5 星的数量
    val ratingCounts = ratingsData
      .filter { case (_, rating) => rating > 0 }  // 过滤掉评分为0的记录
      .map { case (movieId, rating) =>
        val ratingCount = rating match {
          case 1 => (1, 0, 0, 0, 0)
          case 2 => (0, 1, 0, 0, 0)
          case 3 => (0, 0, 1, 0, 0)
          case 4 => (0, 0, 0, 1, 0)
          case 5 => (0, 0, 0, 0, 1)
          case _ => (0, 0, 0, 0, 0)
        }
        (movieId, ratingCount)
      }
      .reduceByKey { case ((count1, count2, count3, count4, count5), (count1New, count2New, count3New, count4New, count5New)) =>
        (count1 + count1New, count2 + count2New, count3 + count3New, count4 + count4New, count5 + count5New)
      }



    // 对 mdata 中的每个电影，统计其类型，并加上对应的评分数量
    val genreStats = moviesData
      .filter { case (_, _, genre) => genre.nonEmpty }
      .flatMap { case (movieId, rating, genre) =>
        // 获取电影的评分数量
        val ratingCount = if (rating > 0) {
          // 如果电影有评分，在 ratingCounts 中查找该电影的评分数据
          val counts = ratingCounts.lookup(movieId).headOption.getOrElse((0, 0, 0, 0, 0))
          counts
        } else {
          (0, 0, 0, 0, 0) // 如果评分为0，则没有对应评分
        }

        // 如果类型是多个类别，用“/”分隔，拆分成多个类别
        genre.split("/").map { g =>
          (g.trim, ratingCount) // 返回每个类别和对应的评分数量
        }
      }

    genreStats.take(5).foreach(println)

    // 按类别聚合统计数据
    val genreAggregated = genreStats
      .reduceByKey { case ((count1, count2, count3, count4, count5), (count1New, count2New, count3New, count4New, count5New)) =>
        (count1 + count1New, count2 + count2New, count3 + count3New, count4 + count4New, count5 + count5New)
      }

    val genreStatsPath = "src/main/scala/FilmDataAnalysis/s5/genreStats"  // 请替换为实际路径
    genreAggregated.saveAsTextFile(genreStatsPath)

  }
}
