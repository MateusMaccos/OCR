from spacy import load  # Carrega um modelo


def buscar_texto(texto_buscado, pasta):
    nlp = load("pt_core_news_lg")

    nomepasta = pasta

    with open(f"{nomepasta}/relatorioEmTexto.txt", "r") as file:
        textoDoArquivo = file.readlines()

    # doc = nlp(textoDoArquivo)
    textoBuscado = nlp(str(texto_buscado).lower())

    palavra_chave = str(textoBuscado[0])

    valor_numerico = None

    for linha in textoDoArquivo:
        linha_processada = nlp(linha.lower().strip())
        if linha_processada.vector_norm != 0 and linha_processada.has_vector:
            similaridade = textoBuscado.similarity(linha_processada)
            if similaridade > 0.5:
                print(linha)
                doc = nlp(linha)
                for token in doc:
                    if token.text.lower() == palavra_chave:
                        j = 1
                        while doc[token.i + j].text != "\n":
                            # Verificar se a próxima palavra após palavra_chave é um número
                            if token.i + j < len(doc) and doc[token.i + j].like_num:
                                valor_numerico = float(doc[token.i + j].text)
                            j = j + 1

    if valor_numerico is not None:
        print(f"Valor de {palavra_chave}:", valor_numerico)
    else:
        print(f"{palavra_chave} não encontrado no texto.")


# Inicializar variáveis para armazenar os valores de IPAP e EPAP
# ipap_min = None
# ipap_max = None
# epap = None

# frase1 = nlp("Porcentagem de dias com uso >= 4 horas")
# frase2 = nlp("Porcentagem de noites de uso >= 4 horas 50,0%")
# print(frase1.similarity(frase2))

# # Iterar sobre as palavras no documento
# for token in doc:
#     # Verificar se a palavra é IPAP ou EPAP e extrair o valor
#     if token.text.lower() == "ipap":
#         j = 1
#         if doc[token.i + 1].text == "máx":
#             while doc[token.i + j].text != "\n":
#                 # Verificar se a próxima palavra após IPAP é um número
#                 if token.i + j < len(doc) and doc[token.i + j].like_num:
#                     ipap_max = float(doc[token.i + j].text)
#                 j = j + 1
#         elif doc[token.i + 1].text == "min":
#             while doc[token.i + j].text != "\n":
#                 # Verificar se a próxima palavra após IPAP é um número
#                 if token.i + j < len(doc) and doc[token.i + j].like_num:
#                     ipap_min = float(doc[token.i + j].text)
#                 j = j + 1
#     elif token.text.lower() == "epap":
#         # Verificar se a próxima palavra após EPAP é um número
#         if token.i + 1 < len(doc) and doc[token.i + 1].like_num:
#             epap = float(doc[token.i + 1].text)

# # Imprimir os valores de IPAP e EPAP, se forem encontrados
# if ipap_max is not None:
#     print("Valor de IPAP MAX:", ipap_max)
# else:
#     print("IPAP MAX não encontrado no texto.")

# if ipap_min is not None:
#     print("Valor de IPAP MIN:", ipap_min)
# else:
#     print("IPAP MIN não encontrado no texto.")

# if epap is not None:
#     print("Valor de EPAP:", epap)
# else:
#     print("EPAP não encontrado no texto.")
