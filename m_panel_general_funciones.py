import m_obtener as obtener

def mostrar_panel_general(lista_de_columnas, longitud):
    '''[Autor: Santiago Vaccarelli]
    [Ayuda: imprime la lista de columnas con los espacios necesarios para que quede parejo]'''

    for columna in range(len(lista_de_columnas)):
        for elemento in range(len(lista_de_columnas[columna])):
            #para cada elemento de la lista se fija cuantos espacios hace falta sumarle
            lista_de_columnas[columna][elemento] += (" " * (longitud[elemento] - len(lista_de_columnas[columna][elemento])))
        #imprime los elementos de la lista juntos y con los espacios correspondientes a cada elemento
        print("\t".join(lista_de_columnas[columna]))

def grabar_panel_control_csv(archivo, lineas):
    '''[Autor: Santiago Vaccarelli]
    [Ayuda: graba las lineas que le llegan por parametro al archivo]'''

    for linea in lineas:
        archivo.write(f'{",".join(linea)}\n')

def crear_panel_general_csv(lista_de_columnas):
    '''[Autor: Santiago Vaccarelli]
    [Ayuda: Crea el archivo csv de panel general y le graba los datos]'''
    
    with open("panel_general.csv", "w") as archivo_panel_general:
        grabar_panel_control_csv(archivo_panel_general, lista_de_columnas)

def generar_tabla_panel_general(diccionario):
    '''[Autor: Santiago Vaccarelli]
    [Ayuda: toma como parametro el diccionario con los datos de todas las funciones y crea variables (columnas_datos, lista_de_columnas)para usar otras funciones (longitudes_maximas,imprimir_tabla)]'''

    #crea la lista longitud y le aplico valores iniciales con la primer linea (los titulos)
    longitud = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    columnas_titulo = ["Funcion", "Parametros", "Lineas", "Invocaciones", "Returns", "If/Elif", "For", "While", "Break", "Exit", "Coment", "Ayuda", "Autor"]
    longitud = obtener.longitud_maxima(columnas_titulo,longitud)
    #crea una lista de listas en donde el primer elemento es la lista de titulos
    lista_de_columnas = [columnas_titulo]
    
    for funcion, datos_funcion in diccionario.items(): 
        #crea una lista de strings con los elementos del diccionario como los pide para la tabla y el csv   
        columnas_datos = [f'{funcion if not "*" in funcion else funcion[1:]}.{datos_funcion["modulo"] if not "*" in datos_funcion["modulo"] else datos_funcion["modulo"][1:]}', 
                        f'{datos_funcion["cantidad_parametros"]}', f'{datos_funcion["cantidad_lineas"]}', f'{datos_funcion["cantidad_invocaciones"]}', 
                        f'{datos_funcion["cantidad_declaraciones"]["returns"]}', f'{datos_funcion["cantidad_declaraciones"]["if/elif"]}', 
                        f'{datos_funcion["cantidad_declaraciones"]["for"]}', f'{datos_funcion["cantidad_declaraciones"]["while"]}', 
                        f'{datos_funcion["cantidad_declaraciones"]["break"]}', f'{diccionario[funcion]["cantidad_declaraciones"]["exit"]}',
                        f'{datos_funcion["cantidad_comentarios"]}', f'{"Si" if datos_funcion["comentarios"]["ayuda"] else "No"}', 
                        f'"{datos_funcion["comentarios"]["autor"].split(": ")[1] if datos_funcion["comentarios"]["autor"] else "Sin Autor"}"']
        #suma a la lista de listas cada una de las listas columna de datos que dependen de la key      
        lista_de_columnas.append(columnas_datos) 
        #calcula las longitudes maximas de cada columna comparando elementos de mismo indice de diferentes listas
        longitud = obtener.longitud_maxima(columnas_datos,longitud)
    
    return lista_de_columnas, longitud

def obtener_panel_general(dict_principal):
    '''[Autor: Santiago Vaccarelli]'''
    
    lista_de_columnas, longitud = generar_tabla_panel_general(dict_principal)
    crear_panel_general_csv(lista_de_columnas)
    mostrar_panel_general(lista_de_columnas, longitud)
