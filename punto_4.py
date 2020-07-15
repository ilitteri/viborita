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
        dicc_funciones[nombre_funcion] = {"lineas":cantidad_lineas,"funciones":funciones_llamadas}

    return dicc_funciones,funcion_main

def printear_modulado(diccionario_informacion,funcion,string):
    '''[Autor: Andrés Kübler]
    [Ayuda: Esta funcion recorre las funciones internas de la funcion que le pasemos, e imprime
    ordenadamente las mismas, indicando a que funcion pertenece y su cantidad de lineas]'''

    #Recorro las funciones internas a la funcion recibida por parametro
    for funcion_interna in diccionario_informacion[funcion]["funciones"]:
        #Me fijo si la funcion interna tiene funciones dentro
        if diccionario_informacion[funcion_interna]["funciones"] != []:
            #Si la funcion interna recorrida es la primera, agrego su nombre y lineas al string
            if funcion_interna == diccionario_informacion[funcion]["funciones"][0]:
                string += " --> {} ({})".format(funcion_interna,diccionario_informacion[funcion_interna]["lineas"])
            #Si no es la primera
            else:
                string += ((" " * len(string)) + " --> {} ({})".format(funcion_interna,diccionario_informacion[funcion_interna]["lineas"]))
            
            printear_modulado(diccionario_informacion,funcion_interna,string)
        else:
            print((" " * len(string)) + " --> {} ({})".format(funcion_interna,diccionario_informacion[funcion_interna]["lineas"]))


def organizar_printeos(diccionario_informacion,funcion_principal):
    '''[Autor: Andrés Kübler]
    [Ayuda: Esta funcion recorre las funciones internas del main del archivo, y si estas poseen funciones
    internas, las direcciona a la funcion printear_modulado()]'''

    #Recorro las funciones del main del archvio/diccionario
    for funcion_interna_main in diccionario_informacion[funcion_principal]["funciones"]:
        #Me armo un string con el nombre y lineas de la función recorrido
        string_a_imprimir = " --> {} ({})".format(funcion_interna_main,diccionario_informacion[funcion_interna_main]["lineas"])
        #Me fijo si la funcion interna llama a otras, de ser asi la recorro en printear_modulado(), sino la imprimo
        if diccionario_informacion[funcion_interna_main]["funciones"] != []:
            printear_modulado(diccionario_informacion,funcion_interna_main,string_a_imprimir)
        else:
            print(string_a_imprimir)

def main_punto4():
    '''[Autor: Andrés Kübler]
    [Ayuda: Esta funcion es el main del punto 4, lee el archvio fuente_unico.csv e imprime
    por pantalla sus funciones indicando cual llama a cual otra]'''

    #Leo el archivo fuente_unico.csv
    lista_de_lineas = leer_archivo()
    #Listo las funciones del archivo
    nombres_funciones = listar_funciones(lista_de_lineas)
    #Creo un diccionario con la informacion a utilizar del archivo
    diccionario_informacion,fun_principal = crear_diccionario(lista_de_lineas,nombres_funciones)
    
    #En construcción
    organizar_printeos(diccionario_informacion,fun_principal)

main_punto4()