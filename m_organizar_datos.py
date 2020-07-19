import m_obtener as obtener

def por_funciones(archivo_fuente, archivo_comentarios):
    '''[Autor: Ivan Litteri]
    [Ayuda: esta funcion recibe los archivos fuente y comentarios (csv) y los analiza y devuelve sus datos
    en funcion de las funciones. Esto quiere decir que cada funcion (key del diccionario) contiene todos 
    los datos de esa funcion (parametros, modulo al que pertenece, lineas, comentarios)'''

    #Declaro el diccionario vacio para llenar luego
    datos_ordenados_por_funcion = {}

    #Cargo la primera linea del archivo fuente
    linea_fuente = archivo_fuente.readline()
    #Cargo la primera linea del archivo de comentarios
    linea_comentarios = archivo_comentarios.readline()
    #Mientras el archivo tenga lineas para leer
    while linea_fuente and linea_comentarios:
        #Desempaqueto los datos de cada linea
        nombre_funcion_f, parametros_funcion_f, modulo_funcion_f, *lineas_funcion_f = linea_fuente.split('","')
        #Desempaqueto los datos de cada linea
        nombre_funcion_c, autor_funcion_c, ayuda_funcion_c, *otros_c = linea_comentarios.split('","')

        nombre_funcion_f = nombre_funcion_c = nombre_funcion_f.replace('"', '')
        #Si la funcion no esta como key del diccionario, entonces la agrego y le doy su forma
        if nombre_funcion_f not in datos_ordenados_por_funcion:
            datos_ordenados_por_funcion[nombre_funcion_f] = {"parametros": None,
                                                            "modulo": None,
                                                            "lineas": None,
                                                            "cantidad_lineas": 0,
                                                            "invocaciones": [],
                                                            "cantidad_invocaciones": 0,
                                                            "cantidad_parametros": 0
                                                            }
        #Agrego los datos a sus respectivos lugares
        datos_ordenados_por_funcion[nombre_funcion_f]["parametros"] = parametros_funcion_f if len(parametros_funcion_f) > 2 else None
        datos_ordenados_por_funcion[nombre_funcion_f]["modulo"] = modulo_funcion_f
        datos_ordenados_por_funcion[nombre_funcion_f]["lineas"] = lineas_funcion_f
        datos_ordenados_por_funcion[nombre_funcion_f]["cantidad_lineas"] = len(lineas_funcion_f)
        datos_ordenados_por_funcion[nombre_funcion_f]["cantidad_parametros"] = len(parametros_funcion_f.split(",")) if parametros_funcion_f else 0
        #Si la key comentarios aun no existe en la funcion lo agrego y le doy forma
        if "comentarios" not in datos_ordenados_por_funcion[nombre_funcion_c]:
            datos_ordenados_por_funcion[nombre_funcion_c]["comentarios"] = {"autor": None,
                                                                            "ayuda": None,
                                                                            "otros": None}
        #Agrego los datos a sus respectivos lugares
        datos_ordenados_por_funcion[nombre_funcion_c]["comentarios"]["autor"] = autor_funcion_c
        datos_ordenados_por_funcion[nombre_funcion_c]["comentarios"]["ayuda"] = ayuda_funcion_c.replace('",\n', '') if ("Ayuda" in ayuda_funcion_c) else None
        datos_ordenados_por_funcion[nombre_funcion_c]["comentarios"]["otros"] = otros_c if len(otros_c) > 0 else None
        if "cantidad_decalraciones" not in datos_ordenados_por_funcion[nombre_funcion_f]:
            datos_ordenados_por_funcion[nombre_funcion_f]["cantidad_declaraciones"] = {"parametros": 0,
                                                                                        "returns": 0,
                                                                                        "if/elif": 0,
                                                                                        "for": 0,
                                                                                        "while": 0,
                                                                                        "break": 0,
                                                                                        "exit": 0,
                                                                                        "coment": len(otros_c)
                                                                                        }
        obtener.cantidad_declaraciones(datos_ordenados_por_funcion, lineas_funcion_f, nombre_funcion_f)
        #Avanzo de linea en el archivo
        linea_fuente = archivo_fuente.readline()
        #Avanzo de linea en el archivo
        linea_comentarios = archivo_comentarios.readline()

    obtener.cantidad_invocaciones(datos_ordenados_por_funcion, "cantidad_invocaciones", archivo_fuente, True)

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
    #Cargo la primera linea del archivo de comentarios
    linea_comentarios = archivo_comentarios.readline()
    #Mientras el archivo tenga lineas para leer
    while linea_fuente and linea_comentarios:
        #Desempaqueto los datos de cada linea
        nombre_funcion_f, parametros_funcion_f, modulo_funcion_f, *lineas_funcion_f = linea_fuente.split('","')
        #Desempaqueto los datos de cada linea
        nombre_funcion_c, autor_funcion_c, ayuda_funcion_c, *otros_c = linea_comentarios.split('","')
        #Si el modulo no esta como key del diccionario, entonces lo agrego
        if modulo_funcion_f not in datos_ordenados_por_modulo:
            datos_ordenados_por_modulo[modulo_funcion_f] = {}
        #Si la funcion no esta como key del modulo entonces la agrego y le doy forma
        if nombre_funcion_f not in datos_ordenados_por_modulo[modulo_funcion_f]:
            datos_ordenados_por_modulo[modulo_funcion_f][nombre_funcion_f] = {"parametros": None,
                                                                            "lineas": None
                                                                        }
        #Agrego los datos a sus respectivos lugares
        datos_ordenados_por_modulo[modulo_funcion_f][nombre_funcion_f]["parametros"] = parametros_funcion_f if len(parametros_funcion_f) > 2 else None
        datos_ordenados_por_modulo[modulo_funcion_f][nombre_funcion_f]["lineas"] = lineas_funcion_f
        #Si la funcion a la que pertenecen los datos no esta como key del diccionario entonces la agrego
        if nombre_funcion_c not in datos_ordenados_por_modulo[modulo_funcion_f]:
            datos_ordenados_por_modulo[modulo_funcion_f][nombre_funcion_c] = {}
        #Si comentarios no es una key del diccioanrio de la funcion entonces la agrego y le doy forma
        if "comentarios" not in datos_ordenados_por_modulo[modulo_funcion_f][nombre_funcion_c]:
            datos_ordenados_por_modulo[modulo_funcion_f][nombre_funcion_c]["comentarios"] = {"autor": None,
                                                                                        "ayuda": None,
                                                                                        "otros": None}
        #Agrego los datos a sus respectivos lugares
        datos_ordenados_por_modulo[modulo_funcion_f][nombre_funcion_c]["comentarios"]["autor"] = autor_funcion_c
        datos_ordenados_por_modulo[modulo_funcion_f][nombre_funcion_c]["comentarios"]["ayuda"] = ayuda_funcion_c if ("Ayuda" in ayuda_funcion_c) else None
        datos_ordenados_por_modulo[modulo_funcion_f][nombre_funcion_c]["comentarios"]["otros"] = otros_c if len(otros_c) > 0 else None
        #Avanzo a la siguiente linea
        linea_fuente = archivo_fuente.readline()
        #Avanzo a la siguiente linea del archivo
        linea_comentarios = archivo_comentarios.readline()

    return datos_ordenados_por_modulo

def por_autor(archivo_fuente, archivo_comentarios):
    '''[Autor: Ivan Litteri]
    [Ayuda: esta funcion recibe por parametro los datos de los archivos fuente y comentarios (csv) y los 
    lee secuencialmente para organizar los datos, en este caso, por autor y cada autor tiene las funciones
    que desarrollo y cada funcion sus datos.]'''

    #Inicializo el diccionario en vacio
    datos_ordenados_por_autor = {}

    #Cargo la primera linea del archivo de comentarios
    linea_comentarios = archivo_comentarios.readline()
    #Cargo la primera linea del archivo fuente
    linea_fuente = archivo_fuente.readline()
    #Mientras haya lineas para leer del archivo comentarios entra al while
    while linea_comentarios and linea_fuente:
        #Desempaqueto los datos de la linea que estoy leyendo en cada iteracion
        nombre_funcion_c, autor_funcion_c, ayuda_funcion_c, *otros_c = linea_comentarios.split('","')
        #Desempaqueto los datos de la linea que estoy leyendo en cada iteracion
        nombre_funcion_f, parametros_funcion_f, modulo_funcion_f, *lineas_funcion_f = linea_fuente.split('","')
        #Le doy forma al diccionario 
        if autor_funcion_c not in datos_ordenados_por_autor:
            datos_ordenados_por_autor[autor_funcion_c] = {}
        if nombre_funcion_c not in datos_ordenados_por_autor[autor_funcion_c]:
            datos_ordenados_por_autor[autor_funcion_c][nombre_funcion_c] = {"comentarios": {"ayuda": None,
                                                                                        "otros": None,
                                                                            "modulo": None,
                                                                            "parametros": None,
                                                                            "lineas": None
                                                                                        }
                                                                        }
        #Agrego los datos al diccionario
        datos_ordenados_por_autor[autor_funcion_c][nombre_funcion_c]["comentarios"]["ayuda"] =  ayuda_funcion_c if ("Ayuda" in ayuda_funcion_c) else None
        datos_ordenados_por_autor[autor_funcion_c][nombre_funcion_c]["comentarios"]["otros"] =  otros_c if len(otros) > 0 else None
        if nombre_funcion_f not in datos_ordenados_por_autor[autor_funcion_c]:
            datos_ordenados_por_autor[autor_funcion_c][nombre_funcion_f] = {"modulo": None,
                                                                        "parametros": None,
                                                                        "lineas": None}
        #Agrego los datos al diccionario por cada autor
        datos_ordenados_por_autor[autor_funcion_c][nombre_funcion_f]["modulo"] = modulo_funcion_f
        datos_ordenados_por_autor[autor_funcion_c][nombre_funcion_f]["parametros"] = parametros_funcion_f if len(parametros_funcion_f) > 2 else None
        datos_ordenados_por_autor[autor_funcion_c][nombre_funcion_f]["lineas"] = lineas_funcion_f
        #Cargo la siguiente linea en el archivo en caso de que haya
        linea_comentarios = archivo_comentarios.readline()
        #Cargo la siguiente linea en el archivo en caso de que haya
        linea_fuente = archivo_fuente.readline()

    return datos_ordenados_por_autor

def por_cantidad_lineas_autor(archivo_fuente, archivo_comentarios):
    '''[Autor: Ivan Litteri]
    [Ayuda: esta funcion recibe por parametro los datos de los archivos fuente y comentarios (csv) y los 
    lee secuencialmente para organizar los datos, en este caso tambien por autor pero por cada funcion
    los datos que tengo son la cantidad de lineas de esa funcion.]'''

    #Inicializo el diccionario en vacio
    datos_ordenados_cantidad_lineas_autor = {}

    #Cargo la primera linea del archivo de comentarios
    linea_comentarios = archivo_comentarios.readline()
    #Cargo la primera linea del archivo fuente
    linea_fuente = archivo_fuente.readline()
    #Mientras haya lineas para leer del archivo comentarios entra al while
    while linea_comentarios and linea_fuente:
        #Desempaqueto los datos de la linea que estoy leyendo en cada iteracion
        nombre_funcion_c, autor_funcion_c, ayuda_funcion_c, *otros_c = linea_comentarios.split('","')
        #Desempaqueto los datos de la linea que estoy leyendo en cada iteracion
        nombre_funcion_f, parametros_funcion_f, modulo_funcion_f, *lineas_funcion_f = linea_fuente.split('","')
        #Elimina la comilla doble al principio del string de la funcion
        nombre_funcion_f = nombre_funcion_c = nombre_funcion_f.replace('"', '')
        #Agrega los datos a el diccionario
        if autor_funcion_c not in datos_ordenados_cantidad_lineas_autor:
            datos_ordenados_cantidad_lineas_autor[autor_funcion_c] = {"lineas_totales": 0, "funciones": {}}
        if nombre_funcion_c not in datos_ordenados_cantidad_lineas_autor[autor_funcion_c]["funciones"]:
            datos_ordenados_cantidad_lineas_autor[autor_funcion_c]["funciones"][nombre_funcion_c] = -1
        if nombre_funcion_f in datos_ordenados_cantidad_lineas_autor[autor_funcion_c]["funciones"]:
            datos_ordenados_cantidad_lineas_autor[autor_funcion_c]["funciones"][nombre_funcion_f] = len(lineas_funcion_f)
            datos_ordenados_cantidad_lineas_autor[autor_funcion_c]["lineas_totales"] += len(lineas_funcion_f)
        #Cargo la siguiente linea en el archivo en caso de que haya
        linea_comentarios = archivo_comentarios.readline()
        #Cargo la siguiente linea en el archivo en caso de que haya
        linea_fuente = archivo_fuente.readline()

    return datos_ordenados_cantidad_lineas_autor