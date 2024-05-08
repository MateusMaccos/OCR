import cv2
import pytesseract
from pytesseract import Output
import os
import ajustarRotacao

img = cv2.imread("relatorio.jpg")
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# from pdf2image import convert_from_path

# images = convert_from_path(
#     "bipap2.pdf", poppler_path=r"C:\Users\mateu\Downloads\poppler-24.02.0\Library\bin"
# )
# images[0].save("relatorio2.jpg", "JPEG")

# 0    Orientation and script detection (OSD) only.
# 1    Automatic page segmentation with OSD.
# 2    Automatic page segmentation, but no OSD, or OCR.
# 3    Fully automatic page segmentation, but no OSD. (Default)
# 4    Assume a single column of text of variable sizes.
# 5    Assume a single uniform block of vertically aligned text.
# 6    Assume a single uniform block of text.
# 7    Treat the image as a single text line.
# 8    Treat the image as a single word.
# 9    Treat the image as a single word in a circle.
# 10    Treat the image as a single character.
# 11    Sparse text. Find as much text as possible in no particular order.
# 12    Sparse text with OSD.
# 13    Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific.

myconfig = r"--psm 3 --oem 3"
nomepasta = "teste1"
invertedImg = cv2.bitwise_not(img)
# os.makedirs(f"./{nomepasta}")
cv2.imwrite(f"{nomepasta}/imagem_invertida.jpg", invertedImg)


def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


grayImg = grayscale(img)
cv2.imwrite(f"{nomepasta}/grayImagem.jpg", grayImg)

thresh, im_bw = cv2.threshold(grayImg, 220, 255, cv2.THRESH_BINARY)
cv2.imwrite(f"{nomepasta}/bw_img.jpg", im_bw)


def noise_removal(image):
    import numpy as np

    kernel = np.ones((2, 2), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    # image = cv2.medianBlur(image, 1)
    return image


no_noise = noise_removal(im_bw)
cv2.imwrite(f"{nomepasta}/no_noise.jpg", no_noise)


def thin_font(image):
    import numpy as np

    image = cv2.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image


def thick_font(image):
    import numpy as np

    image = cv2.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image


eroded_image = thin_font(no_noise)
cv2.imwrite(f"{nomepasta}/eroded.jpg", eroded_image)

dilated_image = thick_font(eroded_image)
cv2.imwrite(f"{nomepasta}/dilated.jpg", dilated_image)

img = dilated_image
texto = pytesseract.image_to_string(img, lang="por", config=myconfig)

# A text file is created and flushed
file = open(f"{nomepasta}/relatorioEmTexto.txt", "w+")
file.write("")
file.close()

d = pytesseract.image_to_data(img, output_type=Output.DICT, lang="por")
n_boxes = len(d["level"])
for i in range(n_boxes):
    (x, y, w, h) = (d["left"][i], d["top"][i], d["width"][i], d["height"][i])
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
cv2.imwrite(f"{nomepasta}/imagem_com_deteccao.jpg", img)

for linha in texto.split("\n"):
    file = open(f"{nomepasta}/relatorioEmTexto.txt", "a")
    file.write(linha)
    file.write("\n")
    file.close
