from cmath import log
#from bs4 import BeautifulSoup
from select import select
from tracemalloc import stop
from typing import final
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re, string
import os
import sys
from os.path import join
import json
import math

#nltk.download('punkt')
#nltk.download('stopwords')
stoplist = stopwords.words("spanish")
stoplist += ['?','aqui','.',',','»','«','â','ã','>','<','(',')','º','u']
stemmer = SnowballStemmer('spanish')



class Indice_invertido:
  N_total=0
  Indice={}
  lista_de_files=[
    "./Data/data_elecciones/tweets_2018-08-07.json",
    #"tweets_2018-08-08.json",
    #"tweets_2018-08-09.json",
    #"tweets_2018-08-10.json",
    #"tweets_2018-08-11.json"
  ]
  """
  lista_de_files=[
    "tweets_2018-08-07.json",
    "tweets_2018-08-08.json",
    "tweets_2018-08-09.json",
    "tweets_2018-08-10.json",
    "tweets_2018-08-11.json",
    "tweets_2018-08-12.json",
    "tweets_2018-08-13.json",
    "tweets_2018-08-14.json",
    "tweets_2018-08-15.json",
    "tweets_2018-08-16.json",
    "tweets_2018-08-17.json",
    "tweets_2018-08-18.json",
    "tweets_2018-08-19.json",
    "tweets_2018-08-20.json",
    "tweets_2018-08-21.json",
    "tweets_2018-08-22.json",
    "tweets_2018-08-23.json",
    "tweets_2018-08-24.json",
    "tweets_2018-08-25.json",
    "tweets_2018-08-26.json",
    "tweets_2018-08-27.json",
    "tweets_2018-08-28.json",
    "tweets_2018-08-29.json",
    "tweets_2018-08-30.json",
    "tweets_2018-08-31.json",
    "tweets_2018-09-02.json",
    "tweets_2018-09-03.json",
    "tweets_2018-09-04.json",
    "tweets_2018-09-05.json",
    "tweets_2018-09-06.json",
    "tweets_2018-09-07.json",
    "tweets_2018-09-08.json",
    "tweets_2018-09-09.json",
    "tweets_2018-09-10.json",
    "tweets_2018-09-11.json",
    "tweets_2018-09-12.json",
    "tweets_2018-09-13.json",
    "tweets_2018-09-14.json",
    "tweets_2018-09-15.json",
    "tweets_2018-09-16.json",
    "tweets_2018-09-17.json",
    "tweets_2018-09-18.json",
    "tweets_2018-09-19.json",
    "tweets_2018-09-20.json",
    "tweets_2018-09-21.json",
    "tweets_2018-09-22.json",
    "tweets_2018-09-23.json",
    "tweets_2018-09-24.json",
    "tweets_2018-09-25.json",
    "tweets_2018-09-26.json",
    "tweets_2018-09-27.json",
    "tweets_2018-09-28.json",
    "tweets_2018-09-29.json",
    "tweets_2018-09-30.json",
    "tweets_2018-10-01.json",
    "tweets_2018-10-02.json",
    "tweets_2018-10-03.json",
    "tweets_2018-10-04.json",
    "tweets_2018-10-05.json"
  ]
  """

  lista_de_tweets=[]


  def __init__(self):
    #print("Leyendo todos los tweets")
    tweets = []

  
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

    for char in characters:
      text = text.replace(char, "")
    return text

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
    #print(lista_tweets)  
    f.close()
    return lista_tweets

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

      #print(self.N_total)
      with open('indice_invertido.json', 'w',encoding='utf-8') as outfile:
        json.dump(self.Indice, outfile,ensure_ascii=False)
      #for i in self.Indice:
      #  print(i," -> ",self.Indice.get(i))
 
  def read_indice(self):
    json_file = open("indice_invertido.json").read()
    first_dict={}
    first_dict = json.loads(json_file)
    #print(first_dict)
    #salidaf = {}
    #salida = json.dumps(data,ensure_ascii=True).encode('utf-8')
    #return json_file

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

    return Indice_query


  def compare_total(self,d1):
    Indice_docs = {}
    lista_cosenos = {}

    terminos_comunes1=d1.keys()
    for f in terminos_comunes1:
      if(f in self.Indice):
        documents=self.Indice.get(f).keys()
        #print(documents)
        for d in documents:
          if(d!="df"):
            if(d not in Indice_docs):
              Indice_docs[d]={}
            ids=self.Indice.get(f).get(d).keys()
            for id in ids:
              Indice_docs[d][id]={f:self.Indice.get(f).get(d).get(id).get("tf")}
              #print(id)
            #print("----")
          #for id in ids:
          #  Indice_docs[d][id]={f:self.Indice.get(f).get(d).get("tf")}
    # Comparando query con documento uno por uno
    documentos=Indice_docs.keys()
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
        #print(values_TF_IDF_1)
        #print(values_TF_IDF_2)
        dot_product=0
        normalizacion=0
        norma1=0
        norma2=0
        for value in range(len(values_TF_IDF_1)):
          mult=values_TF_IDF_1[value]*values_TF_IDF_2[value]
          dot_product=dot_product+mult
          norma1=norma1+values_TF_IDF_1[value]**2
          norma2=norma2+values_TF_IDF_2[value]**2
        normalizacion=math.sqrt(norma1*norma2)
        #print(normalizacion)
        coseno=dot_product/normalizacion
        if(coseno not in lista_cosenos):
          word_edit=str(d)+" "+str(id)
          lista_cosenos[coseno]=[]
          lista_cosenos[coseno].append(word_edit)
        else:
          word_edit=str(d)+" "+str(id)
          lista_cosenos[coseno].append(word_edit)

    sorted_cosenos = json.dumps(lista_cosenos,sort_keys=True)
    cosenos=json.loads(sorted_cosenos)
    return cosenos



reader=Indice_invertido()

#result=reader.read_indice()

#result=reader.construct_indice()
#document_query=reader.query("el pueblo es hacer luis un soplon, buena hacer prueba como tambien tu lo eres soplon y como la politica tambien es de soplones") 
#reader.compare_total(document_query)
#Indice_invertido.readfile("tweets_2018-08-07.json")
#el pueblo es hacer un soplon, buena hacer prueba como tambien tu lo eres soplon y como la politica tambien es de soplones y demas soplones del pueblo para tambien vivir de manera corrupta porque si no es asi los presidentes siguen una causa para seguir en la politica
