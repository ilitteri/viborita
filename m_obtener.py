import os

def ubicaciones_modulos(archivo_principal):
    '''[Autor: Ivan Litteri]
    [Ayuda: Lee el archivo principal que le llega por parametro (en nuestro caso el .txt), y retorna una lista con las 
    lineas de ese archivo (en este caso cada linea corresponde a las ubicaciones de los archivos de la aplicacion a 
    anlizar).]'''
    #Abro el archivo y obtengo una lista de todas sus lineas
    with open(archivo_principal, "r") as archivo:
        ubicaciones = archivo.read().splitlines()

    #Devuelvo la lista de lineas 
    return ubicaciones

def nombres_archivos_csv_individuales(ubicaciones_modulos):
    '''[Autor: Ivan Litteri]
    [Ayuda: Obtiene 2 listas de nombres (uno para fuentes y otro para comentarios).]'''

    #lista de nombres de modulos
    nombres_modulos = [ubicacion_modulo.split("\\")[-1] for ubicacion_modulo in ubicaciones_modulos]
    #Lista de todos los nombres de los archivos fuente
    nombres_archivos_fuente_individuales = [f'fuente_{nombre_modulo}.csv' for nombre_modulo in nombres_modulos]
    #Lista de todos los nombres de los archivos de comentarios
    nombres_archivos_comentarios_individuales = [f'comentarios_{nombre_modulo}.csv' for nombre_modulo in nombres_modulos]

    #Retorna las listas
    return nombres_archivos_fuente_individuales, nombres_archivos_comentarios_individuales

def nombres_modulos(ubicaciones_modulos):
    '''[Autor: Ivan Litteri]'''
    return [ubicacion_modulo.split("\\")[-1] for ubicacion_modulo in ubicaciones_modulos]

def ubicaciones_archivos_csv_individuales(nombres_archivos_csv_individuales):
    '''[Autor: Ivan Litteri]'''

    #Retorna una lista de ubicaciones de todos los archivos .csv individuales
    return [os.path.abspath(nombre_archivo_csv_individual) for nombre_archivo_csv_individual in nombres_archivos_csv_individuales]

def cantidad_invocaciones(datos, key_invocaciones, archivo_fuente, bandera = False):
    '''[Autor: Ivan Litteri]
    [Ayuda: le llega por parametro una linea, y una lista con los nombres de las funciones, analiza por cada
    nombre de funcion si este esta en la linea, en caso verdadero incrementa en uno el contador de invocaciones
    de esa funcion]'''

    for funcion in datos:
        for linea_funcion in datos[funcion]["lineas"]:
            for nombre_funcion in datos:
                if key_invocaciones not in datos[nombre_funcion]:
                    datos[nombre_funcion][key_invocaciones] = 0
                if nombre_funcion in linea_funcion and  (nombre_funcion[0] == linea_funcion[0] or f' {nombre_funcion}(' in linea_funcion):
                    datos[nombre_funcion][key_invocaciones] += 1
                    if bandera:
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

def lineas_codigo_totales(datos_por_cantidad_lineas_autor):
    '''[Autor: Ivan Litteri]
    [Ayuda: le llega por parametro el diccionario ordenado por cantidad de lineas totales por autor (si se pasase otro
    no funcionaria) y devuelve la cantidad de lineas totales de todos los codigos involucrados en la aplicacion]'''
    return sum(datos_por_cantidad_lineas_autor[autor]["funciones"][funcion] for autor in datos_por_cantidad_lineas_autor for funcion in datos_por_cantidad_lineas_autor[autor]["funciones"])

def porcentaje_lineas_codigo(autor, datos_autor, lineas_codigo_totales):
    '''[Autor: Ivan Litteri]
    [Ayuda: le llega por parametro el diccionario ordenado por cantidad de lineas totales por autor (si se pasase otro
    no funcionaria), el autor que se desea evaluar y devuelve el porcentaje de lineas de codigo que ese autor escribio]'''
    
    return (datos_autor["lineas_totales"] / lineas_codigo_totales) * 100

def lista_funciones(archivo_fuente):
    '''[Autor: Ivan Litteri]
    [Ayuda: le llegan un objeto de text.IO (datos del archivo fuente_unico) y devuelve una lista con los nombres de todas
    las funciones]'''

    funciones = []
    #Obtiene la primera linea del archivo
    linea_fuente = archivo_fuente.readline()
    while linea_fuente:
        #Agrega a la lista de funciones la funcion correspondiente al primer campo de la linea
        funciones.append(linea_fuente.split('","')[0])
        #Avanza de linea en el archivo
        linea_fuente = archivo_fuente.readline()

    return funciones

def tabla_para_imprimir(lista_funciones):
    '''[Autor: Joel Glauber]
    [Ayuda: A esta funcion le llega por parametro una lista con los nombres de todas las funciones
    y concatena a estos nombres a una cadena que llamo tabla, con un formato como el que se pide en 
    la consigna (5 columnas, x filas)]'''
    
    #Creo una cadena vacia, para llenar luego con los nombres de las funciones
    tabla = ""
    #Recorro los indices de la lista
    for i in range(len(lista_funciones)):
        #Si llegue a una columna 5 entonces da un enter para pasar a la siguiente fila
        if (i % 5 == 0) and (i != 0):
            tabla += "|\n" 
        separacion = " " * (15-len(lista_funciones[i]))
        fila = f'\t| {lista_funciones[i]}(){separacion}'
        #Sumo los nombres de las funciones separadas con una tabulacion
        tabla += fila

    return tabla