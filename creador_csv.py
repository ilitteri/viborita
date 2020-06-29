def obtener_ubicaciones(archivo_principal):
    '''
    Lee el archivo principal que le llega por parametro (en nuestro caso el .txt), y retorna una lista con las lineas 
    de ese archivo (en este caso cada linea corresponde a las ubicaciones de los archivos de la aplicacion a a anlizar).
    '''
    with open(archivo_principal, "r") as archivo:
        ubicaciones = archivo.read().splitlines()

    return ubicaciones

def leer_programas(archivo_principal):
    '''
    Analiza cada uno de los archivos que se encuentran en el archivo principal (que se pasa por parametro) y devuelve
    un diccionario ordenado con todos los datos de esos archivos con la forma:
    datos_programas ---->funcion_1 ---->{"modulo": modulo_func_1, "parametros": param_func_1, "lineas":[lineas_cod_func_1], "comentarios": [coment_func_1]}
                    ---->funcion_2 ---->{"modulo": modulo_func_2, "parametros": param_func_2, "lineas":[lineas_cod_func_2], "comentarios": [coment_func_2]}
                            ...
                    ---->funcion_n ---->{"modulo": modulo_func_n, "parametros": param_func_n, "lineas":[lineas_cod_func_n], "comentarios": [coment_func_n]}
    '''
    #Lista de ubicaciones de modulos de la aplicacion
    ubicaciones = obtener_ubicaciones(archivo_principal)
    datos_programas = {}
    modulos = []

    #Recorre la lista de ubicaciones de cada archivo de la aplicacion
    for ubicacion in ubicaciones:
        #Nombre del modulo
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
                    #Deja solo el nombre de la funcion con su/sus parametro/s
                    recorte = linea.strip()[4:-1]
                    #Obtiene el nombre de la funcion del anterior recorte
                    nombre_funcion = recorte.split("(")[0]
                    #Obtiene los parametros de la funcion del anterior recorte
                    parametros = recorte.split("(")[1].split(")")[0]
                    #Guarda los datos en un diccionario general, cada funcion es una key y su value son "sus caracteristicas"
                    datos_programas[nombre_funcion] = {"modulo": nombre_modulo, "parametros": f'({parametros})', "lineas": [], "comentarios": []}
                #Filtra comentarios
                if (len(datos_programas) > 0) and linea.startswith("    ") and ("#" not in linea or "'''" not in linea):
                    datos_programas[nombre_funcion]["lineas"].append(linea.strip())
                #Filtra las lineas de codigo
                elif linea.strip().startswith("#") or linea.strip().startswith("'''"):
                    datos_programas[nombre_funcion]["comentarios"].append(linea.strip())
                #Lee la siguiente linea del codigo
                linea = codigo.readline()
    #Devuelve el diccionario, con la forma que se explica al principio de la funcion
    return datos_programas, modulos

def grabar_fuente_individual(archivo_fuente, nombre_funcion, parametros, modulo, lineas):
    archivo_fuente.write(f'{nombre_funcion},{parametros},{modulo},{",".join(repr(linea) for linea in lineas)}\n')

def grabar_comentarios_individual(archivo_comentarios, nombre_funcion, nombre_autor, ayuda, comentarios):
    archivo_comentarios.write(f'{nombre_funcion},{nombre_autor},{ayuda},{",".join(repr(comentario) for comentario in comentarios)}\n')

def obtener_nombres_archivos(modulos):
    nombres_archivos_fuente = []
    nombres_archivos_comentarios = []

    for modulo in modulos:
        nombres_archivos_fuente.append(f'fuente_{modulo}.csv')
        nombres_archivos_comentarios.append(f'comentarios_{modulo}.csv')

    return nombres_archivos_fuente, nombres_archivos_comentarios

def crear_archivos_csv(datos, modulos):
    '''
    Imprime los datos en un archivo .csv que creamon en la misma. Los datos se imprimen en la forma que se pide en
    la consigna.
    Se crea un archivo de fuente y un archivo de comentarios, para cada archivo analizado en la funcion anterior
    '''
    #Lista de nombres de funciones
    nombres_funciones = list(datos.keys())

    #Recorre cada modulo
    for modulo in modulos:
        #Crea 2 archivos .csv con el nombre del modulo
        with open(f'fuente_{modulo}.csv', "w") as archivo_fuente, open(f'comentarios_{modulo}.csv', "w") as archivo_comentarios:
            #Recorre funcion por funcion
            for nombre_funcion in nombres_funciones:
                #Si el modulo de la iteracion actual corresponde al modulo de la funcion de la iteracion actual:
                if modulo == datos[nombre_funcion]["modulo"]:
                    grabar_fuente_individual(archivo_fuente, nombre_funcion, datos[nombre_funcion]["parametros"], modulo, datos[nombre_funcion]["lineas"])
                    grabar_comentarios_individual(archivo_comentarios, nombre_funcion, "nombre_autor", "ayuda", datos[nombre_funcion]["comentarios"])

#EN CONSTRUCCION
def aparear_archivos(lista_archivos):
    archivo_apareado = open("fuente_unico.csv", "w")
    for archivo in lista_archivos:
        with open(archivo, "r") as archivo_individual:
            linea = archivo_individual.readline()

def main():
    archivo_principal = "programas.txt"
    datos, modulos = leer_programas(archivo_principal)
    nombres_archivos_fuente, nombres_archivos_comentarios = obtener_nombres_archivos(modulos)
    crear_archivos_csv(datos, modulos)

main()