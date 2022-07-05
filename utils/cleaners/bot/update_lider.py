#!/usr/bin/env python3
import pickle

import pandas as pd
import numpy as np

from pathlib import Path
from datetime import datetime

import sys
temp = sys.stdout                 # store original stdout object for later
sys.stdout = open('log_lideres.txt', 'w') # redirect all prints to this log file

## Estudiantes

ruta =Path(__file__).parent


sheet_id = "1c-LPkoKsngxi1FdFAdOreyDd2IH7sbu-ZXMLzpa6YUI"
sheet_name = "Form Responses 1"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
url = url.replace(" ", "%20")

df0=pd.read_csv(url)

with open(ruta/'columnas_Lideres.pkl', 'rb') as handle:
    dict_col_est = pickle.load(handle)

df0 = df0.rename(columns=dict_col_est)
df0 = df0.drop(columns=df0.filter(regex=r'eliminar').columns)

df0['N registro']=df0.index

df0['ID']=df0.index

df0['Timestamp'] = pd.to_datetime(df0['Timestamp'])

df0['Fecha'] = df0.Timestamp.dt.strftime('%d/%m')
print(df0['Fecha'][-5:])

df0 = df0.drop(columns='Timestamp')

df5=df0.copy()
df5['Instrumento']="Encuesta Líderes"

df5=df5.dropna(subset=['Código IE'],inplace=False)
df5=df5.drop([0,1,2,3,5,24,34,70,104,149,162,253,255,272],axis=0)

df5['Código IE']=df5['Código IE'].astype(int)
df5=df5[df5['Código IE'] > 0]
df5=df5[df5['Código IE']<253]
df5['Código IE']=df5['Código IE'].astype(str)
df5['Código IE']=df5['Código IE'].str.zfill(3)
print('Códigos líderes después de filtrar mayor menor: ', df5['Código IE'].unique()) #se mantienen 158 datos
print(df5.columns)
new_index=['N registro', 'Fecha', 'Instrumento','Código IE','ID',
       '1.1 Los docentes encargados del área son los responsables de definir lo que se enseña',
       '1.2 El plan de estudios del área cuenta con mejoras realizadas por los docentes de la IE gracias a espacios colaborativos',
       '1.3 El plan de estudio incluye actividades básicas de ofimática y/o alfabetización digital, programación y/o desarrollo del pensamiento computacional.',
       '1.4 En el plan de estudio se da mayor relevancia al pensamiento computacional',
       '1.5 El plan de estudio del área promueve la transición desde la alfabetización digital a las ciencias de la computación',
       '1.6 El plan de estudios del área comprende el pensamiento computacional y su impacto dentro del proceso enseñanza-aprendizaje',
       '1.7 El plan de estudios del área es coherente con la transición de un grado a otro y permite al estudiante desarrollar conocimientos, habilidades y comprensión del pensamiento computacional',
       '1.8 El plan de estudios del área incluye trabajo práctico para el desarrollo del pensamiento computacional.',
       '1.9 El plan de estudio del área cuenta con espacios de socialización a los estudiantes de personas que trabajan en ocupaciones relacionadas al área STEM',
       '1.10 El plan de estudio de las asignaturas No-STEM integran eficientemente los aprendizajes adquiridos por sus estudiantes sobre pensamiento computacional',
       '1.11 La visión institucional menciona el impacto y lugar de la enseñanza del desarrollo del pensamiento computacional dentro del plan de estudios.',
       'Comentarios P1',
       '2.1 La IE identifica a los estudiantes que cuentan con necesidades educativas especiales',
       '2.2 La IE implementa algunas acciones para brindar apoyo a los estudiantes con necesidades educativas especiales en su participación en el área',
       '2.3 La IE establece un plan para la atención de estudiantes con necesidades educativas especiales para su participación en actividades asociadas al pensamiento computacional',
       '2.4 La IE promueve la participación de personas con necesidades educativas especiales en actividades extracurricules para garantiza la inclusión y participación en áreas STEM',
       '2.5 La IE genera estrategias que visibilizan modelos a seguir en carreras en áreas STEM en estudiantes con necesidades educativas especiales',
       '2.6 Los docentes del área que incluyen pensamiento computacional y/o ciencias de la computación muestran la asignatura como accesible para todos(as)',
       '2.7 La IE promueve al trabajo conjunto entre los docente y profesionales externos para impulsar prácticas inclusivas en la enseñanza de la computación y/o pensamiento computacional',
       '2.8 El plan de estudio considera aspectos para la inclusión de estudiantes con trastornos de aprendizaje y/o discapacidad',
       '2.9 El plan de estudios del área incluye acciones de apoyo y adecuaciones a los materiales educativos articuladas con las estrategias de atención de estudiantes con necesidades educativas especiales',
       '2.10  El plan de estudios del área y los recursos educativos se revisan con apoyo de personal experto en la atención a estudiantes con necesidades educativas especiales',
       '2.11 El plan de estudios del área hace explícita la pedagogía a utilizar que incluye adaptaciones para estudiantes con necesidades educativas especiales',
       'Comentarios P2',
       '3.1 La IE hace seguimiento de las diferencias de género en los resultados y el desempeño académico de niños y niñas en áreas STEM',
       '3.2 La IE crea espacios de reflexión sobre las causas y orígenes de las diferencias entre niños y niñas',
       '3.3 La IE realiza iniciativas cívicas y campañas comunicativas con estudiantes para visibilizar las diferencias de género en áreas STEM',
       '3.4 La IE toma acciones concretas para disminuir la diferencias de resultados entre niños y niñas Por ejemplo: organizar competencias diferenciadas entre niños y niñas en áreas STEM',
       '3.5 La IE tiene alianzas con entidades externas que promuevan la equidad género en las áreas STEM',
       '3.6 La institución posee una propuesta estructurada donde garantiza que los niños y niñas continúen su trayectoria de formación educativa en pensamiento computacional y/o ciencias de la computación.',
       '3.7 El plan de estudios del área promueve en niños y niñas el desarrollo de sus conocimientos, habilidades y actitudes',
       '3.8 El plan de estudio del área cuentan con una estructura clara que permite disminuir las diferencias en el desempeño de niños y niñas',
       '3.9 El plan de estudio del área se encuentran en constante revisión e incorporan nuevas estrategias para promover la igualdad en el desempeño de niños y niñas',
       '3.10 El plan de estudio considera aspectos para disminuir las diferencias entre niños y niñas y la inclusión de estudiantes con trastornos de aprendizaje y/o discapacidad',
       'Comentarios P3',
       '4.1 La IE tiene en cuenta el plan de estudios para determinar las actividades de desarrollo profesional',
       '4.2 La IE identifica las necesidades de los docentes para determinar actividades de desarrollo profesional',
       '4.3 La IE cuenta con espacios de discusión y planeación para actividades de desarrollo profesional',
       '4.4 La IE capacita a los docentes en temas de equidad de género y apoya la implementación de acciones afirmativas en el aula de clases',
       '4.5 La IE lleva un registro formal de las necesidades y participación de los docentes en actividades de desarrollo profesional',
       '4.6 Los docentes de otras áreas se interesan por el área de tecnología e informática y la integran a su enseñanza',
       '4.7 La IE incentiva el trabajo coordinado entre los/las responsables del área',
       '4.8 La IE tiene en cuenta los conocimientos del personal docente para enriquecer la visión institucional sobre la enseñanza de la computación y potenciar la comprensión de las/los estudiantes y desarrollo',
       '4.9 La IE promueve al trabajo conjunto entre los docente y profesionales líderes externos para impulsar prácticas inclusivas en la enseñanza de la computación y/o pensamiento computacional',
       '4.10 El Consejo Directivo del colegio está al tanto de que en la institución se está enseñando ciencias de la computación, y se encuentran involucrados en el proceso.',
       '4.11 Las directivas y el Consejo Directivo participan y evalúan la implementación de sistemas eficientes del plan de estudios del área.]',
       'Comentarios P4']

df0=df0.reindex(new_index, axis='columns')
df5=df5.reindex(new_index, axis='columns')

registroseliminados=set(df0['N registro']).difference(set(df5['N registro']))
dfe=df0[df0['N registro'].isin(registroseliminados)]


archivo_eliminados = "eliminados/Eliminados_lideres.xlsx"
archivo_eliminados = ruta/archivo_eliminados

archivo_descargable = ruta.parent.parent.parent/"data/descargables/LideresCFK.xlsx"
dfe.to_excel(archivo_eliminados, index=False)
df5.to_excel(archivo_descargable,index=False)
print('Publicados ', df5.shape)
print('Eliminados ', dfe.shape)
sys.stdout.close()                # ordinary file object
sys.stdout = temp
