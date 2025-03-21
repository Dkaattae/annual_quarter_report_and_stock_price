import argparse

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import md5, concat_ws, col, explode, lit
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql import Row
import re

parser = argparse.ArgumentParser()

parser.add_argument('--input_business_section', required=True)
parser.add_argument('--output', required=True)

args = parser.parse_args()

input_business_section = args.input_business_section
output = args.output

spark = SparkSession.builder \
    .config("spark.jars", "gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.42.0.jar") \
    .appName('WordCountPerFile') \
    .getOrCreate()

words_to_count = {"AI", "restructuring", "sustainability"}
rdd = spark.sparkContext.wholeTextFiles(concat(input_business_section, '/*.txt'))
def count_words(file_content):
    filename, content = file_content
    parts = filename.split("/")[-1].split("_")  # Extract filename and split
    if len(parts) >= 3:
        ticker, file_type, file_date, business, section= parts  # Extract file_date
    else:
        file_date = "unknown"  # Handle unexpected formats
    total_count = len(content.split())  # Get total word count
    word_counts = {word: len(re.findall(rf"\b{word}\b", content, re.IGNORECASE)) for word in words_to_count}
    
    # Convert into a list of (filename, total_count, word, word_count) tuples
    return [(filename.split("/")[-1], file_date, total_count, word, count) for word, count in word_counts.items()]

# Flatten RDD
word_counts_rdd = rdd.flatMap(count_words)

# Convert to DataFrame
schema = StructType([
    StructField("file_name", StringType(), False),
    StructField("file_date", StringType(), False),
    StructField("total_word_count", IntegerType(), False),
    StructField("word", StringType(), False),
    StructField("word_count", IntegerType(), False)
])

df = spark.createDataFrame(word_counts_rdd, schema=schema)

# Generate ID column using md5(concat(file_name, word))
df = df.withColumn("id", md5(concat_ws("_", col("file_name"), col("file_date"), col("word"))))

# Rearrange columns
df = df.select("id", "file_name", "file_date", "total_word_count", "word", "word_count")

word_counts_df.write.mode("overwrite").parquet(output_path)

df_result.write.format('bigquery') \
    .option('table', output) \
    .save()

spark.stop()