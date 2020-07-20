import os
import m_analizar_linea as analizar
import m_grabar as grabar
import m_obtener as obtener

def leer_codigo(codigo, datos_ordenados, nombre_modulo, imports, bandera_funcion = False, bandera_comentario = False, bandera_ayuda = False, nombre_funcion = None):
    '''[Autor: Ivan Litteri]
    [Ayuda: Lee el codigo que le llega por parametro, lo analiza con distintas funciones y actualiza el 
    diccionario donde se guardan los datos analizados cada vez que se llama.]'''

    linea_codigo = codigo.readline().replace('"', "'")
    while linea_codigo:
        #Se habilita esta bandera cuando en el codigo a leer empieza una funcion, se deshabilita cuando termina o empieza otra.
        if bandera_funcion and not linea_codigo.startswith("def"):
            #Se habilita esta bandera cuando se detecta un comentario multilinea que no se cierra en la misma linea.
            if bandera_comentario:
                ayuda_funcion, bandera_ayuda = analizar.ayuda_funcion(linea_codigo, bandera_ayuda)
                datos_ordenados[nombre_funcion]["comentarios"]["ayuda"] += ayuda_funcion
                #Se deshabilita la bandera cuando se detecta que se cierra el comentario multilinea.
                if "'''" in linea_codigo:
                    bandera_comentario = False
            #Guarda otro tipo de comentarios
            elif "#" in linea_codigo:
                if not linea_codigo.startswith("#"):
                    #Si es None, cambia su valor a una lista vacia para que se pueda hacer append.
                    if datos_ordenados[nombre_funcion]["comentarios"]["otros"] == None:
                        datos_ordenados[nombre_funcion]["comentarios"]["otros"] = []
                    otro_comentario, posible_linea = analizar.comentario_numeral(linea_codigo)
                    datos_ordenados[nombre_funcion]["lineas"].append(f'"{posible_linea.strip()}"')
                    datos_ordenados[nombre_funcion]["comentarios"]["otros"].append(f'"{otro_comentario}"')
                else:
                    datos_ordenados[nombre_funcion]["comentarios"]["otros"].append(f'"{otro_comentario}"')
            #Si un comentario multilinea se abre y cierra en la misma linea, analiza la linea y guarda los datos del autor.
            elif linea_codigo.count("'''") == 2:
                autor_funcion = analizar.autor_funcion(linea_codigo)
                datos_ordenados[nombre_funcion]["comentarios"]["autor"] = autor_funcion
            #Si la linea empieza con un comentario multilinea, y no se cierra en la misma linea, se analiza esta primera linea que corresponde
            #al autor, y luego habilita la bandera de comentario multilinea para que se analicen las lineas siguientes hasta que se cierre
            #el comentario multilinea.
            elif linea_codigo.strip().startswith("'''"):
                bandera_comentario = True
                autor_funcion = analizar.autor_funcion(linea_codigo)
                datos_ordenados[nombre_funcion]["comentarios"]["autor"] = autor_funcion
            #Si ninguna linea es un comentario guarda la linea en lineas de codigo.
            else:
                if not linea_codigo.isspace():
                    datos_ordenados[nombre_funcion]["lineas"].append(f'"{linea_codigo.strip()}"')

        if linea_codigo.strip().startswith("return"):
            bandera_funcion = False
        if linea_codigo.startswith("def"):
            bandera_funcion = True
            nombre_funcion, parametros_funcion = analizar.declaracion_funcion(linea_codigo)
            datos_ordenados[nombre_funcion] = {"modulo": nombre_modulo, 
                                                "parametros": parametros_funcion, 
                                                "lineas": [], 
                                                "comentarios": {"autor": "", 
                                                                "ayuda": "",
                                                                "otros": None
                                                                }
                                                }
        #Almaceno las lineas de imports.
        if linea_codigo.startswith("import"):
            #Si el nombre del modulo no esta como key, entonces lo agrega (Esto ocurre una vez sola).
            if nombre_modulo not in imports:
                imports[nombre_modulo] = []
            imports[nombre_modulo].append(linea_codigo)
        #Lee la siguiente linea del codigo.
        linea_codigo = codigo.readline().replace('"', "'")

    #Devuelvo un diccionario de datos de todos los modulos, y uno de imports.
    return datos_ordenados, imports

def crear_archivos_csv_individuales(ubicaciones_modulos):
    '''[Autor: Ivan Litteri]
    [Ayuda: Abre el modulo con su ubicacion especifica (obtenida de el archivo principal) en forma de lectura, 
    el archivo fuente y comentario especifico del modulo, y en paralelo, analiza el codigo del modulo con la 
    funcion leer_codigo que devuelve un diccionario con los datos de los codigos, datos que luego se utilizan para 
    imprimirse de la forma que se pide sobre los archivos especificos del modulo. Una vez que termina de grabar 
    todo, cierra los archivos y repite.]'''

    datos_modulos = {}
    imports = {}

    #Recorro las ubicaciones de los modulos.
    for ubicacion_modulo in ubicaciones_modulos:
        #Nombre del modulo.
        nombre_modulo = ubicacion_modulo.split("\\")[-1]
        #Abre un archivo para leer y dos para escribir, al mismo tiempo.
        with open(ubicacion_modulo, "r") as codigo, open(f'fuente_{nombre_modulo}.csv', "w") as archivo_fuente, open(f'comentarios_{nombre_modulo}.csv', "w") as archivo_comentarios:
            datos_modulos, imports = leer_codigo(codigo, datos_modulos, nombre_modulo, imports)
            #Lista de nombres de funciones.
            nombres_funciones_ordenadas = sorted(list(datos_modulos.keys()))
            #Recorre funcion por funcion.
            for nombre_funcion in nombres_funciones_ordenadas:
                #Si el modulo de la iteracion actual corresponde al modulo de la funcion de la iteracion actual.
                if nombre_modulo == datos_modulos[nombre_funcion]["modulo"]:
                    grabar.fuente(archivo_fuente, nombre_funcion, datos_modulos[nombre_funcion]["parametros"], nombre_modulo, datos_modulos[nombre_funcion]["lineas"])
                    grabar.comentarios(archivo_comentarios, nombre_funcion, datos_modulos[nombre_funcion]["comentarios"])
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

def borrar_archivos_csv_individuales(nombres_archivos_csv_individuales):
    '''[Autor: Ivan Litteri]
    [Ayuda: Borra los archivos .csv individuales (que se encuentran en el repositorio actual) cuyas ubicaciones se obtienen 
    de una funcion a la que le llega por parametro los nombres de los archivos .csv individuales.]'''

    #Obtengo las ubicaciones y las recorro para borrar el archivo que se encuentra en ella.
    for ubicacion_archivo_csv_individual in obtener.ubicaciones_archivos_csv_individuales(nombres_archivos_csv_individuales):
        #Borro el archivo que se encuentra en esa ubicacion.
        os.remove(ubicacion_archivo_csv_individual)

def main(archivo_principal):
    '''[Autor: Ivan Litteri]'''

    #Crea los archivos csv individuales.
    ubicaciones_modulos = obtener.ubicaciones_modulos(archivo_principal)
    crear_archivos_csv_individuales(ubicaciones_modulos)

    #Aparea los archivos csv individuales en uno general.
    nombres_archivos_fuente, nombres_archivos_comentarios = obtener.nombres_archivos_csv_individuales(ubicaciones_modulos)
    aparear_archivos(nombres_archivos_fuente)
    aparear_archivos(nombres_archivos_comentarios)

    #Borra los archivos individuales.
    nombres_archivos_csv_individuales = nombres_archivos_fuente + nombres_archivos_comentarios
    borrar_archivos_csv_individuales(nombres_archivos_csv_individuales)