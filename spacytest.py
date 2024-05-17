from spacy import load  # Carrega um modelo
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

    palavra_chave = str(textoBuscado[0])

    valor_numerico = None

    for linha in textoDoArquivo:
        linhaSemAcentos = remover_acentos(linha)
        linhaMinuscula = linhaSemAcentos.lower()
        linha_processada = nlp(linhaMinuscula)
        if linha_processada.vector_norm != 0 and linha_processada.has_vector:
            similaridade = textoBuscado.similarity(linha_processada)
            if similaridade >= 0.35:
                doc = linha_processada
                for token in doc:
                    if token.text.lower() == palavra_chave:
                        j = 1
                        while doc[token.i + j].text != "\n":
                            # Verificar se a próxima palavra após palavra_chave é um número
                            if token.i + j < len(doc) and doc[token.i + j].like_num:
                                valor_numerico = float(doc[token.i + j].text)
                            j = j + 1

    if valor_numerico is not None:
        return valor_numerico
    else:
        return "Não encontrado"
