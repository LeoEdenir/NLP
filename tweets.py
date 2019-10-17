from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import sqlite3


def retornaTweets():

    conn = sqlite3.connect('bases/tweets.sqlite')
    cursor = conn.cursor()

    # lendo os dados
    cursor.execute("""SELECT text, sentiment FROM Tweet;""")

    lista = []
    for linha in cursor.fetchall():
        lista.append(linha)

    return lista


def tratarTweets(listaTweets, stopwords=stopwords):
    listaNova = []
    stopwords = set(stopwords.words('portuguese'))

    for tweet in listaTweets:

        palavras = word_tokenize(tweet[0].lower())
        palavras = [palavra for palavra in palavras if palavra.isalpha()]

        palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stopwords]

        listaNova.append((' '.join(palavras_sem_stopwords), tweet[1]))

    return listaNova


def retornarTweetsTratados():
    return tratarTweets(retornaTweets())


# fazer a filtragem de tweets com termos específicos
def definir_termos_especificos(listaTweets=tratarTweets(retornaTweets())):
    lista_nova = []
    lista_termos = []

    i = 's'
    while i != 'n':
        termo = input("Adicionar termo para verificação: ")
        lista_termos.append(termo)
        i = input("Quer adicionar outro termo? (s/n) ")

    for tweet in listaTweets:
        palavras = word_tokenize(tweet[0].lower())
        palavras = [palavra for palavra in palavras if palavra in lista_termos]

        if len(palavras) > 0:
            lista_nova.append((' '.join(palavras), tweet[1]))

    return lista_nova
