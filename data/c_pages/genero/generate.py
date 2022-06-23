import pandas as pd

data = pd.read_feather("prepost_inicial_genero_c2.feather")

cols = [
    '12.1 Realizar clubes y actividades extracurriculares para niñas y jóvenes como refuerzo de lo visto en las clases de áreas STEM',
    '12.2 Destacar y reconocer los logros de las niñas y jóvenes, por ejemplo, promover concursos diferenciados por género, como, premio a la niña científica y el niño científico',
    '12.3 Dar referencias o modelos de mujeres destacadas en las áreas STEM, por ejemplo, mostrar la película de Marie Curie',
    '12.4 Motivar que las niñas participen y sean escuchadas, por ejemplo, alternándolas con los niños',
    '12.5 Estimular el liderazgo femenino, por ejemplo, que las niñas y adolescentes sean representantes de grupo',
    '12.6 Generar espacios de confianza para las niñas, por ejemplo, realizando reflexiones sobre el género al comienzo de la clase',
    '12.7 Prohibir y corregir los comentarios, actitudes y acciones sexistas',
    '12.8 Utilizar lenguaje inclusivo y no realizar estereotipos de género, por ejemplo, decir “todas las personas” en vez de “todos los niños” o evitar decir que las niñas son delicadas',  
]

# Discriminando

# Inicial

temp = data[cols].replace({'SI': 1, 'NO': 0}).copy()
temp['Total'] = temp.sum(axis=1)
temp['Género'] = data['Género']
temp['Instrumento'] = data['Instrumento']
temp = temp[['Género','Total','Instrumento']]
temp['Total'] = temp['Total'].replace({1: 0})
temp['Total'] = temp['Total'].astype(bool)
temp = temp.value_counts().reset_index()
temp.columns = ["Género","Respuesta","Test","Porcentaje"]

suma = temp.groupby(["Test","Género","Respuesta"]).sum()
temp = suma.groupby(["Test","Respuesta"]).apply(lambda x:x / float(x.sum())).reset_index()
temp['Respuesta'].replace({True: 'Sí', False: 'No'},inplace=True)
temp = temp.sort_values(['Test'],ascending=False).reset_index(drop=True)

temp.to_feather('genero_2021_discriminado_inicial_c2.feather')


# Avanzado

data = pd.read_feather("preposttest_avanzado_C2.feather")

cols = [
    '14.1 Realizar clubes y actividades extracurriculares para niñas y jóvenes como refuerzo de lo visto en las clases de áreas STEM',
    '14.2 Destacar y reconocer los logros de las niñas y jóvenes, por ejemplo, promover concursos diferenciados por género, como, premio a la niña científica y el niño científico',
    '14.3 Dar referencias o modelos de mujeres destacadas en las áreas STEM, por ejemplo, mostrar la película de Marie Curie',
    '14.4 Motivar que las niñas participen y sean escuchadas, por ejemplo, alternándolas con los niños',
    '14.5 Estimular el liderazgo femenino, por ejemplo, que las niñas y adolescentes sean representantes de grupo',
    '14.6 Generar espacios de confianza para las niñas, por ejemplo, realizando reflexiones sobre el género al comienzo de la clase',
    '14.7 Prohibir y corregir los comentarios, actitudes y acciones sexistas',
    '14.8 Utilizar lenguaje inclusivo y no realizar estereotipos de género, por ejemplo, decir “todas las personas” en vez de “todos los niños” o evitar decir que las niñas son delicadas'
]

temp = data[cols].replace({'SI': 1, 'NO': 0}).copy()
temp['Total'] = temp.sum(axis=1)
temp['Género'] = data['Género']
temp['Instrumento'] = data['Instrumento']
temp = temp[['Género','Total','Instrumento']]
temp['Total'] = temp['Total'].replace({1: 0})
temp['Total'] = temp['Total'].astype(bool)
temp = temp.value_counts().reset_index()
temp.columns = ["Género","Respuesta","Test","Porcentaje"]

suma = temp.groupby(["Test","Género","Respuesta"]).sum()
temp = suma.groupby(["Test","Respuesta"]).apply(lambda x:x / float(x.sum())).reset_index()
temp['Respuesta'].replace({True: 'Sí', False: 'No'},inplace=True)
temp = temp.sort_values(['Test'],ascending=False).reset_index(drop=True)

temp.to_feather('genero_2021_discriminado_avanzado_c2.feather')

# Sin discriminar

# Inicial

data = pd.read_feather("prepost_inicial_genero_c2.feather")

cols = [
    '12.1 Realizar clubes y actividades extracurriculares para niñas y jóvenes como refuerzo de lo visto en las clases de áreas STEM',
    '12.2 Destacar y reconocer los logros de las niñas y jóvenes, por ejemplo, promover concursos diferenciados por género, como, premio a la niña científica y el niño científico',
    '12.3 Dar referencias o modelos de mujeres destacadas en las áreas STEM, por ejemplo, mostrar la película de Marie Curie',
    '12.4 Motivar que las niñas participen y sean escuchadas, por ejemplo, alternándolas con los niños',
    '12.5 Estimular el liderazgo femenino, por ejemplo, que las niñas y adolescentes sean representantes de grupo',
    '12.6 Generar espacios de confianza para las niñas, por ejemplo, realizando reflexiones sobre el género al comienzo de la clase',
    '12.7 Prohibir y corregir los comentarios, actitudes y acciones sexistas',
    '12.8 Utilizar lenguaje inclusivo y no realizar estereotipos de género, por ejemplo, decir “todas las personas” en vez de “todos los niños” o evitar decir que las niñas son delicadas',  
]


temp = data[cols].copy().replace({'SI': 1, 'NO': 0})
temp['Total'] = temp.sum(axis=1)
temp['Instrumento'] = data['Instrumento']
temp = temp[['Total','Instrumento']]
temp['Total'] = temp['Total'].replace({1: 0})
temp['Total'] = temp['Total'].astype(bool)
temp = temp.value_counts().reset_index()
temp.columns = ["Respuesta","Test","Porcentaje"]

suma = temp.groupby(["Test","Respuesta"]).sum()
temp = suma.groupby(["Test"]).apply(lambda x:x / float(x.sum())).reset_index()
temp['Respuesta'].replace({True: 'Sí', False: 'No'},inplace=True)
temp = temp.sort_values(['Test'],ascending=False).reset_index(drop=True)

temp.to_feather('genero_2021_sin_discriminado_inicial_c2.feather')


# Avanzado

data = pd.read_feather("preposttest_avanzado_C2.feather")

cols = [
    '14.1 Realizar clubes y actividades extracurriculares para niñas y jóvenes como refuerzo de lo visto en las clases de áreas STEM',
    '14.2 Destacar y reconocer los logros de las niñas y jóvenes, por ejemplo, promover concursos diferenciados por género, como, premio a la niña científica y el niño científico',
    '14.3 Dar referencias o modelos de mujeres destacadas en las áreas STEM, por ejemplo, mostrar la película de Marie Curie',
    '14.4 Motivar que las niñas participen y sean escuchadas, por ejemplo, alternándolas con los niños',
    '14.5 Estimular el liderazgo femenino, por ejemplo, que las niñas y adolescentes sean representantes de grupo',
    '14.6 Generar espacios de confianza para las niñas, por ejemplo, realizando reflexiones sobre el género al comienzo de la clase',
    '14.7 Prohibir y corregir los comentarios, actitudes y acciones sexistas',
    '14.8 Utilizar lenguaje inclusivo y no realizar estereotipos de género, por ejemplo, decir “todas las personas” en vez de “todos los niños” o evitar decir que las niñas son delicadas'
]

temp = data[cols].copy().replace({'SI': 1, 'NO': 0}).copy()
temp['Total'] = temp.sum(axis=1)
temp['Instrumento'] = data['Instrumento']
temp = temp[['Total','Instrumento']]
temp['Total'] = temp['Total'].replace({1: 0})
temp['Total'] = temp['Total'].astype(bool)
temp = temp.value_counts().reset_index()
temp.columns = ["Respuesta","Test","Porcentaje"]

suma = temp.groupby(["Test","Respuesta"]).sum()
temp = suma.groupby(["Test"]).apply(lambda x:x / float(x.sum())).reset_index()
temp['Respuesta'].replace({True: 'Sí', False: 'No'},inplace=True)
temp = temp.sort_values(['Test'],ascending=False).reset_index(drop=True)

temp.to_feather('genero_2021_sin_discriminado_avanzado_c2.feather')