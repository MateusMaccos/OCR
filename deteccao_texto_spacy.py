from spacy import load
from unidecode import unidecode


def buscar_texto(texto_buscado, pasta):
    def remover_acentos(texto):
        return unidecode(texto)

    nlp = load("pt_core_news_lg")

    nomepasta = pasta

    with open(f"{nomepasta}/relatorioEmTexto.txt", "r") as file:
        textoDoArquivo = file.readlines()
    buscaSemAcentos = remover_acentos(texto_buscado)
    BuscaMinusculo = buscaSemAcentos.lower()
    textoBuscado = nlp(BuscaMinusculo)

    palavras_chave = str(textoBuscado).split()

    valor_numerico = None

    for linha in textoDoArquivo:
        linhaSemAcentos = remover_acentos(linha)
        linhaMinuscula = linhaSemAcentos.lower()
        linha_processada = nlp(linhaMinuscula)
        if linha_processada.vector_norm != 0 and linha_processada.has_vector:
            similaridade = textoBuscado.similarity(linha_processada)
            if similaridade >= 0.20:
                palavras_em_comum = 0
                doc = linha_processada
                for token in doc:
                    if token.text.lower() in palavras_chave:
                        palavras_em_comum += 1
                        j = 1
                        if palavras_em_comum >= 2 or len(palavras_chave) == 1:
                            while doc[token.i + j].text != "\n":
                                if token.i + j < len(doc) and doc[token.i + j].like_num:
                                    valor_numerico = float(doc[token.i + j].text)
                                j = j + 1

    if valor_numerico is not None:
        return valor_numerico
    else:
        return "Não encontrado"
