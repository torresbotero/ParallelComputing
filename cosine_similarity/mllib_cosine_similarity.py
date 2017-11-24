from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.feature import IDF
from pyspark.mllib.feature import Normalizer
import sys, re

#CONFIG
# ----------------------------------------------------------------------------
# Se crea una sesion de spark con los parametros de configuracion necesarios:
# appName = Nombre de la aplicacion Spark
# en el parametro config se establecen las rutas para la conexion con MongoDB
# spark.mongodb.input.uri = Ruta de lectura en MongoDB
# spark.mongodb.output.uri = Ruta de escritura en MongoDB
spark = SparkSession \
    .builder \
    .appName("CosineSimilarityGutenberg") \
    .config("spark.mongodb.input.uri", "mongodb://<user>:<pass>@<host>/<db_name>.read_collection") \
    .config("spark.mongodb.output.uri", "mongodb://<user>:<pass>@<host>/<db_name>.write_collection") \
    .getOrCreate()

# Se obtiene el contexto de Spark y se establece el nivel de log en ERROR
# Esto se hace para no tener muchos mensajes en la terminal al momento de ejecutar el programa
sc = spark.sparkContext
sc.setLogLevel("ERROR")
# ----------------------------------------------------------------------------

# Se obtienen los archivos de texto de la coleccion Gutenberg almacenada en HDFS
# La variable names almacena los nombres de los archivos de texto para ser relacionados luego con los resultados
# En la variable documents se almacenan los documentos separados por palabras
files = sc.wholeTextFiles('/user/ctorres9/datasets/gutenberg')
names = files.keys().map(lambda n: n.rsplit('/', 1)[1])
documents = files.values().map(lambda doc: re.split('\W+', doc))

# Se crea un objeto HashingTF. El paramtro 1500 es el numero de caracteristicas con que quedaran los vectores
# El proceso de hashing funciona con las frecuencias de las palabras y transforma de acuerdo a esto los documentos en
# vectores de longitud 1500. La variable documentos ya tiene los documentos seperados por palabras para poder aplicar
# la función de hashing.
hashingTF = HashingTF(1500)
tf = hashingTF.transform(documents)

# Se crea un objeto IDF el cual calcula la frecuencia inversa del documento de acuerdo a los vectores obtenidos con el
# proceso de hashing en la frecuencia de terminos
idf = IDF(minDocFreq=2).fit(tf)

# Ya con los vectores tf e idf se puede hacer el calculo del tfidf con el fin de tener los documentos vectorizados
# y acordes para el calculo de la similitud.
tfidf = idf.transform(tf)

# Se crea un objeto normalizer para hallar la norma o distancia euclidiana de los vectores tfidf. Esto se hace para
# luego relizar el producto punto entre todos los valores, lo cual se traduce como la formula del coseno.
normalizer = Normalizer()

# Se agregan los nombres de los documentos a su correspondiente vector ya normalizado
data = names.zip(normalizer.transform(tfidf))

# La operacion cartesian realiza el producto punto de los vectores normalizados (coseno) entre todos los vectores, es
# decir, el resultado es la similitud de cada elemento con el resto
result = data.cartesian(data)\
    .map(lambda l: (l[0][0], {'doc_name':l[1][0], 'similarity':float(l[0][1].dot(l[1][1]))}))\
    .groupByKey()\
    .collect()

# Por ultimo se recorren los resultados y se almacenan en MongoDB para ser consultados. Se guarda para cada documento,
# el nombre como el _id y un listado de las relaciones con los demas documentos.
for value in result:
	simil_docs = spark.createDataFrame([(value[0],  list(value[1]))], ["_id", "simil_docs"])
	simil_docs.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()
