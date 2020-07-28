import m_organizar_datos as organizar_datos
#import m_grafo as grafo

def leer_csv():
    with open("fuente_unico.csv", "r") as archivo_fuente, open("comentarios.csv", "r") as archivo_comentarios:
        datos_1, datos_2 = organizar_datos.leer_archivos_csv(archivo_fuente, archivo_comentarios)

    return datos_1

def obtener_funcion_principal(datos):
    
    funcion_principal = ""
    funciones = list(datos.keys())
    incognita = True
    i = 0
    while incognita and i < len(funciones):
        if "*" in funciones[i]:
            funcion_principal = funciones[i]
            incognita = False
        i += 1

    return funcion_principal

def obtener_arbol_invocaciones(datos, invocacion = None, separacion="", espaciar=True):
    arbol = ""
    if invocacion == None:
        invocacion = obtener_funcion_principal(datos)

    jerston = f' --> {invocacion}({datos[invocacion]["cantidad_lineas"]})'

    separacionHijos = separacion + " " * len(jerston)

    str_invocacion = jerston
    if espaciar:
        str_invocacion = separacion + str_invocacion

    arbol += str_invocacion
    invocaciones = datos[invocacion]["invocaciones"]

    for i, invocacion_n in enumerate(invocaciones):
        primero = (i == 0)
        if invocacion == invocacion_n:
            # Es recursiva
            arbol += f'{separacionHijos if not primero else ""} --> {invocacion}({datos[invocacion]["cantidad_lineas"]})\n'
        else:
            arbol += obtener_arbol_invocaciones(datos, invocacion_n, separacionHijos, not primero)

    if len(invocaciones) == 0:
        arbol += "\n"

    return arbol

def imprimir_arbol(arbol):
    print(arbol)

def main():
    datos = leer_csv()
    #grafo.crear_grafo_invocaciones(datos)
    arbol = obtener_arbol_invocaciones(datos)
    imprimir_arbol(arbol)
    #print(datos["crear_csv_finales"]["invocaciones"])
main()