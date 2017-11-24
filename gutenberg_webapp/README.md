# Gutenberg subset - terms search and similar documents #


### ¿Para que es este repositorio? ###

Este repositorio contiene la aplicación web que sera usada en el proyecto como interfaz para el ingreso de datos de consulta y visualizacion de resultados.

#### Resumen
Esta aplicación web es desarrollada haciendo uso de NodeJs en el servidor, javascript, html5 y bootstrap en el frontend y hace uso de
una base de datos MongoDB por defecto.

La aplicación consta de una pagina inicial con un campo de busqueda. Para las palabras ingresadas en este campo, se devolveran los documentos del subconjunto de Gutenberg en los que 
se encuentran. La presentación de los resultados se dividira en dos partes: 

Parte 1: Documentos en los que se encuentran dos o mas de las palabras ingresadas. Estos se obtienen haciendo una busqueda con el operador logico AND entre todas las combinaciones de las palabras ingresadas.

Parte 2: Documentos en los que se encuentra al menos una de las palabras ingresadas. Estos se obtienen haciendo una busqueda con el operador logico OR entre todas las palabras ingresadas.

Los documentos presentados en los resultados, dispondran de la opción: Ver similares, al acceder a esta opción sobre un documento se presentaran los 10 documentos mas similares a este, incluyendo el valor de similaridad encontrado.

#### Versión: 2.0


### Pasos para configurar y ejecutar esta aplicación ###

#### Pre-requisitos:
1. Descargar e instalar la versión 7.10.0 (o superior) de NodJS desde el siguiente enlace: https://nodejs.org/es/download/
2. Instalar MongoDB Community Edition, siguiendo los pasos descritos en el siguiente enlace: https://docs.mongodb.com/manual/installation/
3. (Recomendado) Seguir los pasos descritos en este proyecto para ejecutar el URL(indice invertido) sobre el sub-conjunto de documentos
 y asi generar los datos que luego seran consultados por esta aplicación. En caso de no ejecutar este paso previo, la aplicación
 no devolvera ningun resultado al ingresar los terminos de busqueda.
4. (Recomendado) Seguir los pasos descritos en este proyecto para ejecutar URL(la similaridad de coseno) y asi tener disponible
en base de datos, la similaridad entre todos los documentos. En casi de no ejecutar este paso previo, la aplicación siempre devolvera
que no hay documentos similares a un documento seleccionado.

#### Preparar y ejecutar aplicación

1. Verificar que el gestor de paquetes de nodejs, llamado npm, se encuentra instalado correctamente. Para esto se abre
una consola o terminal y se ejecuta el comando npm --version , si este devuelve un numero como 4.2.0 entonces se encontrara
correctamente instalado, en caso contrario seguir los pasos descritos en el pre-requisito 1 de este documento.
2. Verificar que mongodb se encuentra instalado correctamente. Para esto se abre una consola o terminal y se ejecuta el comando 
mongod --version , si este devuelve un texto como 'db version v3.4.0' entonces se encontrara correctamente instalado, 
en caso contrario seguir los pasos descritos en el pre-requisito 2 de este documento.
3. Iniciar mongodb para hacer uso de la base de datos requerida por la aplicación, si no se inicia mongodb, la aplicación web
 presentara errores al momento de ejecutarse. Para ejecutar mongodb, se debe abrir una consola o terminal, y ejecutar el siguiente
 comando con permisos de administrador: Mac o Linux (sudo mongod), Windows (mongod.exe).
4. Descargar el contenido de este repositorio.
5. En una consola o terminal, usando el comando cd, ubicar el directorio en el que se encuentra el contenido de este repositorio.
6. Obtener los paquetes y dependencias de la aplicación: en la consola o terminal, estando ubicado sobre este directorio, 
ejecutar el comando: npm install
7. Ejecutar aplicación: en la consola o terminal, ejecutar el comando: grunt. Este comando desplegara la aplicación en el puerto 3001,
Si este puerto se encuentra ocupado, se puede cambiar el puerto sobre el que se despliega accediendo al archivo config/config.js y cambiando
el puerto 3001 por otro puerto disponible.
8. Acceder a la aplicación: abrir un navegador e ingresar la url localhost:3001 (o el puerto asignado en el archivo config.js).

#### Cambiar nombre de base de datos
Acceder al archivo config/config.js y en este se presentaran los parametros para los diferentes ambientes de despliegue. 
Uno de los parametros es llamdo db y corresponde al nombre y ubicación de la base de datos en cada ambiente, 
cambiar por el nuevo nombre si es necesario.

#### Dependencias

    "async-foreach": "^0.1.3",
    "body-parser": "^1.13.3",
    "compression": "^1.5.2",
    "cookie-parser": "^1.3.3",
    "dict": "^1.4.0",
    "ejs": "^2.3.1",
    "express": "^4.13.3",
    "glob": "^6.0.4",
    "method-override": "^2.3.0",
    "mongoose": "^4.1.2",
    "morgan": "^1.6.1",
    "serve-favicon": "^2.3.0"


### Contacto ###

Dider Gonzalez - dgleo138@gmail.com

Camilo Torres - camilo.torres.botero@gmail.com