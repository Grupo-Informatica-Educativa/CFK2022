#!/usr/bin/env python3
import pickle

import pandas as pd
import numpy as np

from pathlib import Path
from datetime import datetime

import sys
temp = sys.stdout                 # store original stdout object for later
sys.stdout = open('log_estudiantes.txt', 'w') # redirect all prints to this log file

## Estudiantes

ruta =Path(__file__).parent

sheet_id = "1Zt6ykNc0nc1BxZbodcw9yk1RC-gGQ4Knw4hLjFO0F1E"
sheet_name = "Respuestas de formulario 1"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
url = url.replace(" ", "%20")

df0=pd.read_csv(url)

with open(ruta/'columnas_estudiantes.pkl', 'rb') as handle:
    dict_col_est = pickle.load(handle)

df0 = df0.rename(columns=dict_col_est)
df0 = df0.drop(columns=df0.filter(regex=r'eliminar').columns)

df0['N registro']=df0.index
df0['Instrumento'] = 'Encuesta estudiantes'
df0['Timestamp'] = pd.to_datetime(df0['Timestamp'])
df0['Fecha'] = df0.Timestamp.dt.strftime('%d/%m')
print(df0['Fecha'][:5])

df1= df0.copy()

diccionariogrados={'Noveno':"09", 'Octavo':"08", 'Sexto':"06", 'Décimo':"10", 'Séptimo':"07", 'Once':"11", 'Quinto':"05"}

df1["Grado"]=df1["Grado"].replace(diccionariogrados)

df1.loc[(df1['N registro'].isin(range(9022,9123)))&(df1['Código IE']==105),'Código IE'] = 103

## hubo un cambio de formato de fecha que daña esta línea
#df1 = df1[df1.Timestamp>'2022-04-14']

df1 = df1.drop(columns='Timestamp')

df1.loc[(df1['N registro'].isin(range(1928,1987)))&(df1['Código IE']==6),'Código IE'] = None
df1.loc[(df1['N registro'].isin(range(10,340)))&(df1['Código IE']==247),'Código IE'] = None
df1.loc[(df1['N registro'].isin(range(3369,4505)))&(df1['Código IE']==248),'Código IE'] = None
df1.loc[(df1['N registro'].isin(range(1928,1987)))&(df1['Código IE']==6),'Código IE'] = None

df1=df1.dropna(subset=["Código IE"], inplace=False)

df1.loc[(df1['N registro']==234),'Número de lista'] = 27
df1.loc[(df1['N registro']==672),'Número de lista'] = 6
df1.loc[(df1['N registro']==1701),'Número de lista'] = 16
df1.loc[(df1['N registro']==2270),'Número de lista'] = 30
df1.loc[(df1['N registro']==5497),'Número de lista'] = 13
df1.loc[(df1['N registro']==13853),'Número de lista'] = 28
df1.loc[(df1['N registro']==14205),'Número de lista'] = 11
df1.loc[(df1['N registro']==14453),'Número de lista'] = 2
df1.loc[(df1['N registro']==14533),'Número de lista'] = 3
df1.loc[(df1['N registro']==14614),'Número de lista'] = 10
df1.loc[(df1['N registro']==15382),'Número de lista'] = 27
df1.loc[(df1['N registro']==16279),'Número de lista'] = 31
df1.loc[(df1['N registro']==14614),'Número de lista'] = 10
df1.loc[(df1['N registro']==15382),'Número de lista'] = 27
df1.loc[(df1['N registro']==16279),'Número de lista'] = 31
df1.loc[(df1['N registro']==16466),'Número de lista'] = 17
df1.loc[(df1['N registro']==16628),'Número de lista'] = 15
df1.loc[(df1['N registro']==16701),'Número de lista'] = 27
df1.loc[(df1['N registro']==16736),'Número de lista'] = 31
df1.loc[(df1['N registro']==16749),'Número de lista'] = 14
df1.loc[(df1['N registro']==18501),'Número de lista'] = 28

df1.loc[(df1['N registro']==261),'Grupo'] = 5
df1.loc[(df1['N registro']==2406),'Grupo'] = 6
df1.loc[(df1['N registro']==13600),'Grupo']= 2
df1.loc[(df1['N registro']==13612),'Grupo'] = 2
df1.loc[(df1['N registro']==13630),'Grupo'] = 7
df1.loc[(df1['N registro']==13638),'Grupo'] = 7
df1.loc[(df1['N registro']==13642),'Grupo'] = 7
df1.loc[(df1['N registro']==14471),'Grupo'] = 7
df1.loc[(df1['N registro']==14722),'Grupo'] = 11

df1=df1.dropna(subset=["Grupo"], inplace=False) #para eliminar filas con valores nan
df1['Grupo']=df1['Grupo'].astype(str) #volver todo una cadena
print(df1.Grupo.unique())

df1["Grupo"]=df1["Grupo"].str.replace(" ","")
df1["Grupo"]=df1["Grupo"].str.capitalize().str.replace("Sexto","").str.replace("Noveno","").str.replace("seis","")
df1['Grupo']=df1['Grupo'].str.replace("Jornadatarde","")
df1['Grupo']=df1['Grupo'].str.replace("colegiosansimon","")
print(df1.Grupo.unique())

diccionariogrupos1={'Bo02':"02", 'Ao01':"01",'Co03':"03", 'Do04':"04", 'Eo05':"05", 'Fo06':"06", 'Go07':"07", 'Ho08':"08", 'Io09':"09", 'Jo10':"10", 'Ko11':"11", 'Lo12':"12", "Urbano":None, "Nosequesignificalodegrupo":None, "Noconozco":None, "Nose":None, ".":None} #valor exactamente igual
df1["Grupo"]=df1["Grupo"].replace(diccionariogrupos1)
df1=df1.dropna(subset=["Grupo"], inplace=False)

print(df1.Grupo.unique())

df1["Grupo"]=df1["Grupo"].str.replace("_","", regex=False)
df1["Grupo"]=df1["Grupo"].str.replace("`","", regex=False)
df1["Grupo"]=df1["Grupo"].str.replace("´","", regex=False)
df1["Grupo"]=df1["Grupo"].str.replace(":","", regex=False)
df1["Grupo"]=df1["Grupo"].str.replace("-","", regex=False)
df1["Grupo"]=df1["Grupo"].str.replace("'","", regex=False)
df1["Grupo"]=df1["Grupo"].str.replace("+","", regex=False)
print(df1.Grupo.unique())

df1["Grupo"]=df1["Grupo"].replace(r'[Gg](.*)',"07",regex=True)
df1["Grupo"]=df1["Grupo"].replace(r'[Ff](.*)',"06",regex=True) #regex buscador
df1["Grupo"]=df1["Grupo"].replace(r'[Hh](.*)',"08",regex=True)
df1["Grupo"]=df1["Grupo"].replace(r'[Kk](.*)',"11",regex=True)
df1["Grupo"]=df1["Grupo"].str.replace("No","")
print(df1.Grupo.unique())

diccionariogrupos1={'Tres':"03",'tres':"03",'Seis3':"03",'6seis':"06"}
df1["Grupo"]=df1["Grupo"].replace(diccionariogrupos1)
df1=df1.dropna(subset=["Grupo"], inplace=False)
print('Colegio 250, 6 ', len(df1[df1['Código IE']==250]))
print(df1.Grupo.unique())

df1["Grupo"]=df1["Grupo"].replace(r'[Aa](.*)',"01",regex=True)
df1["Grupo"]=df1["Grupo"].replace(r'[Bb](.*)',"02",regex=True) #regex buscador
df1["Grupo"]=df1["Grupo"].replace(r'[Cc](.*)',"03",regex=True)
df1["Grupo"]=df1["Grupo"].replace(r'[Ee](.*)',"04",regex=True)
df1["Grupo"]=df1["Grupo"].str.replace("o","")

df1["Grupo"]=df1["Grupo"].str.replace("O","", regex=False)
df1["Grupo"]=df1["Grupo"].str.replace(".0","", regex=False)
df1["Grupo"]=df1["Grupo"].str.replace(".","", regex=False)

df1['Grupo']=[x[-2:] if int(x[-2:])<20 else x[-1] for x in df1["Grupo"]]
df1['Grupo']=df1['Grupo'].str.zfill(2)
print(df1.Grupo.unique())

df1= df1[df1['Número de lista'] < 60]

df1['Número de lista']=df1['Número de lista'].astype(int)
df1['Número de lista']=df1['Número de lista'].astype(str)
df1['Número de lista']=df1['Número de lista'].str.zfill(2)
print(df1['Número de lista'].unique())

df1["Código IE"]=df1["Código IE"].astype(str)
df1["Código IE"]=df1["Código IE"].str.replace(".0","", regex=False)

diccionarioIE={'176109002977':"64", '176109000311':"66", '276109005806':"69", '176109002802':"70"}
df1["Código IE"]=df1["Código IE"].replace(diccionarioIE)
df1["Código IE"]=df1["Código IE"].astype(float)
df1["Código IE"]=df1["Código IE"].astype(int)
df1= df1[df1['Código IE'] > 0]
df1= df1[df1['Código IE'] < 253]
print('Colegio 250, 8 ', len(df1[df1['Código IE']==250]))
df1['Código IE']=df1['Código IE'].astype(int)
df1['Código IE']=df1['Código IE'].astype(str)
df1['Código IE']=df1['Código IE'].str.zfill(3)


df1['ID']=df1['Código IE']+df1['Grado']+df1['Grupo']+df1['Número de lista']
print(df1.head())

new_index=['N registro','Deseo participar en el estudio', 'Código IE', 'Grupo',
'Nombre',  'Fecha', 'ID','Número de lista', 'Edad', 'Sexo', 'Sector vivienda', 'Internet',
       'Uso del dispositivo móvil', 'Nivel escolaridad madre',
       'Nivel escolaridad padre', 'Ocupación madre', 'Ocupación padre',
       '¿Con quién vives?', 'Grado', '1.1. Ingeniería', '1.2 Matemáticas', '1.3 Educación', '1.4 Medicina',
        '1.5 Diseño gráfico', '1.6 Química', '1.7 Enfermería',
 '1.8 Desarrollo de software',
       '2.1 Soy capaz de sacar buenas notas en esta asignatura',
       '2.2 Si me va bien en esta asignatura, me ayudará en mi futura ocupación',
       '2.3 A mis padres les gustaría que eligiera un futuro profesional relacionado a esta asignatura',
       '2.4 Sé de alguien en mi familia que utiliza conocimientos relacionados a esta asignatura en su ocupación',
       'Comentarios 1-2', 'Un algoritmo es:',
       '¿Para qué sirven los algoritmos?', 'Un bucle es:',
       '3.1 Siento que soy capaz de explicar lo que es el pensamiento computacional',
       '3.2 Siento que puedo enumerar las sub-habilidades que componen el pensamiento computacional',
       '3.3 Siento que soy capaz de dar ejemplos para explicar las sub-habilidades del pensamiento computacional',
       '3.4 Siento que puedo explicar la forma en que las sub-habilidades del pensamiento computacional se correlacionan con la programación',
       '3.5 Siento que puedo analizar un ejercicio y determinar qué sub-habilidades de pensamiento computacional busca desarrollar',
       '3.6 Siento que puedo resolver problemas a través de programación',
       '3.7 Siento que puedo implementar algoritmos',
       '3.8 Siento que puedo crear un programa de computador',
       '3.9 Siento que puedo automatizar tareas a través de la programación',
       '3.10 Siento que puedo utilizar la computación para resolver problemas simples',
       'Comentarios P3',
       '¿Cuál de las siguientes opciones sí le permite al robot completar la misión de fotografiar cada tortuga?',
       '¿Qué mensaje deseaba enviar la líder Wayuú?',
       '¿Cuál de los siguientes códigos permite que el robot complete su misión sembrando café?',
       '¿Cuál será la foto con más vistas?',
       'Ayuda al robot verde a salir del laberinto',
       'Óscar lleva 2 loncheras a la escuela todos los días ¿Cuál de las siguientes afirmaciones es falsa?',
       '¿Cuál de las siguientes hamburguesas tiene los ingredientes A, E y F?',
       '¿Qué botella debe cambiarse de color para que el resultado final sea una botella de color blanco?',
       'Comentarios conocimiento',
       '5.1 ¿Quién crees que ganará el concurso de matemáticas?',
       '5.2 ¿Quién crees que es capitán del barco?',
       '5.3 ¿Quién es la persona excluida de la construcción de la casa de madera?',
       '5.4 ¿Quién crees que es el personaje que está sentado y esperando junto a la ventana?',
       '5.5 ¿Quién es la persona que trabaja en educación?',
       '5.6 ¿Quién crees que es la persona que prefiere estudiar ingeniería?',
       'Comentarios género',
       '4.1 Es alarmante que el ritmo de desaparición de especies en la Amazonia Colombiana sea cada vez mayor.',
       '4.2 El aumento de la temperatura atmosférica se debe al uso creciente y continuado de combustibles fósiles (carbón, petróleo…).',
       '4.3 La acumulación de basura procedente de las ciudades es un problema realmente grave.',
       '4.4 Hay una disminución de la superficie forestal y de áreas naturales en el país.',
       '4.5 El planeta está tan contaminado por productos químicos que ya supone un problema para la salud.',
       '4.6 Conozco los riesgos que representa para la vida humana la desaparición de especies animales y vegetales.',
       '4.7 Me preocupa lo que sucede con la tala de árboles.',
       'Comentarios medioambiente',
       'Tipo de discapacidad',
       '¿Te reconoces como una persona con algún tipo de discapacidad?',
       'Conoce GreenTIC', 'Instrumento']
df0=df0.reindex(new_index, axis='columns')
df1=df1.reindex(new_index, axis='columns')

registroseliminados=set(df0['N registro']).difference(set(df1['N registro']))
dfe=df0[df0['N registro'].isin(registroseliminados)]
archivo_eliminados = "eliminados/Eliminados_estudiantes.xlsx"
archivo_eliminados = ruta/archivo_eliminados
archivo_descargable = ruta.parent.parent.parent/"data/descargables/EstudiantesCFK.xlsx"
dfe.to_excel(archivo_eliminados, index=False)
df1.to_excel(archivo_descargable,index=False)
         # again nothing appears. it's written to log file instead
sys.stdout.close()                # ordinary file object
sys.stdout = temp
