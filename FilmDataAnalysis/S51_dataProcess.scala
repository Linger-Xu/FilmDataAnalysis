package FilmDataAnalysis

import org.apache.spark.{SparkConf, SparkContext}

object S51_dataProcess {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local").setAppName("S51_dataProcess")
    val sc = new SparkContext(conf)

    //读取movies文件
    val moviesPath = "hdfs://master:9000/movie/input/movies"
    val rawMoviesData = sc.textFile(moviesPath)

    //处理movies数据：保留第1列(movie_id)，第7列(豆瓣评分)，第8列(类型)，并清洗数据
    val result = rawMoviesData.map { line =>
      val cols = line.split(",")  // 按逗号分割
      // 去掉双引号并提取需要的列
      if (cols.length >= 9) {  // 确保有8列
        val movieId = cols(0).replace("\"", "").trim  // 去掉双引号
        val rating = try {
          Some(cols(6).replace("\"", "").trim.toDouble)  // 第7列：豆瓣评分，去掉双引号
        } catch {
          case _: Exception => None  // 如果评分无法转换为数字，则返回None
        }
        val genre = cols(8).replace("\"", "").trim  // 第8列：类型，去掉双引号
        (movieId, rating, genre)
      } else {
        ("", None, "")  // 如果数据不完整，则返回空元组
      }
    }



    // 删除movie_id为空的元组
    val validMovies = result.filter { case (movieId, _, _) => movieId.nonEmpty }

    // 删除类型为空的元组
    val validMoviesWithGenres = validMovies.filter { case (_, _, genre) => genre.nonEmpty }

    // 删除评分为空或数字不合理的元组
    val finalMovies = validMoviesWithGenres.filter {
      case (_, Some(rating), _) => rating > 0 && rating < 10 // 评分在0到10之间
      case _ => false // 排除评分为空或不符合条件的记录
    }.map { case (movieId, Some(rating), genre) => (movieId, rating, genre) } // 直接存储评分的数值



    // 读取ratings文件（路径由你提供）
    val ratingsPath = "hdfs://master:9000/movie/input/ratings"  // 请替换为实际文件路径
    val rawRatingsData = sc.textFile(ratingsPath)

    // 处理ratings数据：只保留第3列(movie_id)和第4列(rating)，并清洗数据
    val result2 = rawRatingsData.map { line =>
      val cols = line.split(",")  // 按逗号分割
      // 去掉双引号并提取需要的列
      if (cols.length >= 4) {  // 确保有4列
        val movieId = cols(2).replace("\"", "").trim  // 第3列：movie_id，去掉双引号
        val rating = try {
          Some(cols(3).replace("\"", "").trim.toInt)  // 第4列：评分，去掉双引号
        } catch {
          case _: Exception => None  // 如果评分无法转换为数字，则返回None
        }
        (movieId, rating)
      } else {
        ("", None)  // 如果数据不完整，则返回空元组
      }
    }

    // 删除movie_id或者rating为空的元组
    val validRatings = result2.filter { case (movieId, rating) => movieId.nonEmpty && rating.isDefined }
      .map { case (movieId, Some(rating)) => (movieId, rating) } // 去掉Some包装，直接使用数值




    val moviesOutputPath = "src/main/scala/FilmDataAnalysis/s5/mdata"
    finalMovies.repartition(1).saveAsTextFile(moviesOutputPath)

    val ratingsOutputPath = "src/main/scala/FilmDataAnalysis/s5/rdata"
    validRatings.repartition(1).saveAsTextFile(ratingsOutputPath)
  }
}
