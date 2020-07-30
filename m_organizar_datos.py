import m_obtener as obtener

def actualizar_diccionario_funciones(datos_por_funciones, nombre_funcion, parametros_funcion, modulo_funcion, lineas_funcion, autor_funcion, ayuda_funcion, otros_c):
    '''[Autor: Ivan Litteri]
    [Ayuda: recibe los datos extraidos de una linea leida de los archivos csv y los guarda en el diccionario final.]'''

    #Si la funcion no esta como key del diccionario, entonces la agrego y le doy su forma
    if (nombre_funcion not in datos_por_funciones):
        datos_por_funciones[nombre_funcion] = {"parametros": None,
                                                        "modulo": None,
                                                        "lineas": None,
                                                        "cantidad_lineas": 0,
                                                        "invocaciones": [],
                                                        "cantidad_invocaciones": 0,
                                                        "cantidad_parametros": 0,
                                                        "cantidad_comentarios": len(otros_c),
                                                        }
    #Agrego los datos a sus respectivos lugares
    datos_por_funciones[nombre_funcion]["parametros"] = parametros_funcion if len(parametros_funcion) > 2 else None
    datos_por_funciones[nombre_funcion]["modulo"] = modulo_funcion
    datos_por_funciones[nombre_funcion]["lineas"] = lineas_funcion
    datos_por_funciones[nombre_funcion]["cantidad_lineas"] = len(lineas_funcion)
    datos_por_funciones[nombre_funcion]["cantidad_parametros"] = obtener.cantidad_parametros(parametros_funcion)
    #Si la key comentarios aun no existe en la funcion lo agrego y le doy forma
    if ("comentarios" not in datos_por_funciones[nombre_funcion]):
        datos_por_funciones[nombre_funcion]["comentarios"] = {"autor": None,
                                                                        "ayuda": None,
                                                                        "otros": None}
    #Agrego los datos a sus respectivos lugares
    datos_por_funciones[nombre_funcion]["comentarios"]["autor"] = autor_funcion
    datos_por_funciones[nombre_funcion]["comentarios"]["ayuda"] = ayuda_funcion.replace('",\n', '') if ("Ayuda" in ayuda_funcion) else None
    datos_por_funciones[nombre_funcion]["comentarios"]["otros"] = otros_c if len(otros_c) > 0 else None
    if ("cantidad_decalraciones" not in datos_por_funciones[nombre_funcion]):
        datos_por_funciones[nombre_funcion]["cantidad_declaraciones"] = {"returns": 0,
                                                                                    "if/elif": 0,
                                                                                    "for": 0,
                                                                                    "while": 0,
                                                                                    "break": 0,
                                                                                    "exit": 0,
                                                                                    }
    obtener.cantidad_declaraciones(datos_por_funciones, lineas_funcion, nombre_funcion)

    return datos_por_funciones

def actualizar_diccionario_autores(datos_por_autores, nombre_funcion, lineas_funcion, autor_funcion):
    '''[Autor: Ivan Litteri]
    [Ayuda: recibe los datos extraidos de una linea leida de los archivos csv y los guarda en el diccionario final.]'''

    #Agrega los datos a el diccionario
    if (autor_funcion not in datos_por_autores):
        datos_por_autores[autor_funcion] = {"lineas_totales": 0, "funciones": {}}
    if (nombre_funcion not in datos_por_autores[autor_funcion]["funciones"]):
        datos_por_autores[autor_funcion]["funciones"][nombre_funcion] = -1
    if (nombre_funcion in datos_por_autores[autor_funcion]["funciones"]):
        datos_por_autores[autor_funcion]["funciones"][nombre_funcion] = len(lineas_funcion)
        datos_por_autores[autor_funcion]["lineas_totales"] += len(lineas_funcion)
            
    return datos_por_autores

def leer_archivos_csv(archivo_fuente, archivo_comentarios):
    '''[Autor: Ivan Litteri]
    [Ayuda: recibe los archivos fuente unico y comentarios csv, los lee secuencialemente, extrayendo de cada linea los
    datos deseados y los organiza en diccionarios segun la necesidad]'''

    #Inicializo el diccionario en vacio
    datos_por_autores = {}
    #Declaro el diccionario vacio para llenar luego
    datos_por_funciones = {}

    #Cargo la primera linea del archivo fuente
    linea_fuente = archivo_fuente.readline().rstrip('"\n')
    #Cargo la primera linea del archivo de comentarios
    linea_comentarios = archivo_comentarios.readline().rstrip('"\n')
    #Mientras el archivo tenga lineas para leer
    while (linea_fuente and linea_comentarios):
        #Desempaqueto los datos de cada linea
        nombre_funcion_f, parametros_funcion, modulo_funcion, *lineas_funcion = linea_fuente.split('","')
        #Desempaqueto los datos de cada linea
        nombre_funcion_c, autor_funcion, ayuda_funcion, *otros_c = linea_comentarios.split('","')
        nombre_funcion = nombre_funcion_f = nombre_funcion_c = nombre_funcion_f.replace('"', '')
        #Actualiza los diccionarios con los datos extraidos de las lineas
        datos_por_funciones = actualizar_diccionario_funciones(datos_por_funciones, nombre_funcion, parametros_funcion, modulo_funcion, lineas_funcion, autor_funcion, ayuda_funcion, otros_c)
        datos_por_autores = actualizar_diccionario_autores(datos_por_autores, nombre_funcion, lineas_funcion, autor_funcion)
        #Avanzo de linea en el archivo
        linea_fuente = archivo_fuente.readline().rstrip('"\n')
        #Avanzo de linea en el archivo
        linea_comentarios = archivo_comentarios.readline().rstrip('"\n')

    obtener.cantidad_invocaciones(datos_por_funciones)

    return datos_por_funciones, datos_por_autores