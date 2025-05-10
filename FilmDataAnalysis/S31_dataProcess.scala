package FilmDataAnalysis

import org.apache.spark.{SparkConf, SparkContext}

object S31_dataProcess {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local").setAppName("S31_dataProcess")
    val sc = new SparkContext(conf)

    // 1. 读取 movies 文件（路径可以空出，由你来填写）
    val filePath = "hdfs://master:9000/movie/input/movies"  // 请替换为实际文件路径
    val rawData = sc.textFile(filePath)

    // 2. 只保留第7列（电影评分）和第14列（所在地区），并去掉双引号
    val result = rawData.map { line =>
      val cols = line.split(",") // 按逗号分割
      if (cols.length >= 14) {
        val rating = cols(6).replace("\"", "").trim  // 第7列（电影评分）
        val region = cols(13).replace("\"", "").trim  // 第14列（所在地区）
        (rating, region)
      } else {
        ("", "")  // 如果数据不完整，返回空元组
      }
    }

    // 3. 删除评分为空或评分不在0-10范围内或不是数字的记录
    val validRatings = result.filter {
      case (rating, _) =>
        try {
          val ratingValue = rating.toDouble
          ratingValue > 0 && ratingValue < 10  // 评分范围检查
        } catch {
          case _: Exception => false  // 如果评分不是数字，删除该记录
        }
    }

    // 4. 删除所在地区为空的记录
    val cleanedData = validRatings.filter {
      case (_, region) => region.nonEmpty
    }

    // 5. 将结果保存到指定路径（路径可以空出，由你来填写）
    val outputPath = "src/main/scala/FilmDataAnalysis/s3/data"  // 请替换为实际保存路径
    cleanedData.saveAsTextFile(outputPath)
  }
}
