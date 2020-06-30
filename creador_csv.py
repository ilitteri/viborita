def obtener_ubicaciones(archivo_principal):
    '''
    Lee el archivo principal que le llega por parametro (en nuestro caso el .txt), y retorna una lista con las lineas 
    de ese archivo (en este caso cada linea corresponde a las ubicaciones de los archivos de la aplicacion a a anlizar).
    '''
    with open(archivo_principal, "r") as archivo:
        ubicaciones = archivo.read().splitlines()

    return ubicaciones

def separar_linea_funcion(linea):
    '''
    Recorre la linea de la funcion y separa el nombre de los parametros de la misma
    '''
    messi = 10
    neymar = 10
    bandera = False
    nombre_funcion = ""
    parametros = ""
    for caracter in linea[3:-2]:
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

def leer_lineas(codigo, datos_actuales, nombre_modulo, imports):
    #Lee la primer linea del archivo que abri
    linea = codigo.readline()
    #Entra al while siempre y cuando no llegue a la ultima linea del codigo del archivo
    while linea:
        #Si la linea empieza con def, entonces se trata de una funcion, por lo tanto:
        if linea.startswith("def"):
            nombre_funcion, parametros = separar_linea_funcion(linea)
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
        if linea.startswith("import"):
            if nombre_modulo not in imports:
                imports[nombre_modulo] = []
            imports[nombre_modulo].append(linea)
        #Filtra comentarios
        if linea.startswith("    "):
            #Filtra las lineas de codigo y los comentarios con "#"
            if ("'''" in linea):
                if "Ayuda" in linea:
                    datos_actuales[nombre_funcion]["comentarios"]["ayuda"] = f'"{linea.strip()}"'
                elif "Autor" in linea:     
                    datos_programas[nombre_funcion]["comentarios"]["autor"] = f'"{linea.strip()}"'
            elif ("#" in linea):
                if datos_actuales[nombre_funcion]["comentarios"]["otros comentarios"] == None:
                    datos_actuales[nombre_funcion]["comentarios"]["otros comentarios"] = []
                datos_actuales[nombre_funcion]["comentarios"]["otros comentarios"].append(f'"{linea.strip()}"')
            else:
                datos_actuales[nombre_funcion]["lineas"].append(f'"{linea.strip()}"')
        #Lee la siguiente linea del codigo
        linea = codigo.readline()

    return datos_actuales

def obtener_datos_programas(archivo_principal):
    '''
    Analiza cada uno de los archivos que se encuentran en el archivo principal (que se pasa por parametro) y devuelve
    una lista con los nombres de cada modulo un diccionario ordenado con todos los datos de esos archivos con la forma:
    datos_programas ---->funcion_1 ---->{"modulo": modulo_func_1, "parametros": param_func_1, "lineas":[lineas_cod_func_1], "comentarios": [coment_func_1]}
                    ---->funcion_2 ---->{"modulo": modulo_func_2, "parametros": param_func_2, "lineas":[lineas_cod_func_2], "comentarios": [coment_func_2]}
                            ...
                    ---->funcion_n ---->{"modulo": modulo_func_n, "parametros": param_func_n, "lineas":[lineas_cod_func_n], "comentarios": [coment_func_n]}
    '''

    #Lista de ubicaciones de modulos de la aplicacion
    ubicaciones = obtener_ubicaciones(archivo_principal)
    datos_programas = {}
    imports = {}
    modulos = []

    #Recorre la lista de ubicaciones de cada archivo de la aplicacion
    for ubicacion in ubicaciones:
        #Nombre del modulo
        nombre_modulo = ubicacion.split("\\")[-1]
        if nombre_modulo not in modulos:
            modulos.append(nombre_modulo)
        #Abro el archivo con la ubicacion en la que se encuentra en la iteracion
        with open(ubicacion, "r") as codigo:
            #Esta funcion actualiza el diccionario de datos
           leer_lineas(codigo, datos_programas, nombre_modulo, imports)
    #Devuelve el diccionario, con la forma que se explica al principio de la funcion
    return datos_programas, modulos

def grabar_fuente_individual(archivo_fuente, nombre_funcion, parametros, modulo, lineas):
    #Escribe una linea en el archivo de fuente del modulo correspondiente
    archivo_fuente.write(f'{nombre_funcion},{parametros},{modulo},{",".join(linea for linea in lineas)}\n')

def grabar_comentarios_individual(archivo_comentarios, nombre_funcion, comentarios):
    nombre_autor = comentarios["autor"]
    ayuda = comentarios["ayuda"]
    otros_comentarios = comentarios["otros comentarios"]
    #Escribe una linea en el archivo de comentarios del modulo correspondiente
    archivo_comentarios.write(f'{nombre_funcion},{nombre_autor},{ayuda},{",".join(comentario for comentario in otros_comentarios) if otros_comentarios is not None else None}\n')

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
    '''
    Imprime los datos en un archivo .csv que creamon en la misma. Los datos se imprimen en la forma que se pide en
    la consigna.
    Se crea un archivo de fuente y un archivo de comentarios, para cada archivo analizado en la funcion anterior
    '''
    #Lista de nombres de funciones
    nombres_funciones_ordenadas = sorted(list(datos.keys()))
    #Recorre cada modulo
    for modulo in modulos:
        #Crea 2 archivos .csv con el nombre del modulo
        with open(f'fuente_{modulo}.csv', "w") as archivo_fuente, open(f'comentarios_{modulo}.csv', "w") as archivo_comentarios:
            #Recorre funcion por funcion
            for nombre_funcion in nombres_funciones_ordenadas:
                #Si el modulo de la iteracion actual corresponde al modulo de la funcion de la iteracion actual:
                if modulo == datos[nombre_funcion]["modulo"]:
                    grabar_fuente_individual(archivo_fuente, nombre_funcion, datos[nombre_funcion]["parametros"], modulo, datos[nombre_funcion]["lineas"])
                    grabar_comentarios_individual(archivo_comentarios, nombre_funcion, datos[nombre_funcion]["comentarios"])

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


def main():
    '''
    Funcion principal del modulo
    '''
    archivo_principal = "programas.txt"
    datos, modulos = obtener_datos_programas(archivo_principal)
    nombres_archivos_fuente, nombres_archivos_comentarios = obtener_nombres_archivos(modulos)
    crear_archivos_csv(datos, modulos)
    aparear_archivos(nombres_archivos_fuente)
    aparear_archivos(nombres_archivos_comentarios)

main()