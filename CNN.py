import cv2
import os
import glob
import math


def procesar_lote_videos_split(ruta_carpeta, carpeta_base_destino, limite_videos=10, cada_n_frames=30):
    ruta_real_origen = os.path.join("..", ruta_carpeta)
    todos = glob.glob(os.path.join(ruta_real_origen, "*.mp4")) # glob() busca archivos terminados en .mp4(videos)

    print(f"Buscando videos en: {os.path.abspath(ruta_real_origen)}")

    # VALIDACIÓN DE CANTIDAD PERMITIDA
    if limite_videos > len(todos):
        print(f"\nERROR: Cantidad de videos no disponible.")
        print(f"Solicitaste {limite_videos} videos, pero la carpeta solo contiene {len(todos)}.")
        return  # Sale de la función y no ejecuta nada más

    lote = todos[:limite_videos] # del video 0 hasta el limite colocado
    corte_train = math.ceil(len(lote) * 0.8) #Split

    for i, ruta in enumerate(lote): #Enumera y la direccion del video
        sub = "train" if i < corte_train else "test" #Si la cantidad es menor al 80% va train si lo pasa a test

        #Ruta de destino
        destino = os.path.join("..", "data", "processed", sub, carpeta_base_destino)

        # Validación de carpeta
        if not os.path.exists(destino):
            print(f"ERROR: La carpeta de destino no existe: {os.path.abspath(destino)}")
            print("Por favor, créala manualmente antes de continuar.")
            return

        cap = cv2.VideoCapture(ruta) #Abre el archivo
        nombre = os.path.basename(ruta).split('.')[0] #Nombra el fotograma
        f_idx, guardados = 0, 0  #Contador

        while True:
            ret, frame = cap.read()
            if not ret: break

            # Salto de seguridad (f_idx > 15) para evitar el inicio negro
            if f_idx % cada_n_frames == 0 and f_idx > 15: #cada_n_frames: Guarda un frame cada 1 segundo, f_idx > 15: ignora primeros 15 segundos
                # Nombre del archivo:
                ruta_final = os.path.join(destino, f"{nombre}_f{f_idx}.jpg")
                cv2.imwrite(ruta_final, frame) #oma la matriz de píxeles y la convierte en un archivo real.
                guardados += 1
            f_idx += 1

        cap.release() #Avisa si está siendo usado por otro programa
        print(f" -> {sub.upper()}: {nombre} ({guardados} fotos)") #proceso visual en la consola




