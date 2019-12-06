from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import sqlite3
import pymysql


# def retornaTweets():
#
#     conn = sqlite3.connect('bases/tweets.sqlite')
#     cursor = conn.cursor()
#
#     # lendo os dados
#     cursor.execute("""SELECT text, sentiment FROM Tweet;""")
#
#     lista = []
#     for linha in cursor.fetchall():
#         lista.append(linha)
#
#     return lista


def retornaTweetsNovo():

    db = pymysql.connect(host="localhost", user="root", password="root", db="twitter")
    cursor = db.cursor()

    cursor.execute("SELECT id, tweet_text, sentiment FROM NoThemeTweets")

    return cursor.fetchall()


def tratarTweets(listaTweets, stopwords=stopwords):
    listaNova = []
    stopwords = set(stopwords.words('portuguese'))

    for tweet in listaTweets:
        sentimento = 1 if tweet[2] == "Positivo" else 0

        palavras = word_tokenize(tweet[1].lower())
        palavras = [palavra for palavra in palavras if palavra.isalpha()]

        palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stopwords or palavra == 'não']

        listaNova.append((' '.join(palavras_sem_stopwords), sentimento))

    return listaNova


def retornarTweetsTratados():
    return tratarTweets(retornaTweetsNovo())


# fazer a filtragem de tweets com termos específicos
# def definir_termos_especificos(listaTweets=tratarTweets(retornaTweets())):
#     lista_nova = []
#     lista_termos = []
#
#     i = 's'
#     while i != 'n':
#         termo = input("Adicionar termo para verificação: ")
#         lista_termos.append(termo)
#         i = input("Quer adicionar outro termo? (s/n) ")
#
#     for tweet in listaTweets:
#         palavras = word_tokenize(tweet[0].lower())
#         palavras = [palavra for palavra in palavras if palavra in lista_termos]
#
#         if len(palavras) > 0:
#             lista_nova.append((' '.join(palavras), tweet[1]))
#
#     return lista_nova
