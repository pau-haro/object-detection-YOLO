'''
Funciones python para crear automáticamente el archivo de configuración data.yml

1. Lee "classes.txt" para obtener la lista de los nombres de las clases
2. Crea el diccionario de los datos con las rutas a las carpetas, número de clases y nombre de las clases
3. Escribe el archivo de configuración en formato YAML
'''

import yaml
import os

def create_data_yaml(path_to_classes_txt, path_to_data_yaml):
    # Lee class.txt para obtener el nombre de las clases
    if not os.path.exists(path_to_classes_txt):
        print(f'no se encuentra el archivo classes.txt! Por favor crea un mapa de etiquetas classes.txt y muévelo a {path_to_classes_txt}')
        return
    
    with open(path_to_classes_txt, 'r') as f:
        classes = []
        for line in f.readlines():
            if len(line.strip()) == 0:
                continue
            classes.append(line.strip())
        number_of_classes = len(classes)

    # Crea el diccionario de datos
    data = {
        'path': '../../data',
        'train': 'train/images',
        'val': 'validation/images',
        'nc': number_of_classes,
        'names': classes
    }

    # Escribe los datos en el archivo YAML
    with open(path_to_data_yaml, 'w') as f:
        yaml.dump(data, f, sort_keys=False)
        print(f'✅ Created config file at {path_to_data_yaml}')

    return

# Definición de las rutas y ejecución de la función
path_to_classes_txt = '../data/classes.txt'     # Ruta al archivo classes.txt
path_to_data_yaml = '../data/config/data.yaml'         # Ruta donde queremos almacenar data.yml

create_data_yaml(path_to_classes_txt, path_to_data_yaml)    # Ejecuta la función creada con las rutas indicadas

# Muestra por terminal el resultaod de la ejecución del código
print('\nFile contents:\n')
with open(path_to_data_yaml, 'r') as f:
    print(f.read())


'''
Autor: Pau Haro 
Propietario: @TSE TECHNOLOGY SOLUTIONS

Se permite el libre uso de este código, con mención al autor/es y propietario/s del mismo
'''