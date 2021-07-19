import oauth2
import urllib
import pandas as pd
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class Twitter:
  def __init__(self,api_key,secret_key,token_key,token_secret):
    self._api_key = api_key
    self._secret_key = secret_key
    self._token_key = token_key
    self._token_secret = token_secret
    self.conexao()

  @property
  def api_key(self):
    return self._api_key
  @api_key.setter
  def api_key(self,key):
    self._api_key = key
    
  @property
  def secret_key(self):
    return self._secret_key
  @secret_key.setter
  def secret_key(self,key):
    self._secret_key = key

  @property
  def token_key(self):
    return self._token_key
  @token_key.setter
  def token_key(self,key):
    self._token_key = key

  @property
  def token_secret(self):
    return self._token_secret
  @token_secret.setter
  def token_secret(self,key):
    self._token_secret = key


  def conexao(self):
    try:
      self.consumer = oauth2.Consumer(self._api_key,self._secret_key)
      self.token = oauth2.Token(self._token_key,self._token_secret)
      self.cliente = oauth2.Client(self.consumer,self.token)
      return True
    except:
      print("Erro")
      return False

  def publicar_tweet(self,tweet):
    try:
      query_codificada = urllib.parse.quote(tweet)
      requisicao = self.cliente.request('https://api.twitter.com/1.1/statuses/update.json?status='+query_codificada,method='POST')
      decodificar = requisicao[1].decode()
      objeto = json.loads(decodificar)
      print('Tweet publicado!')
      return True
    except:
      print("Erro")
      return False

  def pesquisar_tweets(self,palavra,qnt=500,salvar=0,namefile='result.csv'):
    try:
      query_codificada = urllib.parse.quote(palavra)
      result = dict()
      result['usuario'] = []
      result['tweet'] = []
      result['date'] = []
      result['linguagem'] = []
      result['qnt_retweet'] = []
      c = 0
      while len(result['usuario']) < qnt:
        if c==0:
          requisicao = self.cliente.request('https://api.twitter.com/1.1/search/tweets.json?q='+query_codificada+'&count=100')
          c+=1
        else:
          requisicao = self.cliente.request('https://api.twitter.com/1.1/search/tweets.json?q='+query_codificada+'&count=100'+f'&include_entities={c}')
          c+=1
        decodificar = requisicao[1].decode()
        objeto = json.loads(decodificar)
        print(objeto)
        tweets = objeto['statuses']
        for twt in tweets:
          result['usuario'].append((twt['user']['screen_name']))
          result['tweet'].append(twt['text'])
          result['date'].append(twt['created_at'])
          result['linguagem'].append(twt['lang'])
          result['qnt_retweet'].append(twt["retweet_count"])
      
      df_result = pd.DataFrame(result).iloc[:qnt]
      if salvar==1:
        df_result.to_csv(namefile)
      return df_result
    except:
      print('Erro')

  def nuvem_de_palavras(self,tweets,nameimg='wordcloud.png'):
    wordcloud = WordCloud(
    width = 750,
    height = 500,
    background_color = 'white').generate(str(tweets))
    fig = plt.figure(
    figsize = (40, 30),
    facecolor = 'k',
    edgecolor = 'k')
    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(nameimg,format='png')
    plt.show()
