def por_funciones(archivo_fuente, archivo_comentarios):
    '''[Autor: Ivan Litteri]
    [Ayuda: esta funcion recibe los archivos fuente y comentarios (csv) y los analiza y devuelve sus datos
    en funcion de las funciones. Esto quiere decir que cada funcion (key del diccionario) contiene todos 
    los datos de esa funcion (parametros, modulo al que pertenece, lineas, comentarios)'''

    datos_ordenados_por_funcion = {}

    linea_fuente = archivo_fuente.readline()
    while linea_fuente:
        nombre_funcion, parametros_funcion, modulo_funcion, *lineas_funcion = linea_fuente.split('","')
        if nombre_funcion not in datos_ordenados_por_funcion:
            datos_ordenados_por_funcion[nombre_funcion] = {"parametros": None,
                                                            "modulo": None,
                                                            "lineas": None}
        datos_ordenados_por_funcion[nombre_funcion]["parametros"] = parametros_funcion
        datos_ordenados_por_funcion[nombre_funcion]["modulo"] = modulo_funcion
        datos_ordenados_por_funcion[nombre_funcion]["lineas"] = lineas_funcion
        linea_fuente = archivo_fuente.readline()
    
    linea_comentarios = archivo_comentarios.readline()
    while linea_comentarios:
        nombre_funcion, autor_funcion, ayuda_funcion, *otros = linea_comentarios.split('","')
        if nombre_funcion not in datos_ordenados_por_funcion:
            datos_ordenados_por_funcion[nombre_funcion] = {}
        if "comentarios" not in datos_ordenados_por_funcion[nombre_funcion]:
            datos_ordenados_por_funcion[nombre_funcion]["comentarios"] = {"autor": None,
                                                                            "ayuda": None,
                                                                            "otros": None}
        datos_ordenados_por_funcion[nombre_funcion]["comentarios"]["autor"] = autor_funcion
        datos_ordenados_por_funcion[nombre_funcion]["comentarios"]["ayuda"] = ayuda_funcion if ("Ayuda" in ayuda_funcion) else None
        datos_ordenados_por_funcion[nombre_funcion]["comentarios"]["otros"] = otros if len(otros) > 1 else None
        linea_comentarios = archivo_comentarios.readline()

    return datos_ordenados_por_funcion

def por_modulo(archivo_fuente, archivo_comentarios):
    datos_ordenados_por_modulo = {}

    linea_fuente = archivo_fuente.readline()
    while linea_fuente:
        nombre_funcion, parametros_funcion, modulo_funcion, *lineas_funcion = linea_fuente.split('","')
        if modulo_funcion not in datos_ordenados_por_modulo:
            datos_ordenados_por_modulo[modulo_funcion] = {}
        if nombre_funcion not in datos_ordenados_por_modulo[modulo_funcion]:
            datos_ordenados_por_modulo[modulo_funcion][nombre_funcion] = {}
        datos_ordenados_por_modulo[modulo_funcion][nombre_funcion] = {"parametros": parametros_funcion,
                                                                        "lineas": lineas_funcion}
        linea_fuente = archivo_fuente.readline()

    linea_comentarios = archivo_comentarios.readline()
    while linea_comentarios:
        nombre_funcion, autor_funcion, ayuda_funcion, *otros = linea_comentarios.split('","')
        for modulo_funcion in datos_ordenados_por_modulo:
            if nombre_funcion not in datos_ordenados_por_modulo[modulo_funcion]:
                datos_ordenados_por_modulo[modulo_funcion][nombre_funcion] = {}
            if "comentarios" not in datos_ordenados_por_modulo[modulo_funcion][nombre_funcion]:
                datos_ordenados_por_modulo[modulo_funcion][nombre_funcion]["comentarios"] = {"autor": None,
                                                                                            "ayuda": None,
                                                                                            "otros": None}
            datos_ordenados_por_modulo[modulo_funcion][nombre_funcion]["comentarios"]["autor"] = autor_funcion
            datos_ordenados_por_modulo[modulo_funcion][nombre_funcion]["comentarios"]["ayuda"] = ayuda_funcion if ("Ayuda" in ayuda_funcion) else None
            datos_ordenados_por_modulo[modulo_funcion][nombre_funcion]["comentarios"]["otros"] = otros if len(otros) > 1 else None
        linea_comentarios = archivo_comentarios.readline()

    return datos_ordenados_por_modulo