import m_obtener as obtener
import m_organizar_datos as organizar_datos
import m_analizar_linea as analizar_linea

def leer_archivos_csv(nombre_archivo_fuente, nombre_archivo_comentarios):
    '''[Autor: Joel Glauber]
    [Ayuda: esta funcion abre los archivos cuyos nombres o ubicaciones le llegan por parametro, y devuelve
    una lista de datos por cada archivo que lee, cuando termina la lectura, los cierra]'''

    #Abre los dos archivos que le llegan por parametro para su lectura
    with open(nombre_archivo_fuente, "r") as archivo_fuente, open(nombre_archivo_comentarios, "r") as archivo_comentarios:
        datos_por_funciones = organizar_datos.por_funciones(archivo_fuente, archivo_comentarios)
    
    return datos_por_funciones


def obtener_datos_numeral(datos_csv, funcion):
    '''[Autor: Joel Glauber]'''

    cadena_numeral = ""

    cadena_numeral += f'{"*" * 79}\n'
    cadena_numeral += f'Funcion: {funcion}\n'
    cadena_numeral += ("-" * len(f'Funcion: {funcion}') + "\n")
    cadena_numeral += "\nInformacion:\n"
    cadena_numeral += ("-" * len("Informacion:") + "\n")
    if "*" in funcion:
        cadena_numeral += "Es la funcion principal\n"
    cadena_numeral += f'Modulo: {datos_csv[funcion]["modulo"]}\n'
    cadena_numeral += f'{datos_csv[funcion]["comentarios"]["autor"] if "Autor" in datos_csv[funcion]["comentarios"]["autor"] else "El autor es anonimo"}\n'
    cadena_numeral += f'Ayuda: {"Si" if datos_csv[funcion]["comentarios"]["ayuda"] else "No brinda ayuda"}\n'
    cadena_numeral += f'Parametros: {datos_csv[funcion]["cantidad_parametros"]}\n'
    cadena_numeral += f'Lineas de codigo: {datos_csv[funcion]["cantidad_lineas"]}\n'
    if datos_csv[funcion]["cantidad_comentarios"] > 0:
        cadena_numeral += f'Comentarios: {datos_csv[funcion]["cantidad_comentarios"]}\n'
    else:
        cadena_numeral += "No aporta comentarios\n"
    if datos_csv[funcion]["invocaciones"]:
        cadena_numeral += f'Invoca a {"(), ".join(datos_csv[funcion]["invocaciones"])}()\n'
    else:
        cadena_numeral += "No invoca a ninguna funcion\n"
    if datos_csv[funcion]["cantidad_invocaciones"] > 0:
        cadena_numeral += f'Es invocada {datos_csv[funcion]["cantidad_invocaciones"]} {"veces" if datos_csv[funcion]["cantidad_invocaciones"] > 1 else "vez"}\n'
    else:
        cadena_numeral += "No es invocada por ninguna funcion\n"
    cadena_numeral += "\nCantidad de declaraciones: \n"
    cadena_numeral += ("-" * len("Cantidad de declaraciones: ") + "\n")
    for declaracion in datos_csv[funcion]["cantidad_declaraciones"]:
        cadena_numeral += f'{declaracion}: {datos_csv[funcion]["cantidad_declaraciones"][declaracion]}\n'
    cadena_numeral += f'{"*" * 79}\n'

    return cadena_numeral

def obtener_datos_pregunta(datos_csv, funcion):
    '''[Autor: Joel Glauber]'''

    candena_pregunta = ""

    if datos_csv[funcion]["comentarios"]["ayuda"] and (len(datos_csv[funcion]["comentarios"]["ayuda"]) > 80):
        ayuda = analizar_linea.largo_ayuda(datos_csv[funcion]["comentarios"]["ayuda"])
    else:
        ayuda = datos_csv[funcion]["comentarios"]["ayuda"] 
    parametros = datos_csv[funcion]["parametros"]
    modulo = datos_csv[funcion]["modulo"]
    autor = datos_csv[funcion]["comentarios"]["autor"]

    candena_pregunta += f'{"*" * 79}\n'
    candena_pregunta += f'Funcion: {funcion}\n'
    candena_pregunta += f'{ayuda if ayuda else "No brinda ayuda"}\n'
    candena_pregunta += f'Parametros formales: {parametros if parametros else "No tiene parametros formales"}\n'
    candena_pregunta += f'Modulo: {modulo}\n'
    candena_pregunta += f'{autor if "Autor" in autor else "El autor es anonimo"}\n'
    candena_pregunta += f'{"*" * 79}\n'

    return candena_pregunta

def grabar_archivo_ayuda(archivo_ayuda, datos_csv, funcion, opcion):
    '''[Autor: Joel Glauber]'''

    if "?" in opcion:
        informacion = obtener_datos_pregunta(datos_csv, funcion)
        archivo_ayuda.write(informacion)
    
    elif "#" in opcion:
        informacion = obtener_datos_numeral(datos_csv, funcion)
        archivo_ayuda.write(informacion)

def crear_archivo_ayuda(datos_csv, opcion):
    '''[Autor: Joel Glauber]'''

    with open("ayuda_funcion.txt", "w") as archivo_ayuda:
        for funcion in datos_csv:
            grabar_archivo_ayuda(archivo_ayuda, datos_csv, funcion, opcion)

def imprimir_datos_pregunta(datos_csv, funcion):
    '''[Autor: Joel Glauber]'''

    informacion = obtener_datos_pregunta(datos_csv, funcion)
    print(informacion)

def opcion_pregunta(datos_csv, opcion):
    '''[Autor: Joel Glauber]'''

    if opcion == "?todo":
        for funcion in datos_csv:
            imprimir_datos_pregunta(datos_csv, funcion)
    elif opcion[1:] in datos_csv.keys():
        imprimir_datos_pregunta(datos_csv, opcion[1:])
    else:
        print("Esa funcion no existe")

def imprimir_datos_numeral(datos_csv, funcion):
    '''[Autor: Joel Glauber]'''

    informacion = obtener_datos_numeral(datos_csv, funcion)
    print(informacion)

def opcion_numeral(datos_csv, opcion):
    '''[Autor: Joel Glauber]'''

    if opcion == "#todo":
        for funcion in datos_csv:
            imprimir_datos_numeral(datos_csv, funcion)
    elif opcion[1:] in datos_csv.keys():
        imprimir_datos_numeral(datos_csv, opcion[1:])
    else:
        print("Esa funcion no existe")

def analizar_opcion(datos_csv, opcion):
    '''[Autor: Joel Glauber]
    [Ayuda: analiza la opcion que le llega por parametro, la cual fue ingresada por el usuario, y en base a esa opcion,
    realiza distintas cosas]'''

    #Si la opcion es del tipo numeral, la analiza por seraprado
    if opcion[0] == "#" and len(opcion) > 1:
        opcion_numeral(datos_csv, opcion)
    #Si la opcion es del tipo signo de pregunta, la analiza por seraprado
    elif opcion[0] == "?" and len(opcion) > 1:
        opcion_pregunta(datos_csv, opcion)
    #Si se ingresa la opcion "imprimir ?todo" se crea el archivo de ayuda
    elif opcion == "imprimir ?todo":
        print("\nCreando archivo de ayuda...")
        crear_archivo_ayuda(datos_csv, opcion)
        print("Archivo creado con exito!")
    elif opcion == "imprimir #todo":
        print("\nCreando archivo de ayuda...")
        crear_archivo_ayuda(datos_csv, opcion)
        print("Archivo creado con exito!")
    #Si la opcion ingresada es incorrecta, se vuelve a intentar
    else:
        print("\nOpcion incorrecta, ingrese nuevamente\n")

def analizar_ingreso_usuario(datos_csv):
    '''[Autor: Joel Glauber]
    [Ayuda: solicita al autor que ingrese una de las opciones]'''
    opcion = input("\nFuncion: ")
    while opcion:
        analizar_opcion(datos_csv, opcion)
        opcion = input("\nFuncion: ")

def imprimir_tabla(tabla):
    '''[Autor: Joel Glauber]'''
    print(tabla)

def main():
    '''[Autor: Joel Glauber]'''

    datos_csv = leer_archivos_csv("fuente_unico.csv", "comentarios.csv")
    lista_funciones = sorted(datos_csv.keys())
    tabla = obtener.tabla_funciones(lista_funciones)
    imprimir_tabla(tabla)
    analizar_ingreso_usuario(datos_csv)