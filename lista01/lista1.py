import cv2
import numpy as np
import matplotlib.pyplot as plt




def to_gray(img):
    img= cv2.imread('minha_img.jpg', cv2.IMREAD_GRAYSCALE)
    return img

def to_gray2(img):
    img= cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)
    return img

def negativo(img):
    return 255 - img


def normalizacao(img, c, d):
    a = np.min(img)
    b = np.max(img)
    norm = (img - a) * ((d - c) / (b - a)) + c
    return norm.astype(np.uint8)

def logaritmico(img):
    R = np.max(img)
    c = 255 / np.log(1 + R)
    log_img = c * np.log(1 + img.astype(np.float32))
    return np.uint8(log_img)

def potencia(img, c, gamma):
    pot_img = c * (img.astype(np.float32) ** gamma)
    pot_img = np.clip(pot_img, 0, 255)
    return np.uint8(pot_img)

def fatiamento_bits(img):
    gray = to_gray(img)
    planos = []
    for i in range(8):
        plano = (gray >> i) & 1
        planos.append(plano * 255)
    return planos

def histograma(img):
    h = np.zeros(256, dtype=int)
    for v in img.ravel():
        h[v] += 1
    return h

def hist_normalizado(img):
    h = histograma(img)
    return h / np.sum(h)

def hist_acumulado(img):
    h = histograma(img)
    return np.cumsum(h)

def hist_acum_normalizado(img):
    ha = hist_acumulado(img)
    return ha / ha[-1]

def equalizacao(img):
    gray = to_gray(img)
    ha = hist_acumulado(gray)
    N = gray.size
    L = 256
    eq = np.zeros_like(gray)
    for i in range(256):
        eq[gray == i] = (ha[i] - np.min(ha)) * (L-1) / (N - np.min(ha))
    return np.uint8(eq)


def main():

    lena = cv2.imread("lena.png")
    aluno = cv2.imread("minha_img.jpg")
    unequal = cv2.imread("unequalized.jpg")

    gray_lena = to_gray2(lena)
    gray_aluno = to_gray(aluno)
    cv2.imwrite("resultados/ex1_gray_lena.png", gray_lena)
    cv2.imwrite("resultados/ex1_gray_aluno.png", gray_aluno)

    cv2.imwrite("resultados/ex2_neg_lena.png", negativo(lena))
    cv2.imwrite("resultados/ex2_neg_aluno.png", negativo(aluno))

    cv2.imwrite("resultados/ex3_norm_lena.png", normalizacao(lena, 0, 100))
    cv2.imwrite("resultados/ex3_norm_aluno.png", normalizacao(aluno, 0, 100))

    cv2.imwrite("resultados/ex4_log_lena.png", logaritmico(lena))
    cv2.imwrite("resultados/ex4_log_aluno.png", logaritmico(aluno))

    cv2.imwrite("resultados/ex5_pot_lena.png", potencia(lena, 2, 2))
    cv2.imwrite("resultados/ex5_pot_aluno.png", potencia(aluno, 2, 2))

    bits_lena = fatiamento_bits(lena)
    bits_aluno = fatiamento_bits(aluno)
    for i, p in enumerate(bits_lena):
        cv2.imwrite(f"resultados/ex6_bits_lena_{i}.png", p)
    for i, p in enumerate(bits_aluno):
        cv2.imwrite(f"resultados/ex6_bits_aluno_{i}.png", p)

    gray_unequal = to_gray(unequal)
    h_unequal = histograma(gray_unequal)
    plt.bar(range(256), h_unequal); plt.savefig("resultados/ex7_hist_unequal.png"); plt.clf()

    h_R = histograma(aluno[:,:,2])
    h_G = histograma(aluno[:,:,1])
    h_B = histograma(aluno[:,:,0])
    plt.bar(range(256), h_R, color="r"); plt.savefig("resultados/ex7_hist_R.png"); plt.clf()
    plt.bar(range(256), h_G, color="g"); plt.savefig("resultados/ex7_hist_G.png"); plt.clf()
    plt.bar(range(256), h_B, color="b"); plt.savefig("resultados/ex7_hist_B.png"); plt.clf()

    gray_aluno = to_gray(aluno)
    hA = histograma(gray_aluno)
    hB = hist_normalizado(gray_aluno)
    hC = hist_acumulado(gray_aluno)
    hD = hist_acum_normalizado(gray_aluno)

    plt.bar(range(256), hA); plt.savefig("resultados/ex7_hist_A.png"); plt.clf()
    plt.plot(hB); plt.savefig("resultados/ex7_hist_B.png"); plt.clf()
    plt.plot(hC); plt.savefig("resultados/ex7_hist_C.png"); plt.clf()
    plt.plot(hD); plt.savefig("resultados/ex7_hist_D.png"); plt.clf()

   
    cv2.imwrite("resultados/ex8_eq_lena.png", equalizacao(lena))
    cv2.imwrite("resultados/ex8_eq_unequal.png", equalizacao(unequal))
    cv2.imwrite("resultados/ex8_eq_aluno.png", equalizacao(aluno))


main()
