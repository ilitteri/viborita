import m_organizar_datos as organizar_datos
import m_obtener as obtener
import m_grabar as grabar

def imprimir_panel_general(lista_de_listas, longitud):
    '''[Autor: Santiago Vaccarelli]
    [Ayuda: imprime la lista de listas con los espacion necesarios para que quede parejo]'''

    for lista in range(len(lista_de_listas)):
        for elemento in range(len(lista_de_listas[lista])):
            #para cada elemento de la lista se fija cuantos espacios hace falta sumarle
            lista_de_listas[lista][elemento] += (" " * (longitud[elemento] - len(lista_de_listas[lista][elemento])))
        #imprime los elementos de la lista juntos y con los espacios correspondientes a cada elemento
        print("\t".join(lista_de_listas[lista]))

def crear_panel_general(lista_de_listas):
    '''[Autor: Santiago Vaccarelli]
    [Ayuda: Crea el archivo csv de panel general y le graba los datos]'''
    
    with open("panel_general.csv", "w") as archivo_panel_general:
        grabar.panel_control_csv(archivo_panel_general, lista_de_listas)

def obtener_tabla(diccionario):
    '''[Autor: Santiago Vaccarelli]
    [Ayuda: toma como parametro el diccionario con los datos de todas las funciones y crea variables (columnas_datos, lista_de_listas)para usar otras funciones (longitudes_maximas,imprimir_tabla)]'''

    #crea la lista longitud y le aplico valores iniciales con la primer linea (los titulos)
    longitud = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    columnas_titulo = ["Funcion", "Parametros", "Lineas", "Invocaciones", "Returns", "If/Elif", "For", "While", "Break", "Exit", "Coment", "Ayuda", "Autor"]
    longitud = obtener.longitud_maxima(columnas_titulo,longitud)
    #crea una lista de listas en donde el primer elemento es la lista de titulos
    lista_de_listas = [columnas_titulo]
    
    for key, values in diccionario.items(): 
        #crea una lista de strings con los elementos del diccionario como los pide para la tabla y el csv   
        columnas_datos = [f'{key}.{values["modulo"]}', f'{values["cantidad_parametros"]}', 
                        f'{values["cantidad_lineas"]}', f'{values["cantidad_invocaciones"]}', 
                        f'{values["cantidad_declaraciones"]["returns"]}', f'{values["cantidad_declaraciones"]["if/elif"]}', 
                        f'{values["cantidad_declaraciones"]["for"]}', f'{values["cantidad_declaraciones"]["while"]}', 
                        f'{values["cantidad_declaraciones"]["break"]}', f'{diccionario[key]["cantidad_declaraciones"]["exit"]}',
                        f'{values["cantidad_comentarios"]}', 
                        f'{"Si" if values["comentarios"]["ayuda"] else "No"}', f'{values["comentarios"]["autor"].split(": ")[1] if values["comentarios"]["autor"] else "Sin Autor"}']
        #suma a la lista de listas cada una de las listas columna de datos que dependen de la key      
        lista_de_listas.append(columnas_datos) 
        #calcula las longitudes maximas de cada columna comparando elementos de mismo indice de diferentes listas
        longitud = obtener.longitud_maxima(columnas_datos,longitud)
    
    return lista_de_listas, longitud

def main(datos_archivos_csv):
    '''[Autor: Santiago Vaccarelli]'''
    
    lista_de_listas, longitud = obtener_tabla(datos_archivos_csv)
    crear_panel_general(lista_de_listas)
    imprimir_panel_general(lista_de_listas, longitud)
