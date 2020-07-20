import m_organizar_datos as organizar_datos

def longitudes_maximas(columnas_datos, longitud):
    '''[Autor: Santiago Vaccarelli]
    [Ayuda: busca las longitudes mas largas para cada columna del la tabla]'''

    #itera los elementos de una lista
    for elemento in range(len(columnas_datos)):
        #compara para cada indice de la lista si la longitud es mayor
        if len(columnas_datos[elemento]) > longitud[elemento]:
            longitud[elemento] = len(columnas_datos[elemento])
    
    return longitud

def imprimir_tabla(lista_de_listas, longitud):
    '''[Autor: Santiago Vaccarelli]
    [Ayuda: imprime la lista de listas con los espacion necesarios para que quede parejo]'''

    for lista in range(len(lista_de_listas)):
        for elemento in range(len(lista_de_listas[lista])):
            #para cada elemento de la lista se fija cuantos espacios hace falta sumarle
            lista_de_listas[lista][elemento] += (" " * (longitud[elemento] - len(lista_de_listas[lista][elemento])))
        #imprime los elementos de la lista juntos y con los espacios correspondientes a cada elemento
        print("\t".join(lista_de_listas[lista]))

def grabar_panel_general(archivo, linea):
    '''[Autor: Santiago Vaccarelli]'''
    #graba la linea que le llega por parametro al archivo
    archivo.write(linea)

def analizar_diccionario(diccionario):
    '''[Autor: Santiago Vaccarelli]
    [Ayuda: toma como parametro el diccionario con los datos de todas las funciones y crea variables (columnas_datos, lista_de_listas)para usar otras funciones (longitudes_maximas,imprimir_tabla)]'''

    #crea la lista longitud y le aplico valores iniciales con la primer linea (los titulos)
    longitud = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    columnas_titulo = ["Funcion", "Parametros", "Lineas", "Invocaciones", "Returns", "If/Elif", "For", "While", "Break", "Exit", "Coment", "Ayuda", "Autor"]
    longitud = longitudes_maximas(columnas_titulo,longitud)
    #crea una lista de listas en donde el primer elemento es la lista de titulos
    lista_de_listas = [columnas_titulo]
    
    #crea el archivo panel_general
    with open("panel_general.csv", "w") as archivo_panel_general:
        #graba la primer linea del panel general
        grabar_panel_general(archivo_panel_general, "funcion, parametros, lineas, invocaciones, returns, if/elif, for, while, break, exit, coment, ayuda, autor \n")
        for key in diccionario: 
            #crea una lista de strings con los elementos del diccionario como los pide para la tabla y el csv   
            columnas_datos = [f'{key}.{diccionario[key]["modulo"]}', f'{diccionario[key]["cantidad_parametros"]}', 
                            f'{diccionario[key]["cantidad_lineas"]}', f'{diccionario[key]["cantidad_invocaciones"]}', 
                            f'{diccionario[key]["cantidad_declaraciones"]["returns"]}', f'{diccionario[key]["cantidad_declaraciones"]["if/elif"]}', 
                            f'{diccionario[key]["cantidad_declaraciones"]["for"]}', f'{diccionario[key]["cantidad_declaraciones"]["while"]}', 
                            f'{diccionario[key]["cantidad_declaraciones"]["break"]}', f'{diccionario[key]["cantidad_declaraciones"]["exit"]}',
                            f'{diccionario[key]["cantidad_declaraciones"]["coment"]}', 
                            f'{"Si" if diccionario[key]["comentarios"]["ayuda"] else "No"}', f'{diccionario[key]["comentarios"]["autor"][7:] if diccionario[key]["comentarios"]["autor"] else "Sin Autor"}']
            #suma a la lista de listas cada una de las listas columna de datos que dependen de la key      
            lista_de_listas.append(columnas_datos) 
            #graba en el panel_general cada uno de los elementos de las listas con el formato pedido
            grabar_panel_general(archivo_panel_general, f'{columnas_datos[0]},{columnas_datos[1]},{columnas_datos[2]},{columnas_datos[3]},{columnas_datos[4]},{columnas_datos[5]},{columnas_datos[6]},{columnas_datos[7]},{columnas_datos[8]},{columnas_datos[9]},{columnas_datos[10]},{columnas_datos[11]},{columnas_datos[12]}\n')
            #calcula las longitudes maximas de cada columna comparando elementos de mismo indice de diferentes listas
            longitud = longitudes_maximas(columnas_datos,longitud)
    #llama a la funcion que imprime la tabla
    imprimir_tabla(lista_de_listas, longitud)

def main():
    '''[Autor: Santiago Vaccarelli]'''
    
    with open ("fuente_unico.csv", "r") as fuente_unico, open ("comentarios.csv", "r") as comentarios: 
        diccionario = organizar_datos.por_funciones(fuente_unico, comentarios)
    analizar_diccionario(diccionario)

main()