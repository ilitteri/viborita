import m_csv_individuales as csv_individuales
import m_obtener as obtener
import os

def cerrar_csv_individuales(datos):
    '''[Autor: Ivan Litteri]'''

    for archivo in datos:
        datos[archivo].close()

def leer_linea(contenido):
    '''[Autor: Luciano Federico Aguilera]'''

    linea = contenido.readline()

    return linea.rstrip() if linea else chr(255) #Mayor caracter del ASCII

def leer_primeras_lineas(datos):
    '''[Autor: Luciano Federico Aguilera]
    [Ayuda: lee secuencialmente los datos de los archivos individuales que le llegan y los guarda en una lista]'''
    
    #Declara una lista vacia a llenar
    lineas = []

    #Recorro los modulos en el diccionario de datos
    for i in datos:
        #Carga la linea del archivo abierto
        linea = leer_linea(datos[i])
        #Guarda la linea en una lista
        lineas.append(linea)
    
    return lineas

def grabar_csv_final_ordenado(archivo_final, archivos_individuales, lineas_fuera_funcion):
    '''[Autor: Luciano Federico Aguilera]
    [Ayuda: lee las lineas de los archivos individuales, las compara, y graba de forma ordenada alfabeticamente por funcion
    el archivo final]'''

    #Obtiene la menor linea, en este caso la siguiente a imprimir
    obtener_menor_linea = lambda x: min(x)
    #Lee las primeras lineas de los csv
    lineas = leer_primeras_lineas(archivos_individuales)

    #Recorre linea por linea
    linea_menor = obtener_menor_linea(lineas)
    while ((linea_menor != chr(255)) and (linea_menor[0] == '"')):
        indice_menor = lineas.index(linea_menor)
        #Graba la linea y luego la borra de la lista una vez encontrada
        funcion, _, modulo, *otros_datos = linea_menor.split('","')
        if ("*" in modulo) and ((f'{funcion[1:]}()' in lineas_fuera_funcion) or ( f'{funcion[1:]}()\n' in lineas_fuera_funcion)):
            archivo_final.write('"*' + linea_menor[1:] + "\n")
            lineas[indice_menor] = leer_linea(archivos_individuales[f'archivo_{indice_menor}'])
        else:
            archivo_final.write(linea_menor+"\n")
            lineas[indice_menor] = leer_linea(archivos_individuales[f'archivo_{indice_menor}'])
        linea_menor = obtener_menor_linea(lineas)

def abrir_csv_individuales(archivos):
    '''[Autor: Ivan Litteri]
    [Ayuda: se guardan los datos a leer de los archivos individuales en un diccionario.]'''

    diccionario_archivos_abiertos = {}
    for i, archivo in enumerate(archivos):
        if (i not in diccionario_archivos_abiertos):
            diccionario_archivos_abiertos[f'archivo_{i}'] = {}
        diccionario_archivos_abiertos[f'archivo_{i}'] = open(archivo, "r")

    return diccionario_archivos_abiertos

def merge(nombre_archivo_final, archivos_individuales, lineas_fuera_funcion):
    '''[Autor: Luciano Federico Aguilera]
    [Ayuda: abre los "n" archivos individuales y el archivo final en forma paralela, los lee secuencialmente, graba en 
    forma ordenada el archivo final, y luego los cierra una vez finalizado el proceso.]'''

    #Abre los archivos "n" individuales y el archivo final
    archivos_individuales = abrir_csv_individuales(archivos_individuales)
    archivo_final= open(nombre_archivo_final, "w")
    #Graba en forma ordenada las lineas de los individuales en el archivo final
    grabar_csv_final_ordenado(archivo_final, archivos_individuales, lineas_fuera_funcion)
    #Cierra todos los archivos abiertos
    cerrar_csv_individuales(archivos_individuales)
    archivo_final.close()

def borrar_csv_individuales(nombres_archivos_csv_individuales):
    '''[Autor: Ivan Litteri]
    [Ayuda: Borra los archivos .csv individuales (que se encuentran en el repositorio actual) cuyas ubicaciones se obtienen 
    de una funcion a la que le llega por parametro los nombres de los archivos .csv individuales.]'''

    #Obtengo las ubicaciones y las recorro para borrar el archivo que se encuentra en ella.
    for ubicacion_archivo_csv_individual in obtener.ubicaciones_archivos_csv_individuales(nombres_archivos_csv_individuales):
        #Borro el archivo que se encuentra en esa ubicacion.
        os.remove(ubicacion_archivo_csv_individual)

def crear_csv_finales(nombre_archivo):
    '''[Autor: Ivan Litteri]'''

    info_ubicaciones = obtener.informacion_ubicaciones(nombre_archivo)

    archivos_fuente_individuales, archivos_comentarios_individuales, lineas_fuera_funcion = csv_individuales.crear_csv_individuales(info_ubicaciones)
    
    merge("fuente_unico.csv", archivos_fuente_individuales, lineas_fuera_funcion)
    merge("comentarios.csv", archivos_comentarios_individuales, lineas_fuera_funcion)

    nombres_archivos_csv_individuales = archivos_fuente_individuales+archivos_comentarios_individuales
    borrar_csv_individuales(nombres_archivos_csv_individuales)