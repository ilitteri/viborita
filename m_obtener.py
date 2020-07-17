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

def cantidad_declaraciones(datos_fuente, lineas_funciones, nombre_funcion):
    '''[Autor: Santiago Vaccarelli]
    [Ayuda: esta funcion recibe un diccionario, una lista de lineas, un nombre de funcion; en donde
    sera analizada la lista de lineas para contar la cantidad de declaraciones, y estas cantidades una vez
    obtenidas, ser actualizadas en el diccionario con nombre de funcion como key]'''

    for linea_funcion in lineas_funciones:
            if "for" in linea_funcion:
                datos_fuente[nombre_funcion]["for"] += linea_funcion.count("for")
            if "return" in linea_funcion:
                datos_fuente[nombre_funcion]["returns"] += 1
            if "if" in linea_funcion:
                datos_fuente[nombre_funcion]["if/elif"] += 1
            elif "elif" in linea_funcion:
                datos_fuente[nombre_funcion]["if/elif"] += 1
            elif "while" in linea_funcion:
                datos_fuente[nombre_funcion]["while"] += 1
            elif "break" in linea_funcion:
                datos_fuente[nombre_funcion]["break"] += 1
            elif "exit" in linea_funcion:
                datos_fuente[nombre_funcion]["exit"] += 1

def lineas_codigo_totales(datos_por_cantidad_lineas_autor):
    '''[Autor: Ivan Litteri]
    [Ayuda: le llega por parametro el diccionario ordenado por cantidad de lineas totales por autor (si se pasase otro
    no funcionaria) y devuelve la cantidad de lineas totales de todos los codigos involucrados en la aplicacion]'''
    return sum(datos_por_cantidad_lineas_autor[autor]["funciones"][funcion] for autor in datos_por_cantidad_lineas_autor for funcion in datos_por_cantidad_lineas_autor[autor]["funciones"])

def porcentaje_lineas_codigo(datos, autor_actual, lineas_codigo_totales):
    '''[Autor: Ivan Litteri]
    [Ayuda: le llega por parametro el diccionario ordenado por cantidad de lineas totales por autor (si se pasase otro
    no funcionaria), el autor que se desea evaluar y devuelve el porcentaje de lineas de codigo que ese autor escribio]'''
    
    return (datos[autor_actual]["lineas_totales"] / lineas_codigo_totales) * 100

def lista_funciones(archivo_fuente):
    funciones = []

    linea_fuente = archivo_fuente.readline()
    while linea_fuente:
        funciones.append(linea_fuente.split('","')[0].replace('"', ''))
        linea_fuente = archivo_fuente.readline()

    return funciones