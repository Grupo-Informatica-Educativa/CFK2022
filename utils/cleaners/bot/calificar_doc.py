#!/usr/bin/env python3

import pandas as pd
import numpy as np

from pathlib import Path
from datetime import datetime

import sys
temp = sys.stdout                 # store original stdout object for later
sys.stdout = open('log_escalas.txt', 'w') # redirect all prints to this log file

## Calificar DOCENTES

ruta =Path(__file__).parent
rutagit = ruta.parent.parent.parent

archivo_docentes = rutagit/"data/descargables/DocentesCFK.xlsx"
doc = pd.read_excel(archivo_docentes)


respuestas_correctas = {
    "Un algoritmo es:":"Una secuencia lógica de pasos para realizar una tarea.",
    "¿Para qué sirven los algoritmos?":"Para planificar la solución a un problema",
    "Un bucle es:":"Un conjunto de instrucciones que se ejecuta mientras se cumpla una condición",
    '¿Cuál es el error conceptual de Tim?':"Cree que, si la condición se cumple, todo lo que sigue se va a ejecutar",
    '¿Cuál es el error conceptual de Ana?':"No tiene claro el concepto de bucle y por eso no logra identificar que A y C hacen lo mismo"}

de_acuerdo = {"Totalmente en Desacuerdo":1,"En Desacuerdo":2, "Neutro":3, "De acuerdo":4,"Totalmente de acuerdo":5,
              "De Acuerdo":4,"Totalmente de Acuerdo":5, "Totalmente Desacuerdo":1, "Totalmente en desacuerdo":1, "En desacuerdo":2}

no_sabe_conoce = {"No la conozco":0, "No sé":0}

col_index = ['Edad', 'Sexo', 'Código IE', '¿Te reconoces como una persona con algún tipo de discapacidad?']
col_caract = ['N registro','Código IE', 'Tipo ID', 'ID', 'Email', 'Edad', 'Sexo','Cabeza de hogar',
              'Estado civil', 'Líder comunitario', 'Formado CFK', 'Implementa fichas',
              'Formado tecnología e informática', 'Enseña STEM', 'Formado STEM']

col_autoeficacia_PC = doc.filter(regex=r'^1.|^2.*', axis=1).columns.tolist()
col_apoyo_inst= doc.filter(regex=r'^3.[1,2,4,6,7,9]', axis=1).columns.tolist()
col_frust_inst = doc.filter(regex=r'^3.[3,5,8]', axis=1).columns.tolist()
col_autoeficacia_tec = doc.filter(regex=r'^4.', axis=1).columns.tolist()
col_sentido_com = doc.filter(regex=r'^5.', axis=1).columns.tolist()
col_practicas_ped = doc.filter(regex=r'^6.', axis=1).columns.tolist()
col_practicas_eval = doc.filter(regex=r'^7.', axis=1).columns.tolist()
col_conocimiento = list(respuestas_correctas.keys())
col_sexismo_stem = doc.filter(regex=r'^8.1 |^8.[2,3,4,5,6,9]', axis=1).columns.tolist()
col_sexismo_ben =  doc.filter(regex=r'^8.8 |^8.1[0,1,2,16]', axis=1).columns.tolist()
col_estereotipo =  doc.filter(regex=r'^8.1[3,4,5]', axis=1).columns.tolist()
col_genero = doc.filter(regex=r'^8.', axis=1).columns.tolist()
print("col genero ", col_genero)

columnas_no_conoce_pc = doc.filter(regex=r'^1.|^2.', axis=1).columns.tolist()
columnas_institucion = doc.filter(regex=r'^3.',axis=1).columns.tolist()

doc[columnas_no_conoce_pc] = doc[columnas_no_conoce_pc].fillna('Totalmente en Desacuerdo')
doc[columnas_institucion] = doc[columnas_institucion].fillna("Neutro")

doc[col_genero+col_autoeficacia_PC+col_autoeficacia_tec+col_sentido_com+col_apoyo_inst+col_frust_inst] = doc[col_genero+col_autoeficacia_PC+col_autoeficacia_tec+col_sentido_com+col_apoyo_inst+col_frust_inst].replace(de_acuerdo)
doc[col_practicas_ped+col_practicas_eval] = doc[col_practicas_ped+col_practicas_eval].replace(no_sabe_conoce)
print("Shape de docentes: ", doc.shape)

doc_conocimientos = doc[['ID']+col_conocimiento].melt(id_vars='ID',
                                                      value_name='Respuesta',
                                                      var_name='Pregunta')
doc_conocimientos['Respuesta correcta'] = doc_conocimientos['Pregunta'].replace(respuestas_correctas)
doc_conocimientos['Correcta'] = 1*(doc_conocimientos['Respuesta'] == doc_conocimientos['Respuesta correcta'])

doc_cono_pivot = doc_conocimientos.pivot_table(index='ID',
                                               columns='Pregunta',
                                               values='Correcta',
                                               aggfunc='max').reset_index()

docentes = doc.drop(columns=col_conocimiento)
docentes = pd.merge(docentes,doc_cono_pivot, on='ID' )

resultados = docentes[col_conocimiento].sum(axis=1)
media = resultados.mean()
desv = resultados.std()
print("Info de resultados: ", resultados.describe())

docentes['conocimiento'] = 50+(10*(resultados - media)/desv)
docentes['conocimiento']

escalas_dict = {'apoyo':
                    {'cols':col_apoyo_inst,
                     'cargas':[0.776,0.773,0.798,0.827,0.671,0.502]},
                'frustracion':
                    {'cols':col_frust_inst,
                     'cargas':[0.499,0.749,0.736]},
                'sexismoSTEM':{
                    'cols':col_sexismo_stem,
                    'cargas':[0.933,0.936,0.776,0.929,0.755,0.523,0.753]},
                'sexismoBenev':{
                    'cols':col_sexismo_ben,
                    'cargas':[0.782,0.527,0.96,0.82,0.629]},
                'estereoBenev':{
                    'cols':col_estereotipo,
                    'cargas':[0.824,0.892,0.825]},
                'autoeficaciaPC':{
                    'cols':col_autoeficacia_PC,
                    'cargas':[0.807,0.767,0.839,0.881,0.820,0.840,0.892,0.912,0.912]},
                'autoeficaciaTec':{
                    'cols':col_autoeficacia_tec,
                    'cargas':[0.689,0.501,0.887]},
                'sentidoComunidad':{
                    'cols':col_sentido_com,
                    'cargas':[0.687,0.749,0.834,0.441]},
                }

nombres_escalas = list(escalas_dict.keys())
for k in nombres_escalas:
    assert len(escalas_dict[k]['cols']) == len(escalas_dict[k]['cargas']), f'Hay un error en la longitud de {k}'
    docentes[k] = 100*docentes[escalas_dict[k]['cols']].add(-1).multiply(escalas_dict[k]['cargas']).sum(axis=1)/(4*sum(escalas_dict[k]['cargas']))

doc_escalas = pd.merge(doc, docentes[['N registro','conocimiento']+nombres_escalas])

media = doc_escalas.mean()
media = pd.DataFrame(media)
media = media.T
media['Código IE'] = 'Promedio'
media['ID'] = "Promedio"
media['N registro'] = "Promedio"

doc_escalas = pd.concat([doc_escalas,media],ignore_index=True)
doc_escalas = doc_escalas.fillna(doc_escalas.mode().iloc[0])
print('Validar promedio: ', doc_escalas.tail())
print("Shape de docentes y escalas: ", doc_escalas.shape)

ruta_pagina_doc = rutagit/'data/c_pages/consolidacion_pre/Docentes'

doc_autoeficacia = doc_escalas.loc[:,col_caract+col_autoeficacia_PC+col_autoeficacia_tec+col_practicas_eval+col_practicas_ped+['autoeficaciaPC','autoeficaciaTec']]

doc_autoeficacia.to_excel(ruta_pagina_doc/'Autoeficacia.xlsx', index=False)

doc_apoyo = doc_escalas.loc[:,col_caract+col_apoyo_inst+col_frust_inst+col_sentido_com+['apoyo','frustracion','sentidoComunidad']]
doc_apoyo.to_excel(ruta_pagina_doc/'Apoyo.xlsx', index=False)

doc_genero = doc_escalas.loc[:,col_caract+col_genero+['sexismoSTEM','sexismoBenev','estereoBenev']]
doc_genero.to_excel(ruta_pagina_doc/'Genero.xlsx', index=False)

doc_conoc = doc_escalas.loc[:,col_caract+col_conocimiento+['conocimiento']]
doc_conoc.to_excel(ruta_pagina_doc/'Conocimiento.xlsx', index=False)



# again nothing appears. it's written to log file instead
sys.stdout.close()                # ordinary file object
sys.stdout = temp