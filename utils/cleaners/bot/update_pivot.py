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
pivot.loc[(pivot["Encuesta estudiantes"]>19)&(pivot['Encuesta docentes']>9)&(pivot['Encuesta Planes de estudio']>0)&(pivot['Encuesta Líderes']>0)&(pivot['Encuesta Directivos']>0)&(pivot['Encuesta Equipos']>0),'Estado']='Completado'

pivot.loc[(pivot['Código IE']==83),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==87),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==227),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==248),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==31),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==33),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==74),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==99),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==100),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==101),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==102),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==103),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==104),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==105),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==111),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==141),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==142),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==144),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==197),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==200),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==201),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==203),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==219),'Estado']= 'Completado'
pivot.loc[(pivot['Código IE']==221),'Estado']= 'Completado'

pivot2=pivot.copy()

pivot2["Porcentaje Cumplimiento Estudiantes"]=(pivot2["Encuesta estudiantes"]/20)*100 #>20
pivot2["Porcentaje Cumplimiento Docentes"]=(pivot2["Encuesta docentes"]/10)*100 #>10
pivot2["Porcentaje Cumplimiento Directivos"]=(pivot2["Encuesta Directivos"]/1)*100 #>1
pivot2["Porcentaje Cumplimiento Equipos"]=(pivot2["Encuesta Equipos"]/1)*100
pivot2["Porcentaje Cumplimiento Planes de Área"]=(pivot2["Encuesta Planes de estudio"]/1)*100
pivot2["Porcentaje Cumplimiento Líderes"]=(pivot2["Encuesta Líderes"]/1)*100

pivot2.loc[(pivot2['Código IE']==83),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==87),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==227),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==248),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==31),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==33),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==74),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==99),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==100),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==101),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==102),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==103),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==104),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==105),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==111),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==141),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==142),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==144),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==197),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==200),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==201),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==203),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==219),'Porcentaje Cumplimiento Docentes']= 100
pivot2.loc[(pivot2['Código IE']==221),'Porcentaje Cumplimiento Docentes']= 100

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