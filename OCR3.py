import cv2
import pytesseract
from pytesseract import Output

img = cv2.imread("relatorio.jpg")
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplicando suavização com filtro Gaussiano
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# Aplicando a limiarização adaptativa
thresh1 = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 5
)

rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))

# Applying dilation on the threshold image
dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

d = pytesseract.image_to_data(img, output_type=Output.DICT, lang="por")

n_boxes = len(d["text"])
for i in range(n_boxes):
    if int(d["conf"][i]) > 60:
        (x, y, w, h) = (d["left"][i], d["top"][i], d["width"][i], d["height"][i])
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow("img", img)
cv2.waitKey(0)
