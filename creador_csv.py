def obtener_ubicaciones_modulos(archivo_principal):
    '''[Autor: Ivan Litteri]
    [Ayuda: Lee el archivo principal que le llega por parametro (en nuestro caso el .txt), y retorna una lista con las 
    lineas de ese archivo (en este caso cada linea corresponde a las ubicaciones de los archivos de la aplicacion a 
    anlizar).]'''
    #Abro el archivo y obtengo una lista de todas sus lineas
    with open(archivo_principal, "r") as archivo:
        ubicaciones = archivo.read().splitlines()

    #Devuelvo la lista de lineas 
    return ubicaciones

def leer_codigo(codigo, datos_ordenados, nombre_modulo, imports, bandera_funcion = False, bandera_comentario = False, bandera_ayuda = False, nombre_funcion = None):
    '''[Autor: Ivan Litteri]
    [Ayuda: Lee el codigo que le llega por parametro, lo analiza con distintas funciones y actualiza el 
    diccionario donde se guardan los datos analizados cada vez que se llama.]'''

    #Importo las funciones del modulo analizar_linea.py
    import analizar_linea

    linea_codigo = codigo.readline()
    while linea_codigo:
        #Se habilita esta bandera cuando en el codigo a leer empieza una funcion, se deshabilita cuando termina o empieza otra
        if bandera_funcion:
            #Se habilita esta bandera cuando se detecta un comentario multilinea que no se cierra en la misma linea
            if bandera_comentario:
                ayuda_funcion, bandera_ayuda = analizar_linea.ayuda_funcion(linea_codigo, bandera_ayuda)
                datos_ordenados[nombre_funcion]["comentarios"]["ayuda"] += ayuda_funcion
                #Se deshabilita la bandera cuando se detecta que se cierra el comentario multilinea.
                if "'''" in linea_codigo:
                    bandera_comentario = False
            #Guarda otro tipo de comentarios
            elif "#" in linea_codigo:
                #Si es None, cambia su valor a una lista vacia para que se pueda hacer append.
                if datos_ordenados[nombre_funcion]["comentarios"]["otros"] == None:
                    datos_ordenados[nombre_funcion]["comentarios"]["otros"] = []
                otro_comentario = analizar_linea.comentario_numeral(linea_codigo)
                datos_ordenados[nombre_funcion]["comentarios"]["otros"].append(f'"{otro_comentario}"')
            #Si un comentario multilinea se abre y cierra en la misma linea, analiza la linea y guarda los datos del autor.
            elif linea_codigo.count("'''") == 2:
                autor_funcion = analizar_linea.autor_funcion(linea_codigo)
                datos_ordenados[nombre_funcion]["comentarios"]["autor"] = autor_funcion
            #Si la linea empieza con un comentario multilinea, y no se cierra en la misma linea, se analiza esta primera linea que corresponde 
            #al autor, y luego habilita la bandera de comentario multilinea para que se analicen las lineas siguientes hasta que se cierre 
            #el comentario multilinea.
            elif linea_codigo.strip().startswith("'''"):
                bandera_comentario = True
                autor_funcion = analizar_linea.autor_funcion(linea_codigo)
                datos_ordenados[nombre_funcion]["comentarios"]["autor"] = autor_funcion
            #Si ninguna linea es un comentario guarda la linea en lineas de codigo
            else:    
                datos_ordenados[nombre_funcion]["lineas"].append(f'"{linea_codigo.strip()}"')

        if linea_codigo.strip().startswith("return"):
            bandera_funcion = False
        if linea_codigo.startswith("def"):
            bandera_funcion = True
            nombre_funcion, parametros_funcion = analizar_linea.declaracion_funcion(linea_codigo)
            datos_ordenados[nombre_funcion] = {"modulo": nombre_modulo, 
                                                "parametros": parametros_funcion, 
                                                "lineas": [], 
                                                "comentarios": {"autor": "", 
                                                                "ayuda": "",
                                                                "otros": None
                                                                }
                                                }
        #Almaceno las lineas de imports
        if linea_codigo.startswith("import"):
            #Si el nombre del modulo no esta como key, entonces lo agrega (Esto ocurre una vez sola)
            if nombre_modulo not in imports:
                imports[nombre_modulo] = []
            imports[nombre_modulo].append(linea_codigo)
        #Lee la siguiente linea del codigo
        linea_codigo = codigo.readline()

    #Devuelvo un diccionario de datos de todos los modulos, y uno de imports
    return datos_ordenados, imports

def obtener_nombres_archivos_csv_individuales(ubicaciones_modulos):
    '''[Autor: Ivan Litteri]
    [Ayuda: Obtiene 2 listas de nombres (uno para fuentes y otro para comentarios).]'''

    #lista de nombres de modulos
    nombres_modulos = [ubicacion_modulo.split("\\")[-1] for ubicacion_modulo in ubicaciones_modulos]
    #Lista de todos los nombres de los archivos fuente
    nombres_archivos_fuente_individuales = [f'fuente_{nombre_modulo}.csv' for nombre_modulo in nombres_modulos]
    #Lista de todos los nombres de los archivos de comentarios
    nombres_archivos_comentarios_individuales = [f'comentarios_{nombre_modulo}.csv' for nombre_modulo in nombres_modulos]

    #Retorna las listas
    return nombres_archivos_fuente_individuales, nombres_archivos_comentarios_individuales


def crear_archivos_csv_individuales(ubicaciones_modulos):
    '''[Autor: Ivan Litteri]
    [Ayuda: Abre el modulo con su ubicacion especifica (obtenida de el archivo principal) en forma de lectura, 
    el archivo fuente y comentario especifico del modulo, y en paralelo, analiza el codigo del modulo con la 
    funcion leer_codigo que devuelve un diccionario con los datos de los codigos, datos que luego se utilizan para 
    imprimirse de la forma que se pide sobre los archivos especificos del modulo. Una vez que termina de grabar 
    todo, cierra los archivos y repite.]'''

    #Importo las funciones del modulo grabar.py
    import grabar

    datos_modulos = {}
    imports = {}

    #Recorro las ubicaciones de los modulos
    for ubicacion_modulo in ubicaciones_modulos:
        #Nombre del modulo
        nombre_modulo = ubicacion_modulo.split("\\")[-1]
        #Abre un archivo para leer y dos para escribir, al mismo tiempo
        with open(ubicacion_modulo, "r") as codigo, open(f'fuente_{nombre_modulo}.csv', "w") as archivo_fuente, open(f'comentarios_{nombre_modulo}.csv', "w") as archivo_comentarios:
            datos_modulos, imports = leer_codigo(codigo, datos_modulos, nombre_modulo, imports)
            #Lista de nombres de funciones
            nombres_funciones_ordenadas = sorted(list(datos_modulos.keys()))
            #Recorre funcion por funcion
            for nombre_funcion in nombres_funciones_ordenadas:
                #Si el modulo de la iteracion actual corresponde al modulo de la funcion de la iteracion actual:
                if nombre_modulo == datos_modulos[nombre_funcion]["modulo"]:
                    grabar.fuente_individual(archivo_fuente, nombre_funcion, datos_modulos[nombre_funcion]["parametros"], nombre_modulo, datos_modulos[nombre_funcion]["lineas"])
                    grabar.comentarios_individual(archivo_comentarios, nombre_funcion, datos_modulos[nombre_funcion]["comentarios"])

#EN CONSTRUCCION
def aparear_archivos(nombres_archivos_csv_individuales):
    '''[Autor: Ivan Litteri]'''

    lineas_archivos_csv = []
    for nombre_archivo_csv_individual in nombres_archivos_csv_individuales:
        with open(nombre_archivo_csv_individual, "r") as archivo_individual:
            linea_csv = archivo_individual.readline()
            while linea_csv:
                lineas_archivos_csv.append(linea_csv)
                linea_csv = archivo_individual.readline()
    lineas_ordenadas_archivos_csv = sorted(lineas_archivos_csv)
    with open(f'{"fuente_unico.csv" if "fuente" in nombres_archivos_csv_individuales[0] else "comentarios.csv"}', "w") as archivo_final:
        for linea in lineas_ordenadas_archivos_csv:
            archivo_final.write(linea)
    

def obtener_ubicaciones_archivos_csv_individuales(nombres_archivos_csv_individuales):
    '''[Autor: Ivan Litteri]'''

    import os
    
    #Retorna una lista de ubicaciones de todos los archivos .csv individuales
    return [os.path.abspath(nombre_archivo_csv_individual) for nombre_archivo_csv_individual in nombres_archivos_csv_individuales]

def borrar_archivos_csv_individuales(nombres_archivos_csv_individuales):
    '''[Autor: Ivan Litteri]
    [Ayuda: Borra los archivos .csv individuales (que se encuentran en el repositorio actual) cuyas ubicaciones se obtienen 
    de una funcion a la que le llega por parametro los nombres de los archivos .csv individuales.]'''

    import os

    #Obtengo las ubicaciones y las recorro para borrar el archivo que se encuentra en ella
    for ubicacion_archivo_csv_individual in obtener_ubicaciones_archivos_csv_individuales(nombres_archivos_csv_individuales):
        #Borro el archivo que se encuentra en esa ubicacion
        os.remove(ubicacion_archivo_csv_individual)

def main():
    '''[Autor: Ivan Litteri]'''

    archivo_principal = "programas.txt"
    ubicaciones_modulos = obtener_ubicaciones_modulos(archivo_principal)
    nombres_archivos_fuente, nombres_archivos_comentarios = obtener_nombres_archivos_csv_individuales(ubicaciones_modulos)
    nombres_archivos_csv_individuales = nombres_archivos_fuente + nombres_archivos_comentarios
    crear_archivos_csv_individuales(ubicaciones_modulos)
    aparear_archivos(nombres_archivos_fuente)
    aparear_archivos(nombres_archivos_comentarios)
    borrar_archivos_csv_individuales(nombres_archivos_csv_individuales)

main()