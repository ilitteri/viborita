import platform
import os
import m_analizar_linea as analizar_linea

def analizar_archivo_programas(nombre_archivo):
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

def analizar_linea_codigo(linea_codigo, ubicacion, nombre_modulo, ubicaciones, datos_fuente, datos_comentarios, linea_fuente, linea_comentarios, autor, ayuda, otros_comentarios, lineas_fuera_funcion, bandera_funcion, bandera_comentario, bandera_ayuda, contador_def):
    if linea_codigo[0:3] != "def" and linea_codigo[0:3] != "   " and linea_codigo != "\n":
            lineas_fuera_funcion.append(linea_codigo)
    elif linea_codigo[0:3] == "def":
        bandera_funcion = True
        contador_def += 1
        if contador_def > 1:
            linea_fuente += "\n"
            linea_comentarios += f',"{autor}","{ayuda}","{otros_comentarios}"\n'
            datos_fuente.append(linea_fuente)
            datos_comentarios.append(linea_comentarios)
            linea_fuente = linea_comentarios = autor = ayuda = otros_comentarios = ""
        else:
            datos_comentarios = []
            datos_fuente = []
        funcion, parametros = analizar_linea.declaracion_funcion(linea_codigo)
        if ubicacion == ubicaciones[0][0]:
            linea_fuente += f'"{funcion}","{parametros}","*{nombre_modulo}"'
        else:
            linea_fuente += f'"{funcion}","{parametros}","{nombre_modulo}"'
        linea_comentarios += f'"{funcion}"'
    elif bandera_funcion:
        if "return" in linea_codigo:
            bandera_funcion = False
        else:
            if bandera_comentario:
                ayuda_funcion, bandera_ayuda = analizar_linea.ayuda_funcion(linea_codigo, bandera_ayuda)
                ayuda += f'{ayuda_funcion}'
                if "'''" in linea_codigo or '"""' in linea_codigo:
                    bandera_comentario = False
            elif "#" in linea_codigo:
                comentario, linea = analizar_linea.comentario_numeral(linea_codigo)
                otros_comentarios += f'{comentario}'
                if linea != "":
                    linea_fuente += f',"{linea}",'
            elif "'''" in linea_codigo or '"""' in linea_codigo:
                if linea_codigo.count("'''") == 2 or linea_codigo.count('"""') == 2:
                    if "Autor" in linea_codigo:
                        autor += f'{analizar_linea.autor_funcion(linea_codigo)}'
                    elif "Ayuda" in linea_codigo:
                        ayuda += f'{linea_codigo[4:-4]}'
                    else:
                        otros_comentarios += f'{linea_codigo[3:-3]}'
                else:
                    bandera_comentario = True
                    autor += f'{analizar_linea.autor_funcion(linea_codigo)}'
            elif linea_codigo:
                linea_fuente += f',"{linea_codigo.strip()}"'
    else:
        lineas_fuera_funcion.append(linea_codigo.strip())
    
    return datos_fuente, datos_comentarios, linea_fuente, linea_comentarios, autor, ayuda, otros_comentarios, lineas_fuera_funcion, bandera_funcion, bandera_comentario, bandera_ayuda, contador_def

def leer_lineas_codigo(codigo, ubicacion, nombre_modulo, ubicaciones, datos_fuente=[], datos_comentarios=[], linea_fuente="", linea_comentarios="", autor="", ayuda="", otros_comentarios="", lineas_fuera_funcion=[], bandera_funcion=False, bandera_comentario=False, bandera_ayuda=False, contador_def=0):

    linea_codigo = codigo.readline().replace('"', "'")
    while linea_codigo:
        datos_fuente, datos_comentarios, linea_fuente, linea_comentarios, autor, ayuda, otros_comentarios, lineas_fuera_funcion, bandera_funcion, bandera_comentario, bandera_ayuda, contador_def =analizar_linea_codigo(linea_codigo, ubicacion, nombre_modulo, ubicaciones, datos_fuente, datos_comentarios, linea_fuente, linea_comentarios, autor, ayuda, otros_comentarios, lineas_fuera_funcion, bandera_funcion, bandera_comentario, bandera_ayuda, contador_def)
        linea_codigo = codigo.readline().replace('"', "'")
    linea_comentarios += f',"{autor}","{ayuda}","{otros_comentarios}"\n'
    linea_fuente += "\n"
    datos_comentarios.append(linea_comentarios)
    datos_fuente.append(linea_fuente)

    return datos_fuente, datos_comentarios

def grabar_individual(archivo, datos_ordenados):
    for linea in datos_ordenados:
        archivo.write(linea)

def ordenar_datos(datos):
    return sorted(datos)

def crear_csv_individuales(ubicaciones):
    archivos_fuente = []
    archivos_comentarios = []
    for ubicacion, nombre_modulo in ubicaciones:
        with open(f'fuente_{nombre_modulo}.csv', "w") as fuente_modulo, open(f'comentarios_{nombre_modulo}.csv', "w") as comentarios_modulo, open(ubicacion, "r") as codigo:
            datos_fuente, datos_comentarios = leer_lineas_codigo(codigo, ubicacion, nombre_modulo, ubicaciones)
            #Ordena las lineas a grabar en forma alfabetica
            datos_fuente_ordenados = sorted(datos_fuente)
            datos_comentarios_ordenados = sorted(datos_comentarios)
            #Graba los datos en los archivos
            grabar_individual(fuente_modulo, datos_fuente_ordenados)
            grabar_individual(comentarios_modulo, datos_comentarios_ordenados)
            #Guarda el nombre de los archivos en listas
            archivos_fuente.append((f'fuente_{nombre_modulo}.csv', nombre_modulo))
            archivos_comentarios.append((f'comentarios_{nombre_modulo}.csv', nombre_modulo))
    
    return archivos_fuente, archivos_comentarios

def cerrar_archivos_individuales(datos):
    '''[Autores: Luciano Aguilera, Ivan Litteri]'''
    for nombre_modulo in datos:
        datos[nombre_modulo]["contenido"].close()
        
def grabar_final(archivo, linea):
    '''[Autores: Luciano Aguilera, Ivan Litteri]'''
    archivo.write(linea)

def leer_archivos_individuales(datos):
    '''[Autores: Luciano Aguilera, Ivan Litteri]
    [Ayuda: lee secuencialmente los datos de los archivos individuales que le llegan y los guarda en una lista]'''
    
    #Declara una lista vacia a llenar
    lineas = []
    #Recorro los modulos en el diccionario de datos
    for nombre_modulo in datos:
        #Carga la linea del archivo abierto
        linea = datos[nombre_modulo]["contenido"].readline()
        #Mientras el archivo tenga lineas
        while linea:
            #Guarda la linea en una lista
            lineas.append(linea)
            #Avanza de linea en el archivo
            linea = datos[nombre_modulo]["contenido"].readline()
    
    return lineas

def ordenar_lineas(archivo_final, archivos_individuales):
    '''[Autores: Luciano Aguilera, Ivan Litteri]
    [Ayuda: lee las lineas de los archivos individuales, las compara, y graba de forma ordenada alfabeticamente por funcion
    el archivo final]'''

    #Obtiene la menor linea, en este caso la siguiente a imprimir
    obtener_primera_linea = lambda x: min(x)
    #Lista de lineas leidas de los archivos individuales
    lineas = leer_archivos_individuales(archivos_individuales)

    #Mientras la lista de lineas no este vacia
    while lineas:
        #Recorre linea por linea
        linea_menor = obtener_primera_linea(lineas)
        for linea in lineas:
            #Graba la linea y luego la borra de la lista una vez encontrada
            if linea == linea_menor:
                grabar_final(archivo_final, linea)
                lineas.remove(linea)

def crear_archivo_final(nombre_archivo):
    '''[Autores: Luciano Aguilera, Ivan Litteri]'''
    return open(nombre_archivo, "w")

def abrir_archivos_individuales(archivos):
    '''[Autores: Luciano Aguilera, Ivan Litteri]
    [Ayuda: se guardan los datos a leer de los archivos individuales en un diccionario ya que la unica forma que encontramos
    de guardar variables dinamicas fue de esta forma, entonces se pueden tener abiertos "n" archivos. Y devuelve
    un diccionario con el contenido de cada modulo como value de la key (que seria el modulo)]'''

    diccionario_archivos_abiertos = {}
    for archivo, nombre_modulo in archivos:
        if nombre_modulo not in diccionario_archivos_abiertos:
            diccionario_archivos_abiertos[nombre_modulo] = {"contenido": None, "lineas": []}
        diccionario_archivos_abiertos[nombre_modulo]["contenido"] = open(archivo, "r")

    return diccionario_archivos_abiertos

            
def merge(nombre_archivo_final, archivos_individuales):
    '''[Autores: Luciano Aguilera, Ivan Litteri]
    [Ayuda: abre los "n" archivos individuales y el archivo final en forma paralela, los lee secuencialmente, graba en 
    forma ordenada el archivo final, y luego los cierra una vez finalizado el proceso.]'''

    #Abre los archivos "n" individuales y el archivo final
    archivos_individuales = abrir_archivos_individuales(archivos_individuales)
    archivo_final= crear_archivo_final(nombre_archivo_final)
    #Graba en forma ordenada las lineas de los individuales en el archivo final
    ordenar_lineas(archivo_final, archivos_individuales)
    #Cierra todos los archivos abiertos
    cerrar_archivos_individuales(archivos_individuales)

def borrar_archivos_csv_individuales(nombres_archivos_csv_individuales):
    '''[Autor: Ivan Litteri]
    [Ayuda: Borra los archivos .csv individuales (que se encuentran en el repositorio actual) cuyas ubicaciones se obtienen 
    de una funcion a la que le llega por parametro los nombres de los archivos .csv individuales.]'''

    #Obtengo las ubicaciones y las recorro para borrar el archivo que se encuentra en ella.
    for ubicacion_archivo_csv_individual in obtener.ubicaciones_archivos_csv_individuales(nombres_archivos_csv_individuales):
        #Borro el archivo que se encuentra en esa ubicacion.
        os.remove(ubicacion_archivo_csv_individual)

def main(nombre_archivo):
    ubicaciones = analizar_archivo_programas(nombre_archivo)
    archivos_fuente_individuales, archivos_comentarios_individuales = crear_csv_individuales(ubicaciones)
    merge("fuente_unico.csv", archivos_fuente_individuales)
    merge("comentarios.csv", archivos_comentarios_individuales)
    #borrar_archivos_csv_individuales(list(zip(*ubicaciones))[1])

main("programas.txt")