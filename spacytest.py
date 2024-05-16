from spacy import load  # Carrega um modelo
from spacy.matcher import Matcher

nlp = load("pt_core_news_sm")

nomepasta = "teste1"

with open(f"{nomepasta}/relatorioEmTexto.txt", "r") as file:
    textoDoArquivo = file.read()

doc = nlp(textoDoArquivo)


# Inicializar variáveis para armazenar os valores de IPAP e EPAP
ipap_min = None
ipap_max = None
epap = None

# Iterar sobre as palavras no documento
for token in doc:
    # Verificar se a palavra é IPAP ou EPAP e extrair o valor
    if token.text.lower() == "ipap":
        j = 1
        if doc[token.i + 1].text == "máx":
            while doc[token.i + j].text != "\n":
                # Verificar se a próxima palavra após IPAP é um número
                if token.i + j < len(doc) and doc[token.i + j].like_num:
                    ipap_max = float(doc[token.i + j].text)
                j = j + 1
        elif doc[token.i + 1].text == "min":
            while doc[token.i + j].text != "\n":
                # Verificar se a próxima palavra após IPAP é um número
                if token.i + j < len(doc) and doc[token.i + j].like_num:
                    ipap_min = float(doc[token.i + j].text)
                j = j + 1
    elif token.text.lower() == "epap":
        # Verificar se a próxima palavra após EPAP é um número
        if token.i + 1 < len(doc) and doc[token.i + 1].like_num:
            epap = float(doc[token.i + 1].text)

# Imprimir os valores de IPAP e EPAP, se forem encontrados
if ipap_max is not None:
    print("Valor de IPAP MAX:", ipap_max)
else:
    print("IPAP MAX não encontrado no texto.")

if ipap_min is not None:
    print("Valor de IPAP MIN:", ipap_min)
else:
    print("IPAP MIN não encontrado no texto.")

if epap is not None:
    print("Valor de EPAP:", epap)
else:
    print("EPAP não encontrado no texto.")
