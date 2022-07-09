#!/usr/bin/env python3

import pandas as pd
import numpy as np

from pathlib import Path
from datetime import datetime

import sys
temp = sys.stdout                 # store original stdout object for later
sys.stdout = open('log_escalas.txt', 'w') # redirect all prints to this log file

## Calificar ESTUDIANTES

ruta =Path(__file__).parent
rutagit = ruta.parent.parent.parent

archivo_estudiantes = rutagit/"data/descargables/EstudiantesCFK.xlsx"
est = pd.read_excel(archivo_estudiantes)


respuestas_correctas = {
    "Un algoritmo es:":"Una secuencia lógica de pasos para realizar una tarea",
    "¿Para qué sirven los algoritmos?":"Para planificar la solución a un problema",
    "Un bucle es:":"Un conjunto de instrucciones que se ejecuta mientras se cumpla una condición",
    "¿Cuál de las siguientes opciones sí le permite al robot completar la misión de fotografiar cada tortuga?":"a.",
    "¿Qué mensaje deseaba enviar la líder Wayuú?":"c. Nublado",
    "¿Cuál de los siguientes códigos permite que el robot complete su misión sembrando café?":"a.",
    "¿Cuál será la foto con más vistas?":"c) Julio",
    "Ayuda al robot verde a salir del laberinto":"b.",
    "Óscar lleva 2 loncheras a la escuela todos los días ¿Cuál de las siguientes afirmaciones es falsa?":"c) Si Óscar empaca Deditos para merendar, puede hacer Arroz de pollo para almorzar",
    "¿Cuál de las siguientes hamburguesas tiene los ingredientes A, E y F?":"a.",
    "¿Qué botella debe cambiarse de color para que el resultado final sea una botella de color blanco?":"a) La botella B debe ser verde"}

de_acuerdo = {"Totalmente en desacuerdo":1,"En desacuerdo":2, "Neutro":3,
              "De acuerdo":4,"Totalmente de acuerdo":5}

interesa_carreras = {"No la conozco":0,"La evitaría":1,"Me interesa poco":2,"Está entre mis preferidas":3}

estereotipo_h = {'a) Seguramente un hombre':2, 'b) Quizás un hombre':1,
                 'c) Creo que puede ser un hombre o una mujer':0,
                 'd) Quizás una mujer': -1, 'e) Seguramente una mujer':-2}

estereotipo_m = {'a) Seguramente un hombre':-2, 'b) Quizás un hombre':-1,
                 'c) Creo que puede ser un hombre o una mujer':0,
                 'd) Quizás una mujer': 1, 'e) Seguramente una mujer':2}
#The scores range from -2= ‘counter- stereotypic answer’ to 2= ‘stereotype congruent answer’ for all items.
genero_estereotipos = {'5.1 ¿Quién crees que ganará el concurso de matemáticas?':estereotipo_h,
                       '5.2 ¿Quién crees que es capitán del barco?':estereotipo_h,
                       '5.3 ¿Quién es la persona excluida de la construcción de la casa de madera?':estereotipo_m,
                       '5.4 ¿Quién crees que es el personaje que está sentado y esperando junto a la ventana?':estereotipo_m,
                       '5.5 ¿Quién es la persona que trabaja en educación?':estereotipo_m,
                       '5.6 ¿Quién crees que es la persona que prefiere estudiar ingeniería?':estereotipo_h}


col_index = ['Edad', 'Sexo', 'Código IE', '¿Te reconoces como una persona con algún tipo de discapacidad?']
col_caract = ['N registro','Edad', 'Sexo', 'Sector vivienda', 'Internet', 'Uso del dispositivo móvil',
              'Nivel escolaridad madre', 'Nivel escolaridad padre', 'Ocupación madre',
              'Ocupación padre', '¿Con quién vives?', 'Grado', 'Código IE',
              'Grupo', 'Conoce GreenTIC', 'Número de lista', '¿Te reconoces como una persona con algún tipo de discapacidad?']

col_autoeficacia = est.filter(regex=r'^3.*', axis=1).columns.tolist()
col_carreras = est.filter(regex=r'^1.', axis=1).columns.tolist()
col_interes = est.filter(regex=r'^2.1|2.2', axis=1).columns.tolist()
col_conocimiento = list(respuestas_correctas.keys())
col_ambiental = est.filter(regex=r'^4.', axis=1).columns.tolist()
col_genero = est.filter(regex=r'^5.', axis=1).columns.tolist()
print("columnas género est: ",col_genero)

df_conocimientos = est[['N registro']+col_conocimiento].melt(id_vars='N registro', value_name='Respuesta estudiante', var_name='Pregunta')
df_conocimientos['Respuesta correcta'] = df_conocimientos['Pregunta'].replace(respuestas_correctas)
df_conocimientos['Puntaje conocimiento'] = 1*(df_conocimientos['Respuesta estudiante'] == df_conocimientos['Respuesta correcta'])
df_estudiantes = df_conocimientos.pivot_table(index='N registro', columns='Pregunta', values='Puntaje conocimiento').reset_index()


df_estudiantes= pd.merge(est[col_caract], df_estudiantes, on='N registro')

df_ambiente = est[['N registro']+col_ambiental].replace(de_acuerdo)

df_estudiantes = pd.merge(df_estudiantes,
                          df_ambiente, on='N registro')

df_estudiantes = pd.merge(df_estudiantes,
                          est[['N registro']+col_autoeficacia], on='N registro')

escalas_dict = {'medioambiente':
                    {'cols':list(est.filter(regex='^4.*').columns),
                     'cargas':[0.620,0.648,0.732,0.638,0.705,0.707,0.670]},
                'autoeficaciaPC':
                    {'cols':list(est.filter(regex='^3.1 |3.[2-5]|^3.7').columns),
                     'cargas':[0.724,0.822,0.782,0.745,0.574,0.390]},
                'autoeficaciaProg':{
                    'cols':list(est.filter(regex='^3.6 |3.[8-9]|3.10').columns),
                    'cargas':[0.637,0.490,0.755,0.753]
                }}

df_estudiantes[col_ambiental+col_autoeficacia] = df_estudiantes[col_ambiental+col_autoeficacia].apply(pd.to_numeric, errors='coerce')

df_estudiantes = df_estudiantes.dropna(subset=col_ambiental+col_autoeficacia)
print("Head de estudiantes numerico: ",df_estudiantes.head())

for k in list(escalas_dict.keys()):
    try:
        df_estudiantes[k] = 100*df_estudiantes[escalas_dict[k]['cols']].add(-1).multiply(escalas_dict[k]['cargas']).sum(axis=1)/(4*sum(escalas_dict[k]['cargas']))
    except:
        print('Fallo en ', k)

resultados = df_estudiantes[col_conocimiento].sum(axis=1)
media = resultados.mean()
desv = resultados.std()

df_estudiantes['conocimiento'] = 50+(10*(resultados - media)/desv)

estudiantes = pd.merge(est, df_estudiantes[['N registro', 'conocimiento', 'autoeficaciaPC', 'autoeficaciaProg', 'medioambiente']])

df_interes = est[['N registro']+col_interes].melt(id_vars='N registro', value_name='Seleccion', var_name='Pregunta')
df_interes['Interes en tecnologia'] = 1*(df_interes['Seleccion'].str.contains('Tecnología'))
df_puntaje_interes = df_interes.pivot_table(index='N registro', values=['Interes en tecnologia'], aggfunc=['sum', 'max']).reset_index()
df_puntaje_interes.columns = ['N registro', 'Puntaje interes', 'Interesado en tecnologia']
df_puntaje_interes['Puntaje interes'] = 100*(df_puntaje_interes['Puntaje interes']/2)

df_7 = pd.merge(estudiantes, df_puntaje_interes, on='N registro')
print("shape de estudiantes completo ",df_7.shape)

promedio = df_7.mean()
promedio = pd.DataFrame(promedio)
promedio = promedio.T
promedio['Código IE'] = 'Promedio'
promedio['ID'] = "Promedio"
promedio['N registro'] = "Promedio"



df_7 = pd.concat([df_7, promedio],ignore_index=True)
df_7 = df_7.fillna(df_7.mode().iloc[0])
df_7['Código IE'] = df_7['Código IE'].astype(str)

print('Validar promedio: ', df_7.tail())
print("Shape de docentes y escalas: ", df_7.shape)


ruta_pagina_est = rutagit/'data/c_pages/consolidacion_pre/Estudiantes'


est_medioambiente = df_7.loc[:,col_caract+col_ambiental+['medioambiente']]
est_medioambiente.to_excel(ruta_pagina_est/'Medioambiente.xlsx',index=False)

est_autoeficacia = df_7.loc[:,col_caract+col_autoeficacia+['autoeficaciaPC','autoeficaciaProg']]
est_autoeficacia.to_excel(ruta_pagina_est/'Autoeficacia.xlsx',index=False)

est_genero = df_7.loc[:,col_caract+col_carreras+col_interes+col_genero+['Puntaje interes']]
est_genero.to_excel(ruta_pagina_est/'Genero.xlsx',index=False)

est_cono = df_7.loc[:,col_caract+col_conocimiento+['conocimiento']]
est_cono.to_excel(ruta_pagina_est/'Conocimiento.xlsx',index=False)


# again nothing appears. it's written to log file instead
sys.stdout.close()                # ordinary file object
sys.stdout = temp