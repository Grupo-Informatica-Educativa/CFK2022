#!/usr/bin/env python3
import pickle

import pandas as pd
import numpy as np

from pathlib import Path
from datetime import datetime

import sys
temp = sys.stdout                 # store original stdout object for later
sys.stdout = open('log_docentes.txt', 'w') # redirect all prints to this log file

## Estudiantes

ruta =Path(__file__).parent

sheet_id = "1z3cKYEjhjnM2Pkktt3lx5bqUXaxxneboWnSg6mux9co"
sheet_name = "Form Responses 1"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
url = url.replace(" ", "%20")

df0=pd.read_csv(url)

with open(ruta/'columnas_docentes.pkl', 'rb') as handle:
    dict_col_est = pickle.load(handle)

print(dict_col_est['Cuando un estudiante se enfrenta a una dificultad creando un programa y no sabe si está correcto, qué tan a menudo, en una escala de 1-10 (donde 10 es siempre), usted:  [Le sugeriría volver a leer el problema]'])

df0 = df0.rename(columns=dict_col_est)
print('columnas> ',df0.columns)
df0 = df0.drop(columns=df0.filter(regex=r'eliminar').columns)
df0['Timestamp'] = pd.to_datetime(df0['Timestamp'])

df0['Fecha'] = df0.Timestamp.dt.strftime('%d/%m')
print(df0['Fecha'][-5:])

df0['N registro']=df0.index
df3=df0.copy()
df3['Instrumento']="Encuesta docentes"

df3 = df3.drop(columns='Timestamp')

df3['Implementa fichas'] = df3['Implementa fichas'].fillna("No")
df3[df3.filter(regex='^1.*').columns] = df3[df3.filter(regex='^1.*').columns].fillna("Totalmente en Desacuerdo")
df3[df3.filter(regex='^2.*').columns] = df3[df3.filter(regex='^2.*').columns].fillna("Totalmente en Desacuerdo")
df3[df3.filter(regex='^Comentarios*').columns] = df3[df3.filter(regex='^Comentarios*').columns].fillna("")
#%%

df3.loc[(df3['N registro'].isin(range(5535,5846)))&(df3['Código IE']==14),'Código IE'] = 13
df3.loc[(df3['N registro'].isin(range(170,1799)))&(df3['Código IE']==247),'Código IE'] = None

df3=df3.drop([321,389,296,489,494,538,1694,3758,4116,4361,4367,4440,4442,4446,4449,4460,4465,5101,5633,5837,6205,6301,6578],axis=0)
df3=df3.dropna(subset=["Código IE"], inplace=False)

diccionariodocentes={'Nueva Esperanza La Palma ':150}

df3["Código IE"]=df3["Código IE"].replace(diccionariodocentes)
df3["Código IE"]=df3["Código IE"].astype(str)
df3["Código IE"]=df3["Código IE"].str.replace(".0","", regex=False)
df3["Código IE"]=df3["Código IE"].str.replace(".","",regex=False)
df3['Código IE']=df3['Código IE'].astype(float)
df3['Código IE']=df3['Código IE'].astype(int)

df3.loc[(df3['N registro']==6515),'Código IE'] = 139

df3= df3[df3['Código IE'] > 0]
df3=df3[df3['Código IE']<253]
df3['Código IE']=df3['Código IE'].astype(str)
df3['Código IE']=df3['Código IE'].str.zfill(3)
print('Códigos IE después de reemplazo: ',df3["Código IE"].unique())

df3.loc[(df3['N registro']==3206),'ID'] = 24586700
df3.loc[(df3['N registro']==932),'ID'] = 29540947
df3.loc[(df3['N registro']==4448),'ID'] = 36953660
df3.loc[(df3['N registro']==4615),'ID'] = 27159828
df3.loc[(df3['N registro']==4626),'ID'] = 27096608
df3.loc[(df3['N registro']==6117),'ID'] = 59312868
df3.loc[(df3['N registro']==6473),'ID'] = 30716158
df3.loc[(df3['N registro']==353),'ID'] = 66745606
df3.loc[(df3['N registro']==714),'ID'] = 31386953
df3.loc[(df3['N registro']==3291),'ID'] = 5092322
df3.loc[(df3['N registro']==6686),'ID'] = 31988705
df3.loc[(df3['N registro']==3730),'ID'] = 42489542
df3.loc[(df3['N registro']==1819),'ID'] = 35601960
df3.loc[(df3['N registro']==1196),'ID'] = 21994344
df3.loc[(df3['N registro']==955),'ID'] = 31377497
df3.loc[(df3['N registro']==6853),'ID'] = 52270750

#excepciones a la regla de número de cédula
df3.loc[(df3['N registro']==554),'ID'] = 22534255

df3.loc[(df3['N registro']==6853),'Implementa fichas'] = 'No'

df3.loc[(df3['N registro']==4667),'Código IE'] = None
df3.loc[(df3['N registro']==158),'Código IE'] = None
df3.loc[(df3['N registro']==1320),'Código IE'] = None
df3.loc[(df3['N registro']==4081),'Código IE'] = None
df3.loc[(df3['N registro']==5106),'Código IE'] = None
df3.loc[(df3['N registro']==5116),'Código IE'] = None
df3.loc[(df3['N registro']==3469),'Código IE'] = None
df3.loc[(df3['N registro']==4174),'Código IE'] = None
df3.loc[(df3['N registro']==2093),'Código IE'] = None
df3.loc[(df3['N registro']==6579),'Código IE'] = None
df3.loc[(df3['N registro']==6727),'Código IE'] = None
df3.loc[(df3['N registro']==3844),'Código IE'] = None

df3=df3.dropna(subset=['Código IE'], inplace=False)

df3['ID']=df3['ID'].astype(float).astype("int64")
df3= df3[df3['ID'] >= 1000000]
df3= df3[df3['ID'] < 3000000000]

df3.loc[(df3['N registro']==554),'ID'] = 479159

new_index = ['N registro', 'Instrumento', 'Fecha','Política de datos', 'Código IE',
             'Tipo ID', 'ID', 'Email', 'Edad', 'Sexo', 'Cabeza de hogar', 'Estado civil',
             'Líder comunitario', 'Formado CFK', 'Implementa fichas', 'Formado tecnología e informática',
             '¿Cuáles de las siguientes áreas enseña y en qué grado? [Ciencias naturales y educación ambiental.]',
             '¿Cuáles de las siguientes áreas enseña y en qué grado? [Ciencias sociales, historia, geografía, constitución política y democracia.]', '¿Cuáles de las siguientes áreas enseña y en qué grado? [Educación artística.]', '¿Cuáles de las siguientes áreas enseña y en qué grado? [Educación ética y en valores humanos.]', '¿Cuáles de las siguientes áreas enseña y en qué grado? [Educación física, recreación y deportes.]',
             '¿Cuáles de las siguientes áreas enseña y en qué grado? [Educación religiosa.]',
             '¿Cuáles de las siguientes áreas enseña y en qué grado? [Humanidades, lengua castellana e idiomas extranjeros.]',
             '¿Cuáles de las siguientes áreas enseña y en qué grado? [Matemáticas.]',
             '¿Cuáles de las siguientes áreas enseña y en qué grado? [Tecnología e informática.]',
             '¿Cuáles de las siguientes áreas enseña y en qué grado? [Otro]', 'Enseña STEM', 'Formado STEM',
             'Considera importante enseñar el pensamiento computacional desde los primeros niveles educativos',
             '1.1 Siento que puedo aplicar las prácticas y habilidades del pensamiento computacional a mi trabajo',
             '1.2 Siento que puedo definir el pensamiento computacional',
             '1.3 Siento que puedo describir las prácticas y habilidades que componen el pensamiento computacional a mis estudiantes',
             '1.4 Siento que puedo aplicar las prácticas y habilidades del pensamiento computacional a mi vida diaria',
             '2.1 Creo que tengo las habilidades para desarrollar el pensamiento computacional en mis estudiantes',
             '2.2 Siento que puedo enseñar fácilmente sobre nuevas prácticas computacionales',
             '2.3 Siento que puedo diseñar una clase que desarrolle el pensamiento computacional en los estudiantes',
             '2.4 Siento que puedo aplicar mis habilidades en pensamiento computacional para ayudar a los estudiantes a perseguir sus intereses individuales', '2.5 Siento que puedo evaluar la idoneidad de una estrategia pedagógica para desarrollar pensamiento computacional',
             '3.1 El colegio ofrece espacios adicionales para fomentar el pensamiento computacional', '3.2 En la programación anual del colegio existen actividades asociadas al pensamiento computacional', '3.3 Cuando he intentado enseñar pensamiento computacional me he encontrado con obstáculos para gestionar espacios y materiales en el colegio.', '3.4 Recibo apoyo del colegio cuando propongo nuevas ideas y temáticas afines al pensamiento computacional', '3.5 Siento que por más que lo he intentado mis esfuerzos por incluir pensamiento computacional en las clases no han sido efectivos por la rigidez del plan de estudio', '3.6 Los directivos incentivan la implementación de nuevas prácticas pedagógicas sobre pensamiento computacional en el aula', '3.7 Puedo incluir espacios en mis clases para implementar actividades sobre el pensamiento computacional', '3.8 Me siento frustrado porque la programación de las clases y compromisos institucionales no me permite incluir actividades de pensamiento computacional', '3.9 Tener educación en pensamiento computacional mejoraría significativamente las futuras opciones de ocupación para los estudiantes de mi escuela.', '4.1 Creo que sé cómo resolver los problemas técnicos cuando fallan las TIC', '4.2 Siento que puedo aprender sobre nuevas tecnologías fácilmente', '4.3 Creo que sé cómo usar las TIC con los estudiantes en clase', '5.1 Me apoyo en mis colegas para resolver problemas sobre cómo trabajar algún tema', '5.2 Puedo hablar con otros docentes sobre el diseño de cursos', '5.3 Siento que tengo apoyo de otros docentes para el diseño de mis cursos', '5.4 Siento que no tengo con quién conversar sobre el diseño de mis cursos',
             '6.1 Actividades desconectadas', '6.2 Usa-Modifica-Crea', '6.3 Clase magistral', '6.4 Programación en pares', '6.5 Lectura del código', '7.1 Le explicaría la respuesta correcta',
             '7.2 Le sugeriría ir paso a paso por el programa simulando su ejecución',
             '7.3 Le diría que revise sus notas',
             '7.4 Le sugeriría que revise las memorias colectivas',
             '7.5 Le sugeriría volver a leer el problema',
             '7.6 Le sugeriría intentar con varios valores para evaluar el programa',
             '7.7 Le explicaría el problema nuevamente', 'Comentarios P1-7', 'Un algoritmo es:', '¿Para qué sirven los algoritmos?', 'Un bucle es:', '¿Cuál es el error conceptual de Tim?', '¿Cuál es el error conceptual de Ana?', 'Comentarios Conocimientos', '¿Cuáles de las siguientes estrategias usted ha usado en sus clases?', '8.1 Es preferible que las mujeres enseñen ciencias sociales y los hombres ciencias exactas.', '8.2 Es normal que la mayoría de ingenieros mecánicos sean varones porque los hombres son mejores para los números.', '8.3 Por su esencia una mujer tiene mejor desempeño en un proyecto de alto impacto social que en un proyecto de robótica industrial.', '8.4 Los hombres son mejores para la tecnología que las mujeres.', '8.5 Las mujeres tienen mayores habilidades para proyectos sociales que tecnológicos.', '8.6 Los grandes aportes en la computación han sido hechos por hombres.', '8.7 Que la mayoría de mujeres no opte por áreas exactas es simplemente una cuestión de preferencias.', '8.8 Que la mayoría de personas en artes y humanidades sean mujeres es muestra de su sensibilidad.', '8.9 Es natural que los hombres sean buenos para los números y las mujeres para las letras.', '8.10 Los hombres son muy ágiles tomando decisiones importantes.', '8.11 Las niñas son más ordenadas que los niños.', '8.12 Muchas mujeres se caracterizan por una pureza que pocos hombres poseen.', '8.13 Las mujeres deben ser queridas y protegidas por los hombres.', '8.14 Todo hombre debe tener una mujer a quien amar.', '8.15 El hombre está incompleto sin la mujer.', '8.16 Las mujeres en comparación con los hombres, tienden a tener un sentido más refinado de la cultura y el buen gusto.', 'Comentarios género', ]

df0=df0.reindex(new_index, axis='columns')
df3=df3.reindex(new_index, axis='columns')

registroseliminados=set(df0['N registro']).difference(set(df3['N registro']))
dfe=df0[df0['N registro'].isin(registroseliminados)]

archivo_eliminados = "eliminados/Eliminados_docentes.xlsx"
archivo_eliminados = ruta/archivo_eliminados

archivo_descargable = ruta.parent.parent.parent/"data/descargables/DocentesCFK.xlsx"
dfe.to_excel(archivo_eliminados, index=False)
df3.to_excel(archivo_descargable,index=False)

sys.stdout.close()                # ordinary file object
sys.stdout = temp
