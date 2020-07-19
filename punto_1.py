import m_organizar_datos as organizar_datos

def longitudes_maximas(columnas_datos, longitud):
    for elemento in range(len(columnas_datos)):
        if len(columnas_datos[elemento]) > longitud[elemento]:
            longitud[elemento] = len(columnas_datos[elemento])
    
    return longitud

def imprimir(lista_de_listas, longitud):
    for lista in range(len(lista_de_listas)):
        for elemento in range(len(lista_de_listas[lista])):
            lista_de_listas[lista][elemento] += (" " * (longitud[elemento] - len(lista_de_listas[lista][elemento])))
        print("\t".join(lista_de_listas[lista]))
    
def grabar(diccionario):
    longitud = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    columnas_titulo = ["Funcion", "Parametros", "Lineas", "Invocaciones", "Returns", "If/Elif", "For", "While", "Break", "Exit", "Coment", "Ayuda", "Autor"]
    longitud = longitudes_maximas(columnas_titulo,longitud)

    lista_de_listas = [columnas_titulo]
    with open("panel_general.csv", "w") as panel_general:
        panel_general.write("funcion, parametros, lineas, invocaciones, returns, if/elif, for, while, break, exit, coment, ayuda, autor \n")
        for key in diccionario:    
            columnas_datos = [f'{key}.{diccionario[key]["modulo"]}', f'{diccionario[key]["parametros"]}', 
                            f'{diccionario[key]["lineas"]}', f'{diccionario[key]["invocaciones"]}', 
                            f'{diccionario[key]["returns"]}', f'{diccionario[key]["if/elif"]}', 
                            f'{diccionario[key]["for"]}', f'{diccionario[key]["while"]}', 
                            f'{diccionario[key]["break"]}', f'{diccionario[key]["exit"]}',
                            f'{diccionario[key]["coment"]}', 
                            f'{"Si" if diccionario[key]["ayuda"] else "No"}', f'{diccionario[key]["autor"]}']
            lista_de_listas.append(columnas_datos)       
            panel_general.write(f'{columnas_datos[0]},{columnas_datos[1]},{columnas_datos[2]},{columnas_datos[3]},{columnas_datos[4]},{columnas_datos[5]},{columnas_datos[6]},{columnas_datos[7]},{columnas_datos[8]},{columnas_datos[9]},{columnas_datos[10]},{columnas_datos[11]},{columnas_datos[12]}\n')
            longitud = longitudes_maximas(columnas_datos,longitud)

    imprimir(lista_de_listas,longitud)

def main():
    with open ("fuente_unico.csv", "r") as fuente_unico, open ("comentarios.csv", "r") as comentarios: 
        diccionario = organizar_datos.por_cantidad_declaraciones_funcion(fuente_unico, comentarios)
    grabar(diccionario)

main()