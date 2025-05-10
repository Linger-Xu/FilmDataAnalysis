package FilmDataAnalysis

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.rdd.RDD

object S22_dataAnalysis {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local").setAppName("S22_dataAnalysis")
    val sc = new SparkContext(conf)

    // 1. 读取三个文件并合并
    val rawData = sc.textFile("src/main/scala/FilmDataAnalysis/s2/data/part-00000")
      .union(sc.textFile("src/main/scala/FilmDataAnalysis/s2/data/part-00001"))
      .union(sc.textFile("src/main/scala/FilmDataAnalysis/s2/data/part-00002"))

    // 2. 处理数据，拆分并去掉括号
    val ratings: RDD[(String, String, Int)] = rawData.map { line =>
      // 去掉括号并分割
      val cleanedLine = line.stripPrefix("(").stripSuffix(")") // 去掉外层括号
      val cols = cleanedLine.split(",") // 按逗号分割
      if (cols.length == 3) {  // 确保每行有三个字段
        val userId = cols(0).trim
        val movieId = cols(1).trim
        val rating = try {
          cols(2).replace("\"", "").trim.toInt  // 直接转换为整数
        } catch {
          case _: Exception => 0  // 如果转换失败，则设置默认值0
        }
        (userId, movieId, rating)
      } else {
        ("", "", 0)  // 如果数据不完整，则返回空元组，评分为0
      }
    }


    // 3. 删除用户id为空的元组
    val cleanedResult1 = ratings.filter {
      case (userId, _, _) => userId.nonEmpty
    }

    // 4. 删除评价电影id为空的元组
    val cleanedResult2 = cleanedResult1.filter {
      case (_, movieId, _) => movieId.nonEmpty
    }

    // 5. 删除评分为空或评分不合法（只能是1-5）元组
    val cleanedResult3 = cleanedResult2.filter {
      case (_, _, rating) => rating >= 1 && rating <= 5
    }

    // 6. 统计每个用户id打出1, 2, 3, 4, 5星的次数
    val ratingCounts: RDD[(String, Map[Int, Int])] = cleanedResult3
      .map { case (userId, _, rating) => (userId, rating) }
      .filter { case (userId, _) => userId.nonEmpty }
      .groupByKey()
      .mapValues(ratingsList => {
        ratingsList.groupBy(identity).mapValues(_.size).toMap
      })

    ratingCounts.saveAsTextFile("src/main/scala/FilmDataAnalysis/s2/count")

    // 7. 统计只打1星或者5星的用户id，以及他们打1星和5星的次数
    val oneAndFiveUsers: RDD[(String, (Int, Int))] = cleanedResult3
      .filter { case (_, _, rating) => rating == 1 || rating == 5 }
      .map { case (userId, _, rating) => (userId, rating) }
      .groupByKey()
      .filter { case (_, ratings) => ratings.forall(rating => rating == 1 || rating == 5) }
      .mapValues { ratings =>
        val oneCount = ratings.count(_ == 1)
        val fiveCount = ratings.count(_ == 5)
        (oneCount, fiveCount)
      }

    oneAndFiveUsers.saveAsTextFile("src/main/scala/FilmDataAnalysis/s2/oneAndfive")


    // 8. 计算每个用户的平均评分，统计平均分在1.5以下以及4以上的人数
    val userAvgScores: RDD[(String, Double)] = cleanedResult3
      .map { case (userId, _, rating) => (userId, (rating, 1)) }
      .reduceByKey { case ((ratingSum, count), (rating, _)) => (ratingSum + rating, count + 1) }
      .mapValues { case (ratingSum, count) => ratingSum.toDouble / count }

    val lowScoringUsersCount = userAvgScores.filter { case (_, avgScore) => avgScore < 1.5 }.count()
    val highScoringUsersCount = userAvgScores.filter { case (_, avgScore) => avgScore > 4 }.count()

    // 9. 统计1到5星的评价数量
    val starCounts: RDD[(Int, Int)] = cleanedResult3
      .map { case (_, _, rating) => (rating, 1) }
      .reduceByKey(_ + _) // 对每个评分值进行计数

    println(s"参与打分的用户总数是：${cleanedResult3.count()}")
    println(s"只打1星或者5星的用户总数是: ${oneAndFiveUsers.count()}")
    println(s"平均打分在1.5以下的用户总数是: $lowScoringUsersCount")
    println(s"平均打分在4.0以上的用户总数是: $highScoringUsersCount")
    starCounts.collect().foreach { case (rating, count) =>
      println(s"打 $rating 星的评价数量是: $count")
    }
  }
}
