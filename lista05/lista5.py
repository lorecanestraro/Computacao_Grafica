import cv2 as cv
import numpy as np
import os


output_dir = "resultados_exercicios"
os.makedirs(output_dir, exist_ok=True)


print("Executando Exercício 2...")
img2 = cv.imread("quadrados.png", cv.IMREAD_GRAYSCALE)
se2 = np.ones((50,50), np.uint8)  
erosao2 = cv.erode(img2, se2)
restaurado2 = cv.dilate(erosao2, se2)

cv.imwrite(os.path.join(output_dir, "ex2_erosao.png"), erosao2)
cv.imwrite(os.path.join(output_dir, "ex2_restaurado.png"), restaurado2)


print("Executando Exercício 3...")
img3 = cv.imread("ruidos.png", cv.IMREAD_GRAYSCALE)
se3 = np.ones((3,3), np.uint8)

abertura3 = cv.morphologyEx(img3, cv.MORPH_OPEN, se3)
fechamento3 = cv.morphologyEx(img3, cv.MORPH_CLOSE, se3)

cv.imwrite(os.path.join(output_dir, "ex3_abertura.png"), abertura3)
cv.imwrite(os.path.join(output_dir, "ex3_fechamento.png"), fechamento3)

print("Executando Exercício 4...")
img4 = cv.imread("cachorro.png", cv.IMREAD_GRAYSCALE)
se4 = np.ones((3,3), np.uint8)

erosao4 = cv.erode(img4, se4)
dilat4 = cv.dilate(img4, se4)

interna4 = cv.subtract(img4, erosao4)  
externa4 = cv.subtract(dilat4, img4)   

cv.imwrite(os.path.join(output_dir, "ex4_interna.png"), interna4)
cv.imwrite(os.path.join(output_dir, "ex4_externa.png"), externa4)


print("Executando Exercício 5...")
img5 = cv.imread("gato.png", cv.IMREAD_GRAYSCALE)
_, binaria5 = cv.threshold(img5, 127, 255, cv.THRESH_BINARY)

mascara5 = np.zeros((binaria5.shape[0]+2, binaria5.shape[1]+2), np.uint8)
seed_point = (10, 10)  # pode ajustar
preenchida5 = binaria5.copy()
cv.floodFill(preenchida5, mascara5, seed_point, 255)

cv.imwrite(os.path.join(output_dir, "ex5_preenchida.png"), preenchida5)

print("Executando Exercício 6...")
img6 = cv.imread("quadrados.png", cv.IMREAD_GRAYSCALE)
_, binaria6 = cv.threshold(img6, 127, 255, cv.THRESH_BINARY)

num_labels, labels = cv.connectedComponents(binaria6)


x, y = 150, 150  
label = labels[y, x]

saida6 = np.zeros((img6.shape[0], img6.shape[1], 3), np.uint8)
saida6[labels == label] = (0, 255, 255)  # Amarelo

cv.imwrite(os.path.join(output_dir, "ex6_componente.png"), saida6)

print("Executando Exercício 7...")
img7 = cv.imread("img_aluno.jpeg", cv.IMREAD_GRAYSCALE)
se7 = np.ones((5,5), np.uint8)

erosao7 = cv.erode(img7, se7)
dilat7 = cv.dilate(img7, se7)
grad7 = cv.subtract(dilat7, erosao7)

cv.imwrite(os.path.join(output_dir, "ex7_erosao.png"), erosao7)
cv.imwrite(os.path.join(output_dir, "ex7_dilatacao.png"), dilat7)
cv.imwrite(os.path.join(output_dir, "ex7_gradiente.png"), grad7)
