def por_funciones(archivo_fuente, archivo_comentarios):
    '''[Autor: Ivan Litteri]
    [Ayuda: esta funcion recibe los archivos fuente y comentarios (csv) y los analiza y devuelve sus datos
    en funcion de las funciones. Esto quiere decir que cada funcion (key del diccionario) contiene todos 
    los datos de esa funcion (parametros, modulo al que pertenece, lineas, comentarios)'''

    #Declaro el diccionario vacio para llenar luego
    datos_ordenados_por_funcion = {}

    #Cargo la primera linea del archivo fuente
    linea_fuente = archivo_fuente.readline()
    #Mientras el archivo tenga lineas para leer
    while linea_fuente:
        #Desempaqueto los datos de cada linea
        nombre_funcion, parametros_funcion, modulo_funcion, *lineas_funcion = linea_fuente.split('","')
        #Si la funcion no esta como key del diccionario, entonces la agrego y le doy su forma
        if nombre_funcion not in datos_ordenados_por_funcion:
            datos_ordenados_por_funcion[nombre_funcion] = {"parametros": None,
                                                            "modulo": None,
                                                            "lineas": None}
        #Agrego los datos a sus respectivos lugares
        datos_ordenados_por_funcion[nombre_funcion]["parametros"] = parametros_funcion
        datos_ordenados_por_funcion[nombre_funcion]["modulo"] = modulo_funcion
        datos_ordenados_por_funcion[nombre_funcion]["lineas"] = lineas_funcion
        #Avanzo de linea en el archivo
        linea_fuente = archivo_fuente.readline()
    
    #Cargo la primera linea del archivo de comentarios
    linea_comentarios = archivo_comentarios.readline()
    #Mientras el archivo tenga lineas para leer
    while linea_comentarios:
        #Desempaqueto los datos de cada linea
        nombre_funcion, autor_funcion, ayuda_funcion, *otros = linea_comentarios.split('","')
        #Si la funcion no esta como key del diccionario, entonces la agrego
        if nombre_funcion not in datos_ordenados_por_funcion:
            datos_ordenados_por_funcion[nombre_funcion] = {}
        #Si la key comentarios aun no existe en la funcion lo agrego y le doy forma
        if "comentarios" not in datos_ordenados_por_funcion[nombre_funcion]:
            datos_ordenados_por_funcion[nombre_funcion]["comentarios"] = {"autor": None,
                                                                            "ayuda": None,
                                                                            "otros": None}
        #Agrego los datos a sus respectivos lugares
        datos_ordenados_por_funcion[nombre_funcion]["comentarios"]["autor"] = autor_funcion
        datos_ordenados_por_funcion[nombre_funcion]["comentarios"]["ayuda"] = ayuda_funcion if ("Ayuda" in ayuda_funcion) else None
        datos_ordenados_por_funcion[nombre_funcion]["comentarios"]["otros"] = otros if len(otros) > 1 else None
        #Avanzo de linea en el archivo
        linea_comentarios = archivo_comentarios.readline()

    return datos_ordenados_por_funcion

def por_modulos(archivo_fuente, archivo_comentarios):
    '''[Autor: Ivan Litteri]
    [Ayuda: esta funcion recibe los archivos fuente y comentarios (csv) por parametro, los analiza y devuelve
    sus datos en funcion de los modulos. Esto quiere decir que cada archivo modulo (key del diccionario
    devuelto) tiene como value a todas las funciones que estan en el, cada una con sus caracteristicas.]'''
    
    #Declaro el diccionario vacio para llenar luego
    datos_ordenados_por_modulo = {}

    #Cargo la primera linea del archivo fuente
    linea_fuente = archivo_fuente.readline()
    #Mientras el archivo tenga lineas para leer
    while linea_fuente:
        #Desempaqueto los datos de cada linea
        nombre_funcion, parametros_funcion, modulo_funcion, *lineas_funcion = linea_fuente.split('","')
        #Si el modulo no esta como key del diccionario, entonces lo agrego
        if modulo_funcion not in datos_ordenados_por_modulo:
            datos_ordenados_por_modulo[modulo_funcion] = {}
        #Si la funcion no esta como key del modulo entonces la agrego y le doy forma
        if nombre_funcion not in datos_ordenados_por_modulo[modulo_funcion]:
            datos_ordenados_por_modulo[modulo_funcion][nombre_funcion] = {"parametros": None,
                                                                            "lineas": None
                                                                        }
        #Agrego los datos a sus respectivos lugares
        datos_ordenados_por_modulo[modulo_funcion][nombre_funcion]["parametros"] = parametros_funcion
        datos_ordenados_por_modulo[modulo_funcion][nombre_funcion]["lineas"] = lineas_funcion
        #Avanzo a la siguiente linea
        linea_fuente = archivo_fuente.readline()

    #Cargo la primera linea del archivo de comentarios
    linea_comentarios = archivo_comentarios.readline()
    #Mientras el archivo tenga lineas para leer
    while linea_comentarios:
        #Desempaqueto los datos de cada linea
        nombre_funcion, autor_funcion, ayuda_funcion, *otros = linea_comentarios.split('","')
        for modulo_funcion in datos_ordenados_por_modulo:
            #Si la funcion a la que pertenecen los datos no esta como key del diccionario entonces la agrego
            if nombre_funcion not in datos_ordenados_por_modulo[modulo_funcion]:
                datos_ordenados_por_modulo[modulo_funcion][nombre_funcion] = {}
            #Si comentarios no es una key del diccioanrio de la funcion entonces la agrego y le doy forma
            if "comentarios" not in datos_ordenados_por_modulo[modulo_funcion][nombre_funcion]:
                datos_ordenados_por_modulo[modulo_funcion][nombre_funcion]["comentarios"] = {"autor": None,
                                                                                            "ayuda": None,
                                                                                            "otros": None}
            #Agrego los datos a sus respectivos lugares
            datos_ordenados_por_modulo[modulo_funcion][nombre_funcion]["comentarios"]["autor"] = autor_funcion
            datos_ordenados_por_modulo[modulo_funcion][nombre_funcion]["comentarios"]["ayuda"] = ayuda_funcion if ("Ayuda" in ayuda_funcion) else None
            datos_ordenados_por_modulo[modulo_funcion][nombre_funcion]["comentarios"]["otros"] = otros if len(otros) > 1 else None
        #Avanzo a la siguiente linea del archivo
        linea_comentarios = archivo_comentarios.readline()

    return datos_ordenados_por_modulo