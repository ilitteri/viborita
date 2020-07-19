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

def imprimir_tabla(tabla):
    print(tabla)

def imprimir_datos_funcion(datos_csv, funcion):

    ayuda = datos_csv[funcion]["comentarios"]["ayuda"]
    parametros = datos_csv[funcion]["parametros"]
    modulo = datos_csv[funcion]["modulo"]
    autor = datos_csv[funcion]["comentarios"]["autor"]
    print(f'{"*" * 40}')
    print(f'Funcion: {funcion}\n')
    print(f'{ayuda if ayuda else "No brinda ayuda"}')
    print(f'Parametros formales: {parametros if parametros else "No tiene parametros formales"}')
    print(f'Modulo: {modulo}')
    print(f'{autor if "Autor" in autor else "El autor es anonimo"}')
    print(f'{"*" * 40}')

def opcion_pregunta(datos_csv, opcion):
    if opcion == "?todo":
        for funcion in datos_csv:
            imprimir_datos_funcion(datos_csv, funcion)
    elif opcion[1:] in datos_csv.keys():
        imprimir_datos_funcion(datos_csv, opcion[1:])
    else:
        print("Esa funcion no existe")

def grabar_archivo_ayuda(archivo_ayuda, datos_csv, funcion):

    if datos_csv[funcion]["comentarios"]["ayuda"] and (len(datos_csv[funcion]["comentarios"]["ayuda"]) > 80):
        ayuda = analizar_linea.largo_ayuda(datos_csv[funcion]["comentarios"]["ayuda"])
    else:
        ayuda = datos_csv[funcion]["comentarios"]["ayuda"] 
    parametros = datos_csv[funcion]["parametros"]
    modulo = datos_csv[funcion]["modulo"]
    autor = datos_csv[funcion]["comentarios"]["autor"]

    archivo_ayuda.write(f'{"*" * 40}\n')
    archivo_ayuda.write(f'Funcion: {funcion}\n')
    archivo_ayuda.write(f'{ayuda if ayuda else "No brinda ayuda"}\n')
    archivo_ayuda.write(f'Parametros formales: {parametros if parametros else "No tiene parametros formales"}\n')
    archivo_ayuda.write(f'Modulo: {modulo}\n')
    archivo_ayuda.write(f'{autor if "Autor" in autor else "El autor es anonimo"}\n')
    archivo_ayuda.write(f'{"*" * 40}\n')

def crear_archivo_ayuda(datos_csv):
    with open("ayuda_funcion.txt", "w") as archivo_ayuda:
        for funcion in datos_csv:
            grabar_archivo_ayuda(archivo_ayuda, datos_csv, funcion)

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
        crear_archivo_ayuda(datos_csv)
        print("Archivo creado con exito!")
    #Si la opcion ingresada es incorrecta, se vuelve a intentar
    else:
        print("\nOpcion incorrecta, ingrese nuevamente\n")

def obtener_informacion(datos_csv):
    '''[Autor: Joel Glauber]
    [Ayuda: solicita al autor que ingrese una de las opciones]'''
    opcion = input("\nFuncion: ")
    while opcion:
        analizar_opcion(datos_csv, opcion)
        opcion = input("\nFuncion: ")

def main():
    datos_csv = leer_archivos_csv("fuente_unico.csv", "comentarios.csv")
    lista_funciones = sorted(datos_csv.keys())
    tabla = obtener.tabla_para_imprimir(lista_funciones)
    imprimir_tabla(tabla)
    obtener_informacion(datos_csv)

main()