import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB, MultinomialNB, ComplementNB
from tweets import retornarTweetsTratados
from bancoEgressos import retornaPostEgressosLimpo
from sklearn.metrics import accuracy_score

# imports para cross_val_predict
# from sklearn.model_selection import cross_val_predict
# from sklearn.model_selection import KFold
# from sklearn import metrics

import json


def dividir_dados_para_treino_e_validacao():
    dados = retornarTweetsTratados()
    quantidade_total = len(dados)
    percentual_para_treino = 0.75
    treino = []
    validacao = []
    random.shuffle(dados)

    for indice, post in enumerate(dados):
        if post[1] == 1:
            if indice < quantidade_total * percentual_para_treino:
                treino.append(dados[indice])
            else:
                validacao.append(dados[indice])

        else:
            if indice < quantidade_total * percentual_para_treino:
                treino.append(dados[indice])
            else:
                validacao.append(dados[indice])

    return treino, validacao


def realizar_treinamento(registros_de_treino, vetorizador):
    treino_comentarios = [registro_treino[0] for registro_treino in registros_de_treino]
    treino_respostas = [registro_treino[1] for registro_treino in registros_de_treino]

    treino_comentarios = vetorizador.fit_transform(treino_comentarios)

    # modelo = BernoulliNB()
    # modelo = MultinomialNB()
    modelo = ComplementNB()
    modelo.fit(treino_comentarios, treino_respostas)

    # VALIDAÇÃO COM CROSS VALIDATION
    # cv = KFold(n_splits=200)
    # resultado = cross_val_predict(modelo, treino_comentarios, treino_respostas, cv=cv)
    # total = len(resultado)
    # acc = 0
    #
    # score = accuracy_score(treino_respostas, resultado)
    # print(score * 100)
    #
    # for i in range(0, total):
    #     if resultado[i] == treino_respostas[i]:
    #         acc += 1
    #
    # print(acc, total, acc/total * 100)
    #
    # print(metrics.classification_report(treino_respostas, resultado, [0, 1]))
    #
    # exit()

    return modelo


def analisar_frase(classificador, vetorizador, frase):
    return frase, classificador.predict(vetorizador.transform([frase]))


def exibir_resultado(valor):
    frase, resultado = valor
    resultado = "Positivo" if resultado[0] == 1 else "Negativo"
    print(frase + ': ' + resultado)


def exportar_json(valor):
    frase, resultado = valor
    resultado = "Positivo" if resultado[0] == 1 else "Negativo"
    return frase, resultado


registros_de_treino, registros_para_avaliacao = dividir_dados_para_treino_e_validacao()
vetorizador = CountVectorizer(binary='true', ngram_range=(1, 2))
classificador = realizar_treinamento(registros_de_treino, vetorizador)


# para exibir o resultado da avaliação no terminal
# exibir_resultado(analisar_frase(classificador, vetorizador, "Estou triste"))


# para exportar o resultado para Json
f = open('behavior-front-master/src/tweets.json', 'w', encoding='utf-8')
lista_json = {}
for post in retornaPostEgressosLimpo():
    frase, resultado = exportar_json(analisar_frase(classificador, vetorizador, post[0]))
    # exibir_resultado(analisar_frase(classificador, vetorizador, "teste2"))
    lista_json[frase] = resultado

json = json.dumps(lista_json)
f.write(json)


# avaliação de aplicação
def realizar_avaliacao_simples(registros_para_avaliacao):
    avaliacao_comentarios = [registro_avaliacao[0] for registro_avaliacao in registros_para_avaliacao]
    avaliacao_respostas   = [registro_avaliacao[1] for registro_avaliacao in registros_para_avaliacao]

    total = len(avaliacao_comentarios)
    resultados = []

    for indice in range(0, total):
        resultado_analise = analisar_frase(classificador, vetorizador, avaliacao_comentarios[indice])
        frase, resultado = resultado_analise
        resultados.append(resultado)

    # print(metrics.classification_report(avaliacao_respostas, resultados, [0, 1]))
    return round(accuracy_score(avaliacao_respostas, resultados) * 100, 2)


def realizar_avaliacao_completa(registros_para_avaliacao):
    avaliacao_comentarios = [registro_avaliacao[0] for registro_avaliacao in registros_para_avaliacao]
    avaliacao_respostas   = [registro_avaliacao[1] for registro_avaliacao in registros_para_avaliacao]

    total = len(avaliacao_comentarios)
    verdadeiros_positivos = 0
    verdadeiros_negativos = 0
    falsos_positivos = 0
    falsos_negativos = 0

    for indice in range(0, total):
        resultado_analise = analisar_frase(classificador, vetorizador, avaliacao_comentarios[indice])
        frase, resultado = resultado_analise
        if resultado[0] == 0:
            verdadeiros_negativos += 1 if avaliacao_respostas[indice] == 0 else 0
            falsos_negativos += 1 if avaliacao_respostas[indice] != 0 else 0
        else:
            verdadeiros_positivos += 1 if avaliacao_respostas[indice] == 1 else 0
            falsos_positivos += 1 if avaliacao_respostas[indice] != 1 else 0

    return (round(verdadeiros_positivos * 100 / total, 2),
            round(verdadeiros_negativos * 100 / total, 2),
            round(falsos_positivos * 100 / total, 2),
            round(falsos_negativos * 100 / total, 2)
            )


percentual_acerto = realizar_avaliacao_simples(registros_para_avaliacao)
informacoes_analise = realizar_avaliacao_completa(registros_para_avaliacao)
verdadeiros_positivos,verdadeiros_negativos,falsos_positivos,falsos_negativos = informacoes_analise

print("\nO modelo teve uma taxa de acerto de", percentual_acerto, "%")

print("Onde", verdadeiros_positivos, "% são verdadeiros positivos")
print("e", verdadeiros_negativos, "% são verdadeiros negativos")

print("e", falsos_positivos, "% são falsos positivos")
print("e", falsos_negativos, "% são falsos negativos")
