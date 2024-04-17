import re

# Texto retornado pelo Pytesseract
texto = """
Teste de valor 26
Camila
Relatório
detalhado
Data
de
nasc:
08/05/1991
Organização:
Camila
Ferreira
Leite,
Am...
Intervalo
de
datas:
—
04/05/2022
-
10/05/2022
Referência:
Morada:
Rua
Coronel
Nunes
de
Melo,
1142,
—
Data
de
configuração:
11/05/2022
;
e
,
Rodoifo
Teófilo
Á
1D
do
paciente:
CamilaSilva
e
Sil...
Fortaleza,
CÉ
60416-000
Máscara:
Telefone:
App
vinculado:
Telefone:
Dispositivos:
BIPAP
AVAPS
30
(System
One
60
Series)
3.05.01
(1169P)
C20346083C819
Equipa
de
cuidados
médicos
Leite,
Camila
Camila
Ferreira
Leite
Rua
Coronel
Nunes
de
Melo,
1142,
Fortaleza
-
CE,
60416-000,
BRA
Informações
de
aderência
à
terapêutica
04/05/2022
-
10/05/2022
 
Definições
do
Dispositivo
a
partir
de
10/05/2022
Modo
do
aparelho
S/T
-
AVAPS
Configurações
do
dispositivo
Parâmetro
Valor
IPAP
máx.
26
cmH2O0
IPAP
min.
18
cmH2O0
Pressão
EPAP
7
cmH20
Taxa
respiratória
12
Inspiração
cronometrada
15
Volume
corrente
450
Definição
do
tempo
de
elevação
2
Bloqueio
da
definição
do
tempo
de
elevação
—
Afivado
Rampa
D
Resistência
da
máscara
1
Tipo
de
tubo
22
Trava
do
tipo
de
tubo
Desativado
Alarme
de
desconexão
Desativado
"""

entrada = "ipap min."

padrao = r""
# Escapando espaços na entrada para a expressão regular
for parte in entrada.lower().split():
    padrao += parte + r"\s*"

# Expressão regular para encontrar o valor da entrada variável
padrao += r"(.+)"

# Busca pelo valor da entrada no texto usando a expressão regular
match = re.search(padrao, texto.lower())

# Verifica se houve um match e extrai o valor encontrado
if match:
    valor_encontrado = match.group(1)
    print("Valor encontrado:", valor_encontrado)
else:
    print("Valor não encontrado no texto.")
