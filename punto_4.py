def leer_archivo():
    '''[Autor: Andrés Kübler]
    [Ayuda: Esta funcion lee el archivo csv y devuelve sus lineas en forma de listas]'''

    #Abro y leo el archivo
    with open("fuente_unico.csv","r") as archivo_funciones:
        lineas = archivo_funciones.readlines()
    return lineas

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
    cantidad de lineas, funcionea a las que llama. También indica cual es la funcion principal del archivo.]'''

    #Creo diccionario vacio donde voy a ir guardando la informacion
    dicc_funciones = {}

    for linea in lista_de_lineas:
        #Convierto la linea en una lista para asi recorrerla por indices
        linea_listada = linea.split(",")
        #Busco el nombre de la funcion en la linea y me fijo si es la funcion principal del archivo
        nombre_funcion = linea_listada[0].strip('"')
        if nombre_funcion.startswith("*"):
            nombre_funcion = nombre_funcion.lstrip("*")
            funcion_main = nombre_funcion
        #Saco la cantidad de lineas de la funcion
        cantidad_lineas = len(linea_listada) - 3
        
        funciones_llamadas = []
        for funcion in nombres_funciones:
            if (funcion in linea[2:]) and (funcion not in funciones_llamadas):
                funciones_llamadas.append(funcion)
        
        #Agrego los datos encontrados al diccionario 
        dicc_funciones[nombre_funcion] = [cantidad_lineas,funciones_llamadas]

    return dicc_funciones,funcion_main

def printear_funciones(diccionario_informacion,funcion_principal):
    encontrar = diccionario_informacion[funcion_principal]
    print(encontrar)


def main_punto4():
    lista_de_lineas = leer_archivo()
    nombres_funciones = listar_funciones(lista_de_lineas)
    diccionario_informacion,funcion_principal = crear_diccionario(lista_de_lineas,nombres_funciones)
    
    #En construcción
    printear_funciones(diccionario_informacion,funcion_principal)

main_punto4()