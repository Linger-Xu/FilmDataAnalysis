package FilmDataAnalysis

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.Row
import org.apache.spark.sql.functions._

object S11_dataProcess {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local").setAppName("S11_dataProcess")
    val sc = new SparkContext(conf)

    val filePath = "hdfs://master:9000/movie/input/movies"
    val rawData = sc.textFile(filePath)


    //处理数据，只保留豆瓣评分和上映年份（第7列和第19列）
    val result: RDD[(Double, Int)] = rawData
      .map(line => {
        val cleanedLine=line.replaceAll("\"", "")
        val cols = cleanedLine.split(",")
        if (cols.length >= 19) {
          val score = try {
            Some(cols(6).toDouble)  // 第7列是豆瓣评分
          } catch {
            case _: Exception => None  // 如果评分不是数字，则为None
          }
          val year = try {
            Some(cols(18).take(4).toInt)  // 第19列是上映年份，取前4位作为年份
          } catch {
            case _: Exception => None  // 如果年份无法转换为整数，则为None
          }
          (score, year)
        } else {
          (None, None)
        }
      })
      .filter {
        case (Some(score), Some(year)) =>
          score > 0 && score < 10 && year >= 1900 && year <= 2025  // 过滤不合理数据
        case _ => false
      }
      .map {
        case (Some(score), Some(year)) => (score, year)
        case _ => null
      }
      .filter(_ != null)  // 进一步过滤掉null值

    val outputPath = "src/main/scala/FilmDataAnalysis/s1/data"
    result.saveAsTextFile(outputPath)
    sc.stop()
  }
}
