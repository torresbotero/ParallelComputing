from mrjob.job import MRJob
from mrjob.step import MRStep
import os
import unidecode
import sys
import numpy as np
from pymongo import MongoClient
from datetime import datetime
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# CONFIG
# ---------------------------------------------------------------------------------------------
# Conexión a la base de datos Mongodb
#client = MongoClient()
client = MongoClient('mongodb://<user>:<pass>@<host>/<bd_name>')

# nombre de la base de datos mongodb
db = client.bd_name

# Total de documentos (corriendo desde python local)
D = 461
# ---------------------------------------------------------------------------------------------


# Limpieza de Stop Words
englishStopWords = [u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u'your',
                    u'yours', u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', u'her',
                    u'hers', u'herself', u'it', u'its', u'itself', u'they', u'them', u'their', u'theirs',
                    u'themselves', u'what', u'which', u'who', u'whom', u'this', u'that', u'these', u'those',
                    u'am', u'is', u'are', u'was', u'were', u'be', u'been', u'being', u'have', u'has', u'had',
                    u'having', u'do', u'does', u'did', u'doing', u'a', u'an', u'the', u'and', u'but', u'if',
                    u'or', u'because', u'as', u'until', u'while', u'of', u'at', u'by', u'for', u'with',
                    u'about', u'against', u'between', u'into', u'through',
                    u'during', u'before', u'after', u'above', u'below', u'to', u'from', u'up', u'down', u'in',
                    u'out', u'on', u'off', u'over', u'under', u'again', u'further', u'then', u'once', u'here',
                    u'there', u'when', u'where', u'why', u'how', u'all', u'any', u'both', u'each', u'few',
                    u'more', u'most', u'other', u'some', u'such', u'no', u'nor', u'not', u'only', u'own',
                    u'same', u'so', u'than', u'too', u'very', u's', u't', u'can', u'will', u'just', u'don',
                    u'should', u'now', u'd', u'll', u'm', u'o', u're', u've', u'y', u'ain', u'aren', u'couldn',
                    u'didn', u'doesn', u'hadn', u'hasn', u'haven', u'isn', u'ma', u'mightn', u'mustn', u'needn',
                    u'shan', u'shouldn', u'wasn', u'weren', u'won', u'wouldn']
spanishStopWords = [u'de', u'la', u'que', u'el', u'en', u'y', u'a', u'los', u'del', u'se', u'las', u'por',
                    u'un', u'para', u'con', u'no', u'una', u'su', u'al', u'lo', u'como', u'mas', u'pero',
                    u'sus', u'le', u'ya', u'o', u'este', u'si', u'porque', u'esta', u'entre', u'cuando', u'muy',
                    u'sin', u'sobre', u'tambien', u'me', u'hasta', u'hay', u'donde', u'quien', u'desde',
                    u'todo', u'nos', u'durante', u'todos', u'uno', u'les', u'ni', u'contra', u'otros', u'ese',
                    u'eso', u'ante', u'ellos', u'e', u'esto', u'mi', u'antes', u'algunos', u'que', u'unos',
                    u'yo', u'otro', u'otras', u'otra', u'el', u'tanto', u'esa', u'estos', u'mucho', u'quienes',
                    u'nada', u'muchos', u'cual', u'poco', u'ella', u'estar', u'estas', u'algunas', u'algo',
                    u'nosotros', u'mi', u'mis', u'tu', u'te', u'ti', u'tu', u'tus', u'ellas', u'nosotras',
                    u'vosostros', u'vosostras', u'os', u'mio', u'mia', u'mios', u'mias', u'tuyo', u'tuya',
                    u'tuyos', u'tuyas', u'suyo', u'suya', u'suyos', u'suyas', u'nuestro', u'nuestra',
                    u'nuestros', u'nuestras', u'vuestro', u'vuestra', u'vuestros', u'vuestras', u'esos',
                    u'esas', u'estoy', u'estas', u'esta', u'estamos', u'estais', u'estan', u'este', u'estes',
                    u'estemos', u'esteis', u'esten', u'estare', u'estaras', u'estara', u'estaremos',
                    u'estareis', u'estaran', u'estaria', u'estarias', u'estariamos', u'estariais', u'estarian',
                    u'estaba', u'estabas', u'estabamos', u'estabais', u'estaban', u'estuve', u'estuviste',
                    u'estuvo', u'estuvimos', u'estuvisteis', u'estuvieron', u'estuviera', u'estuvieras',
                    u'estuvieramos', u'estuvierais', u'estuvieran', u'estuviese', u'estuvieses',
                    u'estuviesemos', u'estuvieseis', u'estuviesen', u'estando', u'estado', u'estada',
                    u'estados', u'estadas',
                    u'estad', u'he', u'has', u'ha', u'hemos', u'habeis', u'han', u'haya', u'hayas', u'hayamos',
                    u'hayais', u'hayan', u'habre', u'habras', u'habra', u'habremos', u'habreis', u'habran',
                    u'habria', u'habrias', u'habriamos', u'habriais', u'habrian', u'habia', u'habias',
                    u'habiamos', u'habiais', u'habian', u'hube', u'hubiste', u'hubo', u'hubimos', u'hubisteis',
                    u'hubieron', u'hubiera', u'hubieras', u'hubieramos', u'hubierais', u'hubieran', u'hubiese',
                    u'hubieses', u'hubiesemos', u'hubieseis', u'hubiesen', u'habiendo', u'habido', u'habida',
                    u'habidos', u'habidas', u'soy', u'eres', u'es', u'somos', u'sois', u'son', u'sea', u'seas',
                    u'seamos', u'seais', u'sean', u'sere', u'seras', u'sera', u'seremos', u'sereis', u'seran',
                    u'seria', u'serias', u'seriamos', u'seriais', u'serian', u'era', u'eras', u'eramos',
                    u'erais', u'eran', u'fui', u'fuiste', u'fue', u'fuimos', u'fuisteis', u'fueron', u'fuera',
                    u'fueras', u'fueramos', u'fuerais', u'fueran', u'fuese', u'fueses', u'fuesemos', u'fueseis',
                    u'fuesen', u'sintiendo', u'sentido', u'sentida', u'sentidos', u'sentidas', u'siente',
                    u'sentid', u'tengo', u'tienes', u'tiene', u'tenemos', u'teneis', u'tienen', u'tenga',
                    u'tengas', u'tengamos', u'tengais', u'tengan', u'tendre', u'tendras', u'tendra',
                    u'tendremos', u'tendreis', u'tendran', u'tendria', u'tendrias', u'tendriamos', u'tendriais',
                    u'tendrian', u'tenia', u'tenias', u'teniamos', u'teniais', u'tenian', u'tuve', u'tuviste',
                    u'tuvo', u'tuvimos', u'tuvisteis', u'tuvieron', u'tuviera', u'tuvieras', u'tuvieramos',
                    u'tuvierais', u'tuvieran', u'tuviese', u'tuvieses', u'tuviesemos', u'tuvieseis',
                    u'tuviesen', u'teniendo', u'tenido', u'tenida', u'tenidos', u'tenidas', u'tened']




class MRInvertedIndexWF(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_words_and_docs,
                   reducer=self.reducer_store_frequencies),
            MRStep(reducer=self.reducer_get_max_tf_per_doc),
            MRStep(reducer=self.reducer_store_tf_idf)
        ]

    def mapper_get_words_and_docs(self, _, line):

        words_in_line = line.decode('iso-8859-1', 'ignore').split()

        for word in words_in_line:

            # Limpieza de datos
            # ---------------------------------------------------------------------------------

            # convertir las palabras a lowercase
            word_to_add = word.lower()

            # Retirar caracteres especiales y acentuaciones en las palabras.
            unaccented_string = unidecode.unidecode(word_to_add)
            finalWord = ''.join(e for e in unaccented_string if e.isalnum())

            # Filtrar las Stop Words tanto en Ingles como en Espanol.
            if (finalWord not in spanishStopWords) and (finalWord not in englishStopWords):
                # Se toma de la ruta del documento, solo el nombre del documento.
                docName = os.environ['mapreduce_map_input_file'].rsplit('/', 1)
                yield finalWord, docName[1]
            # ---------------------------------------------------------------------------------
            
    def reducer_store_frequencies(self, key, values):

        # Obtener el listado de documentos en los que se encuentra la palabra (key)
        docs = list(values)
        # Crear un diccionario vacio para ir almacenando cada documento y la frecuencia de la palabra (key)
        docs_aux = {}
        # Recorrer el listado de documentos
        for doc in docs:
            # Si el documento se encuentra en el diccionario docs_aux, incrementar en uno el valor de este en el diccionario
            if doc in docs_aux:
                docs_aux[doc] += 1
            else:
                docs_aux[doc] = 1
        # Recorrer el diccionario docs_aux formado anteriormente, en cada iteracion se obtiene el nombre del documento y
        # la frecuencia de la palabra (key) en ese documento
        # Hallar el idf para la palabra 
        idf = np.log(D / 1 + len(docs_aux.keys()))
        for doc_n, tf in docs_aux.iteritems():
            # Enviar el nombre del documento recorrido y una tupla que contiene la frecuencia de la palabra que luego sera
            # usada para normalizar el term frequency, un objeto con informacion para enviar a base de datos. 
            # Este objeto contiene: la palabra, el nombre del documento, la frecuencia de la palabra en el documento y 
            # el idf (inverse document frequency) de la palabra.
            yield doc_n, (tf, {'term': key, 'doc_name': doc_n, 'frequency': tf, 'idf': idf})

    def reducer_get_max_tf_per_doc(self, doc_name, doc_word_data):
        # Para cada documento obtener un listado con todas las tuplas genereadas en el reducer anterior para ese documento.
        doc_word_data_list = list(doc_word_data)
        # con el listado de tuplas se hallar el maximo valor de la frecuencia, entre todas las palabras del documento.
        max_tf = max(doc_word_data_list)[0]
        # Crear un array para almacenar la informacion de las palabras de cada documento que posteriormente sera almacenada
        # en base de datos
        docs_array_to_store = []
        # Recorrer cada tupla de la lista doc_word_data_list
        for doc in doc_word_data_list:
            # Obtener la frecuencia del cada palabra en el documento y se normaliza dividiendola por la maxima frecuencia 
            # de todo el documento.
            tfn = doc[0] / float(max_tf)
            # Almacenar el valor de tfn en el objeto recorrido
            doc[1]['tfn'] = tfn
            # Hallar el valor de tf_idf (term frequency - inverse document frequency), haciendo uso de tfn y el idf almacenado
            # anteriormente en el objeto recorrido.
            tf_idf = tfn * doc[1]['idf']
            # Almacenar el valor de tf_idf en el objeto recorrido
            doc[1]['tf_idf'] = tf_idf
            # Almacenar en el array docs_array_to_store la informacion relevante a ser guardada para la palabra 
            # recorrida dentro del documento. Se almacena: la palabra,la frecuencia en el documento y el tf_idf.
            docs_array_to_store.append({'term': doc[1]['term'], 'frequency': doc[1]['frequency'], 'tf_idf': doc[1]['tf_idf']})
            # Se envia la palabra recorrida y toda la informacion almacenada para la palabra {'term','doc_name','frequency','idf','tfn','tf_idf'}
            yield doc[1]['term'], doc[1]
        # Almacenar el documento doc_name y la informacion asignada a docs_array_to_store, en la coleccion docsIndex de mongodb
        # Validar si el documento ya existe en base de datos
        key_validate = db.docsIndex.find({"_id": doc_name})
        # Si el documento no existe en base de datos
        if key_validate.count() == 0:
            # Insertar la informacion en la coleccion
            db.docsIndex.insert({"_id": doc_name, "words": docs_array_to_store}, check_keys=False)
        # Si el documento ya existe en base de datos
        else:
            # Actualizar la informacion del registro encontrado, agregando las nuevas palabras encontradas
            db.docsIndex.update_one({"_id": doc_name}, {"$push": {"words": {"$each": docs_array_to_store}}})

    def reducer_store_tf_idf(self, term, doc_word_data):
        # Obtener el listado de objetos con la informacion de los documentos en los que se encuentra la palabra (term)
        doc_word_data_list = list(doc_word_data)
        # Crear array para almacenar el listado de documentos de la palabra (term) y toda la informacion que se almacenara
        # en base de datos.
        words_array_to_store = []
        # Recorrer el listado de documentos en los que se encuentra la palabra (term)
        for doc in doc_word_data_list:
            # Almacenar cada documento en el array words_array_to_store con la siguiente informacion:
            # {'nombre del documento', 'frecuencia de la palabra en el documento', 'tf_idf', 'tfn', 'idf'}
            words_array_to_store.append({'doc_name': doc['doc_name'], 'frequency': doc['frequency'], 'tf_idf': doc['tf_idf'], 'tfn': doc['tfn'], 'idf': doc['idf']})
        # Almacenar la palabra (term) y la informacion asignada a words_array_to_store, en la coleccion invertedIndex de mongodb
        # Validar si la palabra ya existe en base de datos
        key_validate = db.invertedIndex.find({"_id": term})
        # Si la palabra no existe en base de datos
        if key_validate.count() == 0:
            # Insertar la informacion en la coleccion
            db.invertedIndex.insert({"_id": term, "docs": words_array_to_store}, check_keys=False)
        # Si la palabra ya existe en base de datos
        else:
            # Actualizar la informacion del registro encontrado, agregando los nuevos documentos encontrados
            db.invertedIndex.update_one({"_id": term}, {"$push": {"docs": {"$each": words_array_to_store}}})


if __name__ == '__main__':
    MRInvertedIndexWF.run()
