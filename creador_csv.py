def leer_archivo_principal(archivo_principal):
    '''
    Lee el archivo principal que le llega por parametro (en nuestro caso el .txt), y retorna una lista con las lineas 
    de ese archivo (en este caso cada linea corresponde a las ubicaciones de los archivos de la aplicacion a a anlizar).
    '''
    with open(archivo_principal, "r") as archivo:
        lineas = archivo.read().splitlines()
    return lineas

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
    ubicaciones = leer_archivo_principal(archivo_principal)
    #Ubicacion del modulo principal
    u_programa_principal = ubicaciones[0]
    datos_programas = {}

    #Recorre la lista de ubicaciones de cada archivo de la aplicacion
    for ubicacion in ubicaciones:
        #Nombre del modulo
        nombre_modulo = ubicacion.split("\\")[-1]
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
    return datos_programas

def guardar_datos():
    '''
    Imprime los datos en un archivo .csv que creamon en la misma. Los datos se imprimen en la forma que se pide en
    la consigna.
    Se crea un archivo de fuente y un archivo de comentarios, para cada archivo analizado en la funcion anterior
    '''
    #Diccionario con los datos de todos los programas
    datos = leer_programas("programas.txt")
    #Lista de nombres de funciones
    nombres_funciones = list(datos.keys())
    #Lista de todos los modulos
    modulos = list(set([datos[nombre_funcion]["modulo"] for nombre_funcion in nombres_funciones]))
    #Recorre cada modulo
    for modulo in modulos:
        #Crea 2 archivos .csv con el nombre del modulo
        with open(f'fuente_{modulo}.csv', "w") as archivo_fuente, open(f'comentarios_{modulo}.csv', "w") as archivo_comentarios:
            #Recorre funcion por funcion
            for nombre_funcion in nombres_funciones:
                #Si el modulo de la iteracion actual corresponde al modulo de la funcion de la iteracion actual:
                if modulo == datos[nombre_funcion]["modulo"]:
                    #Parametros de la funcion
                    parametros = datos[nombre_funcion]["parametros"]
                    #Lista de lineas de la funcion
                    lineas = datos[nombre_funcion]["lineas"]
                    #Imprime una linea del .csv fuente correspondiente al modulo
                    archivo_fuente.write(f'{nombre_funcion},{parametros},{modulo},{",".join(repr(linea) for linea in lineas)}\n')
                    #Si la funcion tiene comentarios:
                    if len(datos[nombre_funcion]["comentarios"]) > 0:
                        #Escribe una linea en el .csv de comentarios correspondiente al modulo
                        archivo_comentarios.write(f'{nombre_funcion},nombre de autor,ayuda,{datos[nombre_funcion]["comentarios"]}\n')


def main():
    print("¡Binevenido!\nEste programa consta en analizar y evaluar programas escritos en Python\n")
    guardar_datos()

    bandera = True
    while bandera:
        print("Menú de interacción\n1. Panel general de funciones\n2. Consulta de funciones\n3. Analizador de reutilización de codigo\n4. Arbol de invocación\n5. Información por desarrollador\n6. Salir")

        opcion = input("Ingrese una opcion:")
        if opcion == "1":
            print("Aca va el punto 1\n")
        elif opcion == "2":
            print("Aca va el punto 2\n")
        elif opcion == "3":
            print("Aca va el punto 3\n")
        elif opcion == "4":
            print("Aca va el punto 4\n")
        elif opcion == "5":
            print("Aca va el punto 5\n")
        elif opcion == "6":
            print("\nGracias, vuelva pronto!")
            bandera = False
        else:
            print("\n¡LA OPCION INGRESADA ES INCORRECTA!\n")

main()