# Import required packages
import cv2
import pytesseract

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# from pdf2image import convert_from_path


# images = convert_from_path('bipap.pdf',poppler_path=r'C:\Users\mateu\Downloads\poppler-24.02.0\Library\bin')
# images[0].save('relatorio.jpg', 'JPEG')

# Read image from which text needs to be extracted
img = cv2.imread("relatorio.jpg")

# Preprocessing the image starts

# Convert the image to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplicando suavização com filtro Gaussiano
# gray = cv2.GaussianBlur(gray, (5, 5), 0)

# Salva a nova imagem com os contornos
cv2.imwrite("imagem_gray.jpg", gray)

# Aplicando a limiarização adaptativa
thresh1 = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 5
)

# Performing OTSU threshold
# ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

# Salva a nova imagem com os contornos
cv2.imwrite("thresh1.jpg", thresh1)

# Specify structure shape and kernel size.
# Kernel size increases or decreases the area
# of the rectangle to be detected.
# A smaller value like (10, 10) will detect
# each word instead of a sentence.
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))

# Applying dilation on the threshold image
dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
# dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
cv2.imwrite("dilation.jpg", dilation)

# Finding contours
contours, hierarchy = cv2.findContours(
    dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
)

# Creating a copy of image
im2 = img.copy()

# A text file is created and flushed
file = open("relatorioEmTexto.txt", "w+")
file.write("")
file.close()

import numpy as np

# Cria uma cópia da imagem original para desenhar os contornos
im_with_contours = img.copy()

# Desenha os contornos na imagem copiada
cv2.drawContours(im_with_contours, contours, -1, (0, 255, 0), 3)

# Salva a nova imagem com os contornos
cv2.imwrite("imagem_com_contornos.jpg", im_with_contours)

contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[1])

# Looping through the identified contours
# Then rectangular part is cropped and passed on
# to pytesseract for extracting text from it
# Extracted text is then written into the text file
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)

    # Drawing a rectangle on copied image
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Cropping the text block for giving input to OCR
    cropped = im2[y : y + h, x : x + w]

    # Open the file in append mode
    file = open("relatorioEmTexto.txt", "a")

    # Apply OCR on the cropped image
    text = pytesseract.image_to_string(cropped, lang="por")

    # Appending the text into file
    file.write(text)
    file.write("\n")

    # Close the file
    file.close
