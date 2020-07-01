import os

def obtener_ubicaciones_modulos(archivo_principal):
    '''
    Lee el archivo principal que le llega por parametro (en nuestro caso el .txt), y retorna una lista con las lineas 
    de ese archivo (en este caso cada linea corresponde a las ubicaciones de los archivos de la aplicacion a a anlizar).
    '''

    with open(archivo_principal, "r") as archivo:
        ubicaciones = archivo.read().splitlines()

    return ubicaciones

def separar_linea_funcion(linea_codigo):
    '''
    Recorre la linea de la funcion y separa el nombre de los parametros de la misma
    '''

    bandera = False
    nombre_funcion = ""
    parametros = ""
    for caracter in linea_codigo[3:-2]:
        if caracter == "(":
            bandera = True
        if not caracter.isspace():
            if bandera:
                parametros += caracter
            else:
                nombre_funcion += caracter
        if caracter == ")":
            bandera = False

    return nombre_funcion, parametros

def leer_lineas_codigo(codigo, datos_actuales, nombre_modulo, imports):
    '''
    Lee linea por linea el codigo, y actualiza con los datos procesados al diccionario de datos_actuales y tambien
    el diccionario de imports
    '''

    #Lee la primer linea del archivo que abri
    linea_codigo = codigo.readline()
    #Entra al while siempre y cuando no llegue a la ultima linea del codigo del archivo
    while linea_codigo:
        #Si la linea empieza con def, entonces se trata de una funcion, por lo tanto:
        if linea_codigo.startswith("def"):
            nombre_funcion, parametros = separar_linea_funcion(linea_codigo)
            #Guarda los datos en un diccionario general, cada funcion es una key y su value son "sus caracteristicas"
            datos_actuales[nombre_funcion] = {"modulo": nombre_modulo, 
                                                "parametros": parametros, 
                                                "lineas": [], 
                                                "comentarios": {"autor": None, 
                                                                "ayuda": None,
                                                                "otros comentarios": None
                                                                }
                                                }
        #Almaceno las lineas de imports
        if linea_codigo.startswith("import"):
            #Si el nombre del modulo no esta como key, entonces lo agrega (Esto ocurre una vez sola)
            if nombre_modulo not in imports:
                imports[nombre_modulo] = []
            imports[nombre_modulo].append(linea_codigo)
        #Filtra comentarios
        if linea_codigo.startswith("    "):
            #Filtra las lineas de codigo y los comentarios con "#"
            if ("'''" in linea_codigo):
                if "Ayuda" in linea_codigo:
                    datos_actuales[nombre_funcion]["comentarios"]["ayuda"] = f'"{linea_codigo.strip()}"'
                elif "Autor" in linea_codigo:     
                    datos_programas[nombre_funcion]["comentarios"]["autor"] = f'"{linea_codigo.strip()}"'
            #Filtra las lineas de codigo y los comentarios con tres comillas
            elif ("#" in linea_codigo):
                #Si aun no hay otros comentarios, entonces cambia el estado de None a una lista vacia para poder agregar el comentario (Esto ocurre una sola vez)
                if datos_actuales[nombre_funcion]["comentarios"]["otros comentarios"] == None:
                    datos_actuales[nombre_funcion]["comentarios"]["otros comentarios"] = []
                datos_actuales[nombre_funcion]["comentarios"]["otros comentarios"].append(f'"{linea_codigo.strip()}"')
            #Entran solo las lineas
            else:
                datos_actuales[nombre_funcion]["lineas"].append(f'"{linea_codigo.strip()}"')
        #Lee la siguiente linea del codigo
        linea_codigo = codigo.readline()

    return datos_actuales, imports

def obtener_datos_programas(archivo_principal):
    '''
    Analiza cada uno de los archivos que se encuentran en el archivo principal (que se pasa por parametro) y devuelve
    una lista con los nombres de cada modulo un diccionario ordenado con todos los datos de esos archivos con la forma:
    datos_programas ---->funcion_1 ---->{"modulo": modulo_func_1, "parametros": param_func_1, "lineas":[lineas_cod_func_1], "comentarios": {"autor": "autor_func_1", "ayuda": "ayuda_func_1", "otros comentarios": [otros_comentarios_func_1]}}
                    ---->funcion_2 ---->{"modulo": modulo_func_2, "parametros": param_func_2, "lineas":[lineas_cod_func_2], "comentarios": {"autor": "autor_func_2", "ayuda": "ayuda_func_2", "otros comentarios": [otros_comentarios_func_2]}}
                            ...
                    ---->funcion_n ---->{"modulo": modulo_func_n, "parametros": param_func_n, "lineas":[lineas_cod_func_n], "comentarios": {"autor": "autor_func_n", "ayuda": "ayuda_func_n", "otros comentarios": [otros_comentarios_func_n]}}
    '''

    #Lista de ubicaciones de modulos de la aplicacion
    ubicaciones_modulos = obtener_ubicaciones_modulos(archivo_principal)
    datos_modulos = {}
    imports = {}
    nombres_modulos = []

    #Recorre la lista de ubicaciones de cada archivo de la aplicacion
    for ubicacion_modulo in ubicaciones_modulos:
        #Nombre del modulo
        nombre_modulo = ubicacion_modulo.split("\\")[-1]
        if nombre_modulo not in nombres_modulos:
            nombres_modulos.append(nombre_modulo)
        #Abro el archivo con la ubicacion en la que se encuentra en la iteracion
        with open(ubicacion_modulo, "r") as codigo:
            #Esta funcion actualiza el diccionario de datos
            leer_lineas_codigo(codigo, datos_modulos, nombre_modulo, imports)
            
    #Devuelve el diccionario, con la forma que se explica al principio de la funcion
    return datos_modulos, nombres_modulos

def grabar_fuente_individual(archivo_fuente, nombre_funcion, parametros_funcion, nombre_modulo, lineas_codigo):
    #Escribe una linea en el archivo de fuente del modulo correspondiente
    archivo_fuente.write(f'{nombre_funcion},{parametros_funcion},{nombre_modulo},{",".join(linea_codigo for linea_codigo in lineas_codigo)}\n')

def grabar_comentarios_individual(archivo_comentarios, nombre_funcion, comentarios):
    nombre_autor = comentarios["autor"]
    ayuda = comentarios["ayuda"]
    otros_comentarios = comentarios["otros comentarios"]
    #Escribe una linea en el archivo de comentarios del modulo correspondiente
    archivo_comentarios.write(f'{nombre_funcion},{nombre_autor},{ayuda},{",".join(comentario for comentario in otros_comentarios) if otros_comentarios is not None else None}\n')

def obtener_nombres_archivos_csv_individuales(nombres_modulos):
    '''
    Obtiene 2 listas de nombres (uno para fuentes y otro para comentarios)
    '''

    #Lista de todos los nombres de los archivos fuente
    nombres_archivos_fuente_individuales = [f'fuente_{nombre_modulo}.csv' for nombre_modulo in nombres_modulos]
    #Lista de todos los nombres de los archivos de comentarios
    nombres_archivos_comentarios_individuales = [f'comentarios_{nombre_modulo}.csv' for nombre_modulo in nombres_modulos]

    #Retorna las listas
    return nombres_archivos_fuente_individuales, nombres_archivos_comentarios_individuales


def crear_archivos_csv_individuales(datos_programas, nombres_modulos):
    '''
    Imprime los datos en un archivo .csv que creamon en la misma. Los datos se imprimen en la forma que se pide en
    la consigna.
    Se crea un archivo de fuente y un archivo de comentarios, para cada archivo analizado en la funcion anterior
    '''

    #Lista de nombres de funciones
    nombres_funciones_ordenadas = sorted(list(datos_programas.keys()))
    #Recorre cada modulo
    for nombre_modulo in nombres_modulos:
        #Crea 2 archivos .csv con el nombre del modulo
        with open(f'fuente_{nombre_modulo}.csv', "w") as archivo_fuente, open(f'comentarios_{nombre_modulo}.csv', "w") as archivo_comentarios:
            #Recorre funcion por funcion
            for nombre_funcion in nombres_funciones_ordenadas:
                #Si el modulo de la iteracion actual corresponde al modulo de la funcion de la iteracion actual:
                if nombre_modulo == datos_programas[nombre_funcion]["modulo"]:
                    grabar_fuente_individual(archivo_fuente, nombre_funcion, datos_programas[nombre_funcion]["parametros"], nombre_modulo, datos_programas[nombre_funcion]["lineas"])
                    grabar_comentarios_individual(archivo_comentarios, nombre_funcion, datos_programas[nombre_funcion]["comentarios"])

#EN CONSTRUCCION
def aparear_archivos(nombres_archivos_csv_individuales):
    archivo_apareado = open(f'{"fuente_unico.csv" if "fuente" in nombres_archivos_csv_individuales[0] else "comentarios.csv"}', "w")
    for nombre_archivo_csv_individual in nombres_archivos_csv_individuales:
        with open(nombre_archivo_csv_individual, "r") as archivo_individual:
            linea_csv = archivo_individual.readline()
            while linea_csv:
                archivo_apareado.write(linea_csv)
                linea_csv = archivo_individual.readline()
    archivo_apareado.close()

def obtener_ubicaciones_archivos_csv_individuales(nombres_archivos_csv_individuales):
    return [os.path.abspath(nombre_archivo_csv_individual) for nombre_archivo_csv_individual in nombres_archivos_csv_individuales]

def borrar_archivos_csv_individuales(nombres_archivos_csv_individuales):
    ubicaciones_archivos_csv_individuales = obtener_ubicaciones_archivos_csv_individuales(nombres_archivos_csv_individuales)
    for ubicacion_archivo_csv_individual in ubicaciones_archivos_csv_individuales:
        os.remove(ubicacion_archivo_csv_individual)
    return "Archivos .csv individuales borrados"    

def main():
    '''
    Funcion principal del modulo
    '''

    archivo_principal = "programas.txt"
    datos_modulos, nombres_modulos = obtener_datos_programas(archivo_principal)
    nombres_archivos_fuente, nombres_archivos_comentarios = obtener_nombres_archivos_csv_individuales(nombres_modulos)
    nombres_archivos_csv_individuales = nombres_archivos_fuente + nombres_archivos_comentarios
    crear_archivos_csv_individuales(datos_modulos, nombres_modulos)
    aparear_archivos(nombres_archivos_fuente)
    aparear_archivos(nombres_archivos_comentarios)
    borrar_archivos_csv_individuales(nombres_archivos_csv_individuales)

main()