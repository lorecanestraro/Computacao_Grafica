import cv2
import numpy as np
from matplotlib import pyplot as plt



def show_and_save(img, title, filename):
    """Mostra e salva a imagem."""
    cv2.imwrite(filename, img)
    plt.imshow(img, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()


img1 = cv2.imread("circuito.tif", cv2.IMREAD_GRAYSCALE)

med1 = cv2.medianBlur(img1, 3)
med2 = cv2.medianBlur(med1, 3)
med3 = cv2.medianBlur(med2, 3)

show_and_save(med1, "Mediana 1", "resultado_mediana1.png")
show_and_save(med2, "Mediana 2", "resultado_mediana2.png")
show_and_save(med3, "Mediana 3", "resultado_mediana3.png")


img2 = cv2.imread("pontos.png", cv2.IMREAD_GRAYSCALE)

kernel = np.array([[-1,-1,-1],
                   [-1, 8,-1],
                   [-1,-1,-1]])

pontos = cv2.filter2D(img2, -1, kernel)
_, pontos_bin = cv2.threshold(pontos, 200, 255, cv2.THRESH_BINARY)

show_and_save(pontos_bin, "Pontos isolados", "resultado_pontos.png")


img3 = cv2.imread("linhas.png", cv2.IMREAD_GRAYSCALE)


horizontal = np.array([[-1,-1,-1],
                       [ 2, 2, 2],
                       [-1,-1,-1]])

vertical = np.array([[-1, 2,-1],
                     [-1, 2,-1],
                     [-1, 2,-1]])

diag1 = np.array([[ 2,-1,-1],
                  [-1, 2,-1],
                  [-1,-1, 2]])

diag2 = np.array([[-1,-1, 2],
                  [-1, 2,-1],
                  [ 2,-1,-1]])


lin_h = cv2.filter2D(img3, -1, horizontal)
lin_v = cv2.filter2D(img3, -1, vertical)
lin_d1 = cv2.filter2D(img3, -1, diag1)
lin_d2 = cv2.filter2D(img3, -1, diag2)


_, th_h = cv2.threshold(lin_h, 50, 255, cv2.THRESH_BINARY)
_, th_v = cv2.threshold(lin_v, 50, 255, cv2.THRESH_BINARY)
_, th_d1 = cv2.threshold(lin_d1, 50, 255, cv2.THRESH_BINARY)
_, th_d2 = cv2.threshold(lin_d2, 50, 255, cv2.THRESH_BINARY)


final = cv2.bitwise_or(cv2.bitwise_or(th_h, th_v), cv2.bitwise_or(th_d1, th_d2))
show_and_save(final, "Linhas Detectadas", "resultado_linhas.png")


img4 = cv2.imread("igreja.png", cv2.IMREAD_GRAYSCALE)

canny = cv2.Canny(img4, 100, 200)
show_and_save(canny, "Canny", "resultado_canny.png")


def region_growing(img, seed, threshold=5):
    visited = np.zeros_like(img, dtype=np.uint8)
    h, w = img.shape
    seed_value = img[seed]
    stack = [seed]

    while stack:
        x, y = stack.pop()
        if visited[x,y] == 0:
            visited[x,y] = 255
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < h and 0 <= ny < w:
                        if visited[nx,ny] == 0 and abs(int(img[nx,ny]) - int(seed_value)) < threshold:
                            stack.append((nx,ny))
    return visited

img5 = cv2.imread("root.jpg", cv2.IMREAD_GRAYSCALE)
seed_point = (50,50)
region = region_growing(img5, seed_point)
show_and_save(region, "Crescimento de Região", "resultado_regiao.png")


def otsu_threshold(img):
    hist, bins = np.histogram(img.ravel(), 256, [0,256])
    total = img.size
    sumB, wB, maximum, sum1 = 0, 0, 0, np.dot(np.arange(256), hist)
    for i in range(256):
        wB += hist[i]
        if wB == 0: continue
        wF = total - wB
        if wF == 0: break
        sumB += i*hist[i]
        mB = sumB / wB
        mF = (sum1 - sumB) / wF
        between = wB * wF * (mB - mF) ** 2
        if between > maximum:
            maximum = between
            threshold = i
    return threshold

for img_name in ["harewood.jpg", "nuts.jpg", "snow.jpg", "img_aluno.png"]:
    img6 = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
    t = otsu_threshold(img6)
    _, otsu = cv2.threshold(img6, t, 255, cv2.THRESH_BINARY)
    show_and_save(otsu, f"Otsu - {img_name}", f"resultado_otsu_{img_name}.png")
