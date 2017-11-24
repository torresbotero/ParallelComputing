# Inverted index

### ¿Para que es este repositorio? ###

Este repositorio contiene el archivo mllib_cosine_similarity.py; este archivo incluye codigo en Python que por medio de 
PySpark (Spark) usando la librería MlLib encuentra la similitud entre un conjunto de documentos de acuerdo a la función
similitud del coseno y lo almacena en base de datos.

#### Resumen

Se realiza un programa en PySpark haciendo uso de la librería MlLib que
permite implementar funciones de machine learning de forma ágil en Spark. Con
este se halla la similitud del coseno entre todos los documentos del dataset,
es decir, la similitud de todos con todos.
Para este procesamiento se usan las funciones HashingTF para convertir los
documentos a vectores de acuerdo a la frecuencia de los terminos pero aplicando
en ellos una función de hashing para reducir el tamaño y la dimensionalidad. Se usa
también la función IDF para calcular la frecuencia de documentos inversa a partir
de los vectores de fercuencias ya hallados. Con los valores obtenidos a partir
de estas dos funciones se halla el valor del tfidf el cual sirve para representar los
documentos de tal forma que puedan ser comparados de acuerdo a sus palabras más relevantes,
penalizando palabras comunes en todos como artículos, preposiciones, es decir, las llamadas
stopwords. 

#### Versión: 1.0


### Pasos para configurar y ejecutar esta aplicación ###

#### Pre-requisitos:
1. (Importante) este script solo puede ser ejecutado con PySpark y la librería MlLib de Spark, es decir, se requiere 
tener instalado un ambiente con Spark. Además es necesario correrlo en un ecosistema Hadoop para leer los archivos 
desde HDFS. No esta probado en un ambiente con Spark standalone aunque debería funcionar correctamente. 
Nota: Para instalar Spark en el ecosistema Hadoop puede seguir esta guía: https://spark.apache.org/docs/latest/running-on-yarn.html
2. Instalar MongoDB Community Edition, siguiendo los pasos descritos en el siguiente enlace: 
https://docs.mongodb.com/manual/installation/
3. Iniciar mongodb para hacer uso de la base de datos requerida por el script, si no se inicia mongodb, el script
presentara errores al momento de ejecutarse. Para ejecutar mongodb, se debe abrir una consola o terminal, y ejecutar
el siguiente comando con permisos de administrador: Mac o Linux (sudo mongod), Windows (mongod.exe).
4. Cambiar los parametros del script para la base de datos: Se debe abrir el archivo mllib_cosine_similarity.py para
edición y en este se debe buscar el comentario CONFIG. En este bloque se encontrara la configuración de la sesión de
Spark donde se encuentran las rutas de conexión a la base de datos, tanto de lectura como de escritura, la siguiente
es la estructura del String de conexión tanto para la colección de la que se quieran leer datos como para la colección
en la cual se quieran escribir o guardar resultados:
	- spark.mongodb.input.uri: "mongodb://<user>:<pass>@<host>/bd_name.read_collection"
	- spark.mongodb.output.uri: "mongodb://<user>:<pass>@<host>/bd_name.write_collection"
5. Tener disponible un conjunto de documentos de texto, con extensión .txt, estos seran los datos de entrada que
procesara el script presente en este repositorio con el fin de hallar la similitud entre todos los documentos.
Se recomienda usar el dataset, con documentos de Gutenberg, disponible en este repositorio.
6. En el script se puede encontrar un linea luego de la configuración que carga los documentos de texto desde HDFS:
    - files = sc.wholeTextFiles('/user/ctorres9/datasets/gutenberg')

Esta linea tiene por defecto una ruta donde se encuentran los documentos de gutenberg, se debe cambiar esta linea por
la ruta donde se encuentran los documentos txt, en este caso la ruta apunta al cluster HDFS.

#### Ejecutar script mllib_cosine_similarity.py
Nota: Se debe ejecutar este script en un ambiente con Spark dentro de un ecosistema Hadoop. Como se aclara en esta guía
no se ha probado con la versión standalone de Spark pero debería funcionar similar al ejecutar el script con PySpark.

1. Abrir una consola o terminal e ingresar el siguiente comando:
/bin/spark-submit mllib_cosine_similarity.py

2. Revisar en MongoDB la colección que se configuró para escribir donde debieron quedar almacenados los resultados. Debe haber un número
de registros igual a la cantidad de documentos analizados ya que lo que se guarda es un registro para cada documento
con la similitud que tiene con los demás.

### Contacto ###

Dider Gonzalez - dgleo138@gmail.com

Camilo Torres - camilo.torres.botero@gmail.com