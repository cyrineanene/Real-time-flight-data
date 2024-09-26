#In this project, a new dataset called 'airports_external.csv' was added. It was due to the lack of airports informations in the other csv daatset/API of AirLab.
#An additional treatement will be conducted for this dataset.

#This script processes streaming data from Kafka topic 'flight', enriches it with additional information from csv dataset, and writes the results to Elasticsearch.

from pyspark.sql import SparkSession #to create DataFrames and manage configurations
from pyspark.conf import SparkConf #to configure Spark settings
from pyspark.sql.types import StructType, StructField, DoubleType, IntegerType
from pyspark.sql.functions import from_json, col, when, length
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

#Step 1: define the schema of the incoming JSON file from Kafka 
flight_schema = StructType([
    StructField("position", StructType([
        StructField("lat", DoubleType(), True),
        StructField("lon", DoubleType(), True)
    ]), True),
    StructField("hex", StringType(), True),
    StructField("reg_number", StringType(), True),
    StructField("flag", StringType(), True),
    StructField("alt", DoubleType(), True),
    StructField("dir", DoubleType(), True),
    StructField("speed", IntegerType(), True),
    StructField("v_speed", IntegerType(), True),
    StructField("flight_number", StringType(), True),
    StructField("flight_icao", StringType(), True),
    StructField("flight_iata", StringType(), True),
    StructField("dep_icao", StringType(), True),
    StructField("dep_iata", StringType(), True),
    StructField("arr_icao", StringType(), True),
    StructField("arr_iata", StringType(), True),
    StructField("airline_icao", StringType(), True),
    StructField("airline_iata", StringType(), True),
    StructField("aircraft_icao", StringType(), True),
    StructField("status", StringType(), True),
])

#Step 2: configuring the spark: 
# Parameters: name:flight_consumer
#             spark_mode:local
#             memory of spark executors:2GB
#             number of CPU cores of the spark executors:2 CPUs
spark_conf = SparkConf() \
    .setAppName("flight_consumer") \
    .setMaster("local") \
    .set("spark.executor.memory", "2g") \
    .set("spark.executor.cores", "2")

#Step 3: creating a spark session
spark = SparkSession.builder.config(conf=spark_conf).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

#Step 4: getting the data from Kafka
#Using the 9092 port because it's using Kafka from within (internally)
#the first option specifies the server to listen to kafka from
#the second option specifies the topic to use
dataframe = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", 'kafka:9092') \
    .option("subscribe", "flight") \
    .load()

#Step 5: processing the data
#loading csv into dictionaries
#first directionary contains the IATA (type of ID) of the contries of the airport 
#second directionary contains the IATA (type of ID) of the position (latitude and longitude) of the airport
#third directionary contains the IATA (type of ID) of the name of the airport 
iata_country_dict = spark.read.csv("airports_external.csv", header=True) \
                            .rdd \
                            .map(lambda row: (row["iata"], row["country_code"])) \
                            .collectAsMap()

iata_position_dict = spark.read.csv("airports_external.csv", header=True) \
                            .rdd \
                            .map(lambda row: (row["iata"], (float(row["lat"]), float(row["lon"])))) \
                            .collectAsMap()

iata_name_dict = spark.read.csv("airports_external.csv", header=True) \
                            .rdd \
                            .map(lambda row: (row["iata"], row["Name"])) \
                            .collectAsMap()
