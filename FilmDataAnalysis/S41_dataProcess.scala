package FilmDataAnalysis

import org.apache.spark.{SparkConf, SparkContext}
import java.text.SimpleDateFormat

object S41_dataProcess {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local").setAppName("S41_dataProcess")
    val sc = new SparkContext(conf)

    // 1. 读取 ratings 文件（路径由你提供）
    val filePath = "hdfs://master:9000/movie/input/ratings"  // 请替换为实际文件路径
    val rawData = sc.textFile(filePath)

    // 2. 只保留第二列（用户ID），第四列（评分），第五列（评价时间），并去掉双引号
    val result = rawData.map { line =>
      val cols = line.split(",") // 按逗号分割
      if (cols.length >= 5) {
        val userId = cols(1).replace("\"", "").trim  // 第二列：用户ID
        val rating = cols(3).replace("\"", "").trim  // 第四列：评分
        val timestamp = cols(4).replace("\"", "").trim  // 第五列：评价时间
        (userId, rating, timestamp)
      } else {
        ("", "", "")  // 如果数据不完整，则返回空元组
      }
    }

    // 3. 删除用户ID为空的元组（用户ID是MD5码）
    val cleanedResult1 = result.filter {
      case (userId, _, _) => userId.matches("^[a-f0-9]{32}$")  // 检查用户ID是否是有效的MD5
    }

    // 4. 删除评分为空或不合法的元组（评分必须是1、2、3、4、5）
    val cleanedResult2 = cleanedResult1.filter {
      case (_, rating, _) => rating.matches("^[1-5]$")  // 确保评分是1到5之间的数字
    }


    // 5. 删除评价时间为空或格式不合法的元组（格式应为 "yyyy/MM/dd HH:mm"）
    val dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm")
    val cleanedResult3 = cleanedResult2.filter {
      case (_, _, timestamp) =>
        try {
          dateFormat.parse(timestamp)  // 尝试解析日期，若格式不对则抛出异常
          true
        } catch {
          case _: Exception => false  // 日期格式不合法，删除该记录
        }
    }

    // 6. 将结果保存到指定路径（路径可以空出，由你来填写）
    val outputPath = "src/main/scala/FilmDataAnalysis/s4/data"  // 请替换为实际保存路径
    cleanedResult3.saveAsTextFile(outputPath)
  }
}
