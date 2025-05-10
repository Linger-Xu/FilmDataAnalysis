package FilmDataAnalysis

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.rdd.RDD

object S21_dataProcess {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local").setAppName("S21_dataProcess")
    val sc = new SparkContext(conf)

    // 1. 读取 ratings 文件（路径可以空出，由你来填写）
    val filePath = "hdfs://master:9000/movie/input/ratings"  // 请替换为实际文件路径
    val rawData = sc.textFile(filePath)

    // 2. 只保留第二列（用户id），第三列（评价电影id），第四列（评分），生成新的 RDD
    val result: RDD[(String, String, Int)] = rawData.map { line =>
      val cols = line.split(",") // 假设数据用逗号分隔
      if (cols.length >= 4) {
        // 去掉字段中的引号
        val userId = cols(1).replace("\"", "").trim
        val movieId = cols(2).replace("\"", "").trim
        // 评分字段的处理：去掉引号并转换为整数
        val rating = try {
          Some(cols(3).replace("\"", "").trim.toInt)  // 转换为整数
        } catch {
          case _: Exception => None  // 如果转换失败，则为None
        }

        // 如果rating是None，则返回一个默认值，比如0
        (userId, movieId, rating.getOrElse(0))  // 使用getOrElse来避免Option
      } else {
        ("", "", 0)  // 如果行格式不对，返回一个默认值
      }
    }

    // 3. 删除用户id为空的元组
    val cleanedResult1 = result.filter {
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

    // 6. 将结果保存到指定路径（路径可以空出，由你来填写）
    val outputPath = "src/main/scala/FilmDataAnalysis/s2/data"  // 请替换为实际保存路径
    cleanedResult3.saveAsTextFile(outputPath)
  }
}
