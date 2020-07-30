import m_obtener as obtener
import m_analizar_linea as analizar_linea

def formatear_datos_numeral(datos_csv, funcion):
    '''[Autor: Joel Glauber]
    [Ayuda: crea una cadena de caracteres vacia para ir concatenando en la forma que se quiere que se impriman los datos
    en pantalla, pero para las opciones que empiezan con numeral (#)]'''

    cadena_numeral = ""

    cadena_numeral += f'{"*" * 79}\n'
    cadena_numeral += f'Funcion: {funcion if "*" not in funcion else funcion[1:]}\n'
    cadena_numeral += ("-" * len(f'Funcion: {funcion}') + "\n")
    cadena_numeral += "\nInformacion:\n"
    cadena_numeral += ("-" * len("Informacion:") + "\n")
    if ("*" in funcion):
        cadena_numeral += "Es la funcion principal\n"
    cadena_numeral += f'Modulo: {datos_csv[funcion]["modulo"] if "*" not in datos_csv[funcion]["modulo"] else datos_csv[funcion]["modulo"][1:]}\n'
    cadena_numeral += f'{datos_csv[funcion]["comentarios"]["autor"] if "Autor" in datos_csv[funcion]["comentarios"]["autor"] else "El autor es anonimo"}\n'
    cadena_numeral += f'Ayuda: {"Si" if datos_csv[funcion]["comentarios"]["ayuda"] else "No brinda ayuda"}\n'
    cadena_numeral += f'Parametros: {datos_csv[funcion]["cantidad_parametros"]}\n'
    cadena_numeral += f'Lineas de codigo: {datos_csv[funcion]["cantidad_lineas"]}\n'
    if (datos_csv[funcion]["cantidad_comentarios"] > 0):
        cadena_numeral += f'Comentarios: {datos_csv[funcion]["cantidad_comentarios"]}\n'
    else:
        cadena_numeral += "No aporta comentarios\n"
    if datos_csv[funcion]["invocaciones"]:
        texto_invocaciones = f'Invoca a {"(), ".join(datos_csv[funcion]["invocaciones"])}()\n'
        if len(texto_invocaciones) > 80:
            cadena_numeral += analizar_linea.largo_linea(texto_invocaciones)
        else:
            cadena_numeral += texto_invocaciones
    else:
        cadena_numeral += "No invoca a ninguna funcion\n"
    if (datos_csv[funcion]["cantidad_invocaciones"] > 0):
        cadena_numeral += f'Es invocada {datos_csv[funcion]["cantidad_invocaciones"]} {"veces" if datos_csv[funcion]["cantidad_invocaciones"] > 1 else "vez"}\n'
    else:
        cadena_numeral += "No es invocada por ninguna funcion\n"
    cadena_numeral += "\nCantidad de declaraciones: \n"
    cadena_numeral += ("-" * len("Cantidad de declaraciones: ") + "\n")
    for declaracion in datos_csv[funcion]["cantidad_declaraciones"]:
        cadena_numeral += f'{declaracion}: {datos_csv[funcion]["cantidad_declaraciones"][declaracion]}\n'
    cadena_numeral += f'{"*" * 79}\n'

    return cadena_numeral

def formatear_datos_pregunta(datos_csv, funcion):
    '''[Autor: Joel Glauber]
    [Ayuda: crea una cadena de caracteres vacia para ir concatenando en la forma que se quiere que se impriman los datos
    en pantalla, pero para las opciones que empiezan con signo de pregunta (?)]'''

    candena_pregunta = ""

    modulo = datos_csv[funcion]["modulo"] if "*" not in datos_csv[funcion]["modulo"] else datos_csv[funcion]["modulo"][1:]
    autor = datos_csv[funcion]["comentarios"]["autor"]

    candena_pregunta += f'{"*" * 79}\n'
    candena_pregunta += f'Funcion: {funcion if "*" not in funcion else funcion[1:]}\n'

    if datos_csv[funcion]["comentarios"]["ayuda"] and (len(datos_csv[funcion]["comentarios"]["ayuda"]) > 80):
        candena_pregunta += f'{analizar_linea.largo_linea(datos_csv[funcion]["comentarios"]["ayuda"])}\n'
    elif datos_csv[funcion]["comentarios"]["ayuda"]:
        candena_pregunta += f'{datos_csv[funcion]["comentarios"]["ayuda"]}\n'
    else:
        candena_pregunta += "No brinda ayuda\n"

    if datos_csv[funcion]["parametros"] and (len("Parametros formales: ")+len(datos_csv[funcion]["parametros"]) > 80):
        candena_pregunta += f'{analizar_linea.largo_linea("Parametros formales: " + datos_csv[funcion]["parametros"])}\n'
    elif datos_csv[funcion]["parametros"]:
        candena_pregunta += f'{"Parametros formales: " + datos_csv[funcion]["parametros"][1:-1]}\n'
    else:
        candena_pregunta += "No tiene parametros formales\n"
        
    candena_pregunta += f'Modulo: {modulo}\n'
    candena_pregunta += f'{autor if "Autor" in autor else "El autor es anonimo"}\n'
    candena_pregunta += f'{"*" * 79}\n'

    return candena_pregunta

def grabar_ayuda_txt(archivo_ayuda, datos_csv, funcion, opcion):
    '''[Autor: Joel Glauber]
    [Ayuda: le llega por parametro la opcion ingresada por el usuario, el archivo para grabar, los datos a grabar,
    y la funcion solicitada por el autor para analizar dicha opcion y grabar en el archivo la informacion requerida]'''

    #Si hay un signo de pregunta en la opcion entonces obtiene los datos solicitados y los graba en el archivo
    if ("?" in opcion):
        informacion = formatear_datos_pregunta(datos_csv, funcion)
        archivo_ayuda.write(informacion)
    #Si hay un numeral en la opcion entonces obtiene los datos solicitados y los graba en el archivo
    elif ("#" in opcion):
        informacion = formatear_datos_numeral(datos_csv, funcion)
        archivo_ayuda.write(informacion)

def crear_ayuda_txt(datos_csv, opcion):
    '''[Autor: Joel Glauber]
    [Ayuda: crea y graba el archivo de ayuda]'''

    with open("ayuda_funcion.txt", "w") as archivo_ayuda:
        for funcion in datos_csv:
            grabar_ayuda_txt(archivo_ayuda, datos_csv, funcion, opcion)

def mostrar_datos_funcion(datos_csv, funcion, opcion):
    '''[Autor: Joel Glauber]
    [Ayuda: analiza la opcion ingresada y dependiendo de esta, imprime la informacion solicitada.]'''

    #Si hay un numeral en la opcion entonces obtiene los datos solicitados y los imprime en pantalla
    if ("#" in opcion):
        informacion = formatear_datos_numeral(datos_csv, funcion)
        print(informacion)
    #Si hay un signo de pregunta en la opcion entonces obtiene los datos solicitados y los imprime en pantalla
    elif ("?" in opcion):
        informacion = formatear_datos_pregunta(datos_csv, funcion)
        print(informacion)

def opcion_pregunta(datos_csv, opcion):
    '''[Autor: Joel Glauber]
    [Ayuda: analiza si se quiere saber todo o solo de una funcion en especifico.]'''

    #Si se quiere saber todo, imprime los datos para cada funcion
    if (opcion == "?todo"):
        for funcion in datos_csv:
            mostrar_datos_funcion(datos_csv, funcion, opcion)
    #Si se quiere saber de una funcion especifica entonces imprime sobre esa funcion
    elif (opcion[1:] in datos_csv.keys()):
        mostrar_datos_funcion(datos_csv, opcion[1:], opcion)
    else:
        print("Esa funcion no existe")

def opcion_numeral(datos_csv, opcion):
    '''[Autor: Joel Glauber]
    [Ayuda: analiza si se quiere saber todo o solo de una funcion en especifico.]'''

    #Si se quiere saber todo, imprime los datos para cada funcion
    if (opcion == "#todo"):
        for funcion in datos_csv:
            mostrar_datos_funcion(datos_csv, funcion, opcion)
    #Si se quiere saber de una funcion especifica entonces imprime sobre esa funcion
    elif (opcion[1:] in datos_csv.keys()):
        mostrar_datos_funcion(datos_csv, opcion[1:], opcion)
    else:
        print("Esa funcion no existe")

def analizar_opcion(datos_csv, opcion):
    '''[Autor: Joel Glauber]
    [Ayuda: analiza la opcion que le llega por parametro, la cual fue ingresada por el usuario, y en base a esa opcion,
    realiza distintas cosas]'''

    #Si la opcion es del tipo numeral, la analiza por seraprado
    if (opcion[0] == "#") and (len(opcion) > 1):
        opcion_numeral(datos_csv, opcion)
    #Si la opcion es del tipo signo de pregunta, la analiza por seraprado
    elif (opcion[0] == "?") and (len(opcion) > 1):
        opcion_pregunta(datos_csv, opcion)
    #Si se ingresa la opcion "imprimir ?todo" se crea el archivo de ayuda
    elif (opcion == "imprimir ?todo"):
        print("\nCreando archivo de ayuda...")
        crear_ayuda_txt(datos_csv, opcion)
        print("Archivo creado con exito!")
    #Si se ingresa la opcion "imprimir #todo" se crea el archivo de ayuda
    elif (opcion == "imprimir #todo"):
        print("\nCreando archivo de ayuda...")
        crear_ayuda_txt(datos_csv, opcion)
        print("Archivo creado con exito!")
    #Si la opcion ingresada es incorrecta, se vuelve a intentar
    else:
        print("\nOpcion incorrecta, ingrese nuevamente\n")

def solicitar_ingreso_usuario(datos_csv, tabla, cantidad_guiones):
    '''[Autor: Joel Glauber]
    [Ayuda: solicita al autor que ingrese una de las opciones]'''

    print("\nPresion ENTER para salir")
    #Se solicita ingreso al usuario
    opcion = input("\nFuncion: ")
    while opcion:
        #Analiza la opcion ingresada
        analizar_opcion(datos_csv, opcion)
        #Se muestra la tabla y las instrucicones de uso denuevo
        mostrar_tabla_funciones(tabla, cantidad_guiones)
        mostrar_instrucciones_uso()
        #Se solicita ingreso al usuario
        print("\nPresion ENTER para salir")
        opcion = input("\nFuncion: ")

def mostrar_tabla_funciones(tabla, cantidad_guiones):
    '''[Autor: Joel Glauber]
    [Ayuda: Imprime la tabla de funciones]'''
    
    print(f'{"-" * (cantidad_guiones)}')
    print(tabla)
    print(f'{"-" * (cantidad_guiones)}')

def mostrar_instrucciones_uso():
    '''[Autor: Ivan Litteri]
    [Ayuda: Imprime las instrucciones de uso del modulo]'''

    print("?<funcion> ---> indica la descripcion asociada al uso, parametros, autor, y modulo de la funcion")
    print("?todo ---> indica la descripcion asociada al uso, parametros, autor, y modulo de todas las funciones")
    print("imprimir ?todo ---> lo mismo que ?todo pero lo graba en un archivo")
    print("#<funcion> ---> indica todo lo relativo a la funcion")
    print("#todo ---> indica todo lo relativo a todas las funciones")
    print("imprimir #todo ---> lo mismo que #todo pero lo graba en un archivo")

def consultar_funciones(datos_archivos_csv):
    '''[Autor: Joel Glauber]'''

    lista_funciones = sorted(datos_archivos_csv.keys())
    tabla, cantidad_guiones = obtener.tabla_funciones(lista_funciones)
    mostrar_tabla_funciones(tabla, cantidad_guiones)
    mostrar_instrucciones_uso()
    solicitar_ingreso_usuario(datos_archivos_csv, tabla, cantidad_guiones)