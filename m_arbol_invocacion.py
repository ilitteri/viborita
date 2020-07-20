  
def leer_archivo():
    '''[Autor: Andrés Kübler]
    [Ayuda: Lee el archivo .csv y devuelve sus lineas en forma de lista]'''

    #Abre y lee el archivo
    with open("fuente_unico.csv","r") as archivo_funciones:
        lineas = archivo_funciones.readlines()
    return lineas

def listar_funciones(lista_de_lineas):
    '''[Autor: Andrés Kübler]
    [Ayuda: Lista los nombres de las funciones del archvio]'''

    #Crea una lista vacia donde va a ir agregando los nombres de las funciones
    nombres_funciones = []
    #Recorre cada parametro de la lista y agrega el nombre a nombres_funciones
    for linea in lista_de_lineas:
        nueva_linea = linea.split(",")
        nombres_funciones.append(nueva_linea[0].strip('"'))

    return nombres_funciones

def crear_diccionario(lista_de_lineas,nombres_funciones):
    '''[Autor: Andrés Kübler]
    [Ayuda: Crea el diccionario el cual va a contener la información necesaria para su uso: nombre de la funcion, 
    cantidad de lineas, funcionea a las que llama. También indica cual es la funcion principal del archivo]'''

    #Crea diccionario vacio donde va a ir guardando la información extraida
    dicc_funciones = {}
    
    #Recorre la lista
    for linea in lista_de_lineas:
        #Convierte la linea en una lista para asi recorrerla por índices
        linea_listada = linea.split(",")
        #Busca el nombre de la función en la linea y se fija si es la funcion principal del archivo
        nombre_funcion = linea_listada[0].strip('"')
        if nombre_funcion.startswith("*"):
            nombre_funcion = nombre_funcion.lstrip("*")
            funcion_main = nombre_funcion
        #Busca la cantidad de lineas de la función evaluada
        cantidad_lineas = len(linea_listada) - 3
        
        #Crea una lista vacia y agrega las funciones internas que llama la función evaluada
        funciones_llamadas = []        
        for elemento in linea_listada[2:]:
            for funcion in nombres_funciones:
                if (funcion in elemento):
                    funciones_llamadas.append(funcion)
        
        #Agrega los datos extraidos al diccionario 
        dicc_funciones[nombre_funcion] = {"lineas":cantidad_lineas,"funciones":funciones_llamadas}
    
    return dicc_funciones,funcion_main

def recorrer_funcion(diccionario_informacion,funcion,string):
    '''[Autor: Andrés Kübler]
    [Ayuda: Recorre las funciones internas de la funcion que le pasemos, e imprime
    ordenadamente las mismas, indicando a que funcion pertenece y su cantidad de lineas]'''
    funciones_recorridas = []

    #Recorre las funciones internas a la funcion recibida por parametro
    for funcion_interna in diccionario_informacion[funcion]["funciones"]:
        funciones_recorridas.append(funcion_interna)
        #Comprueba si la funcion interna llama a otras funciones
        if diccionario_informacion[funcion_interna]["funciones"] != []:
            #Si la funcion interna recorrida es la primera, agrega su nombre y lineas al string
            if (funcion_interna == diccionario_informacion[funcion]["funciones"][0]) and (funciones_recorridas.count(funcion_interna) == 1):
                string += " --> {} ({})".format(funcion_interna,diccionario_informacion[funcion_interna]["lineas"])
            #Si no es la primera, modifica el string agregando espacios correspondientes
            else:
                string = ((" " * len(string)) + " --> {} ({})".format(funcion_interna,diccionario_informacion[funcion_interna]["lineas"]))
            #Llama a la misma funcion para comprobar si la funcion interna a funcion_interna posee otras funciones dentro
            recorrer_funcion(diccionario_informacion,funcion_interna,string)
        #Si funcion_interna no llama a otras funciones organiza su impresión
        else:
            if (funcion_interna == diccionario_informacion[funcion]["funciones"][0]) and (funciones_recorridas.count(funcion_interna) == 1):
                print(string + " --> {} ({})".format(funcion_interna,diccionario_informacion[funcion_interna]["lineas"]))
            else:
                print((" " * len(string)) + " --> {} ({})".format(funcion_interna,diccionario_informacion[funcion_interna]["lineas"]))

def organizar_impresion(diccionario_informacion,funcion_principal):
    '''[Autor: Andrés Kübler]
    [Ayuda: Recorre las funciones internas de la función principal del archivo, y si estas poseen funciones
    internas, las direcciona a la funcion recorrer_funcion() para su próxima impresión]'''

    #Crea una variable donde guarda la longitud del string de funcion_principal    
    longitud = 0
    funciones_recorridas = []

    #Recorre las funciones de la funcion principal del archvio/diccionario
    for funcion_interna_main in diccionario_informacion[funcion_principal]["funciones"]:
        funciones_recorridas.append(funcion_interna_main)
        #Crea un string con el nombre y cantidad de lineas de la funcion_principal
        string_a_imprimir = " --> {} ({})".format(funcion_interna_main,diccionario_informacion[funcion_interna_main]["lineas"])
        
        #Prueba si la funcion_interna_main recorrida es la primera de la funcion_principal,si lo es agrega el nombre de la funcion y cantidad lineas antes del string de funcion_principal
        if (funcion_interna_main == diccionario_informacion[funcion_principal]["funciones"][0]) and (funciones_recorridas.count(funcion_interna_main) == 1):
            string_funcion_principal = "--> {} ({})".format(funcion_principal,diccionario_informacion[funcion_principal]["lineas"])
            longitud += len(string_funcion_principal)
            string_a_imprimir = string_funcion_principal + string_a_imprimir
        elif(funcion_interna_main == diccionario_informacion[funcion_principal]["funciones"][0]) and (funciones_recorridas.count(funcion_interna_main) > 1):
            string_a_imprimir = (" " * len("--> {} ({})".format(funcion_principal,diccionario_informacion[funcion_principal]["lineas"]))) + " --> {} ({})".format(funcion_interna_main,diccionario_informacion[funcion_interna_main]["lineas"])
        #Si no es la primera función, imprime su equivalente en longitud en espacios blancos
        elif (funcion_interna_main != diccionario_informacion[funcion_principal]["funciones"][0]):
            string_a_imprimir = (" " * longitud) + " --> {} ({})".format(funcion_interna_main,diccionario_informacion[funcion_interna_main]["lineas"])

        #Comprueba si la funcion interna llama a otras, de ser asi la recorre en recorrer_funcion(), sino la imprime
        if diccionario_informacion[funcion_interna_main]["funciones"] != []:
            recorrer_funcion(diccionario_informacion,funcion_interna_main,string_a_imprimir)
        else:
            print(string_a_imprimir)

def main():
    '''[Autor: Andrés Kübler]
    [Ayuda: Esta funcion es el main del punto 4, lee el archvio fuente_unico.csv e imprime
    por pantalla sus funciones indicando cual llama a cual otra]'''

    #Lee el archivo fuente_unico.csv
    lista_de_lineas = leer_archivo()
    #Lista las funciones del archivo
    nombres_funciones = listar_funciones(lista_de_lineas)
    #Crea un diccionario con la informacion a utilizar del archivo
    diccionario_informacion,fun_principal = crear_diccionario(lista_de_lineas,nombres_funciones)
    #Analiza las funciones del diccionario e imprime un diagrama de las mismas y sus funciones internas
    organizar_impresion(diccionario_informacion,fun_principal)