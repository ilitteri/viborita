def encontrar_main_archivo(diccionario_informacion, funcion_main_dicc = None):
    '''[Autor: Andrés Kübler]
    [Ayuda: Busca la funcion main en una lista de las claves del diccionario, y la devuelve como variable ]'''

    #Crea una variable con las claves del diccionario en forma de lista
    lista_de_keys = list(diccionario_informacion.keys())
    
    #Define un contador en 0 y una condición de corte
    contador = 0
    bandera = True

    #Recorre los elementos de la lista_de_keys
    while (contador < len(lista_de_keys)) and bandera:
        #Se fija si el elemento es el main si comienza con un *
        if lista_de_keys[contador].startswith("*"):
            #Guarda la funcion en dos variable
            funcion_main_dicc = lista_de_keys[contador]
            #Define la condición false para salir del ciclo
            bandera = False
        #Suma una posición al contador
        contador += 1

    #Si no se encontró la funcion princiapl, genera un NameError
    if funcion_main_dicc == None:
        raise NameError("¡ERROR: NO SE ENCONTRÓ LA FUNCION PRINCIPAL!")

    return funcion_main_dicc

def grafica_arbol_invocaciones(diccionario_informacion, funcion = None, string = ""):
    '''[Autor: Andrés Kübler]
    [Ayuda: Esta función recursiva analiza las invocaciones de cada función del diccionario. Recibe una funcion y un string como parametros. Minetras
    este en funcionamiento imprime las invocaciones con sus respectivas cantidades de lineas]'''

    #Se fija si la funcion es vacia
    if (funcion == None):
        #Busca la funcion main/principal en el diccionario
        funcion = encontrar_main_archivo(diccionario_informacion)
        #Crea una variable string con la información de la funcion main/principal y el contenido anterior a ella
        str_invocacion = f'{string}---> {funcion.lstrip("*")}({diccionario_informacion[funcion]["cantidad_lineas"]})'
    #Si la variable función no es vacia, crea una variable string con la funcion recorrida
    else:
        str_invocacion = f'{string} ---> {funcion}({diccionario_informacion[funcion]["cantidad_lineas"]})'
    
    #Crea una variable con las invocaciones de la función recorrida
    invocaciones = diccionario_informacion[funcion]["invocaciones"]

    #Se fija si la funcion no tiene invocaciones, e imprime el string
    if (len(invocaciones) == 0):
        print(str_invocacion)
    #Si la funcion recorrida tiene invocaciones las recorre
    else:
        for invocacion_de_funcion in range(len(invocaciones)):
            #Si la invocación recorrida es la misma que la funcion analizada (recursividad), la imprime
            if (invocaciones[invocacion_de_funcion] == funcion):
                print(f'{" " * len(str_invocacion)} ---> {invocaciones[invocacion_de_funcion]}({diccionario_informacion[funcion]["cantidad_lineas"]})')
            #Si la invocacion recorrida es la primera de las invocaciones, la función se llama a si misma y pasa el string como variable
            elif (invocacion_de_funcion == 0):
                grafica_arbol_invocaciones(diccionario_informacion, invocaciones[invocacion_de_funcion], str_invocacion)
            #Sino es la primera, se llama a si misma y pasa la longitud del string pero en espacios
            else:
                grafica_arbol_invocaciones(diccionario_informacion, invocaciones[invocacion_de_funcion], " " * len(str_invocacion))