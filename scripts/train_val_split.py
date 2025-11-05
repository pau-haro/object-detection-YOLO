'''
    Este código pretende dividir el conjunto de datos en carpetas de entrenamiento y validación
'''

# Importamos las librerías necesarias para la división del conjunto
from pathlib import Path
import random
import os
import sys
import shutil
import argparse

'''
    Definición del parser para identificar argumentos de entrada del usuario
    para la división del conjunto de datos
'''
parser = argparse.ArgumentParser(description="Script para dividir dataset en train/val")
parser.add_argument('--datapath', help='Ruta a la carpeta de datos que contiene los archivos de imagen y anotación',
                    required=True)
parser.add_argument('--train_pct', help='Proporción de imágenes que se envían a la carpeta de entrenamiento; \
                    el resto se envía a la carpeta de validación (ejemplo: ".8")',
                    default=.8)

# Con parser.parse_args() corre el analizador y coloca los datos en un objeto argparse.Namespace
args = parser.parse_args()

# Almacenamos en variables los valores de entrada introducidos por el usuario
data_path = args.datapath
train_percent = float(args.train_pct)

'''
    En este paso comprobamos si son válidos los valores de entrada:

    --> Si el path introducido no es válido (no encuentra los datos)
    --> El porcentaje de entrenamiento está por debajo del 1% o por encima del 99% (no tendría sentido)
'''
if not os.path.isdir(data_path):    ## Caso de no encontrar el directorio indicado por el usuario
  print('Directorio especificado en --datapath no encontrado. Verifica que la ruta es correcta (y utiliza barras invertidas dobles si es un sistema en Windows) y prueba de nuevo.')
  sys.exit(0)
if train_percent < .01 or train_percent > 0.99:     ## Caso en el que el valor de training introducido no cumple con las condiciones indicadas
  print('Entrada inválida para train_pct. Por favor, introduce un número entre .01 y .99.')
  sys.exit(0)
val_percent = 1 - train_percent

# Definición de la ruta del dataset de entrada
input_image_path = os.path.join(data_path,'images')
input_label_path = os.path.join(data_path,'labels')

# Ruta a las carpetas de las imágenes y archivos de anotación
cwd = os.getcwd()   # Obtiene el directorio actual de trabajo
train_img_path = os.path.join(cwd,'../data/train/images')
train_txt_path = os.path.join(cwd,'../data/train/labels')
val_img_path = os.path.join(cwd,'../data/validation/images')
val_txt_path = os.path.join(cwd,'../data/validation/labels')

# Crea los directorios si no existen
for dir_path in [train_img_path, train_txt_path, val_img_path, val_txt_path]:
  if not os.path.exists(dir_path):
    os.makedirs(dir_path)
    print(f'Carpeta creada en {dir_path}.')

# Obtenemos lista de todas las imágenes y archivos de anotación
img_file_list = [path for path in Path(input_image_path).rglob('*')]
txt_file_list = [path for path in Path(input_label_path).rglob('*')]

print(f'Number of image files: {len(img_file_list)}')
print(f'Number of annotation files: {len(txt_file_list)}')

# Definimos el número de archivos que hay que mover a cada carpeta
file_num = len(img_file_list)
train_num = int(file_num*train_percent)
val_num = file_num - train_num
print('Images moving to train: %d' % train_num)
print('Images moving to validation: %d' % val_num)

# Selecciona archivos aleatoriamente y los copia en las carpetas de train o val
for i, set_num in enumerate([train_num, val_num]):
  for ii in range(set_num):
    img_path = random.choice(img_file_list)
    img_fn = img_path.name
    base_fn = img_path.stem
    txt_fn = base_fn + '.txt'
    txt_path = os.path.join(input_label_path,txt_fn)

    if i == 0: # Copia el primer conjunto de archivos a la carpeta de train
      new_img_path, new_txt_path = train_img_path, train_txt_path
    elif i == 1: # Copia el segundo conjunto de archivos a la carpeta de val
      new_img_path, new_txt_path = val_img_path, val_txt_path

    shutil.copy(img_path, os.path.join(new_img_path,img_fn))
    #os.rename(img_path, os.path.join(new_img_path,img_fn))
    if os.path.exists(txt_path): # Si la ruta del archivo txt no existe, se trata de una imagen de fondo, por lo que se omite el archivo txt.
      shutil.copy(txt_path,os.path.join(new_txt_path,txt_fn))
      #os.rename(txt_path,os.path.join(new_txt_path,txt_fn))

    img_file_list.remove(img_path)

# Eliminar carpetas del dataset sin dividir --> Por aseo
shutil.rmtree(os.path.join(cwd, '../data/images'))
shutil.rmtree(os.path.join(cwd, '../data/labels'))