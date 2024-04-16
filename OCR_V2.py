# Import required packages
import cv2
import pytesseract

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

imagem = cv2.imread("relatorio.jpg")

# Convertendo a imagem para escala de cinza
imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

# Aplicando binarização (thresholding)
_, imagem_binaria = cv2.threshold(imagem_cinza, 128, 255, cv2.THRESH_BINARY)

# Ajustando o contraste (opcional)
alpha = 1  # Fator de contraste
beta = 1  # Fator de brilho
imagem_processada = cv2.convertScaleAbs(imagem_binaria, alpha=alpha, beta=beta)

# Exibindo a imagem original e a imagem processada
# cv2.imshow("Imagem Original", imagem)
# cv2.imshow("Imagem Processada", imagem_processada)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Detecção de contornos na imagem
contornos, _ = cv2.findContours(
    imagem_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)

# Iterando sobre os contornos encontrados
for contorno in contornos:
    # Ignorando contornos muito pequenos
    if cv2.contourArea(contorno) > 100:
        # Obtendo as coordenadas do retângulo que envolve o contorno
        x, y, w, h = cv2.boundingRect(contorno)

        # Desenhando o retângulo na imagem original
        cv2.rectangle(imagem, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Recortando a região de texto da imagem original
        regiao_texto = imagem[y : y + h, x : x + w]

        # Aplicando OCR na região de texto
        texto_detectado = pytesseract.image_to_string(
            regiao_texto, lang="por"
        )  # Use o idioma adequado

        # Imprimindo o texto detectado
        print(f"Texto Detectado: {texto_detectado}")

# Exibindo a imagem com os contornos e retângulos
cv2.imshow("Imagem com Contornos", imagem)
cv2.waitKey(0)
cv2.destroyAllWindows()
