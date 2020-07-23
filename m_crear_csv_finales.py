import m_crear_csv_individuales as crear_csv_individuales

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

def ordenar_lineas(archivo_final, archivos_individuales, lineas_fuera_funcion):
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
                nombre_funcion, _, nombre_modulo, *otros_datos = linea.split('","')
                if "*" in nombre_modulo and f'{nombre_funcion[1:]}()\n' in lineas_fuera_funcion:
                    grabar_final(archivo_final, '"*' + linea[1:])
                else:
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

            
def merge(nombre_archivo_final, archivos_individuales, lineas_fuera_funcion):
    '''[Autores: Luciano Aguilera, Ivan Litteri]
    [Ayuda: abre los "n" archivos individuales y el archivo final en forma paralela, los lee secuencialmente, graba en 
    forma ordenada el archivo final, y luego los cierra una vez finalizado el proceso.]'''

    #Abre los archivos "n" individuales y el archivo final
    archivos_individuales = abrir_archivos_individuales(archivos_individuales)
    archivo_final= crear_archivo_final(nombre_archivo_final)
    #Graba en forma ordenada las lineas de los individuales en el archivo final
    ordenar_lineas(archivo_final, archivos_individuales, lineas_fuera_funcion)
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
    archivos_fuente_individuales, archivos_comentarios_individuales, lineas_fuera_funcion = crear_csv_individuales.main(nombre_archivo)
    merge("fuente_unico.csv", archivos_fuente_individuales, lineas_fuera_funcion)
    merge("comentarios.csv", archivos_comentarios_individuales, lineas_fuera_funcion)
    print(lineas_fuera_funcion)
    #borrar_archivos_csv_individuales(list(zip(*ubicaciones))[1])