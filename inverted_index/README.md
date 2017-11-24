# Inverted index

### �Para que es este repositorio? ###

Este repositorio contiene el archivo inverted_index.py; este archivo incluye codigo en Python que por medio de Map Reduce (MrJob) encuentra el indice invertido sobre un conjunto de documentos y lo almacena en base de datos.

#### Resumen

Se realiza un programa en Python haciendo uso de la librer�a mrjob que
permite implementar el paradigma de programaci�n Map Reduce. Con
este se halla el �ndice invertido para todos los documentos del dataset.
En este primer procesamiento se consider� adecuado realizar el calculo
del tf-idf (term frequency -inverse document frequency) con el objetivo de
usarlo en la creaci�n de los vectores de cada documento para la detecci�n
de los documentos m�s similares en un procesamiento posterior. 

#### Versi�n: 1.0


### Pasos para configurar y ejecutar esta aplicaci�n ###

#### Pre-requisitos:
1. (Importante) este script solo puede ser ejecutado con una versi�n 2.7.x de python, de lo contrario se presentaran errores en la ejecuci�n. En caso de tener una versi�n diferente de Python, a continuaci�n se presentan dos opci�nes para 
crear y administrar diferentes ambientes con diferentes versiones de Python o con diferentes paquetes instalados.  
	- La primera opci�n se encuantra en este enlace: https://conda.io/docs/user-guide/tasks/manage-environments.html  
		Nota: Para usar la guia anterior es necesario tener instalado Conda y sus dependencias, para esto se presenta la siguiente guia: https://conda.io/docs/user-guide/install/index.html  
	- La segunda opci�n, que no requiere instalar Conda, es la siguiente:  
		  instalar pyenv (https://github.com/pyenv/pyenv-installer)  
		  curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash  
		  pyenv update  
		  pyenv install 2.7.13  
		  pyenv local 2.7.13  
2. Instalar MongoDB Community Edition, siguiendo los pasos descritos en el siguiente enlace: https://docs.mongodb.com/manual/installation/
3. Iniciar mongodb para hacer uso de la base de datos requerida por el script, si no se inicia mongodb, el script presentara errores al momento de ejecutarse. Para ejecutar mongodb, se debe abrir una consola o terminal, y ejecutar el siguiente comando con permisos de administrador: Mac o Linux (sudo mongod), Windows (mongod.exe).
4. Cambiar los parametros del script para la base de datos: Se debe abrir el archivo inverted_index.py para edici�n y en este se debe buscar el comentario CONFIG. En este se encontraran dos variables correspondientes a la configuraci�n de la base de datos, estas son:
	- client: En este se define la conexi�n a la base de datos Mongodb, por defecto se asigna el valor MongoClient() el cual asume la conexion a la base de datos mongodb local (sin usuario y password definidos). Para definir una base de datos en otro servidor o con usuario y password definidos, se puede usar el siguiente valor: MongoClient('mongodb://usuario:password@ip_servidor/nombre_base_de_datos')
	- db: en esta propiedad se debe indicar el nombre de la base de datos mongodb que se usara, el valor debe definirse asi: client.nombre_base_de_datos
5. Definir el numero de documentos que se pasara como parametro al script: Se debe abrir el archivo inverted_index.py para edici�n y en este se debe buscar el comentario CONFIG. En este se encontrara la variable D y en esta se debe asignar el valor numerico correspondiente al numero de documentos que se enviaran al script.
6. Tener disponible un conjunto de documentos de texto, con extensi�n .txt, estos seran los datos de entrada que procesara el script presente en este repositorio con el fin de hallar el indice invertido a esos documentos. Se recomienda usar el dataset, con documentos de Gutenberg, disponible en este repositorio.
7. Instalar las dependencias de python descritas en el apartado Dependencias


#### Ejecutar script inverted_index.py
Nota: Si se tiene una version de python diferente a la 2.7.x, se debe seguir el paso 1 de los pre-requisitos.

Ejecutar script localmente:

1. Abrir una consola o terminal e ingresar el siguiente comando: python /ruta_al_archivo_inverted_index.py/inverted_index.py /ruta_al_dataset/*.txt

Ejecutar script en HDFS:

1. Abrir una consola o terminal e ingresar el siguiente comando: python inverted_index.py hdfs:///ruta_al_dataset_en_hdfs/*.txt



#### Dependencias
	**MrJob:** permite escribir tareas en map reduce y ejecutarlas en varias plataformas.  
	Instalaci�n usando pip: pip install mrjob  
	**Unidecode:** toma datos Unicode e intenta representarlos en caracteres ASCII  
	Instalaci�n usando pip: pip install unidecode  
	**Numpy:** es el paquete fundamental para la computaci�n cient�fica con Python.  
	Instalaci�n usando pip: pip install numpy  
	**Pymongo:** contiene herramientas para interactuar con la base de datos MongoDB desde Python  
	Instalaci�n usando pip: pip install pymongo  
	**Datetime:** Este paquete proporciona un tipo de datos DateTime  
	Instalaci�n usando pip: pip install datetime  
	**nltk:** es una plataforma l�der para construir programas de Python que trabajen con datos de lenguaje humano.  
	Instalaci�n usando pip: pip install nltk  
	**String:** Una peque�a biblioteca de utilidades para verificar y manipular Strings.
	Instalaci�n usando pip: pip install python-string-utils

### Contacto ###

Dider Gonzalez - dgleo138@gmail.com

Camilo Torres - camilo.torres.botero@gmail.com