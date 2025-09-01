import cv2
import numpy as np

img1 = cv2.imread('imagem.jpeg')
img2 = cv2.imread('img2.jpg')

print('Dimensões originais da Imagem 1: {}'.format(img1.shape))
print('Dimensões originais da Imagem 2: {}'.format(img2.shape))


altura = img2.shape[0]
largura = img2.shape[1]

img1_redimensionada = cv2.resize(img1, (largura, altura))

print('Dimensões da Imagem 1 após redimensionar: {}'.format(img1_redimensionada.shape))


img3 = cv2.add(img1_redimensionada, img2)

print('Imagem 3 (resultado): {} {}'.format(img3.shape, img3.dtype))

cv2.imshow('Soma', img3)
cv2.waitKey(0)
cv2.destroyAllWindows()