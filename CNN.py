import cv2
import os
import glob
import math
import numpy as np


def procesar_lote_videos_split(ruta_carpeta, carpeta_base_destino, limite_videos=10, cada_n_frames=30, umbral=2.5,
                               max_fotos_video=40):
    ruta_real_origen = os.path.join("..", ruta_carpeta)
    todos = glob.glob(os.path.join(ruta_real_origen, "*.mp4")) #Lista de todos los archivos terminados en .mp4

    # Limite de videos procesados
    if limite_videos > len(todos): #Limite de videos procesados
        print(f"ERROR: Solo hay {len(todos)} videos disponibles.")
        return

    lote = todos[:limite_videos]
    corte_train = math.ceil(len(lote) * 0.8) # Train y test division

    for i, ruta in enumerate(lote): # Envio a carpeta test y train
        sub = "train" if i < corte_train else "test"
        destino = os.path.join("..", "data", "processed", sub, carpeta_base_destino)

        if not os.path.exists(destino):
            os.makedirs(destino, exist_ok=True)  # Verificación y crea la carpeta si no existe

        cap = cv2.VideoCapture(ruta)
        nombre = os.path.basename(ruta).split('.')[0]
        f_idx, guardados = 0, 0

        # Detección de movimiento
        ret, prev_frame = cap.read()
        if not ret: continue
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

        while True: #Empieza a leer el video cuadro por cuadro hasta que se acabe.
            ret, frame = cap.read()
            if not ret: break

            # Evalua cada N frames y si no ha llegado al límite por video
            if f_idx % cada_n_frames == 0 and f_idx > 15 and guardados < max_fotos_video:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Cálculo de movimiento
                flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
                mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
                intensidad = mag.mean()

                if intensidad > umbral:
                    ruta_final = os.path.join(destino, f"{nombre}_f{f_idx}.jpg")
                    cv2.imwrite(ruta_final, frame)
                    guardados += 1

                prev_gray = gray

            f_idx += 1

        cap.release()
        print(f" -> {sub.upper()}: {nombre} ({guardados} fotos)")


def vaciar_contenido():
    # Ruta base donde están train y test
    ruta_base = "../data/processed"
    categorias = ["Normal", "Asaltos", "Pelea", "Vandalismo"]

    for sub in ["train", "test"]:
        for cat in categorias:
            # Construccion de la ruta:
            ruta_carpeta = os.path.join(ruta_base, sub, cat)

            # Solo actuamos si la carpeta ya existe
            if os.path.exists(ruta_carpeta):
                archivos = os.listdir(ruta_carpeta)
                for archivo in archivos:
                    ruta_archivo = os.path.join(ruta_carpeta, archivo)
                    # Solo borramos si es un archivo (ignora carpetas internas si las hubiera)
                    if os.path.isfile(ruta_archivo):
                        os.remove(ruta_archivo)
                print(f"Contenido eliminado de: {sub}/{cat}")
            else:
                print(f"Saltando: {sub}/{cat} (La carpeta no existe)")





