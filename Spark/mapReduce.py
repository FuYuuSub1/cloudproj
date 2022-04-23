import os
import sys

from pyspark import SparkContext
from pyspark import HiveContext

def try_int(x):
    try:
        return int(x)
    except ValueError:
        return 0

sc = SparkContext()
sqlContext = HiveContext(sc)
args = sys.argv
inputFile = args[1]
outputFile = args[2]
textFile = sc.textFile(inputFile+"*")

'''
  isRapidlySpeedup,
  isRapidlySlowdown
  isNeutralSlide,
  isNeutralSlideFinished,
  neutralSlideTime,
  isOverspeed,
  isOverspeedFinished,
  overspeedTime,
  isFatigueDriving,
  isHthrottleStop,
  isOilLeak,
'''

emptyData = ['','','','','','','','','','','']
# split and create key value pair (key = array[0])
result = textFile.map(lambda line: tuple(line.split(","))) \
                  .map(lambda array: (array[0], list(array[1:2])+list(array[9:])) if len(array)>9 else (array[0],list(array[1:2])+ [e for e in emptyData])) \
                  .map(lambda array: (array[0], tuple(list(array[1][:1]) + [try_int(x) for x in array[1][1:]]))) \
                  .reduceByKey(lambda x, y: (x[0], x[1]+y[1],x[2]+y[2],x[3]+y[3],x[4]+y[4],x[5]+y[5],x[6]+y[6],x[7]+y[7],x[8]+y[8],x[9]+y[9],x[10]+y[10],x[11]+y[11]))

result.coalesce(1).saveAsTextFile(outputFile)

sc.stop()