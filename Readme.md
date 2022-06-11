# Proyecto 2 - BD2 - Recuperacion de Documentos de Texto

## Integrantes 

* Cristhoper Heredia Lapa Michel
* Luis Ponce Contreras Eduardo

## Introduccion

Este proyecto consiste en aplicar algoritmos de busqueda y recuperacion de la informacion basada en el contenido.Para esto se construye un Indice Invertido para tareas de busqueda y recuperacion en documentos de texto, usando el modelo de recuperacion por ranking para consultas de texto libre.Los datos utilizados como contenido son un conjunto de tweets en formato json almacenados en memoria secundaria.

##### NOTA: El video se encuentra al final del documento

## Indice Invertido

### Preprocesamiento 

#### Filtrado de stopwords

Uso de NTLK.

```
stoplist = stopwords.words("spanish")
stoplist += ['?','aqui','.',',','»','«','â','ã','>','<','(',')','º','u']
```

#### Stemming

```
stemmer = SnowballStemmer('spanish')
```

Uso:

```
        if(word_lower not in stoplist): 
          token = stemmer.stem(word_lower)
```



#### Tokenizacion

Se hace uso de estas funciones para filtrar los terminos dentro de cada tweet.

```
def break_emojis(self,emoji):
    return emoji.encode('ascii', 'ignore').decode('ascii')

  def break_url(self, text):
    t = text.find('https://t.co/')
    if t != -1:
      text = re.sub('https://t.co/\w{10}', '', text)
      #print(text)
    return text


  def break_special_character(self, text):
    characters = ('\"','\'','º','&','¿','?','¡','!',' “','…','👏',
								'-','—','‘','•','›','‼','€','£','↑','→','↓','↔',
								'↘','↪','√','∧','⊃','⌒','⌛','⏬','⏯','⏰','⏹',':',
                '@','³','.','Â',',', ';', ':', '%', '#', '¿', '?', 
                '_', '~', '-', '`', 'jaja', 'jaj', 'ajaj', 'aa', 'ss',
                'jjj', 'jj', 'gg', 'rrr', 'www', 'zz', '@', '$', '(',
                ')', '&', '^', '=', '+', '{', '}', '.','[', ']', '*',
                '¡', '!', '/', '\\', '\'', '\"', '<', '>', '|', '…',
                '“', '“', '👏', '🤣', '🚨', '🙋', '🤔', '🙌', '🇵', '🇪',
                '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                'â', '±', '©'
                )
```

El filtro se realiza desde el texto total y tambien por cada termino:

```
  def parse(self, query):
    new_query=self.break_url(query)
    new_query=self.break_special_character(new_query)

    finalquery = []
    texto_tokens=nltk.word_tokenize(new_query)

    for i in texto_tokens:
      a,b = 'áéíóúüñÃ','aeiouuna'
      trans = str.maketrans(a,b)
      i = i.translate(trans)
      filter2=len(self.break_emojis(i))

      if(filter2>1):
        word_lower=i.lower()
        if(word_lower not in stoplist): 
          token = stemmer.stem(word_lower)
          #print(token)
          finalquery.append(token)

    return finalquery

```

### Construccion del Indice invertido

Primero se realiza una lectura por cada archivo con formato "JSON" en la cual diferenciamos los tweets de los retweets

```
  def readfile(self, filename):
    lista_tweets=[]
    f = open(filename, "r", encoding='latin-1')
    values = json.loads(f.read())
    it = 0
    for i in values:
      tweet = {}
      tweet["file"] = filename
      tweet["id"] = it 
      if i.get("RT_text"):
        tweet["text"] = self.parse(i["RT_text"])
      else:
        tweet["text"] = self.parse(i["text"])    
      lista_tweets.append(tweet)
      it += 1

    f.close()
    return lista_tweets
```

Almacenando todo en una lista de tweets con esta estructura por cada tweet:

```
tweet = {
	'file':'tweets_2018-08-07.json',
	'id':1660,
	'text':['recuerdosperu', 'luis', 'castaaed', 'pard', 'mentir', 'pretend', 'alcald', 'lim', 'pued', 'esper', 'padr', 'corrupt']
}
```

 Por ultimo creamos el indice invertido usando las siguientes condiciones:

* La estructura almacenara un indice de terminos en la cual dentro de cada termino se encuentran los nombres de los archivos de formato "JSON" almacenados en memoria secundaria.
* Ademas de almacenar los nombres de los archivos dentro del termino tambien se almacenan los DF de cada termino.
* Dentro de cada nombre de archivo se almacenara el "ID" del tweet.
* Dentro de cada "ID" de tweet se almacenara el "TF" equivalente al texto de ese tweet.

```
  def construct_indice(self):
    for i in self.lista_de_files:
      self.lista_de_tweets.append(self.readfile(i))

    for j in self.lista_de_tweets:
      for i in j:
        self.N_total+=1
        texto=i.get("text")
        #cont_tf=1
        file_indi=i.get("file")
        for term in texto:
          # df y tf
        
          if(len(self.Indice) > 0):
            if term not in self.Indice:
              self.Indice[term]={"df":1}
              self.Indice[term][file_indi]={}            
              self.Indice[term][file_indi][i.get("id")]={"tf":1}
            else:
              lista_files_del_term=[]
              lista_files_del_term=self.Indice[term].keys()
              if (file_indi not in lista_files_del_term):
                new_df=int(self.Indice.get(term).get('df'))+1
                self.Indice[term][file_indi]={}            
                self.Indice[term][file_indi][i.get("id")]={"tf":1}
                self.Indice[term]["df"]=new_df
              else:
                lista_ids_del_term=self.Indice[term][file_indi].keys()
                if(i.get("id") not in lista_ids_del_term):
                  new_df=int(self.Indice.get(term).get("df"))+1              
                  self.Indice[term][file_indi][i.get("id")]={"tf":1}
                  self.Indice[term]["df"]=new_df
                else:
                new_tf=int(self.Indice.get(term).get(file_indi).get(i.get("id")).get("tf"))+1
                  self.Indice[term][file_indi][i.get("id")]={"tf":new_tf}                  
          else:
            self.Indice[term]={"df":1}
            self.Indice[term][file_indi]={}
            self.Indice[term][file_indi][i.get("id")]={"tf":1}

```

La estructura del indice seria de esta manera:

```
"impresent": {
    "df": 4,
    "tweets_2018-08-07.json": {
      "1571": {
        "tf": 1
      },
      "1579": {
        "tf": 1
      },
      "1591": {
        "tf": 1
      },
      "1625": {
        "tf": 1
      }
   	}
  }
```



## Query

Creamos un indice en base a los terminos que podemos encontrar en el texto de la consulta

```
  def query(self,texto):
    Indice_query = {}
    new_texto = self.parse(texto)
    #print(new_texto)
    # Creando indice para la query 
    for term in new_texto:
      if(len(Indice_query) > 0):
        if(term not in Indice_query.keys()):
          Indice_query[term]={"df":1}        
          Indice_query[term]["query"]={"tf":1}
        else:
          new_tf=Indice_query[term]["query"].get("tf")+1
          Indice_query[term]["query"]={"tf":new_tf}
      else:
        Indice_query[term]={"df":1}        
        Indice_query[term]["query"]={"tf":1}
```

Se toma una lista de todos los documentos a los que pertenecen los terminos, se obtienen los score de cada termino por cada documento y se realiza la normalizacion

```
    for d in documentos:
      ids=Indice_docs.get(d).keys()
      for id in ids:
        values_TF_IDF_1=[]
        values_TF_IDF_2=[]
        for term in terminos_comunes1:

          # CALCULANDO TF-IDF DE CADA UNO
          if (term not in Indice_docs.get(d).get(id).keys()):
            values_TF_IDF_1.append(0)
          else:
            tf=(1 + math.log(Indice_docs.get(d).get(id).get(term),10))
            idf=((1 + math.log((self.N_total/self.Indice.get(term).get("df")),10)))
            values_TF_IDF_1.append(tf*idf)
            #print("a")
          values_TF_IDF_2.append(d1.get(term).get("query").get("tf"))
```

  ## Pruebas de Uso y Presentacion

![link](https://drive.google.com/file/d/1SeBRB0PNK-kOHta6ToTz9SqzG0BLIUvI/view?usp=sharing)




























