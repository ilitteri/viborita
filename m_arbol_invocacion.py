def encontrar_main_archivo(datos_csv, funcion_principal = None):
    '''[Autor: Andrés Kübler]
    [Ayuda: Busca la funcion main en una lista de las claves del diccionario, y la devuelve como variable ]'''

    #Crea una variable con las claves del diccionario en forma de lista
    lista_de_keys = list(datos_csv.keys())
    
    #Define un contador en 0 y una condición de corte
    i = 0
    bandera = True

    #Recorre los elementos de la lista_de_keys
    while bandera and (i < len(lista_de_keys)):
        #Se fija si el elemento es el main si comienza con un *
        if lista_de_keys[i].startswith("*"):
            #Guarda la funcion en dos variable
            funcion_principal = lista_de_keys[i]
            #Define la condición false para salir del ciclo
            bandera = False
        #Suma una posición al contador
        i += 1

    return funcion_principal

def procesar_impresion_arbol(diccionario_informacion, funcion = None, string = ""):
    '''[Autor: Andrés Kübler]
    [Ayuda: Esta función recursiva analiza las invocaciones de cada función del diccionario. Recibe una funcion y un string como parametros. Minetras
    este en funcionamiento imprime las invocaciones con sus respectivas cantidades de lineas]'''

    #Si la variable función no es vacia, crea una variable string con la funcion recorrida
    str_invocacion = f'{string} ---> {funcion[1:] if "*" in funcion else funcion}({datos_csv[funcion]["cantidad_lineas"]})'
    
    #Crea una variable con las invocaciones de la función recorrida
    invocaciones = datos_csv[funcion]["invocaciones"]

    #Se fija si la funcion no tiene invocaciones, e imprime el string
    if (len(invocaciones) == 0):
        print(str_invocacion)
    #Si la funcion recorrida tiene invocaciones las recorre
    else:
        for invocacion_de_funcion in range(len(invocaciones)):
            #Si la invocación recorrida es la misma que la funcion analizada (recursividad), la imprime
            if (invocaciones[invocacion_de_funcion] == funcion):
                print(f'{" " * len(str_invocacion)} ---> {invocaciones[invocacion_de_funcion]}({datos_csv[funcion]["cantidad_lineas"]})')
            #Si la invocacion recorrida es la primera de las invocaciones, la función se llama a si misma y pasa el string como variable
            elif (invocacion_de_funcion == 0):
                procesar_impresion_arbol(diccionario_informacion, invocaciones[invocacion_de_funcion], str_invocacion)
            #Sino es la primera, se llama a si misma y pasa la longitud del string pero en espacios
            else:
                procesar_impresion_arbol(diccionario_informacion, invocaciones[invocacion_de_funcion], " " * len(str_invocacion))

def grafica_arbol_invocaciones(diccionario_informacion):
    '''[Autor: Andrés Kübler]
    [Ayuda: Esta es la funcion principal del punto. Recorre el diccionario, simepre y cuando exista una funcion
    principal. Si no la encuentra imprime error]'''

    try:
        procesar_impresion_arbol(diccionario_informacion)
    #Exceptua el error si no encuentra el main
    except Exception:
        print("¡ERROR: NO SE ENCONTRÓ FUNCIÓN PRINCIPAL!")
