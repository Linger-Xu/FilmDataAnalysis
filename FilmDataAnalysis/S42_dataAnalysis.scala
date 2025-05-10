package FilmDataAnalysis

import org.apache.spark.{SparkConf, SparkContext}
import java.text.SimpleDateFormat
import java.util.Calendar

object S42_dataAnalysis {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local").setAppName("S42_dataAnalysis")
    val sc = new SparkContext(conf)

    // 1. 读取多个文件并合并
    val dataPath = "src/main/scala/FilmDataAnalysis/s4/data"
    val rawData = sc.textFile(dataPath + "/part-00000")
      .union(sc.textFile(dataPath + "/part-00001"))
      .union(sc.textFile(dataPath + "/part-00002"))

    // 2. 提取评分、评价时间和年份信息
    val result = rawData.map { line =>
      // 去掉括号并分割
      val cleanedLine = line.stripPrefix("(").stripSuffix(")")  // 去掉外层括号
      val cols = cleanedLine.split(",")  // 按逗号分割
      if (cols.length >= 3) {  // 确保每行至少有5列
        val rating = try {
          Some(cols(1).trim.toInt)  // 第2列：评分
        } catch {
          case _: Exception => None  // 如果评分无法转换为数字，则返回None
        }

        val timestamp = cols(2).trim  // 第3列：评价时间
        val dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
        val year = try {
          val date = dateFormat.parse(timestamp)
          val calendar = Calendar.getInstance()
          calendar.setTime(date)
          calendar.get(Calendar.YEAR)  // 提取年份
        } catch {
          case _: Exception => 0  // 如果日期无法解析，则返回0
        }

        val month = try {
          val date = dateFormat.parse(timestamp)
          val calendar = Calendar.getInstance()
          calendar.setTime(date)
          calendar.get(Calendar.MONTH) + 1  // 提取月份（1-12）
        } catch {
          case _: Exception => 0  // 如果日期无法解析，则返回0
        }

        val hour = try {
          val date = dateFormat.parse(timestamp)
          val calendar = Calendar.getInstance()
          calendar.setTime(date)
          calendar.get(Calendar.HOUR_OF_DAY)  // 提取小时（0-23）
        } catch {
          case _: Exception => -1  // 如果日期无法解析，则返回-1
        }

        (year, month, hour, rating.getOrElse(0), 1)  // 返回元组：年份、月份、小时、评分、计数
      } else {
        (0, 0, -1, 0, 0)  // 如果数据格式不正确，则返回无效元组
      }
    }
    result.take(5)

    // 3. 删除无效数据：去掉无效年份、月份、小时和评分数据
    val validRatings = result.filter { case (year, _, _, _, _) => year > 0 && year < 9999 }  // 有效年份
      .filter { case (_, month, _, _, _) => month >= 1 && month <= 12 }  // 有效月份
      .filter { case (_, _, hour, _, _) => hour >= 0 && hour <= 23 }  // 有效小时
      .filter { case (_, _, _, rating, _) => rating >= 1 && rating <= 5 }  // 有效评分

    // 4. 统计每一年的均分及评分数量（1星到5星的数量）
    val yearStats = validRatings
      .map { case (year, _, _, rating, _) =>
        // 返回每年评分的元组： (年份, (评分, 1))
        (year, (rating, 1))
      }
      .reduceByKey { case ((ratingSum1, count1), (ratingSum2, count2)) =>
        (ratingSum1 + ratingSum2, count1 + count2) // 累加评分总和和用户计数
      }
      .mapValues { case (ratingSum, count) =>
        ratingSum.toDouble / count // 计算每年的平均评分
      }

    // 统计每一年的1星到5星的用户数量
    val yearRatingCounts = validRatings
      .map { case (year, _, _, rating, _) =>
        // 返回每年不同评分的数量： (年份, (1星数量, 2星数量, 3星数量, 4星数量, 5星数量))
        rating match {
          case 1 => (year, (1, 0, 0, 0, 0)) // 1星
          case 2 => (year, (0, 1, 0, 0, 0)) // 2星
          case 3 => (year, (0, 0, 1, 0, 0)) // 3星
          case 4 => (year, (0, 0, 0, 1, 0)) // 4星
          case 5 => (year, (0, 0, 0, 0, 1)) // 5星
          case _ => (year, (0, 0, 0, 0, 0)) // 如果评分无效，则返回0
        }
      }
      .reduceByKey { case ((count1, count2, count3, count4, count5), (count1New, count2New, count3New, count4New, count5New)) =>
        // 对每年的评分数量进行累加
        (count1 + count1New, count2 + count2New, count3 + count3New, count4 + count4New, count5 + count5New)
      }

    // 5. 统计不同季节的均分和评分数量（1星到5星的数量）
    val seasonStats = validRatings
      .map {
        case (year, month, _, rating, _) =>
          val season = month match {
            case 3 | 4 | 5 => "Spring"  // 春季
            case 6 | 7 | 8 => "Summer"  // 夏季
            case 9 | 10 | 11 => "Autumn"  // 秋季
            case 12 | 1 | 2 => "Winter"  // 冬季
            case _ => "Unknown"
          }

          // 根据评分来统计1-5星数量
          val ratingCount = rating match {
            case 1 => (1, 0, 0, 0, 0)  // 1星
            case 2 => (0, 1, 0, 0, 0)  // 2星
            case 3 => (0, 0, 1, 0, 0)  // 3星
            case 4 => (0, 0, 0, 1, 0)  // 4星
            case 5 => (0, 0, 0, 0, 1)  // 5星
            case _ => (0, 0, 0, 0, 0)  // 无效评分
          }

          // 返回季节、评分（1-5星数量的元组）
          (season, (rating, 1, ratingCount._1, ratingCount._2, ratingCount._3, ratingCount._4, ratingCount._5))
      }

    val seasonStatsAggregated = seasonStats
      .reduceByKey { case ((ratingSum1, count1, count1_1, count1_2, count1_3, count1_4, count1_5),
      (ratingSum2, count2, count2_1, count2_2, count2_3, count2_4, count2_5)) =>
        // 累加评分总和、计数、1-5星数量
        (
          ratingSum1 + ratingSum2,    // 累加评分总和
          count1 + count2,            // 累加计数
          count1_1 + count2_1,        // 累加1星数量
          count1_2 + count2_2,        // 累加2星数量
          count1_3 + count2_3,        // 累加3星数量
          count1_4 + count2_4,        // 累加4星数量
          count1_5 + count2_5         // 累加5星数量
        )
      }
      .mapValues { case (ratingSum, count, count1, count2, count3, count4, count5) =>
        val avgRating = if (count > 0) ratingSum.toDouble / count else 0.0  // 计算均分
        (avgRating, count1, count2, count3, count4, count5)  // 返回每个季节的均分和1-5星数量
      }

    // 6. 统计每小时的均分及1星到5星的数量
    val hourStats = validRatings
      .map { case (_, _, hour, rating, _) =>
        // 这里为每个小时返回评分均分的元组
        (hour, (rating, 1))
      }
      .reduceByKey { case ((ratingSum1, count1), (ratingSum2, count2)) =>
        (ratingSum1 + ratingSum2, count1 + count2)  // 累加评分总和和计数
      }
      .mapValues { case (ratingSum, count) =>
        ratingSum.toDouble / count  // 计算均分
      }

    // 统计每小时的1星到5星的数量
    val hourRatingCounts = validRatings
      .map { case (_, _, hour, rating, _) =>
        // 为每个小时生成评分数量的元组
        val ratingCount = rating match {
          case 1 => (1, 0, 0, 0, 0)  // 1星
          case 2 => (0, 1, 0, 0, 0)  // 2星
          case 3 => (0, 0, 1, 0, 0)  // 3星
          case 4 => (0, 0, 0, 1, 0)  // 4星
          case 5 => (0, 0, 0, 0, 1)  // 5星
          case _ => (0, 0, 0, 0, 0)  // 如果评分不在1-5之间，则返回全为0
        }
        (hour, ratingCount)
      }
      .reduceByKey { case ((c1, c2, c3, c4, c5), (d1, d2, d3, d4, d5)) =>
        // 累加每个小时内1-5星的数量
        (c1 + d1, c2 + d2, c3 + d3, c4 + d4, c5 + d5)
      }


    // 7. 保存结果到指定路径
    //val yearStatsPath = "src/main/scala/FilmDataAnalysis/s4/yearRatingCounts"  // 请替换为实际保存路径
    //yearRatingCounts.saveAsTextFile(yearStatsPath)

    val seasonStatsPath = "src/main/scala/FilmDataAnalysis/s4/seasonStats"  // 请替换为实际保存路径
    seasonStatsAggregated.repartition(1).saveAsTextFile(seasonStatsPath)

    //val hourStatsPath = "src/main/scala/FilmDataAnalysis/s4/hourStats"  // 请替换为实际保存路径
    //hourStats.saveAsTextFile(hourStatsPath)

    //val hourRatingCountsPath = "src/main/scala/FilmDataAnalysis/s4/hourRatingCounts"  // 请替换为实际保存路径
    //hourRatingCounts.saveAsTextFile(hourRatingCountsPath)

  }
}
