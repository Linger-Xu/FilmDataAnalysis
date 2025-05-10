package FilmDataAnalysis

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.rdd.RDD
import scala.math.sqrt

object S32_dataAnalysis {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local").setAppName("S32_dataAnlysis")
    val sc = new SparkContext(conf)

    // 1. 读取文件（路径由你给出）
    val filePath = "src/main/scala/FilmDataAnalysis/s3/data/part-00000"  // 请替换为实际文件路径
    val rawData = sc.textFile(filePath)

    // 2. 处理数据：去掉括号并按逗号分割，提取评分和所在地区
    val ratingsAndRegions: RDD[(String, Double)] = rawData.map { line =>
      // 去掉括号并分割
      val cleanedLine = line.stripPrefix("(").stripSuffix(")") // 去掉外层括号
      val cols = cleanedLine.split(",") // 按逗号分割
      if (cols.length == 2) {  // 确保每行有两个字段
        val region = cols(1).trim  // 第2列：所在地区
        val rating = try {
          Some(cols(0).trim.toDouble)  // 第1列：评分
        } catch {
          case _: Exception => None  // 如果评分无法转换为数字，则返回None
        }
        (region, rating.getOrElse(0.0))  // 如果评分无效，则设置为0
      } else {
        ("", 0.0)  // 如果数据格式不正确，则返回空元组
      }
    }

    // 3. 删除地区为空的记录
    val validRatings = ratingsAndRegions.filter { case (region, _) => region.nonEmpty }

    // 4. 计算每个地区的平均分和标准差
    val regionStats: RDD[(String, (Double, Double, Int))] = validRatings
      .mapValues(rating => (rating, rating * rating, 1))  // 每个评分： (评分, 评分的平方, 计数)
      .reduceByKey { case ((sum, sumOfSquares, count), (rating, ratingSquared, _)) =>
        (sum + rating, sumOfSquares + ratingSquared, count + 1)
      }
      .mapValues { case (sum, sumOfSquares, count) =>
        val mean = sum / count
        val variance = (sumOfSquares / count) - (mean * mean)
        val stddev = sqrt(variance)
        (mean, stddev, count)  // 返回平均分、标准差和评分数
      }

    // 5. 将结果保存到指定路径
    val outputPath = "src/main/scala/FilmDataAnalysis/s3/regionStats"  // 请替换为实际输出路径
    regionStats.saveAsTextFile(outputPath)

  }
}
