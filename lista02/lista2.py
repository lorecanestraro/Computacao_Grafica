import cv2
import numpy as np
import matplotlib.pyplot as plt
import os



def filtro_media(img, ksize=3):
    w = np.ones((ksize, ksize), dtype=np.float32) / (ksize * ksize)
    return cv2.filter2D(img, -1, w)


def filtro_k_vizinhos(img, ksize=3, k=5):
    N, M = img.shape
    pad = ksize // 2
    out = np.zeros_like(img)

    for i in range(pad, N - pad):
        for j in range(pad, M - pad):
            vizinhos = img[i-pad:i+pad+1, j-pad:j+pad+1].flatten()
            vizinhos.sort()
            centro = len(vizinhos)//2
            low = max(0, centro - k//2)
            high = min(len(vizinhos), centro + k//2 + 1)
            out[i, j] = np.mean(vizinhos[low:high])
    return out.astype(np.uint8)


def filtro_mediana(img, ksize=3):
    return cv2.medianBlur(img, ksize)


def filtro_laplaciano(img):
    return cv2.Laplacian(img, cv2.CV_8U)


def filtro_roberts(img):
    kernelx = np.array([[1, 0], [0, -1]], dtype=np.float32)
    kernely = np.array([[0, 1], [-1, 0]], dtype=np.float32)
    gx = cv2.filter2D(img, -1, kernelx)
    gy = cv2.filter2D(img, -1, kernely)
    return cv2.convertScaleAbs(gx + gy)


def filtro_prewitt(img):
    kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
    kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
    gx = cv2.filter2D(img, -1, kernelx)
    gy = cv2.filter2D(img, -1, kernely)
    return cv2.convertScaleAbs(gx + gy)


def filtro_sobel(img):
    sobelx = cv2.Sobel(img, cv2.CV_8U, 1, 0, ksize=3)
    sobely = cv2.Sobel(img, cv2.CV_8U, 0, 1, ksize=3)
    return cv2.convertScaleAbs(sobelx + sobely)


def processar_imagem(nome_img):
    img = cv2.imread(nome_img, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Erro: não achei {nome_img}")
        return
    
    filtros = {
        "media": filtro_media(img, 3),
        "k_vizinhos": filtro_k_vizinhos(img, 3, 5),
        "mediana": filtro_mediana(img, 3),
        "laplaciano": filtro_laplaciano(img),
        "roberts": filtro_roberts(img),
        "prewitt": filtro_prewitt(img),
        "sobel": filtro_sobel(img)
    }

    
    pasta_saida = "resultados"
    os.makedirs(pasta_saida, exist_ok=True)

    
    for nome, res in filtros.items():
        saida = os.path.join(pasta_saida, f"{os.path.splitext(nome_img)[0]}_{nome}.png")
        cv2.imwrite(saida, res)

    
    plt.figure(figsize=(15,10))
    plt.subplot(2,4,1)
    plt.imshow(img, cmap="gray")
    plt.title("Original")
    plt.axis('off')

    for i, (nome, res) in enumerate(filtros.items()):
        plt.subplot(2,4,i+2)
        plt.imshow(res, cmap="gray")
        plt.title(nome)
        plt.axis('off')
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    processar_imagem("lena.png")
    processar_imagem("img_aluno.jpg")
    print("Processamento concluído! Resultados salvos na pasta 'resultados'.")
