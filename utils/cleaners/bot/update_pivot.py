#!/usr/bin/env python3
import pickle

import pandas as pd
import numpy as np

from pathlib import Path
from datetime import datetime

import sys
temp = sys.stdout                 # store original stdout object for later
sys.stdout = open('log_pivot.txt', 'w') # redirect all prints to this log file

## Estudiantes

ruta =Path(__file__).parent
archivo_descargable = ruta.parent.parent.parent/"data/descargables/"
print(ruta)
df = pd.DataFrame(columns=['N registro','Instrumento','Código IE','ID'])

columnas_pivot = set(df.columns)
archivos = list(archivo_descargable.glob("*.xlsx"))
df_temp=pd.read_excel(archivos[0])
for file in archivos:
    df_temp = pd.read_excel(file)
    if len(columnas_pivot.difference(set(df_temp.columns))) > 0:
        print('Error!! ', file.name)
        print(columnas_pivot.difference(set(df_temp.columns)))
    else:
        df = pd.concat([df,df_temp],ignore_index=True, join='inner')

print(df.head())

pivot = df.pivot_table(index='Código IE',columns='Instrumento', values='ID', aggfunc= 'count')
pivot=pivot.reset_index()
print('Tamaño pivot', pivot.shape)

pivot=pivot.fillna(0)
pivot['Fecha'] =pd.Timestamp.today()
pivot['Fecha']=pivot['Fecha'].dt.strftime("%d-%m-%Y")

pivot['Estado']="En proceso"
pivot.loc[(pivot["Encuesta estudiantes"]>20)&(pivot['Encuesta docentes']>10)&(pivot['Encuesta Planes de estudio']==1)&(pivot['Encuesta Líderes']==1)&(pivot['Encuesta Directivos']>1)&(pivot['Encuesta Equipos']==1),'Estado']='Completado'

pivot2=pivot.copy()

pivot2["Porcentaje Cumplimiento Estudiantes"]=(pivot2["Encuesta estudiantes"]/20)*100 #>20
pivot2["Porcentaje Cumplimiento Docentes"]=(pivot2["Encuesta docentes"]/10)*100 #>10
pivot2["Porcentaje Cumplimiento Directivos"]=(pivot2["Encuesta Directivos"]/2)*100 #>1
pivot2["Porcentaje Cumplimiento Equipos"]=(pivot2["Encuesta Equipos"]/1)*100
pivot2["Porcentaje Cumplimiento Planes de Área"]=(pivot2["Encuesta Planes de estudio"]/1)*100
pivot2["Porcentaje Cumplimiento Líderes"]=(pivot2["Encuesta Líderes"]/1)*100

new_names= ['Código IE',
 'Encuesta Directivos', 'Porcentaje Cumplimiento Directivos',
 'Encuesta Equipos',  'Porcentaje Cumplimiento Equipos',
 'Encuesta Líderes',  'Porcentaje Cumplimiento Líderes',
 'Encuesta Planes de estudio', 'Porcentaje Cumplimiento Planes de Área',
 'Encuesta docentes',  'Porcentaje Cumplimiento Docentes',
 'Encuesta estudiantes',  'Porcentaje Cumplimiento Estudiantes',
 'Estado']
pivot2=pivot2.reindex(new_names,axis='columns')

columnasporcentaje=pivot2.filter(regex='Porcentaje').columns
pivot2.loc[:,columnasporcentaje]=(pivot2.loc[:,columnasporcentaje]).clip(0,100)
pivot2['Porcentaje de completitud']=(pivot2['Porcentaje Cumplimiento Estudiantes']*(1/6))+(pivot2['Porcentaje Cumplimiento Equipos']*(1/6))+(pivot2['Porcentaje Cumplimiento Líderes']*(1/6))+(pivot2['Porcentaje Cumplimiento Docentes']*(1/6))+(pivot2['Porcentaje Cumplimiento Planes de Área']*(1/6))+(pivot2['Porcentaje Cumplimiento Directivos']*(1/6))

archivo_pivot2 = ruta.parent.parent.parent/"data/descargables/Instrumentos_DetalleCFK.xlsx"
archivo_pivot = ruta.parent.parent.parent/"data/descargables/InstrumentosCFK.xlsx"
pivot2.to_excel(archivo_pivot2)
pivot.to_excel(archivo_pivot)
sys.stdout.close()                # ordinary file object
sys.stdout = temp