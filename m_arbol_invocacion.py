def printear_arbol(arbol):
    '''[Autor: Andrés Kübler]
    [Ayuda: Imprime el arbol de forma ordenada y le quita el ultimo salto de linea]'''
    print(arbol.rstrip("\n"))

def analizar_recursividad_funcion(funcion,invocaciones):
    '''[Autor: Andrés Kübler]
    [Ayuda: Modifica la lista de invocaciones, quitando de ella la funcion pasada por parámetro, y la devuelve]'''

    nueva_lista = []
    #Recorre la lista de invocaciones
    for funcion_invocada in invocaciones:
        #Si la funcion_invocada es distinta de la función la agrega a la lista_nueva
        if funcion_invocada != funcion:
            nueva_lista.append(funcion_invocada)
    
    return nueva_lista

def encontrar_main_archivo(diccionario_informacion, funcion_main_dicc = None, funcion_main_imprimir = None):
    '''[Autor: Andrés Kübler]
    [Ayuda: Busca la funcion main en una lista de las claves del diccionario, y la devuelve como 2 variable 
    diferente: la primera con el * y la segunda sin el mismo]'''

    #Crea una variable con las claves del diccionario en forma de lista
    lista_de_keys = list(diccionario_informacion.keys())
    
    #Define un contador en 0 y una condición de corte
    contador = 0
    bandera = True

    #Recorre los elementos de la lista_de_keys
    while (contador < len(lista_de_keys)) and bandera:
        #Se fija si el elemento es el main si comienza con un *
        if lista_de_keys[contador].startswith("*"):
            #Guarda la funcion en dos variables (una con el * y otra sin el mismo)
            funcion_main_dicc = lista_de_keys[contador]
            funcion_main_imprimir = lista_de_keys[contador].lstrip("*")
            #Define la condición false para salir del ciclo
            bandera = False
        #Suma una posición al contador
        contador += 1

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

    existe_funcion_recursiva = ""
    #Si la funcion se llama a ella misma (es recursiva)
    if (funcion in invocaciones) and (len(invocaciones) > 0):
        #Modifica las invocaciones sacando de la lista la funcion recursiva
        invocaciones = analizar_recursividad_funcion(funcion,invocaciones)
        #Agrega la funcion recursiva al string
        existe_funcion_recursiva += funcion

    #Revisa si la función invoca a otras
    if len(invocaciones) > 0:
        #Si invoca, se autollama pasandole como parametro: el diccionario; la primera invocación; un string vacio. Luego, lo agrega al string arbol
        arbol += obtener_arbol_invocaciones(diccionario_informacion, invocaciones[0], "")

    #Recorre las invocaciones de la función recorrida, comenzando desde la posición 1
    for invocacion_n in invocaciones[1:]:
        #Para cada invocacion, pasa como parametro la función y su longitud, y autollama la función 
        arbol += obtener_arbol_invocaciones(diccionario_informacion, invocacion_n, " " * len(str_invocacion))
    
    #Se fija si existe la funcion recursiva, y de ser así la agrega al arbol
    if existe_funcion_recursiva != "":
        arbol += f'{" " * len(str_invocacion)} ---> {funcion}({diccionario_informacion[funcion]["cantidad_lineas"]})\n'

    #Si la longitud de las invocaciones es nula, agrega un salto de linea
    if len(invocaciones) == 0:
        arbol += "\n"

    return arbol

def grafica_arbol_invocaciones(diccionario_informacion):
    '''[Autor: Andrés Kübler]
    [Ayuda: Esta funcion es el main del punto 4; arma el arbol de funciones llamando a la función obtener_arbol_invocaciones, e imprime
    por pantalla sus invocaciones indicando que función llama a otra función]'''

    #Analiza las invocaciones del diccionario y arma un diagrama de las mismas y sus invocaciones internas
    arbol = obtener_arbol_invocaciones(diccionario_informacion)
    #Imprime el arbol
    printear_arbol(arbol)