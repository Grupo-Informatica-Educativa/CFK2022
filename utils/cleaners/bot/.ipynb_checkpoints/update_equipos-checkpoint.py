#!/usr/bin/env python3
import pickle

import pandas as pd
import numpy as np

from pathlib import Path
from datetime import datetime

import sys
temp = sys.stdout                 # store original stdout object for later
sys.stdout = open('log_equipos.txt', 'w') # redirect all prints to this log file

## Estudiantes

ruta =Path(__file__).parent


sheet_id = "1VmeS6Ns0j4bxKPxLlQtQKVrUVMARhsljf6qVvqfrlfo"
sheet_name = "Form Responses 1"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
url = url.replace(" ", "%20")

df0=pd.read_csv(url)

# with open(ruta/'columnas_Lideres.pkl', 'rb') as handle:
#     dict_col_est = pickle.load(handle)
#
# df0 = df0.rename(columns=dict_col_est)
# df0 = df0.drop(columns=df0.filter(regex=r'eliminar').columns)

df0['N registro']=df0.index


df0['Timestamp'] = pd.to_datetime(df0['Timestamp'])
df0['Fecha'] = df0.Timestamp.dt.strftime('%d/%m')
print(df0['Fecha'][-5:])

df0 = df0.drop(columns='Timestamp')

df6=df0.copy()
df6['Instrumento']="Encuesta Equipos"

df6 = df6[df6['N registro']>0]

df6=df6.rename(columns={'Código de la Institución Educativa, provisto por el proyecto':'Código IE'})

df6=df6.drop([15,16,18,36,72,79,125,134,147,153,204,206,208,223,226],axis=0)

df6.loc[(df6['N registro']==125),'Código IE'] = 39
df6.loc[(df6['N registro']==228),'Código IE'] = 126

df6=df6.dropna(subset=['Código IE'],inplace=False)

df6['Código IE']=df6['Código IE'].astype(int)
df6=df6[df6['Código IE']<271]
df6=df6[df6['Código IE'] > 0]
df6['Código IE']=df6['Código IE'].astype(str)
df6['Código IE']=df6['Código IE'].str.zfill(3)

df6['ID']=df6.index

new_index = ['N registro', 'Fecha', 'Instrumento', 'Código IE','ID','Email Address',
       '¿Cuántas aulas de informática tiene la sede?',
       'Además de los equipos de cómputo en aulas de informática, ¿hay computadores en las aulas de clase?',
       '¿Cuántas de las aulas de clase, diferentes al aula de informática, cuentan con al menos un computador?',
       '¿Hay algún otro tipo de dispositivos en las aulas de clase? Marque todas las opciones que apliquen',
       '¿Hay algún tipo de infraestructura de telecomunicaciones? Marque todas las opciones que apliquen',
       'Agregue cualquier comentario u observación adicional que tenga sobre las preguntas anteriores',
       '¿Cuántos computadores portátiles y/o de escritorio hay, en total, en las aulas de informática?',
       '¿Cuántos de los computadores portátiles y/o de escritorio son funcionales?',
       '¿Cuántos de estos computadores tienen instalado el MakeCode?',
       '¿Tienen acceso a internet los computadores portátiles y/o de escritorio de la sala?',
       '¿Qué sistema operativo tienen instalado los equipos portátiles y/o de escritorio de la sala?',
       '¿Cuántos de los equipos portátiles y/o de escritorio tienen instalada la aplicación GreenTIC?',
       '¿Qué tipos de programas se encuentran instalados en los computadores de la sala? (Marque todas las opciones que cuenten con, al menos, un programa instalado en la mayoría de los equipos de cómputo)',
       '¿Tiene comentarios adicionales sobre los equipos portátiles y/o de escritorio, o del software disponibles en la sede?',
       '¿Hay tabletas disponibles para uso de los estudiantes, en el aula?',
       '¿Cuántas tabletas funcionales hay en el aula?',
       '¿Las tabletas se pueden conectar a internet?',
       '¿Cuántas tabletas tienen instalada la aplicación GreenTIC?',
       'Indique los diferentes tipos de microprocesadores que hay disponibles para el desarrollo de proyectos de computación física.',
       '¿Cuántas tarjetas micro:bit funcionales hay en la sede?',
       'Indique los elementos para desarrollo de proyectos de computación física que hay disponibles en la sede.',
       'Amplíe sus comentarios sobre elementos disponibles en la sede, para el desarrollo de proyectos de computación física.',
       '¿Se cuenta al menos con una impresión de la versión desconectada de GreenTIC?',
       '¿Hay, al menos, un kit de Ruta STEM disponible en la sede?',
       '¿Hay algún otro tipo de materiales desconectados para promover el pensamiento computacional?',
       'Amplíe sus comentarios sobre los elementos desconectados disponibles en la sede.'
       ]
df0=df0.reindex(new_index, axis='columns')
df6=df6.reindex(new_index, axis='columns')

registroseliminados=set(df0['N registro']).difference(set(df6['N registro']))
dfe=df0[df0['N registro'].isin(registroseliminados)]


archivo_eliminados = "eliminados/Eliminados_equipos.xlsx"
archivo_eliminados = ruta/archivo_eliminados

archivo_descargable = ruta.parent.parent.parent/"data/descargables/RecursosCFK.xlsx"
dfe.to_excel(archivo_eliminados, index=False)
df6.to_excel(archivo_descargable,index=False)

print('Publicados ', df6.shape)
print('Eliminados ', dfe.shape)
sys.stdout.close()                # ordinary file object
sys.stdout = temp
