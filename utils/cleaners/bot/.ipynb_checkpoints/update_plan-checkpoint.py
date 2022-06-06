#!/usr/bin/env python3
import pickle

import pandas as pd
import numpy as np

from pathlib import Path
from datetime import datetime

import sys
temp = sys.stdout                 # store original stdout object for later
sys.stdout = open('log_plan.txt', 'w') # redirect all prints to this log file

## Estudiantes

ruta =Path(__file__).parent


sheet_id = "1FapfBl5ms4afAa4OeagWut37sMKQMwG74gEcYVg7sOA"
sheet_name = "Form Responses 1"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
url = url.replace(" ", "%20")

df0=pd.read_csv(url)

with open(ruta/'columnas_PlanEstudios.pkl', 'rb') as handle:
    dict_col_est = pickle.load(handle)

df0 = df0.rename(columns=dict_col_est)
df0 = df0.drop(columns=df0.filter(regex=r'eliminar').columns)

df0['N registro']=df0.index

df0['Timestamp'] = pd.to_datetime(df0['Timestamp'])
df0 = df0[df0.Timestamp>'2022-04-14']
df0['Fecha'] = df0.Timestamp.dt.strftime('%d/%m')
print(df0['Fecha'][-5:])

df0 = df0.drop(columns='Timestamp')

df7=df0.copy()
df7['Instrumento']="Encuesta Planes de estudio"
#df7=df7.rename(columns={'Código de la institución educativa asignado por el proyecto':'Código IE'})
df7=df7.dropna(subset=['Código IE'],inplace=False)

df7=df7.drop([114],axis=0)

df7['Código IE']=df7['Código IE'].astype(int)
df7=df7[df7['Código IE']<253]
df7=df7[df7['Código IE'] > 0]
df7['Código IE']=df7['Código IE'].astype(str)
df7['Código IE']=df7['Código IE'].str.zfill(3)
print('Códigos después de filtrar: ', df7['Código IE'].unique())
print('Columnas ', df7.columns)
df7['ID']=df7.index
new_index = [ 'N registro', 'Instrumento','Fecha', 'Código IE','ID',
       '1.1 En el plan de estudios se especifica como responsables de su elaboración a los docentes encargados del área',
       '1.2 El plan de estudio incluye actividades básicas de ofimática y/o alfabetización digital, y de programación y/o desarrollo del pensamiento computacional.',
       '1.3 En el plan de estudio se da mayor relevancia al pensamiento computacional',
       '1.4 El plan de estudio del área promueve la transición desde la alfabetización digital a las ciencias de la computación.',
       '1.5 El plan de estudios del área le permite al docente destacar la importancia del pensamiento computacional y su influencia en la formación de los estudiantes',
       '1.6 El plan de estudios del área es coherente con la transición de un grado a otro y permite al estudiante desarrollar conocimientos, habilidades y comprensión del pensamiento computacional',
       '1.7 El plan de estudios del área incluye trabajo práctico para el desarrollo del pensamiento computacional.',
       '1.8 El plan de estudio del área plantea espacios en los que personas que trabajan en ocupaciones relacionadas con áreas STEM socialicen sus experiencias con los/las estudiantes',
       '1.9 El plan de estudio incluye actividades transversales con áreas No-STEM, para el desarrollo del pensamiento computacional',
       '1.10 El plan de estudio considera aspectos para la inclusión de estudiantes con trastornos de aprendizaje y/o discapacidad',
       '1.11 Entre los responsables del plan de estudios del área y los recursos educativos se incluye personal experto en la atención a estudiantes con necesidades educativas especiales',
       '1.12 El plan de estudios del área hace explícita la pedagogía a utilizar y las adaptaciones para estudiantes con trastornos del aprendizaje y/o con discapacidad',
       '1.13 El plan de estudio del área cuenta con una estructura clara que permite disminuir las diferencias en el desempeño de niños y niñas',
       'Comentarios P1', 'Información otro plan de estudios',
       'Misión de la institución educativa',
       'Visión de la institución educativa']


df0=df0.reindex(new_index, axis='columns')
df7=df7.reindex(new_index, axis='columns')

registroseliminados=set(df0['N registro']).difference(set(df7['N registro']))
dfe=df0[df0['N registro'].isin(registroseliminados)]


archivo_eliminados = "eliminados/Eliminados_plan.xlsx"
archivo_eliminados = ruta/archivo_eliminados

archivo_descargable = ruta.parent.parent.parent/"data/descargables/PlanCFK.xlsx"
dfe.to_excel(archivo_eliminados, index=False)
df7.to_excel(archivo_descargable,index=False)
print('Publicados ', df7.shape)
print('Eliminados ', dfe.shape)
sys.stdout.close()                # ordinary file object
sys.stdout = temp
