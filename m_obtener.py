import os
import platform

def informacion_ubicaciones(nombre_archivo):
    '''[Autor: Ivan Litteri]
    [Ayuda: Lee el archivo principal que le llega por parametro (en nuestro caso el .txt), y retorna una lista con las 
    lineas de ese archivo (en este caso cada linea corresponde a las ubicaciones de los archivos de la aplicacion a 
    anlizar).]'''
    ubicaciones = []
    os = platform.system()
    with open(nombre_archivo, "r") as archivo_programas:
        ubicacion = archivo_programas.readline().strip()
        while ubicacion:
            if os == "Linux" or os == "Darwin":
                ubicaciones.append((ubicacion, ubicacion.split("/")[-1]))
            elif os == "Windows":
                ubicaciones.append((ubicacion, ubicacion.split("\\")[-1]))
            ubicacion = archivo_programas.readline().strip()

    return ubicaciones

def ubicaciones_archivos_csv_individuales(nombres_archivos_csv_individuales):
    '''[Autor: Ivan Litteri]'''

    #Retorna una lista de ubicaciones de todos los archivos .csv individuales
    return [os.path.abspath(nombre_archivo_csv_individual) for nombre_archivo_csv_individual in nombres_archivos_csv_individuales]

def cantidad_invocaciones(datos, archivo_fuente):
    '''[Autor: Ivan Litteri]
    [Ayuda: le llega por parametro una linea, y una lista con los nombres de las funciones, analiza por cada
    nombre de funcion si este esta en la linea, en caso verdadero incrementa en uno el contador de invocaciones
    de esa funcion]'''



    for funcion in datos:
        for linea_funcion in datos[funcion]["lineas"]:
            for nombre_funcion in datos:
                if "cantidad_invocaciones" not in datos[nombre_funcion]:
                    datos[nombre_funcion]["cantidad_invocaciones"] = 0
                if (f'{nombre_funcion}(' in linea_funcion or f'{nombre_funcion[:-2]}(' in linea_funcion) and (not f'_{nombre_funcion}' in linea_funcion):
                    datos[nombre_funcion]["cantidad_invocaciones"] += 1
                    datos[funcion]["invocaciones"].append(nombre_funcion)
                elif (f'{datos[nombre_funcion]["modulo"]}.{nombre_funcion}(' in linea_funcion) or (f'{datos[nombre_funcion]["modulo"]}.{nombre_funcion[:-2]}(' in linea_funcion):
                    datos[nombre_funcion]["cantidad_invocaciones"] += 1
                    datos[funcion]["invocaciones"].append(nombre_funcion)

    return datos

def cantidad_declaraciones(datos_fuente, lineas_funcion, nombre_funcion):
    '''[Autor: Santiago Vaccarelli]
    [Ayuda: esta funcion recibe un diccionario, una lista de lineas, un nombre de funcion; en donde
    sera analizada la lista de lineas para contar la cantidad de declaraciones, y estas cantidades una vez
    obtenidas, ser actualizadas en el diccionario con nombre de funcion como key]'''

    for linea_funcion in lineas_funcion:
        if "for" in linea_funcion:
            datos_fuente[nombre_funcion]["cantidad_declaraciones"]["for"] += linea_funcion.count("for")
        if "return" in linea_funcion:
            datos_fuente[nombre_funcion]["cantidad_declaraciones"]["returns"] += 1
        if "if" in linea_funcion:
            datos_fuente[nombre_funcion]["cantidad_declaraciones"]["if/elif"] += 1
        elif "elif" in linea_funcion:
            datos_fuente[nombre_funcion]["cantidad_declaraciones"]["if/elif"] += 1
        elif "while" in linea_funcion:
            datos_fuente[nombre_funcion]["cantidad_declaraciones"]["while"] += 1
        elif "break" in linea_funcion:
            datos_fuente[nombre_funcion]["cantidad_declaraciones"]["break"] += 1
        elif "exit" in linea_funcion:
            datos_fuente[nombre_funcion]["cantidad_declaraciones"]["exit"] += 1

    return datos_fuente

def porcentaje_lineas_codigo(autor, datos_autor, lineas_codigo_totales):
    '''[Autor: Ivan Litteri]
    [Ayuda: le llega por parametro el diccionario ordenado por cantidad de lineas totales por autor (si se pasase otro
    no funcionaria), el autor que se desea evaluar y devuelve el porcentaje de lineas de codigo que ese autor escribio]'''
    
    return (datos_autor["lineas_totales"] / lineas_codigo_totales) * 100

def tabla_funciones(lista_funciones, primera_fila = True):
    '''[Autor: Joel Glauber]
    [Ayuda: A esta funcion le llega por parametro una lista con los nombres de todas las funciones
    y concatena a estos nombres a una cadena que llamo tabla, con un formato como el que se pide en 
    la consigna (5 columnas, x filas)]'''
    
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
        separacion = " " * (longitud_maxima_funcion-len(lista_funciones[i]))
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
        if len(columnas_datos[elemento]) > longitud[elemento]:
            longitud[elemento] = len(columnas_datos[elemento])
    
    return longitud

def maxima_longitud(lista_funciones):
    '''[Autor: Ivan Litteri]'''
    return len(max(lista_funciones, key=len))