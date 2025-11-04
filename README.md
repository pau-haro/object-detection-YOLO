# PROYECTO EXPERIMENTAL DE DETECCIÓN DE OBJETOS

Este proyecto se basará en el entrenamiento de **YOLO** para detección de objetos.

## REQUISITOS PREVIOS

Para poder hacer este proyecto de manera eficaz, se recomienda disponer de Anaconda, un gestor de entornos python que nos permite disponer de las versiones óptimas tanto de python como de las librerías para que el programa funcione sin fallos de incompatibilidad entre librerías.

Por ello, el primer paso es tener Anaconda instalado en nuestro dispositivo, en caso de no tenerlo, puedes descargarlo desde [este enlace](https://www.anaconda.com/download).

Una vez instalado creamos el entorno de python desde el que trabajaremos mediante el siguiente comando (**en caso de no tenerlo ya creado**), el cual se ha de ejecutar desde Anaconda prompt, o desde un powershell habilitado para ejecución de comandos Anaconda: 

```bash

# Creamos el entorno indicando el nombre y la versión de python deseada
conda create --name nombreEntorno python=3.12

```

Lo siguiente una vez creado es activarlo, que podemos hacer de la siguiente manera:

```bash

# Activar el entorno creado
conda activate nombreEntorno

```

Y una vez probado todo, desactivar el entorno:

```bash

# Desactivar el entorno creado
conda deactivate

```

## ETIQUETADO DE LAS IMÁGENES

Para el etiquetado de las imágenes utilizarmos una herramienta de python de código abierto que llamada label studio, que se instalaría de la siguiente manera (como puede verse también en la [página oficial](https://labelstud.io/)):

```bash

# Instalamos los paquetes dentro del entorno python en de Anaconda
pip install -U label-studio

# Lo lanzamos a ejecución
label-studio

```

Una vez lanzado a ejecución, se nos abrirá una ventana en el navegador como la que se ve a continuación:

![Ventana de inicio](src/image.png)

Como se ve, esto se lanza en un servidor local, por lo que lo ideal es registrarse con un correo inventado, ya que no requiere de verificación al tratarse de un daemon al que únicamente nos podemos conectar de manera local.

Una vez registrado, el siguiente paso es iniciar sesión con el correo y contraseña del registro, y accederemos a la ventana de los proyectos:

![Ventana de proyectos](src/image-1.png)

En esta ventana tendríamos que crear el proyecto y añadir las imágenes que deseamos etiquetar, que, idealmente tendríamos que tener en una carpeta.

Para ello, le damos a crear proyecto, indicamos el nombre, añadimos las miestras, y antes de guardar, nos dirigimos al apartado de "Labeling Setup", y seleccionar la opción de "object detection with bounding boxes", como se ve en la siguiente imagen.

![Labeling Setup](src/image-2.png)

Una vez guardamos, el siguiente paso es etiquetar los objetos cen sus respectivas clases, para ello, seleccionamos la imagen, y se abrirá un menú, seleccionaremos la clase del objeto, y recuadraremos el objeto correspondiente como se puede ver en la imagen.

![Objeto etiquetado en la imagen](src/image-3.png)

Una vez etiquetadas, exportamos el proyecto desde el menú principal del proyecto de las imágenes etiquetadas (formato YOLO with images), nos lo descargará en formato .zip, lo recomendable es almacenarlo en la carpeta de imágenes del proyecto

## ENTRENAMIENTO DEL MODELO

En este proyecto se usa [Ultralytics](https://docs.ultralytics.com/es/) para entrenar YOLO11, YOLOv8 o YOLOv5 en detección de objetos con un dataset custom. La finalidad de este proyecto es tener un código funcional para entrenar nuestro propio modelo YOLO para correr desde nuestro propio PC, teléfono o incluso en una Raspberry Pi.

El primer paso es renombrar el archivo comprimido a data.zip y añadirlo a la carpeta raíz de nuestro proyecto, donde lo extraeremos.

El siguiente paso es ejecutar el código train_val_split.py para dividir el dataset en train y validation, al cual le tenemos que pasar como aprgumentos la ruta de la carpeta generada al descomprimir data.zip y el porcentaje de datos que queremos en la carpeta de training (sobre 1, ej: 0.8 ), este último es opcional porque se pone a .8 como defaultValue. Este código se encuentra en la carpeta /code.

```bash

# División del conjunto
python .\train_val_split.py --datapath="..\data" --train_pct=0.9    # Ubicados en la carpeta del script

```

Después de esto, es necesario instalar la librería de ultralytics para poder entrenar nuestro modelo YOLO.

```bash

# Instalación de la librería
pip install ultralytics

```