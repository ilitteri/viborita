def printear_arbol(arbol):
    '''[Autor: Andrés Kübler]
    [Ayuda: Imprime el arbol de forma ordenada]'''
    return print(arbol)

def encontrar_main_archivo(diccionario_informacion):
    '''[Autor: Andrés Kübler]
    [Ayuda: Busca la funcion main en el diccionario y la devuelve 2 veces: la primera con el * y la segunda sin el mismo]'''

    #Recorre las key del diccionario
    for clave in diccionario_informacion.keys():
        #Si la key arranca con * me la guardo como variable
        if clave.startswith("*"):
            funcion_main_dicc = clave
            funcion_main_imprimir = clave.lstrip("*")
    
    return funcion_main_dicc,funcion_main_imprimir

def obtener_arbol_invocaciones(diccionario_informacion, funcion = None, separacion = ""):
    '''[Autor: Andrés Kübler]
    [Ayuda: Esta funcion recursiva, analiza la funcion y separacion pasadas por parametros, para ir armando un ]'''

    #Crea un string vacio donde se va a guardar todo el arbol
    arbol = ""
    #Se fija si la funcion es vacia
    if funcion == None:
        #Busca la funcion main/principal en el diccionario
        funcion,funcion_imprimir = encontrar_main_archivo(diccionario_informacion)
        #Crea una variable string con la información de la funcion main/principal
        str_invocacion = f'{separacion}---> {funcion_imprimir}({diccionario_informacion[funcion]["cantidad_lineas"]})'
    #Si la variable función no es vacia, crea una variable string con la funcion recorrida
    else:
        str_invocacion = f'{separacion} ---> {funcion}({diccionario_informacion[funcion]["cantidad_lineas"]})'

    #Agrega el string creado al string arbol
    arbol += str_invocacion
    #Crea una variable con las invocaciones de la función recorrida para ser reemplazada próximamente
    invocaciones = diccionario_informacion[funcion]["invocaciones"]

    #Revisa si la función invoca a otras
    if len(invocaciones) > 0:
        #Si invoca, se autollama pasandole como parametro: el diccionario; la primera invocación; un string vacio. Luego, lo agrega al string arbol
        arbol += obtener_arbol_invocaciones(diccionario_informacion, invocaciones[0], "")

    #Recorre las invocaciones de la función recorrida, comenzando desde la posición 1
    for invocacion_n in invocaciones[1:]:
        #Para cada invocacion, pasa como parametro la función y su longitud, y autollama la función 
        arbol += obtener_arbol_invocaciones(diccionario_informacion, invocacion_n, " " * len(str_invocacion))
    #Si la longitud de las invocaciones es nula, agrega un salto de linea
    if len(invocaciones) == 0:
        arbol += "\n"

    return arbol

def main(diccionario_informacion):
    '''[Autor: Andrés Kübler]
    [Ayuda: Esta funcion es el main del punto 4; arma el arbol de funciones llamando a la función obtener_arbol_invocaciones, e imprime
    por pantalla sus invocaciones indicando que función llama a otra función]'''

    #Analiza las invocaciones del diccionario y arma un diagrama de las mismas y sus invocaciones internas
    arbol = obtener_arbol_invocaciones(diccionario_informacion)
    ##Imprime el arbol
    printear_arbol(arbol)