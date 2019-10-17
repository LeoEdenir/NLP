# NLP

Tive problemas com o Git e não consegui subir a pasta da virtualEnv, então para rodar o projeto é preciso iniciar um projeto python com o PyCharm e colocar os aquivos dentro para instalar as dependências manualmente. 

Para testar o algorítimo com o banco de dados do Egressos como está no *index.py*, é preciso adicionar o banco de dados ao MySql, o mesmo está na pasta "bases" e só precisa ser importado para o servidor local da máquina.
Para testar o algorítimo com uma frase qualquer, basta escrevê-la como último parâmetro na função *analisar_frase* quando chamada na função *exibir_resultado*. Ex: exibir_resultado(analisar_frase(classificador, vetorizador, "estou triste")).
