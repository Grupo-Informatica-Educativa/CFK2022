def graph_answer(datos, pregunta, preguntas, pregunta_con_numero=True):
    if 'respuestas' in preguntas:
        if pregunta_con_numero:
            numero = pregunta.split(' ')[0][:-1]
        else:
            numero = pregunta
        if numero not in preguntas['respuestas']:
            return datos
        else:
            color = "Eficacia"
            resp = preguntas['respuestas'][numero]
            datos[color] = (datos[pregunta] == resp)
            datos[color] = datos[color].replace(
                {True: "Correcto", False: "Incorrecto"})
            return datos


def has_answer(datos, pregunta, categoria, pregunta_con_numero=True):
    if categoria == None:
        return False
    if 'respuestas' in categoria:
        if pregunta_con_numero:
            numero = pregunta.split(' ')[0][:-1]
        else:
            numero = pregunta
        return (numero in categoria['respuestas'])
    else:
        return False