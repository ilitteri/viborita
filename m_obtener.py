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

    import os
    
    #Retorna una lista de ubicaciones de todos los archivos .csv individuales
    return [os.path.abspath(nombre_archivo_csv_individual) for nombre_archivo_csv_individual in nombres_archivos_csv_individuales]

def datos_csv():
    '''[Autor: Santiago Vaccarelli]
    [Ayuda: Devuelve un diccionario con los datos de cada funcion]'''
    import m_organizar_datos
    with open("fuente_unico.csv", "r") as fuente_unico, open("comentarios.csv", "r") as comentarios:
        datos_archivos_csv = m_organizar_datos.por_funciones(fuente_unico, comentarios)
    return datos_archivos_csv