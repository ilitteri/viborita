def listar_funciones(lista_de_lineas):
    '''[Autor: Andrés Kübler]
    [Ayuda: Esta funcion lista los nombres de las funciones del archvio]'''
    #Creo una lista vacia donde voy a ir agregando los nombres
    nombres_funciones = []
    #recorro cada parametro de la lista y agrego el nombre a la lista vacia de arriba 
    for linea in lista_de_lineas:
        nueva_linea = linea.split(",")
        nombres_funciones.append(nueva_linea[0].strip('"'))

    return nombres_funciones

def crear_diccionario(lista_de_lineas,nombres_funciones):
    '''[Autor: Andrés Kübler]
    [Ayuda: Esta funcion crea el diccionario el cual contiene la informacion necesaria: nombre de la funcion, 
    cantidad de lineas, funcionea a las que llama. a partir de aca solo vamos a usar este diccionario como fuente
    de información]'''

    #Creo diccionario vacio donde voy a ir guardando la informacion
    dicc_funciones = {}

    for linea in lista_de_lineas:
        #Convierto la linea en una lista para asi recorrerla por indices
        linea_listada = linea.split(",")
        #Saco el nombre de la funcion de la linea evaluada
        nombre_funcion = linea_listada[0].strip('"')
        #Saco la cantidad de lineas de la funcion
        cantidad_lineas = len(linea_listada) - 3
        
        funciones_llamadas = []
        for funcion in nombres_funciones:
            if (funcion in linea[2:]) and (funcion not in funciones_llamadas):
                funciones_llamadas.append(funcion)
        
        #Agrego los datos encontrados al diccionario 
        dicc_funciones[nombre_funcion,cantidad_lineas] = funciones_llamadas
    
    return dicc_funciones


def leer_archivo():
    '''[Autor: Andrés Kübler]
    [Ayuda: Esta funcion lee el archivo csv y su informacion se procesa]'''
    with open("fuente_unico.csv","r") as archivo_funciones:
        lineas = archivo_funciones.readlines()

        nombres_funciones = listar_funciones(lineas)
        diccionario_informacion = crear_diccionario(lineas,nombres_funciones)

leer_archivo()