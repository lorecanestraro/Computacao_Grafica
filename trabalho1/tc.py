import tkinter as tk
from tkinter import filedialog
from ultralytics import YOLO
import cv2
from PIL import Image, ImageTk
import numpy as np
import yt_dlp
import os
import pygame
import time


pygame.mixer.init()
SOM_ARQUIVO = "hino_santos.mp3"


janela = tk.Tk()
janela.title("Trabalho Computação Gráfica")
janela.geometry("350x200") 


def aplicar_filtro(img, tipo):
    if tipo == "cinza":
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif tipo == "negativo":
        return cv2.bitwise_not(img)
    elif tipo == "binario":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binario = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        return binario
    elif tipo == "suavizacao media":
        ksize=3
        w = np.ones((ksize, ksize), dtype=np.float32) / (ksize*ksize)
        return cv2.filter2D(img, -1, w)
    elif tipo == "suavizacao mediana":
        return cv2.medianBlur(img, 3)
    elif tipo == "original":
        return img
    elif tipo == "detector de bordas":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.Canny(gray, 100, 200)
    elif tipo == "erosao":
        kernel = np.ones((5,5), np.uint8)
        return cv2.erode(img, kernel, iterations=1)
    elif tipo == "dilatacao":
        kernel = np.ones((5,5), np.uint8)
        return cv2.dilate(img, kernel, iterations=1)
    elif tipo == "abertura":
        kernel = np.ones((5,5), np.uint8)
        return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    elif tipo == "fechamento":
        kernel = np.ones((5,5), np.uint8)
        return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return img


def nova_janela(caminho):
    nova = tk.Toplevel(janela)
    nova.title("Visualizador de Imagem")
    nova.geometry("700x600")

    img = cv2.imread(caminho)
    if img is None:
        tk.Label(nova, text="Erro ao carregar a imagem").pack()
        return

    lbl = tk.Label(nova)
    lbl.pack(pady=10)

    def atualizar_imagem(img_cv):
        if len(img_cv.shape) == 2:
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_GRAY2RGB)
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb).resize((500,400))
        foto = ImageTk.PhotoImage(img_pil)
        lbl.config(image=foto)
        lbl.image = foto

    def aplicar(tipo):
        filtrada = aplicar_filtro(img.copy(), tipo)
        atualizar_imagem(filtrada)

    
    botoes = ["Cinza","Negativo","Binário","Suavização Média","Suavização Mediana",
              "Original","Detector de Bordas","Erosão","Dilatação","Abertura","Fechamento"]
    tipos = ["cinza","negativo","binario","suavizacao media","suavizacao mediana",
             "original","detector de bordas","erosao","dilatacao","abertura","fechamento"]

    frame_botoes = tk.Frame(nova)
    frame_botoes.pack()
    for i, (b, t) in enumerate(zip(botoes, tipos)):
        tk.Button(frame_botoes, text=b, command=lambda x=t: aplicar(x)).grid(row=i//5, column=i%5, padx=5, pady=10)

    atualizar_imagem(img)

def escolher_arquivo():
    caminho = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=(("Imagens", "*.jpg;*.png;*.jpeg;*.bmp;*.gif"), ("Todos os arquivos", "*.*"))
    )
    if caminho:
        nova_janela(caminho)

def carregar_video(tipo):
    url = "https://youtu.be/yYHcqzLIuQQ?si=8jb33Egb1kpdOii_"
    output_file = "video_youtube.mp4"

    if not os.path.exists(output_file):
        ydl_opts = {'format':'bestvideo','outtmpl':output_file}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    cap = cv2.VideoCapture(output_file)
    nome_janela = "Vídeo"
    cv2.namedWindow(nome_janela, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(nome_janela, 500, 350)

    
    if tipo == "Detectar Garrafa":
        model = YOLO("yolov8n.pt")
        pygame.mixer.music.load(SOM_ARQUIVO)
        pygame.mixer.music.play(-1)  # Loop infinito
        pygame.mixer.music.pause()   

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = model(frame_rgb)
            garrafa_detectada = False

            for r in results:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    name = model.names[cls_id]
                    if name == "bottle" and conf > 0.5:
                        garrafa_detectada = True
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                        cv2.putText(frame,f"{name}: {conf:.2f}",(x1,y1-10),
                                    cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)

            
            if garrafa_detectada:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()

            frame = cv2.resize(frame,(500,350))
            cv2.imshow(nome_janela, frame)

            if cv2.waitKey(25)&0xFF==ord('q'):
                break

        pygame.mixer.music.stop()
        cap.release()
        cv2.destroyAllWindows()

    else:
      
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame,(500,350))
            if tipo=="cinza":
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            elif tipo=="negativo":
                frame = cv2.bitwise_not(frame)
            elif tipo=="binario":
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                _, frame = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
            cv2.imshow(nome_janela, frame)
            if cv2.waitKey(25)&0xFF==ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

def nova_janela2():
    nova = tk.Toplevel(janela)
    nova.title("Vídeo")
    nova.geometry("500x200")
    frame_botoes = tk.Frame(nova)
    frame_botoes.pack()

    tk.Button(frame_botoes, text="Cinza", command=lambda: carregar_video("cinza")).grid(row=0,column=0,padx=5,pady=10)
    tk.Button(frame_botoes, text="Negativo", command=lambda: carregar_video("negativo")).grid(row=0,column=1,padx=5,pady=10)
    tk.Button(frame_botoes, text="Binário", command=lambda: carregar_video("binario")).grid(row=0,column=2,padx=5,pady=10)
    tk.Button(frame_botoes, text="Detectar Garrafa", command=lambda: carregar_video("Detectar Garrafa")).grid(row=1,column=0,padx=5,pady=10)



def camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Não foi possível abrir a webcam")
        return

    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        frame = cv2.resize(frame, (500, 350))
        cv2.imshow("Detecção de Rosto", frame)

        if cv2.waitKey(1) & 0xFF == 27:  
            break

    cap.release()
    cv2.destroyAllWindows()



tk.Button(janela, text="Carregar Imagem", command=escolher_arquivo).grid(row=0,column=0,padx=5,pady=10)
tk.Button(janela, text="Carregar Vídeo", command=nova_janela2).grid(row=0,column=1,padx=5,pady=10)
tk.Button(janela, text="Camera", command=camera).grid(row=0,column=2,padx=5,pady=10)

janela.mainloop()
