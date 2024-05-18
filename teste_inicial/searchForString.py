import re

with open("relatorioEmTexto.txt", "r") as file:
    textoDoArquivo = file.read()

entrada = "ipap máx."

padrao = r""
# Escapando espaços na entrada para a expressão regular
for parte in entrada.lower().split():
    padrao += parte + r"\s*"

# Expressão regular para encontrar o valor da entrada variável
padrao += r"(.+)"

# Busca pelo valor da entrada no texto usando a expressão regular
match = re.search(padrao, textoDoArquivo.lower())

# Verifica se houve um match e extrai o valor encontrado
if match:
    valor_encontrado = match.group(1)
    print("Valor encontrado:", valor_encontrado)
else:
    print("Valor não encontrado no texto.")
