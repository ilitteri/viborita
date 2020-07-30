import os

def informacion_ubicaciones(nombre_archivo):
    '''[Autor: Ivan Litteri]
    [Ayuda: Lee el archivo principal que le llega por parametro (en nuestro caso el .txt), y retorna una lista con las 
    lineas de ese archivo (en este caso cada linea corresponde a las ubicaciones de los archivos de la aplicacion a 
    anlizar).]'''

    ubicaciones = []
    #Obtiene el sistema operativo en el que se esta ejecutando la aplicacion
    sep = os.path.sep
    #Abre el archivo de programas para obtener las ubicaciones
    with open(nombre_archivo, "r") as archivo_programas:
        #Carga la primera linea del archivo, que corresponde a la primera ubicacion
        ubicacion = archivo_programas.readline().strip()
        #Mientras haya linea para leer en el archivo
        while ubicacion:
            ubicaciones.append((ubicacion, ubicacion.split(sep)[-1]))
            ubicacion = archivo_programas.readline().strip()

    return ubicaciones

def ubicaciones_archivos_csv_individuales(nombres_csv_individuales):
    '''[Autor: Ivan Litteri]'''

    #Retorna una lista de ubicaciones de todos los archivos .csv individuales
    return [os.path.abspath(nombre_csv_individual) for nombre_csv_individual in nombres_csv_individuales]

def cantidad_invocaciones(datos_csv):
    '''[Autor: Ivan Litteri]
    [Ayuda: agrega invocaciones a la lista de invocaciones si una funcion invoca alguna funcion, e incrementa la cantidad de veces que es invocada esa funcion.]'''

    #Recorre todas las funciones
    for funcion in datos_csv:
        #Por cada funcion itera sobre todas las lineas de esa funcion
        for linea_funcion in datos_csv[funcion]["lineas"]:
            #Por cada linea itero todas las funciones, fijandome si esa funcion es invocada en la linea
            for nombre_funcion in datos_csv:
                if ("cantidad_invocaciones" not in datos_csv[nombre_funcion]):
                    datos_csv[nombre_funcion]["cantidad_invocaciones"] = 0
                if (f'{nombre_funcion}(' in linea_funcion) and (not f'_{nombre_funcion}' in linea_funcion):
                    datos_csv[nombre_funcion]["cantidad_invocaciones"] += 1
                    datos_csv[funcion]["invocaciones"].append(nombre_funcion)
                elif (f'{datos_csv[nombre_funcion]["modulo"]}.{nombre_funcion}(' in linea_funcion):
                    datos_csv[nombre_funcion]["cantidad_invocaciones"] += 1
                    datos_csv[funcion]["invocaciones"].append(nombre_funcion)

    #Devuelve el diccionario actualizado
    return datos_csv

def cantidad_declaraciones(datos_csv, lineas_funcion, nombre_funcion):
    '''[Autor: Santiago Vaccarelli]
    [Ayuda: incrementa la cantidad de declaraciones en caso de encontrarlas mientras recorre cada linea.]'''

    #Recorre todas las lineas de la funcion e incrementa la declaracion que sea valida en caso de encontrarla
    for linea_funcion in lineas_funcion:
        if ("for " in linea_funcion):
            datos_csv[nombre_funcion]["cantidad_declaraciones"]["for"] += linea_funcion.count("for")
        if ("return " in linea_funcion):
            datos_csv[nombre_funcion]["cantidad_declaraciones"]["returns"] += 1
        if ("if " in linea_funcion): #Contamos solo "if " porque en todo "elif " hay un "if "
            datos_csv[nombre_funcion]["cantidad_declaraciones"]["if/elif"] += 1
        if ("while " in linea_funcion):
            datos_csv[nombre_funcion]["cantidad_declaraciones"]["while"] += 1
        if ("break" in linea_funcion):
            datos_csv[nombre_funcion]["cantidad_declaraciones"]["break"] += 1
        if ("exit" in linea_funcion):
            datos_csv[nombre_funcion]["cantidad_declaraciones"]["exit"] += 1

    #Devuelve el diccionario actualizado 
    return datos_csv

def porcentaje_lineas_codigo(autor, datos_csv, lineas_codigo_totales):
    '''[Autor: Ivan Litteri]
    [Ayuda: le llega por parametro el diccionario ordenado por cantidad de lineas totales por autor (si se pasase otro
    no funcionaria), el autor que se desea evaluar y devuelve el porcentaje de lineas de codigo que ese autor escribio]'''
    
    return (datos_csv["lineas_totales"] / lineas_codigo_totales) * 100

def tabla_funciones(lista_funciones):
    '''[Autor: Joel Glauber]
    [Ayuda: repasa la lista que le llega y devuelve una tabla formateada por 5 columnas y "x" filas.]'''
    
    primera_fila = True
    cantidad_guiones = 0
    longitud_maxima_funcion = maxima_longitud(lista_funciones)
    #Creo una cadena vacia, para llenar luego con los nombres de las funciones
    tabla = ""
    #Recorro los indices de la lista
    for i in range(len(lista_funciones)):
        #Si llegue a una columna 5 entonces da un enter para pasar a la siguiente fila
        if (i % 5 == 0) and (i != 0):
            tabla += "|\n"
            if primera_fila:
                cantidad_guiones = len(tabla)
                primera_fila = False
        separacion = " " * (longitud_maxima_funcion - len(lista_funciones[i]))
        fila = f'| {lista_funciones[i]}(){separacion}'
        #Sumo los nombres de las funciones separadas con una tabulacion
        tabla += fila
    tabla += "|"
    
    return tabla, cantidad_guiones

def longitud_maxima(columnas_datos, longitud):
    '''[Autor: Santiago Vaccarelli]
    [Ayuda: busca las longitudes mas largas para cada columna del la tabla]'''

    #itera los elementos de una lista
    for elemento in range(len(columnas_datos)):
        #compara para cada indice de la lista si la longitud es mayor
        if (len(columnas_datos[elemento]) > longitud[elemento]):
            longitud[elemento] = len(columnas_datos[elemento])
    
    return longitud

def maxima_longitud(lista_funciones):
    '''[Autor: Ivan Litteri]'''
    #Devuelve la longitud del elemento mas largo de la lista que le llega por parametro
    return len(max(lista_funciones, key=len))

def cantidad_parametros(parametros):
    '''[Autor: Ivan Litteri]
    [Ayuda: le llegan parametros entre parentesis y cuenta la cantidad de los mismos]'''

    cant_param = 0
    i = 0
    
    #Si llegan parentesis vacios devuelve 0
    if parametros == "()":
        cant_param = 0
    #Si hay una coma incrementa, y se fija cuantas comas hay
    elif "," in parametros:
        cant_param += 1
        while i < len(parametros):
            if parametros[i] == "," and parametros[i+1] != ")":
                cant_param += 1
            i += 1
    #Si no hay comas ni el parentesis es vacio, hay un solo parametro
    else:
        cant_param = 1
    
    return cant_param