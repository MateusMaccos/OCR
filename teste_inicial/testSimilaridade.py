from spacy import load
from unidecode import unidecode


def tratar_texto(texto):
    """Remove acentos, converte para minúsculas e remove stop words."""
    texto_tratado = unidecode(texto).lower()
    doc = nlp(texto_tratado)
    tokens_filtrados = [token.text for token in doc if not token.is_stop]
    return " ".join(tokens_filtrados)


nlp = load("pt_core_news_lg")

text = "Pressao EPAP 7 cmH20"

string = "pressao EPAP"

textoBuscado = tratar_texto(string)
textoNoTxt = tratar_texto(text)

textoBuscadoNLP = nlp(textoBuscado)
textoNoTxtNLP = nlp(textoNoTxt)

similaridade = similaridade = textoBuscadoNLP.similarity(textoNoTxtNLP)
print(similaridade)
