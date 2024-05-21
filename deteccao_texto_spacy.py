from spacy import load
from unidecode import unidecode


def buscar_texto(texto_buscado, pasta, tipo="num"):
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
    valor_textual = ""

    for linha in textoDoArquivo:
        linhaSemAcentos = remover_acentos(linha)
        linhaMinuscula = linhaSemAcentos.lower()
        linha_processada = nlp(linhaMinuscula)
        if linha_processada.vector_norm != 0 and linha_processada.has_vector:
            similaridade = textoBuscado.similarity(linha_processada)
            if similaridade >= 0.20:
                palavras_em_comum = 0
                for token in linha_processada:
                    if token.text.lower() in palavras_chave:
                        palavras_em_comum += 1
                        if palavras_em_comum >= 2 or len(palavras_chave) == 1:
                            j = 1
                            ultima_chave = palavras_chave[len(palavras_chave) - 1]
                            while linha_processada[token.i + j].text != "\n":
                                if token.i + j < len(linha_processada):
                                    if (
                                        linha_processada[token.i + j].like_num
                                        and tipo == "num"
                                    ):
                                        valor_numerico = float(
                                            linha_processada[token.i + j].text.replace(
                                                ",", "."
                                            )
                                        )
                                    elif (
                                        linha_processada[token.i].text == ultima_chave
                                        and tipo == "str"
                                    ):
                                        valor_textual = (
                                            valor_textual
                                            + linha_processada[token.i + j].text
                                            + " "
                                        )
                                j = j + 1

    if valor_numerico is not None:
        return valor_numerico
    elif valor_textual != "":
        return valor_textual.replace(":", "")
    else:
        return "Não encontrado"
