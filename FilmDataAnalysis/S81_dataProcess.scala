package FilmDataAnalysis

import org.apache.spark.{SparkConf, SparkContext}

object S81_dataProcess {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local").setAppName("S81_dataProcess")
    val sc = new SparkContext(conf)

    // 读取movies数据
    val moviesPath = "hdfs://master:9000/movie/input/movies"
    val rawMoviesData = sc.textFile(moviesPath)

    // 处理数据：按逗号分隔，去掉双引号，提取豆瓣评分（第7列）、豆瓣投票数（第8列）和电影名字（第2列）
    val result = rawMoviesData.map { line =>
      val cols = line.split(",")  // 按逗号分割
      // 去掉双引号并提取需要的列
      if (cols.length >= 8) {  // 确保数据列数足够
        val rating = try {
          cols(6).replace("\"", "").trim.toDouble  // 第7列：豆瓣评分
        } catch {
          case _: Exception => -1.0  // 如果评分无法转换为数字，则返回-1.0
        }
        val votes = try {
          cols(7).replace("\"", "").trim.toInt  // 第8列：豆瓣投票数
        } catch {
          case _: Exception => -1  // 如果投票数无法转换为数字，则返回-1
        }
        val movieName = cols(1).replace("\"", "").trim  // 第2列：电影名字
        (movieName, rating, votes)
      } else {
        ("", -1.0, -1)  // 如果数据格式不正确，则返回无效数据
      }
    }

    // 删除评分为空、评分不合理、不是数字的元组
    val validData = result.filter { case (_, rating, _) => rating > 0 && rating <= 10 }

    // 删除电影名字为空的元组
    val validMovies = validData.filter { case (movieName, _, _) => movieName.nonEmpty }

    // 删除豆瓣投票数为空或不合理的元组
    val finalResult = validMovies.filter { case (_, _, votes) => votes > 0 }

    val outputPath = "src/main/scala/FilmDataAnalysis/s8/data"
    finalResult.saveAsTextFile(outputPath)

  }
}
