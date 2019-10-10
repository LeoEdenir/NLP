from nltk.tokenize import word_tokenize
import pymysql
import re


def retornaBanco():
    db = pymysql.connect(host="localhost", user="root", password="root", db="egressos_teste")
    cursor = db.cursor()

    cursor.execute("SELECT titulo, descricao, id_post FROM post")

    return cursor.fetchall()


def retornaPostLimpo(postagens=retornaBanco()):
    lista_postagens = []

    for post in postagens:
        titulo = post[0].lower()
        descricao = post[1].lower()
        id_post = post[2]

        # tira tags html
        descricao = re.sub(r'<[^>]+>', '', descricao)
        descricao = re.sub(r'nbsp', '', descricao)

        #limpa palavras
        palavras = word_tokenize(titulo + ' ' + descricao)
        palavras = [palavra for palavra in palavras if palavra.isalpha()]

        # junta palavras e adiciona na lista
        lista_postagens.append((' '.join(palavras), id_post))

    return lista_postagens
