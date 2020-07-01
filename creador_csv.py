<<<<<<< HEAD
def obtener_ubicaciones(archivo_principal):
=======
import os

def obtener_ubicaciones_modulos(archivo_principal):
>>>>>>> affd2838dcd329be04d460607efc554cd73e578a
    '''
    Lee el archivo principal que le llega por parametro (en nuestro caso el .txt), y retorna una lista con las lineas 
    de ese archivo (en este caso cada linea corresponde a las ubicaciones de los archivos de la aplicacion a a anlizar).
    '''

    with open(archivo_principal, "r") as archivo:
        ubicaciones = archivo.read().splitlines()

    return ubicaciones
<<<<<<< HEAD

def separar_linea_funcion(linea):
    #Creo una nueva linea(str) donde guardo la linea pero sin espacios(" ")
    nueva_linea = ""
    for caracter in linea[3:-1]:
        if caracter.isspace() == False:
            nueva_linea += caracter
    #Obtiene el nombre de la funcion de la variable nueva_linea
    nombre_funcion = nueva_linea.split("(")[0]
    #Guarda los parametros de la funcion de la siguiente manera (param_1,para,_2,...,param_n)
    parametros = "(" + nueva_linea.split("(")[1][:-2] + ")"

    return nombre_funcion, parametros
=======
>>>>>>> affd2838dcd329be04d460607efc554cd73e578a

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
<<<<<<< HEAD
    datos_programas ---->funcion_1 ---->{"modulo": modulo_func_1, "parametros": param_func_1, "lineas":[lineas_cod_func_1], "comentarios": [coment_func_1]}
                    ---->funcion_2 ---->{"modulo": modulo_func_2, "parametros": param_func_2, "lineas":[lineas_cod_func_2], "comentarios": [coment_func_2]}
=======
    datos_programas ---->funcion_1 ---->{"modulo": modulo_func_1, "parametros": param_func_1, "lineas":[lineas_cod_func_1], "comentarios": {"autor": "autor_func_1", "ayuda": "ayuda_func_1", "otros comentarios": [otros_comentarios_func_1]}}
                    ---->funcion_2 ---->{"modulo": modulo_func_2, "parametros": param_func_2, "lineas":[lineas_cod_func_2], "comentarios": {"autor": "autor_func_2", "ayuda": "ayuda_func_2", "otros comentarios": [otros_comentarios_func_2]}}
>>>>>>> affd2838dcd329be04d460607efc554cd73e578a
                            ...
                    ---->funcion_n ---->{"modulo": modulo_func_n, "parametros": param_func_n, "lineas":[lineas_cod_func_n], "comentarios": {"autor": "autor_func_n", "ayuda": "ayuda_func_n", "otros comentarios": [otros_comentarios_func_n]}}
    '''

    #Lista de ubicaciones de modulos de la aplicacion
<<<<<<< HEAD
    ubicaciones = obtener_ubicaciones(archivo_principal)
    datos_programas = {}
    modulos = []
=======
    ubicaciones_modulos = obtener_ubicaciones_modulos(archivo_principal)
    datos_modulos = {}
    imports = {}
    nombres_modulos = []
>>>>>>> affd2838dcd329be04d460607efc554cd73e578a

    #Recorre la lista de ubicaciones de cada archivo de la aplicacion
    for ubicacion_modulo in ubicaciones_modulos:
        #Nombre del modulo
<<<<<<< HEAD
        nombre_modulo = ubicacion.split("\\")[-1]
        if nombre_modulo not in modulos:
            modulos.append(nombre_modulo)
        #Abro el archivo con la ubicacion en la que se encuentra en la iteracion
        with open(ubicacion, "r") as codigo:
            #Lee la primer linea del archivo que abri
            linea = codigo.readline()
            #Entra al while siempre y cuando no llegue a la ultima linea del codigo del archivo
            while linea:
                #Si la linea empieza con def, entonces se trata de una funcion, por lo tanto:
                if linea.startswith("def"):
                    nombre_funcion, parametros = separar_linea_funcion(linea)
                    #Guarda los datos en un diccionario general, cada funcion es una key y su value son "sus caracteristicas"
                    datos_programas[nombre_funcion] = {"modulo": nombre_modulo, "parametros": parametros, "lineas": [], "comentarios": []}
                #Filtra comentarios
                if (len(datos_programas) > 0) and linea.startswith("    ") and ("#" not in linea or "'''" not in linea):
                    datos_programas[nombre_funcion]["lineas"].append(f'"{linea.strip()}"')
                #Filtra las lineas de codigo
                elif linea.strip().startswith("#") or linea.strip().startswith("'''"):
                    datos_programas[nombre_funcion]["comentarios"].append(f'"{linea.strip()}"')
                #Lee la siguiente linea del codigo
                linea = codigo.readline()
    #Devuelve el diccionario, con la forma que se explica al principio de la funcion
    return datos_programas, modulos

def grabar_fuente_individual(archivo_fuente, nombre_funcion, parametros, modulo, lineas):
    #Escribe una linea en el archivo de fuente del modulo correspondiente
    archivo_fuente.write(f'{nombre_funcion},{parametros},{modulo},{",".join(linea for linea in lineas)}\n')

def grabar_comentarios_individual(archivo_comentarios, nombre_funcion, nombre_autor, ayuda, comentarios):
    #Escribe una linea en el archivo de comentarios del modulo correspondiente
    archivo_comentarios.write(f'{nombre_funcion},{nombre_autor},{ayuda},"{",".join(comentario for comentario in comentarios)}"\n')

def obtener_nombres_archivos(modulos):
    '''
    Obtiene 2 listas de nombres (uno para fuentes y otro para comentarios)
    '''
    #Lista de todos los nombres de los archivos fuente
    nombres_archivos_fuente = [f'fuente_{modulo}.csv' for modulo in modulos]
    #Lista de todos los nombres de los archivos de comentarios
    nombres_archivos_comentarios = [f'comentarios_{modulo}.csv' for modulo in modulos]

    #Retorna las listas
    return nombres_archivos_fuente, nombres_archivos_comentarios

def crear_archivos_csv(datos, modulos):
=======
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
>>>>>>> affd2838dcd329be04d460607efc554cd73e578a
    '''
    Imprime los datos en un archivo .csv que creamon en la misma. Los datos se imprimen en la forma que se pide en
    la consigna.
    Se crea un archivo de fuente y un archivo de comentarios, para cada archivo analizado en la funcion anterior
    '''
<<<<<<< HEAD
    #Lista de nombres de funciones
    nombres_funciones_ordenadas = sorted(list(datos.keys()))

=======

    #Lista de nombres de funciones
    nombres_funciones_ordenadas = sorted(list(datos_programas.keys()))
>>>>>>> affd2838dcd329be04d460607efc554cd73e578a
    #Recorre cada modulo
    for nombre_modulo in nombres_modulos:
        #Crea 2 archivos .csv con el nombre del modulo
        with open(f'fuente_{nombre_modulo}.csv', "w") as archivo_fuente, open(f'comentarios_{nombre_modulo}.csv', "w") as archivo_comentarios:
            #Recorre funcion por funcion
            for nombre_funcion in nombres_funciones_ordenadas:
                #Si el modulo de la iteracion actual corresponde al modulo de la funcion de la iteracion actual:
<<<<<<< HEAD
                if modulo == datos[nombre_funcion]["modulo"]:
                    grabar_fuente_individual(archivo_fuente, nombre_funcion, datos[nombre_funcion]["parametros"], modulo, datos[nombre_funcion]["lineas"])
                    grabar_comentarios_individual(archivo_comentarios, nombre_funcion, "nombre_autor", "ayuda", datos[nombre_funcion]["comentarios"])

#EN CONSTRUCCION
def aparear_archivos(lista_archivos):
    archivo_apareado = open(f'{"fuente_unico.csv" if "fuente" in lista_archivos[0] else "comentarios.csv"}', "w")
    for archivo in lista_archivos:
        with open(archivo, "r") as archivo_individual:
            linea = archivo_individual.readline()
            while linea:
                archivo_apareado.write(linea)
                linea = archivo_individual.readline()
    archivo_apareado.close()

=======
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
    #Retorna una lista de ubicaciones de todos los archivos .csv individuales
    return [os.path.abspath(nombre_archivo_csv_individual) for nombre_archivo_csv_individual in nombres_archivos_csv_individuales]

def borrar_archivos_csv_individuales(nombres_archivos_csv_individuales):
    '''
    Borra los archivos .csv individuales (que se encuentran en el repositorio actual) cuyas ubicaciones se obtienen 
    de una funcion a la que le llega por parametro los nombres de los archivos .csv individuales
    '''

    #Obtengo las ubicaciones
    ubicaciones_archivos_csv_individuales = obtener_ubicaciones_archivos_csv_individuales(nombres_archivos_csv_individuales)
    for ubicacion_archivo_csv_individual in ubicaciones_archivos_csv_individuales:
        #Borro el archivo que se encuentra en esa ubicacion
        os.remove(ubicacion_archivo_csv_individual)
>>>>>>> affd2838dcd329be04d460607efc554cd73e578a

def main():
    '''
    Funcion principal del modulo
    '''
<<<<<<< HEAD
    archivo_principal = "programas.txt"
    datos, modulos = leer_programas(archivo_principal)
    nombres_archivos_fuente, nombres_archivos_comentarios = obtener_nombres_archivos(modulos)
    crear_archivos_csv(datos, modulos)
    aparear_archivos(nombres_archivos_fuente)
    aparear_archivos(nombres_archivos_comentarios)
=======

    archivo_principal = "programas.txt"
    datos_modulos, nombres_modulos = obtener_datos_programas(archivo_principal)
    nombres_archivos_fuente, nombres_archivos_comentarios = obtener_nombres_archivos_csv_individuales(nombres_modulos)
    nombres_archivos_csv_individuales = nombres_archivos_fuente + nombres_archivos_comentarios
    crear_archivos_csv_individuales(datos_modulos, nombres_modulos)
    aparear_archivos(nombres_archivos_fuente)
    aparear_archivos(nombres_archivos_comentarios)
    borrar_archivos_csv_individuales(nombres_archivos_csv_individuales)
>>>>>>> affd2838dcd329be04d460607efc554cd73e578a

main()