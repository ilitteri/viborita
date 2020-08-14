import m_analizar_linea as analizar_linea

def grabar_csv_individual(archivo, lineas):
    '''[Autor: Ivan Litteri]'''
    lineas_ordenadas = sorted(lineas, key=lambda x: x.lower())
    for linea in lineas_ordenadas:
        archivo.write(linea)

def guardar_comentario_multilinea(linea_codigo, datos_formateados):
    '''[Autor: Ivan Litteri]
    [Ayuda: le llega una linea en la que se abre un comentario multilinea, se analiza si este se cierra en la misma linea y lo guarada, sino levanta la bandera, guarda la linea y continua concatenando caracteres]'''

    #Esta declaracion cubre aquellos casos en el que el comentario empieza y termina en la misma linea
    if linea_codigo.count("'''") == 2:
        #Si "Autor" esta en esa linea entonces analiza y guarda al autor
        if "Autor" in linea_codigo:
            datos_formateados["autor"] = analizar_linea.autor_funcion(linea_codigo)
        #Si "Ayuda" esta en esa linea entonces analiza y guarda la ayuda
        elif "Ayuda" in linea_codigo:
            datos_formateados["ayuda"] = linea_codigo[4:-4]
        #Si no se trata del autor ni de la ayuda entonces es un comentario extra
        else:
            #Si hasta el momento la cadena de otros_comentario esta vacia, se iguala al comentario hallado
            if datos_formateados["comentarios"] == "":
                datos_formateados["comentarios"] = f'{linea_codigo.strip()}'
            #Si ya existia otro comentario en la cadena otros_comentarios entonces lo concatena
            else:
                datos_formateados["comentarios"] += f'","{linea_codigo.strip()}'
    #En caso de que no se trate de un comentario de triple comilla que empieza y termina en la misma linea
    else:
        #Levanta la bandera de comentario
        datos_formateados["bandera_comentario"] = True
        #Analiza el autor en caso de haberlo
        if "Autor" in linea_codigo:
            datos_formateados["autor"] = analizar_linea.autor_funcion(linea_codigo)

    return datos_formateados

def guardar_comentario_numeral(linea_codigo, datos_formateados):
    '''[Autor: Ivan Litteri]
    [Ayuda: le llega una linea que previamente fue catalogada como comentario, la analiza y guarda el comentario y posible linea de codigo en variables]'''

    #Se analiza la linea de comentario, y devuelve el comentario y la posible linea de codigo (en caso de que este la linea y luego de ella el comentario)
    comentario, linea = analizar_linea.comentario_numeral(linea_codigo)
    #Si hasta el momento la cadena de otros_comentario esta vacia, se iguala al comentario hallado
    if datos_formateados["comentarios"] == "":
        datos_formateados["comentarios"] = f'{comentario}'
    #Si ya existia otro comentario en la cadena otros_comentarios entonces lo concatena
    else:
        datos_formateados["comentarios"] += f'","{comentario}'
    #En caso de que se haya devuelto una linea en el analisis de la linea que contenia un comentario se agrega a las lineas de la funcion
    if linea:
        datos_formateados["lineas_funcion"] += f',"{linea}"'
    #Se apaga la bandera de comentario
    datos_formateados["bandera_comentario"] = False

    return datos_formateados

def resetear_por_inicio(linea_codigo, datos_formateados):
    '''[Autor: Ivan Litteri]
    [Ayuda: guarda la linea que le llega por parametro y resetea las variables y banderas]'''

    #Se declaran las banderas de comentarios y ayuda por si acaso (no se baja la bandera de funcion ya que se continua en una)
    datos_formateados["bandera_comentario"] = datos_formateados["bandera_ayuda"] =  False
    #Agrega un asterisco en el modulo principal, esto se usa luego para facilitar la deteccion de la funcion principal
    if datos_formateados["modulo"] == datos_formateados["modulo_principal"]:
        datos_formateados["lineas_fuente"].append(f'"{datos_formateados["funcion"]}","{datos_formateados["parametros"]}","*{datos_formateados["modulo"]}"{datos_formateados["lineas_funcion"]}\n')
    #Guarda la primera parte de la linea a grabar en el fuente correspondiente
    else:
        datos_formateados["lineas_fuente"].append(f'"{datos_formateados["funcion"]}","{datos_formateados["parametros"]}","{datos_formateados["modulo"]}"{datos_formateados["lineas_funcion"]}\n')
    datos_formateados["lineas_comentarios"].append(f'"{datos_formateados["funcion"]}","{datos_formateados["autor"]}","{datos_formateados["ayuda"]}","{datos_formateados["comentarios"]}"\n')
    #Se reinician las variables que acumulan la informacion de las lineas de la funcion para que comiencen de cero
    datos_formateados["autor"] = datos_formateados["ayuda"] = datos_formateados["comentarios"] = datos_formateados["lineas_funcion"] = ""
    #Se obtiene la informacion de la linea de declaracion de funcion
    datos_formateados["funcion"], datos_formateados["parametros"] = analizar_linea.declaracion_funcion(linea_codigo)

    return datos_formateados

def analizar_linea_funcion(linea_codigo, datos_formateados):
    '''[Autor: Ivan Litteri]
    [Ayuda: Analiza las lineas que previamente se catalogaron como dentro de una funcion, y les da formato para el csv]'''

    #Analiza las lineas sabiendo que se encuentran dentro de un comentarios de tres comillas cuando esta bandera esta en True
    if datos_formateados["bandera_comentario"]:
        #Si en la linea de comentario esta la cadena "Ayuda" y ademas la bandera de ayuda es False
        if "Ayuda" in linea_codigo and not datos_formateados["bandera_ayuda"]:
            #Analiza la linea de ayuda desde que empieza ("[") hasta que termina ("]") y obtendo la linea de ayuda (que se va concatenando) y la bandera de ayuda que indica si debe seguir concatenando o si ya se termino el comentarios de ayuda
            datos_formateados["ayuda"], datos_formateados["bandera_ayuda"] = analizar_linea.ayuda_funcion(linea_codigo, datos_formateados["bandera_ayuda"])
        elif datos_formateados["bandera_ayuda"]:
            nueva_linea_ayuda, datos_formateados["bandera_ayuda"] = analizar_linea.ayuda_funcion(linea_codigo, datos_formateados["bandera_ayuda"])
            datos_formateados["ayuda"] += nueva_linea_ayuda
        #Las banderas de comentario y ayuda se "bajan" en caso de que se detecte que se termina el comentario de triple comilla
        if "'''\n" in linea_codigo or '"""\n' in linea_codigo:
            datos_formateados["bandera_comentario"] = False
            datos_formateados["bandera_ayuda"] = False
    #Esa declaracion cubre aquellos casos en los que una funcion no dispone de return para indicar que se termino
    elif linea_codigo[0:3] == "def":
        datos_formateados = resetear_por_inicio(linea_codigo, datos_formateados)
    #Esta declaracion detecta si hay un numeral en la linea, pero lo analiza como comentario si y solo si el formato es correcto
    elif "#" in linea_codigo and not("'#" in linea_codigo or "('#" in linea_codigo) and "#todo" not in linea_codigo:
        datos_formateados = guardar_comentario_numeral(linea_codigo, datos_formateados)
    #Si se comienza un comentario de triple comilla
    elif linea_codigo.strip().startswith("'''["):
        datos_formateados = guardar_comentario_multilinea(linea_codigo, datos_formateados)
    #Si pasa todas las interrogacones y llega aca, significa que se trata de una linea de codigo corriente
    else:
        #Esta declaracion filtra a las lineas fuera de funcion
        if linea_codigo[0].isalpha():
            datos_formateados["lineas_fuera_funcion"].append(linea_codigo.strip())
        #Esta declaracion concatena aquellas lineas de codigo no vacias
        elif linea_codigo.strip() != "":
            datos_formateados["lineas_funcion"] += f',"{linea_codigo.strip()}"'
    
    return datos_formateados

def formatear_declaracion_funcion(linea_codigo, datos_formateados):
    '''[Autor: Ivan Litteri]
    [Ayuda: Analiza las lineas que previamente se catalogaron como declaracion de funcion, y les da formato para el csv]'''

    #Se levanta la bandera de funcion
    datos_formateados["bandera_funcion"] = True
    #Se bajan las banderas de comentario y ayuda en caso de que hayan quedado levantadas
    datos_formateados["bandera_comentario"] = datos_formateados["bandera_ayuda"] = False
    #Se analiza la linea de declaracion
    datos_formateados["funcion"], datos_formateados["parametros"] = analizar_linea.declaracion_funcion(linea_codigo)

    return datos_formateados

def analizar_linea_modulo(linea_codigo, datos_formateados):
    '''[Autor: Ivan Litteri]
    [Ayuda: analiza la linea que le llega por parametro y la separa segun si es linea de codigo, o comentario, o ayuda de funcion o autor, y guarda esta informacion]'''

    #Analiza las lineas sabiendo que se encuentran dentro de una funcion cuando esta bandera esta en True
    if datos_formateados["bandera_funcion"]:
        #formatea la linea de funcion
        datos_formateados = analizar_linea_funcion(linea_codigo, datos_formateados)
    #Si no esta la bandera de funcion levantada y la linea leida se trata de la declaracion de una funcion
    elif linea_codigo[0:3] == "def":
        #Formatea la linea de declaracion de funcion
        datos_formateados = formatear_declaracion_funcion(linea_codigo, datos_formateados)
    #Si no esta levantada la bandera de funcion y la linea no es una que declara una funcion entonces se trata de una linea que esta fuera de funcion
    else:
        #Guarda la linea fuera de funcion
        datos_formateados["lineas_fuera_funcion"].append(linea_codigo.strip())
        #Baja las banderas de comentarios y ayuda en caso de que hayan quedado levantadas
        datos_formateados["bandera_comentario"] = datos_formateados["bandera_ayuda"] = False

    return datos_formateados

def leer_modulo(archivo_modulo, modulo, info_ubicaciones, lineas_fuera_funcion):
    '''[Autor: Ivan Litteri]
    [Ayuda: lee las lineas del modulo que le es pasado por parametro, y formatea sus datos (luego de ser analizados) para la grabacion de su csv correspondiente]'''
    
    datos_formateados = {"lineas_fuente": [],
                    "lineas_comentarios": [],
                    "bandera_funcion": False,
                    "bandera_comentario": False,
                    "bandera_ayuda": False,
                    "funcion": "",
                    "parametros": "",
                    "modulo": modulo,
                    "lineas_funcion": "",
                    "autor": "",
                    "ayuda": "",
                    "comentarios": "",
                    "modulo_principal": info_ubicaciones[0][1],
                    "lineas_fuera_funcion": lineas_fuera_funcion
                    }

    #Carga la primera linea del archivo y reemplaza las comillas dobles por simples
    linea_codigo = archivo_modulo.readline().replace('"', "'")

    #Analiza las lineas mientras existan en el archivo
    while linea_codigo:
        #Analiza las lineas y obtiene los datos formateados
        datos_formateados = analizar_linea_modulo(linea_codigo, datos_formateados)
        #Carga la siguiente linea del archivo y reemplaza las comillas dobles por simples
        linea_codigo = archivo_modulo.readline().replace('"', "'")
    
    #Esta declaracion cubre los casos en el que la ultima de funcion del modulo leido no tiene return, entonces guarda esa ultima linea que no se guardo en el analisis
    if f'"{datos_formateados["funcion"]}","{datos_formateados["autor"]}","{datos_formateados["ayuda"]}","{datos_formateados["comentarios"]}"\n' != '"","","",""\n':
        datos_formateados["lineas_comentarios"].append(f'"{datos_formateados["funcion"]}","{datos_formateados["autor"]}","{datos_formateados["ayuda"]}","{datos_formateados["comentarios"]}"\n')
    #Agrega un enter en aquellas lineas que no lo tienen
    if f'"{datos_formateados["funcion"]}","{datos_formateados["parametros"]}","{datos_formateados["modulo"]}"{datos_formateados["lineas_funcion"]}\n' != '"","","",""\n':
        datos_formateados["lineas_fuente"].append(f'"{datos_formateados["funcion"]}","{datos_formateados["parametros"]}","*{datos_formateados["modulo"]}","{datos_formateados["lineas_funcion"]}"\n')
    
    #Devuelve las lineas a grabar y la lista de lineas de fuera de funcion
    return datos_formateados["lineas_fuente"], datos_formateados["lineas_comentarios"], datos_formateados["lineas_fuera_funcion"]
    
def crear_csv_individuales(info_ubicaciones):
    '''[Autor: Ivan Litteri]'''

    archivos_fuente = [] #Lista de nombres de archivos fuente_csv
    archivos_comentarios = [] #Lista de nombres de archivos comentarios_csv
    lineas_fuera_funcion = []
    
    #Recorre la informacion de las ubicaciones de la forma: (ubicacion, nombre_modulo)
    for ubicacion, nombre_modulo in info_ubicaciones:
        #Abre el archivo de la ubicacion y crea los fuente y comentarios csv de ese modulo abierto
        with open(ubicacion, "r", encoding='utf-8') as archivo_modulo, open(f'fuente_{nombre_modulo}.csv', "w") as archivo_fuente, open(f'comentarios_{nombre_modulo}.csv', "w") as archivo_comentarios:
            #Lee las lineas, las analiza y formatea y obtiene las lineas a grabar
            lineas_fuente, lineas_comentarios, lineas_fuera_funcion = leer_modulo(archivo_modulo, nombre_modulo, info_ubicaciones, lineas_fuera_funcion)
            #Graba los csv individuales (fuente y comentarios)
            grabar_csv_individual(archivo_fuente, lineas_fuente)
            grabar_csv_individual(archivo_comentarios, lineas_comentarios)
            #Guarda el nombre de los archivos en listas
            archivos_fuente.append(f'fuente_{nombre_modulo}.csv')
            archivos_comentarios.append(f'comentarios_{nombre_modulo}.csv')

    return archivos_fuente, archivos_comentarios, lineas_fuera_funcion