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

def leer_codigo(codigo, datos_actuales, nombre_modulo, imports):
    '''
    Lee el codigo que le llega por parametro, lo analiza y actualiza el diccionario donde se guardan los datos 
    analizados cada vez que se llama.
    '''
    bandera_comentario = False
    bandera_funcion = False
    contador_comillas_triples = 0
    contador_def = 0

    #Lee la primer linea del archivo que abri
    linea_codigo = codigo.readline()
    #Entra al while siempre y cuando no llegue a la ultima linea del codigo del archivo
    while linea_codigo:
        if linea_codigo.strip().startswith("return") or contador_def == 2:
            contador_def = 0
            bandera_funcion = False
        #Si la linea empieza con def, entonces se trata de una funcion, por lo tanto:
        if linea_codigo.startswith("def"):
            bandera_funcion = True
            nombre_funcion, parametros = separar_linea_funcion(linea_codigo)
            #Guarda los datos en un diccionario general, cada funcion es una key y su value son "sus caracteristicas"
            datos_actuales[nombre_funcion] = {"modulo": nombre_modulo, 
                                                "parametros": parametros, 
                                                "lineas": [], 
                                                "comentarios": {"autor": "", 
                                                                "ayuda": "",
                                                                "otros comentarios": []
                                                                }
                                                }
        #Almaceno las lineas de imports
        if linea_codigo.startswith("import"):
            #Si el nombre del modulo no esta como key, entonces lo agrega (Esto ocurre una vez sola)
            if nombre_modulo not in imports:
                imports[nombre_modulo] = []
        if bandera_funcion:
            imports[nombre_modulo].append(linea_codigo)
            if "#" not in linea_codigo and "'''" not in linea_codigo and not bandera_comentario:
                datos_actuales[nombre_funcion]["lineas"].append(f'"{linea_codigo.strip()}"')
            elif linea_codigo.startswith(" ") and linea_codigo.strip().startswith("'''") and linea_codigo.count("'''") == 1:
                contador_comillas_triples += 1
                bandera_comentario = True
                if contador_comillas_triples == 2:
                    contador_comillas_triples = 0
                    bandera_comentario = False
            elif linea_codigo.startswith(" ") and linea_codigo.count("'''") == 2:
                datos_actuales[nombre_funcion]["comentarios"]["autor"] = f'"{linea_codigo.strip()[3:-3]}"'
            elif linea_codigo.strip().startswith("#"):
                datos_actuales[nombre_funcion]["comentarios"]["otros comentarios"].append(f'"{linea_codigo.strip()}"')
            if bandera_comentario and contador_comillas_triples < 2:
                datos_actuales[nombre_funcion]["comentarios"]["ayuda"] += f'{linea_codigo.strip()}'
        #Lee la siguiente linea del codigo
        linea_codigo = codigo.readline()

    return datos_actuales, imports

def grabar_fuente_individual(archivo_fuente, nombre_funcion, parametros_funcion, nombre_modulo, lineas_codigo):
    #Escribe una linea en el archivo de fuente del modulo correspondiente
    archivo_fuente.write(f'{nombre_funcion},"{parametros_funcion}",{nombre_modulo},{",".join(linea_codigo for linea_codigo in lineas_codigo)}\n')

def grabar_comentarios_individual(archivo_comentarios, nombre_funcion, comentarios):
    #Extraigo el nombre del autor del diccionario comentarios
    nombre_autor = comentarios["autor"]
    #Extraigo la ayuda de funcion del diccionario comentarios
    ayuda = comentarios["ayuda"]
    #Extraigo otros comentrios del diccionario comentarios
    otros_comentarios = comentarios["otros comentarios"]
    #Escribe una linea en el archivo de comentarios del modulo correspondiente
    archivo_comentarios.write(f'{nombre_funcion},{nombre_autor},"{ayuda[3:]}",{",".join(comentario for comentario in otros_comentarios) if otros_comentarios is not None else None}\n')

def obtener_nombres_archivos_csv_individuales(ubicaciones_modulos):
    '''
    Obtiene 2 listas de nombres (uno para fuentes y otro para comentarios)
    '''

    #lista de nombres de modulos
    nombres_modulos = [ubicacion_modulo.split("\\")[-1] for ubicacion_modulo in ubicaciones_modulos]
    #Lista de todos los nombres de los archivos fuente
    nombres_archivos_fuente_individuales = [f'fuente_{nombre_modulo}.csv' for nombre_modulo in nombres_modulos]
    #Lista de todos los nombres de los archivos de comentarios
    nombres_archivos_comentarios_individuales = [f'comentarios_{nombre_modulo}.csv' for nombre_modulo in nombres_modulos]

    #Retorna las listas
    return nombres_archivos_fuente_individuales, nombres_archivos_comentarios_individuales


def crear_archivos_csv_individuales(ubicaciones_modulos):
    ''' 
    Abre el modulo con su ubicacion especifica (obtenida de el archivo principal) en forma de lectura, el archivo 
    fuente y comentario especifico del modulo, y en paralelo, analiza el codigo del modulo con la funcion 
    leer_codigo que devuelve un diccionario con los datos de los codigos, datos que luego se utilizan para imprimirse 
    de la forma que se pide sobre los archivos especificos del modulo. Una vez que termina de grabar todo, cierra los 
    archivos y repite.
    '''

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
                    grabar_fuente_individual(archivo_fuente, nombre_funcion, datos_modulos[nombre_funcion]["parametros"], nombre_modulo, datos_modulos[nombre_funcion]["lineas"])
                    grabar_comentarios_individual(archivo_comentarios, nombre_funcion, datos_modulos[nombre_funcion]["comentarios"])

#EN CONSTRUCCION
def aparear_archivos(nombres_archivos_csv_individuales):
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

def main():
    '''
    Funcion principal del modulo
    '''

    archivo_principal = "programas.txt"
    ubicaciones_modulos = obtener_ubicaciones_modulos(archivo_principal)
    nombres_archivos_fuente, nombres_archivos_comentarios = obtener_nombres_archivos_csv_individuales(ubicaciones_modulos)
    nombres_archivos_csv_individuales = nombres_archivos_fuente + nombres_archivos_comentarios
    crear_archivos_csv_individuales(ubicaciones_modulos)
    aparear_archivos(nombres_archivos_fuente)
    aparear_archivos(nombres_archivos_comentarios)
    borrar_archivos_csv_individuales(nombres_archivos_csv_individuales)

main()