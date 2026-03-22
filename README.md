# SmartCityIA

Desarrollar un sistema inteligente que ayude a las autoridades de seguridad pública a detectar actividad sospechosa en imágenes de cámaras CCTV, predecir zonas de mayor incidencia delictiva y emitir alertas preventivas en tiempo real usando modelos CNN y RNN/LSTM en Python.

-   **Módulo CNN** — Clasifica frames de cámaras CCTV en categorías de actividad (Normal, Pelea, Asaltos, Vandalismo).
-   **Módulo RNN/LSTM** — Predice zonas y horarios de mayor incidencia delictiva usando series temporales de datos del OIJ.

------------------------------------------------------------------------

## 🗂️ Estructura del Proyecto

```         
SmartCityIA/
├── CNN.py                        ← Funciones de extracción de frames con OpenCV
├── notebooks/
│   ├── 01_EDA.ipynb              ← Análisis exploratorio de datos
│   ├── 02_CNN_CCTV.ipynb         ← Entrenamiento del modelo CNN
│   └── 03_RNN_Incidencias.ipynb  ← Entrenamiento del modelo RNN/LSTM
├── data/
│   ├── raw/                      ← Videos originales del dataset UCF-Crime
│   └── processed/
│       ├── train/
│       │   ├── Normal/
│       │   ├── Asaltos/
│       │   ├── Pelea/
│       │   └── Vandalismo/
│       └── test/
│           ├── Normal/
│           ├── Asaltos/
│           ├── Pelea/
│           └── Vandalismo/
├── models/                       
├── src/                          ← Código fuente auxiliar
├── api/                          ← Endpoints REST con FastAPI
├── app/                          ← Interfaz demo con Streamlit
└── requirements.txt
```

------------------------------------------------------------------------

## 🎬 Preparación de datos — Módulo CNN

### Dataset

**UCF-Crime Dataset** — Videos de vigilancia con escenas normales y criminales.

-   Kaggle: [mission-ai/crimeucfdataset](https://www.kaggle.com/datasets/mission-ai/crimeucfdataset)
-   UCF: [Real-World Anomaly Detection](https://crcv.ucf.edu/research/real-world-anomaly-detection-in-surveillance-videos/)

### Mapeo de carpetas del dataset a clases del proyecto

| Carpeta UCF-Crime      | Clase en SmartCityIA |
|------------------------|----------------------|
| `Normal_Videos_event/` | Normal               |
| `Fighting/`            | Pelea                |
| `Assault/`             | Asaltos              |
| `Arson/`, `Vandalism/` | Vandalismo           |

### Extracción de frames

Desde la carpeta `notebooks/`, ejecutar en el notebook `02_CNN_CCTV.ipynb`:

``` python
from CNN import procesar_lote_videos_split, vaciar_contenido

# Limpiar carpetas
vaciar_contenido()

# Extraer frames por clase
procesar_lote_videos_split(
    ruta_carpeta="data/raw/Normal-Videos-Part-1",
    carpeta_base_destino="Normal",
    limite_videos=50,
    cada_n_frames=10,
    umbral=0.0,
    max_fotos_video=20
)
```

La función `procesar_lote_videos_split` divide automáticamente los videos en **80% train / 20% test** y usa flujo óptico para filtrar frames con movimiento relevante.

------------------------------------------------------------------------

## 🏫 Información Académica

**Institución:** Colegio Universitario de Cartago (CUC)\
**Curso:** Inteligencia Artificial\
**Proyecto:** Proyecto 2 — Smart City IA\
**Integrantes:** - Camila Jiménez, - Roberto Coto, - Kendall Solano, - Wedell Orozco

------------------------------------------------------------------------

## 📄 Licencia

Este proyecto es de uso académico. Dataset UCF-Crime sujeto a los términos de uso.
