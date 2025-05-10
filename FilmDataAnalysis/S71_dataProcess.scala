package FilmDataAnalysis

import org.apache.spark.{SparkConf, SparkContext}

object S71_dataProcess {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local").setAppName("S71_dataProcess")
    val sc = new SparkContext(conf)

    // 读取movies数据
    val moviesPath = "hdfs://master:9000/movie/input/movies"
    val rawMoviesData = sc.textFile(moviesPath)

    // 处理数据：先按逗号分隔，再去掉双引号，提取豆瓣评分（第7列）和导演（第6列）
    val result = rawMoviesData.map { line =>
      val cols = line.split(",")  // 按逗号分割
      // 去掉双引号并提取需要的列
      if (cols.length >= 7) {  // 确保数据列数足够
        val rating = try {
          cols(6).replace("\"", "").trim.toDouble  // 第7列：豆瓣评分
        } catch {
          case _: Exception => -1.0  // 如果评分无法转换为数字，则返回-1.0
        }
        val director = cols(5).replace("\"", "").trim  // 第6列：导演
        (rating, director)
      } else {
        (-1.0, "")  // 如果数据格式不正确，则返回无效数据
      }
    }

    // 删除评分为空、评分不合理、不是数字的元组
    val validData = result.filter { case (rating, _) => rating > 0 && rating <= 10 }

    // 删除导演为空的元组
    val validMovies = validData.filter { case (_, director) => director.nonEmpty }


    val outputPath = "src/main/scala/FilmDataAnalysis/s7/data"
    validMovies.saveAsTextFile(outputPath)

  }
}
