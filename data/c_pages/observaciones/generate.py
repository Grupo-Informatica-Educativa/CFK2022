import pandas as pd
import textdistance

instantanea = pd.read_excel("instantenea.xlsx");
tablero = pd.read_excel("tablero.xlsx",engine='openpyxl',sheet_name='Reporte Consolidación 2022 - Co')
observaciones =  pd.read_excel("observaciones.xlsx",engine='openpyxl')


tablero = tablero[tablero['Estado Obs Aula'] == 'Realizada']
tablero = tablero[tablero['Observación de Aula'].notnull()]
mentores_observaciones = observaciones['Nombre del observador(a)'].unique()
mentores_tablero = tablero['Nombre mentor'].unique()

matches = []
# Vemos que tanto se parecen los nombres en ambas columnas
for mentor_obs in mentores_observaciones:
    for mentor_tab in mentores_tablero:
        obs = mentor_obs.lower()
        tab = mentor_tab.lower()
        score = textdistance.mra(obs,tab)
        if score > 4:
            matches.append({
                'observaciones': mentor_obs,
                'tablero': mentor_tab
            })

temp = list(pd.DataFrame(matches)['observaciones'].unique())
observaciones = observaciones[observaciones['Nombre del observador(a)'].isin(temp)]
observaciones['Asignatura en la que se hace la observación (implementa fichas)'] = observaciones['Asignatura en la que se hace la observación (implementa fichas)'].str.strip()


_list = observaciones['Asignatura en la que se hace la observación (implementa fichas)'].unique()

STEM = [
    'TECNOLOGÍA E INFORMÁTICA',
    'TECNOLOGÍA E INFORMATICA',
    'TECNOLOGIA E INFORMATICA',
    'BIOLOGÍA',
    'ELECTRÓNICA',
    'STEM',
    'GEOMETRÍA',
    'MATEMÁTICAS',
    'TALLER DE PENSAMIENTO COMPUTACIONAL',
]


observaciones['isSTEM'] = observaciones['Asignatura en la que se hace la observación (implementa fichas)'].isin(STEM)



# Generating graphs

'''Grafica #1'''

data_graf = observaciones[['Sesión','isSTEM']].copy()
temp = data_graf.groupby('isSTEM').count().reset_index()
temp.columns = ['Es STEM','Count']
temp['Sesión'] = 'Total'
data_graf = data_graf.value_counts().reset_index()
data_graf.columns = ['Sesión','EsSTEM','Count']
data_graf['EsSTEM'] = data_graf['EsSTEM'].astype(str).replace({'True': "Sí", 'False': "No"})
data = pd.concat([data_graf,temp],axis=0,ignore_index=True)

data.to_feather('datasets/grafica1.feather')

'''Grafica #2'''

data = observaciones[['Sesión']].copy()
data = data.value_counts().reset_index()
data.columns = ['Sesión','Count']
data['Percentage'] = (data['Count']/data['Count'].sum())*100

data.to_feather('datasets/grafica2.feather')


del data

'''Grafica #3'''

temp = observaciones['¿Se presentan los objetivos de aprendizaje de la lección?'].copy()
temp.replace({
    'Sí, se presentan aprendizajes esperados relacionados con pensamiento computacional': 'Sí',
       'No se presentan los objetivos que se espera lograr': 'No',
       'Parcialmente. Se presentan objetivos, pero estos no están relacionados con pensamiento computacional. Ej. El objetivo presentado por el/la docente es que los estudiantes estén callados y trabajen juiciosos': 'Parcialmente'
},inplace=True)
temp = temp.value_counts().reset_index()
temp.columns = ['Respuesta','Número de observaciones']

temp.to_feather('datasets/grafica3.feather')


'''Grafica #4'''

temp = observaciones['¿Se exploran los conocimientos previos de los estudiantes y su conexión con los temas de la lección?'].copy()
temp.replace({'Parcialmente. Se hace exploración de conocimientos previos, pero no se conectan claramente con el tema que se presenta': 'Parcialmente'},inplace=True)
temp = temp.value_counts().reset_index()
temp.columns = ['Respuesta','Número de observaciones']

temp.to_feather('datasets/grafica4.feather')


'''Grafica #5'''

temp1 = observaciones['¿Cuántos estudiantes completan la actividad desconectada?'].copy()
temp2 = observaciones['¿Cuántos estudiantes llevan a cabo la actividad desconectada según las instrucciones dadas?'].copy()

temp1 = temp1.value_counts().reset_index()
temp2 = temp2.value_counts().reset_index()

temp1["Pregunta"] = '¿Cuántos estudiantes completan la actividad desconectada?'
temp2["Pregunta"] = '¿Cuántos estudiantes llevan a cabo la actividad desconectada según las instrucciones dadas?'

temp1.columns = ['Observacion','Número de observaciones','Pregunta']
temp2.columns = ['Observacion','Número de observaciones','Pregunta']

temp = pd.concat([temp1,temp2],axis=0,ignore_index=True)

temp.to_feather('datasets/grafica5.feather')


'''Grafica #6'''
temp = observaciones[['Momentos Usa que suceden en la sesión y la forma como se orientan',
               'Momentos Modifica que suceden en la sesión y la forma como se orientan',
               'Momentos Crea que suceden en la sesión y la forma como se orientan']].copy()
temp.rename(columns={'Momentos Usa que suceden en la sesión y la forma como se orientan':'Usa','Momentos Modifica que suceden en la sesión y la forma como se orientan': 'Modifica','Momentos Crea que suceden en la sesión y la forma como se orientan':'Crea'},inplace=True)
temp.replace({
    'Liderado y realizado por el/la docente, sin participación de los estudiantes': 'Liderado por el docente',
    'Trabajo conjunto de Docente y Estudiantes': 'Ambos',
    'Estudiantes desarrollan el trabajo de forma autónoma': 'Estudiantes de forma autónoma'
},inplace=True)
temp = temp.melt()
temp = temp.value_counts().reset_index()
temp.columns = ['Accion','Tipo','Conteo']
temp = temp[temp['Tipo'] != '0'].reset_index(drop=True)
temp.to_feather('datasets/grafica6.feather')



'''Grafica 7'''
temp = observaciones["¿Se usa el vocabulario adecuado para la enseñanza del pensamiento computacional (terminología correcta)?"].copy()
temp = temp.value_counts().reset_index()
temp.columns = ['Respuesta','Número de observaciones']
temp.to_feather('datasets/grafica7.feather')


'''Grafica 8'''
temp = observaciones['¿Se hace uso de la memoria colectiva?'].copy()
temp = temp.value_counts().reset_index()

temp.columns = ['Respuesta','Número de observaciones']
temp['Porcentaje de observaciones'] = (temp['Número de observaciones']/temp['Número de observaciones'].sum())*100

temp.to_feather('datasets/grafica8.feather')

'''Grafica 9'''
temp = observaciones['¿Se siguen fielmente las actividades de la ficha?'].copy()
temp = temp.value_counts().reset_index()

temp.columns = ['Respuesta','Número de observaciones']
temp.to_feather('datasets/grafica9.feather')

'''Grafica 10'''

temp = observaciones[['Se usan los dispositivos de computo',
               'Se usan las tarjetas micro:bit',
               'Se cuenta con acceso a MakeCode',
               'Se usa el acceso a internet',
               'Se utilizan herramientas tecnológicas adicionales para apoyar el desarrollo de la sesión']].copy()
temp = temp.astype(bool)
temp['Total'] = temp.sum(axis=1)
temp = temp['Total'].value_counts().reset_index()
temp.columns = ['Cantidad','Conteo']
temp['Porcentaje de observaciones'] = (temp['Conteo']/temp['Conteo'].sum())*100
temp.to_feather('datasets/grafica10.feather')

'''Grafica 10'''