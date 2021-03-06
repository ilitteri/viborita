############################################################################
'''CSV INDIVIDUALES FINALES Y MERGE VERSION 1'''
############################################################################
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

############################################################################
'''CSV INDIVIDUALES VERSION 2'''
############################################################################
import m_analizar_linea as analizar_linea
import m_obtener as obtener
import m_grabar as grabar

def analizar_linea_codigo(linea_codigo, ubicacion, nombre_modulo, ubicaciones, datos_fuente, datos_comentarios, linea_fuente, linea_comentarios, autor, ayuda, otros_comentarios, lineas_fuera_funcion, bandera_funcion, bandera_comentario, bandera_ayuda, contador_def):
    '''[Autor: Ivan Litteri]'''

    if linea_codigo[0:3] == "def":
        bandera_funcion = True
        contador_def += 1
        if contador_def > 1:
            linea_fuente += "\n"
            linea_comentarios += f',"{autor}","{ayuda}","{otros_comentarios}"\n'
            datos_fuente.append(linea_fuente)
            datos_comentarios.append(linea_comentarios)
            linea_fuente = linea_comentarios = autor = ayuda = otros_comentarios = ""
        else:
            datos_comentarios = []
            datos_fuente = []
        funcion, parametros = analizar_linea.declaracion_funcion(linea_codigo)
        if ubicacion == ubicaciones[0][0]:
            linea_fuente += f'"{funcion}","{parametros}","*{nombre_modulo}"'
        else:
            linea_fuente += f'"{funcion}","{parametros}","{nombre_modulo}"'
        linea_comentarios += f'"{funcion}"'
    elif bandera_funcion:
        if "return" in linea_codigo:
            linea_fuente += f',"{linea_codigo.strip()}"'
            bandera_funcion = False
        else:
            if bandera_comentario:
                ayuda_funcion, bandera_ayuda = analizar_linea.ayuda_funcion(linea_codigo, bandera_ayuda)
                ayuda += f'{ayuda_funcion}'
                if "'''" in linea_codigo or '"""' in linea_codigo:
                    bandera_comentario = False
            elif "#" in linea_codigo:
                comentario, linea = analizar_linea.comentario_numeral(linea_codigo)
                otros_comentarios += f'{comentario}'
                if linea.strip() != "":
                    linea_fuente += f',"{linea}",'
            elif "'''" in linea_codigo or '"""' in linea_codigo:
                if linea_codigo.count("'''") == 2 or linea_codigo.count('"""') == 2:
                    bandera_comentario = False
                    if "Autor" in linea_codigo:
                        autor += f'{analizar_linea.autor_funcion(linea_codigo)}'
                    elif "Ayuda" in linea_codigo:
                        ayuda += f'{linea_codigo[4:-4]}'
                    else:
                        otros_comentarios += f'{linea_codigo[3:-3]}'
                else:
                    bandera_comentario = True
                    autor += f'{analizar_linea.autor_funcion(linea_codigo)}'
            elif linea_codigo.strip() != "":
                linea_fuente += f',"{linea_codigo.strip()}"'
    else:
        lineas_fuera_funcion.append(linea_codigo.strip())
    
    return datos_fuente, datos_comentarios, linea_fuente, linea_comentarios, autor, ayuda, otros_comentarios, lineas_fuera_funcion, bandera_funcion, bandera_comentario, bandera_ayuda, contador_def

def leer_lineas_codigo(codigo, ubicacion, nombre_modulo, ubicaciones, datos_fuente=[], datos_comentarios=[], linea_fuente="", linea_comentarios="", autor="", ayuda="", otros_comentarios="", lineas_fuera_funcion=[], bandera_funcion=False, bandera_comentario=False, bandera_ayuda=False, contador_def=0):
    '''[Autor: Ivan Litteri]'''

    linea_codigo = codigo.readline().replace('"', "'")
    while linea_codigo:
        datos_fuente, datos_comentarios, linea_fuente, linea_comentarios, autor, ayuda, otros_comentarios, lineas_fuera_funcion, bandera_funcion, bandera_comentario, bandera_ayuda, contador_def =analizar_linea_codigo(linea_codigo, ubicacion, nombre_modulo, ubicaciones, datos_fuente, datos_comentarios, linea_fuente, linea_comentarios, autor, ayuda, otros_comentarios, lineas_fuera_funcion, bandera_funcion, bandera_comentario, bandera_ayuda, contador_def)
        linea_codigo = codigo.readline().replace('"', "'")
    linea_comentarios += f',"{autor}","{ayuda}","{otros_comentarios}"\n'
    linea_fuente += "\n"
    datos_comentarios.append(linea_comentarios)
    datos_fuente.append(linea_fuente)

    return datos_fuente, datos_comentarios, lineas_fuera_funcion

def ordenar_datos(datos):
    '''[Autor: Ivan Litteri]'''
    return sorted(datos)

def crear_csv_individuales(ubicaciones):
    '''[Autor: Ivan Litteri]'''

    archivos_fuente = []
    archivos_comentarios = []
    for ubicacion, nombre_modulo in ubicaciones:
        with open(f'fuente_{nombre_modulo}.csv', "w") as fuente_modulo, open(f'comentarios_{nombre_modulo}.csv', "w") as comentarios_modulo, open(ubicacion, "r", encoding='utf-8') as codigo:
            datos_fuente, datos_comentarios, lineas_fuera_funcion = leer_lineas_codigo(codigo, ubicacion, nombre_modulo, ubicaciones)
            #Ordena las lineas a grabar en forma alfabetica
            datos_fuente_ordenados = sorted(datos_fuente)
            datos_comentarios_ordenados = sorted(datos_comentarios)
            #Graba los datos en los archivos
            grabar.cadenas(fuente_modulo, datos_fuente_ordenados)
            grabar.cadenas(comentarios_modulo, datos_comentarios_ordenados)
            #Guarda el nombre de los archivos en listas
            archivos_fuente.append((f'fuente_{nombre_modulo}.csv', nombre_modulo))
            archivos_comentarios.append((f'comentarios_{nombre_modulo}.csv', nombre_modulo))
    
    return archivos_fuente, archivos_comentarios, lineas_fuera_funcion

def obtener_csv_individuales(nombre_archivo):
    '''[Autor: Ivan Litteri]'''
    
    ubicaciones = obtener.ubicaciones_modulos(nombre_archivo)
    archivos_fuente, archivos_comentarios, lineas_fuera_funcion = crear_csv_individuales(ubicaciones)

    return archivos_fuente, archivos_comentarios, lineas_fuera_funcion