#!/usr/bin/env python3
import pickle

import pandas as pd

from pathlib import Path
from datetime import datetime

import sys
temp = sys.stdout                 # store original stdout object for later
sys.stdout = open('log_desconectadas_est.txt', 'w') # redirect all prints to this log file

## Estudiantes

ruta =Path(__file__).parent

ruta_eliminados = "eliminados/Eliminados_estudiantes.xlsx"
ruta_eliminados = ruta/ruta_eliminados
ruta_descargable = ruta.parent.parent.parent/"data/descargables/EstudiantesCFK.xlsx"

ruta_desconectadas = ruta.parent/'Desconectadas/Estudiantes desconectadas.xlsx'
ruta_desc_eliminados = ruta.parent/'Desconectadas/Eliminados_Estudiantes_Desconectadas.xlsx'

#ruta_unido_descargable = ruta.parent.parent.parent/"data/descargables/EstudiantesCFK.xlsx"
auto_d = pd.read_excel(ruta_descargable)
desc_d = pd.read_excel(ruta_desconectadas)

unidos_d = pd.concat([auto_d, desc_d])

columnas_a_rellenar = unidos_d.filter(regex='^(?!.*Comentarios|Nombre|Tipo de discapacidad).*$').columns
unidos_d[columnas_a_rellenar] = unidos_d[columnas_a_rellenar].fillna(method='ffill')

print('Tamaño final descargables: ', unidos_d.shape)

auto_e = pd.read_excel(ruta_eliminados)
desc_e = pd.read_excel(ruta_desc_eliminados)

unidos_e = pd.concat([auto_e, desc_e])

print('Tamaño final eliminados: ', unidos_e.shape)

unidos_e.to_excel(ruta_eliminados, index=False)
unidos_d.to_excel(ruta_descargable,index=False)
         # again nothing appears. it's written to log file instead
sys.stdout.close()                # ordinary file object
sys.stdout = temp
