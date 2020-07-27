import m_analizar_linea as analizar_linea
import m_obtener as obtener

def grabar_csv_individual(archivo, lineas):
    '''[Autor: Ivan Litteri]'''
    for linea in lineas:
        archivo.write(linea)

def guardar_comentario_multilinea(linea_codigo, banderas, info_lineas):
    '''[Autor: Ivan Litteri]
    [Ayuda: le llega una linea en la que se abre un comentario multilinea, se analiza si este se cierra en la misma linea y lo guarada, sino levanta la bandera, guarda la linea y continua concatenando caracteres]'''

    #Esta declaracion cubre aquellos casos en el que el comentario empieza y termina en la misma linea
    if linea_codigo.count("'''") == 2:
        #Si "Autor" esta en esa linea entonces analiza y guarda al autor
        if "Autor" in linea_codigo:
            info_lineas[1] = analizar_linea.autor_funcion(linea_codigo)
        #Si "Ayuda" esta en esa linea entonces analiza y guarda la ayuda
        elif "Ayuda" in linea_codigo:
            info_lineas[2] = linea_codigo[4:-4]
        #Si no se trata del autor ni de la ayuda entonces es un comentario extra
        else:
            #Si hasta el momento la cadena de otros_comentario esta vacia, se iguala al comentario hallado
            if info_lineas[3] == "":
                info_lineas[3] = f'{coment}'
            #Si ya existia otro comentario en la cadena otros_comentarios entonces lo concatena
            else:
                info_lineas[3] += f'","{coment}'
    #En caso de que no se trate de un comentario de triple comilla que empieza y termina en la misma linea
    else:
        #Levanta la bandera de comentario
        banderas[1] = True
        #Analiza el autor en caso de haberlo
        if "Autor" in linea_codigo:
            info_lineas[1] = analizar_linea.autor_funcion(linea_codigo)

    return banderas, info_lineas

def guardar_comentario_numeral(linea_codigo, cadenas, banderas, info_lineas):
    '''[Autor: Ivan Litteri]
    [Ayuda: le llega una linea que previamente fue catalogada como comentario, la analiza y guarda el comentario y posible linea de codigo en variables]'''

    #Se analiza la linea de comentario, y devuelve el comentario y la posible linea de codigo (en caso de que este la linea y luego de ella el comentario)
    coment, seudo_line = analizar_linea.comentario_numeral(linea_codigo)
    #Si hasta el momento la cadena de otros_comentario esta vacia, se iguala al comentario hallado
    if info_lineas[3] == "":
        info_lineas[3] = f'{coment}'
    #Si ya existia otro comentario en la cadena otros_comentarios entonces lo concatena
    else:
        info_lineas[3] += f'","{coment}'
    #En caso de que se haya devuelto una linea en el analisis de la linea que contenia un comentario se agrega a las lineas de la funcion
    if seudo_line:
        cadenas[0] += f',"{seudo_line}"'
    #Se apaga la bandera de comentario
    banderas[1] = False

    return cadenas, banderas, info_lineas

def resetear_por_inicio(linea_codigo, nombre_modulo, lineas_a_grabar, cadenas, banderas, info_lineas, info_ubicaciones):
    '''[Autor: Ivan Litteri]
    [Ayuda: guarda la linea que le llega por parametro y resetea las variables y banderas]'''

    #Se declaran las banderas de comentarios y ayuda por si acaso (no se baja la bandera de funcion ya que se continua en una)
    banderas[1] = banderas[2] =  False
    #Se agrega a la lista de lineas a grabar la informacion acumulada hasta el momento 
    lineas_a_grabar[0].append(cadenas[0]+"\n")
    lineas_a_grabar[1].append(f'"{info_lineas[0]}","{info_lineas[1]}","{info_lineas[2]}","{info_lineas[3]}"\n')
    #Se reinician las variables que acumulan la informacion de las lineas de la funcion para que comiencen de cero
    cadenas[0] = cadenas[1] = info_lineas[1] = info_lineas[2] = info_lineas[3] = ""
    #Se obtiene la informacion de la linea de declaracion de funcion
    info_lineas[0], param = analizar_linea.declaracion_funcion(linea_codigo)
    #Agrega un asterisco en el modulo principal, esto se usa luego para facilitar la deteccion de la funcion principal
    if nombre_modulo == info_ubicaciones[0][1]:
        cadenas[0] += f'"{info_lineas[0]}","{param}","*{nombre_modulo}"'
    #Guarda la primera parte de la linea a grabar en el fuente correspondiente
    else:
        cadenas[0] += f'"{info_lineas[0]}","{param}","{nombre_modulo}"'

    return lineas_a_grabar, cadenas, banderas, info_lineas

def resetear_por_fin(linea_codigo, lineas_a_grabar, cadenas, banderas, info_lineas):
    '''[Autor: Ivan Litteri]
    [Ayuda: guarda la linea que le llega por parametro y resetea las variables y banderas]'''

    #Se bajan las banderas de funcion, comentario, ayuda
    banderas[0] = banderas[1] = banderas[2] =  False
    #Se guarda la linea en la que se encuentra en el return como ultima linea de la funcion leida hasta el momento
    cadenas[0] += f',"{linea_codigo.strip()}"'
    #Se añaden las lineas a las listas de lineas a grabar
    lineas_a_grabar[0].append(cadenas[0]+"\n")
    lineas_a_grabar[1].append(f'"{info_lineas[0]}","{info_lineas[1]}","{info_lineas[2]}","{info_lineas[3]}"\n')  
    #Se reinician las variables que acumulan la informacion de las lineas de la funcion para que comiencen de cero
    cadenas[0] = cadenas[1] = info_lineas[0] = info_lineas[1] = info_lineas[2] = info_lineas[3] = ""

    return lineas_a_grabar, cadenas, banderas, info_lineas

def analizar_linea_funcion(linea_codigo, nombre_modulo, info_ubicaciones, lineas_a_grabar, banderas, cadenas, info_lineas, lineas_fuera_funcion):
    '''[Autor: Ivan Litteri]
    [Ayuda: Analiza las lineas que previamente se catalogaron como dentro de una funcion, y les da formato para el csv]'''

    #Analiza las lineas sabiendo que se encuentran dentro de un comentarios de tres comillas cuando esta bandera esta en True
    if banderas[1]:
        #Si en la linea de comentario esta la cadena "Ayuda" y ademas la bandera de ayuda es False
        if "Ayuda" in linea_codigo and not banderas[2]:
            #Analiza la linea de ayuda desde que empieza ("[") hasta que termina ("]") y obtendo la linea de ayuda (que se va concatenando) y la bandera de ayuda que indica si debe seguir concatenando o si ya se termino el comentarios de ayuda
            info_lineas[2], banderas[2] = analizar_linea.ayuda_funcion(linea_codigo, banderas[2])
        #Las banderas de comentario y ayuda se "bajan" en caso de que se detecte que se termina el comentario de triple comilla
        if "'''\n" in linea_codigo or '"""\n' in linea_codigo:
            banderas[1] = False
            banderas[2] = False
    #Esa declaracion cubre aquellos casos en los que una funcion no dispone de return para indicar que se termino
    elif linea_codigo[0:3] == "def":
        lineas_a_grabar, cadenas, banderas, info_lineas = resetear_por_inicio(linea_codigo, nombre_modulo, lineas_a_grabar, cadenas, banderas, info_lineas, info_ubicaciones)
    #Esta declaracion detecta que una funcion termina en el return
    elif linea_codigo.strip().startswith("return"):
        lineas_a_grabar, cadenas, banderas, info_lineas = resetear_por_fin(linea_codigo, lineas_a_grabar, cadenas, banderas, info_lineas)
    #Esta declaracion detecta si hay un numeral en la linea, pero lo analiza como comentario si y solo si el formato es correcto
    elif "#" in linea_codigo and not("'#" in linea_codigo or "('#" in linea_codigo) and "#todo" not in linea_codigo:
        cadenas, banderas, info_lineas = guardar_comentario_numeral(linea_codigo, cadenas, banderas, info_lineas)
    #Si se comienza un comentario de triple comilla
    elif linea_codigo.strip().startswith("'''["):
        banderas, info_lineas = guardar_comentario_multilinea(linea_codigo, banderas, info_lineas)
    #Si pasa todas las interrogacones y llega aca, significa que se trata de una linea de codigo corriente
    else:
        #Esta declaracion filtra a las lineas fuera de funcion
        if linea_codigo[0].isalpha():
            lineas_fuera_funcion.append(linea_codigo.strip())
        #Esta declaracion concatena aquellas lineas de codigo no vacias
        elif linea_codigo.strip() != "":
            cadenas[0] += f',"{linea_codigo.strip()}"'
    
    return lineas_a_grabar, banderas, cadenas, info_lineas, lineas_fuera_funcion

def formatear_declaracion_funcion(linea_codigo, nombre_modulo, cadenas, banderas, info_lineas, info_ubicaciones):
    '''[Autor: Ivan Litteri]
    [Ayuda: Analiza las lineas que previamente se catalogaron como declaracion de funcion, y les da formato para el csv]'''

    #Se levanta la bandera de funcion
    banderas[0] = True
    #Se bajan las banderas de comentario y ayuda en caso de que hayan quedado levantadas
    banderas[1] = banderas[2] = False
    #Se analiza la linea de declaracion
    info_lineas[0], param = analizar_linea.declaracion_funcion(linea_codigo)
    #Agrega un asterisco en el modulo principal, esto se usa luego para facilitar la deteccion de la funcion principal
    if nombre_modulo == info_ubicaciones[0][1]:
        cadenas[0] += f'"{info_lineas[0]}","{param}","*{nombre_modulo}"'
    #Guarda la primera parte de la linea a grabar en el fuente correspondiente
    else:
        cadenas[0] += f'"{info_lineas[0]}","{param}","{nombre_modulo}"'

    return cadenas, banderas, info_lineas, info_ubicaciones

def analizar_linea_modulo(linea_codigo, nombre_modulo, info_ubicaciones, lineas_a_grabar, banderas, cadenas, info_lineas, lineas_fuera_funcion):
    '''[Autor: Ivan Litteri]
    [Ayuda: analiza la linea que le llega por parametro y la separa segun si es linea de codigo, o comentario, o ayuda de funcion o autor, y guarda esta informacion]'''

    #Analiza las lineas sabiendo que se encuentran dentro de una funcion cuando esta bandera esta en True
    if banderas[0]:
        #formatea la linea de funcion
        lineas_a_grabar, banderas, cadenas, info_lineas, lineas_fuera_funcion = analizar_linea_funcion(linea_codigo, nombre_modulo, info_ubicaciones, lineas_a_grabar, banderas, cadenas, info_lineas, lineas_fuera_funcion)
    #Si no esta la bandera de funcion levantada y la linea leida se trata de la declaracion de una funcion
    elif linea_codigo[0:3] == "def":
        #Formatea la linea de declaracion de funcion
        cadenas, banderas, info_lineas, info_ubicaciones = formatear_declaracion_funcion(linea_codigo, nombre_modulo, cadenas, banderas, info_lineas, info_ubicaciones)
    #Si no esta levantada la bandera de funcion y la linea no es una que declara una funcion entonces se trata de una linea que esta fuera de funcion
    else:
        #Guarda la linea fuera de funcion
        lineas_fuera_funcion.append(linea_codigo.strip())
        #Baja las banderas de comentarios y ayuda en caso de que hayan quedado levantadas
        banderas[1] = banderas[2] = False

    return lineas_a_grabar, banderas, cadenas, info_lineas, lineas_fuera_funcion

def leer_modulo(archivo_modulo, nombre_modulo, info_ubicaciones, lineas_fuera_funcion):
    '''[Autor: Ivan Litteri]
    [Ayuda: lee las lineas del modulo que le es pasado por parametro, y formatea sus datos (luego de ser analizados) para la grabacion de su csv correspondiente]'''

    lineas_a_grabar = [[],[]] #Lista de listas de lineas a grabar
    banderas = [False, False, False] #Lista de banderas de funcion, comentario y ayuda
    cadenas = ["",""] #Lista de cadenas a formatear
    info_lineas = ["", "", "", ""] #lista de cadenas a guardar informacion

    #Carga la primera linea del archivo y reemplaza las comillas dobles por simples
    linea_codigo = archivo_modulo.readline().replace('"', "'")

    #Analiza las lineas mientras existan en el archivo
    while linea_codigo:
        #Analiza las lineas y obtiene los datos formateados
        lineas_a_grabar, banderas, cadenas, info_lineas, lineas_fuera_funcion = analizar_linea_modulo(linea_codigo, nombre_modulo, info_ubicaciones, lineas_a_grabar, banderas, cadenas, info_lineas, lineas_fuera_funcion)
        #Carga la siguiente linea del archivo y reemplaza las comillas dobles por simples
        linea_codigo = archivo_modulo.readline().replace('"', "'")
    
    #Esta declaracion cubre los casos en el que la ultima de funcion del modulo leido no tiene return, entonces guarda esa ultima linea que no se guardo en el analisis
    if f'"{info_lineas[0]}","{info_lineas[1]}","{info_lineas[2]}","{info_lineas[3]}"\n' != '"","","",""\n':
        lineas_a_grabar[1].append(f'"{info_lineas[0]}","{info_lineas[1]}","{info_lineas[2]}","{info_lineas[3]}"\n')
    #Agrega un enter en aquellas lineas que no lo tienen
    if cadenas[0] != "":
        lineas_a_grabar[0].append(cadenas[0]+"\n")
    
    #Devuelve las lineas a grabar y la lista de lineas de fuera de funcion
    return lineas_a_grabar, lineas_fuera_funcion
    

def crear_csv_individuales(info_ubicaciones):
    '''[Autor: Ivan Litteri]'''

    archivos_fuente = [] #Lista de nombres de archivos fuente_csv
    archivos_comentarios = [] #Lista de nombres de archivos comentarios_csv
    lineas_fuera_funcion = [] #Lista de lineas fuera de funcion
    
    #Recorre la informacion de las ubicaciones de la forma: (ubicacion, nombre_modulo)
    for ubicacion, nombre_modulo in info_ubicaciones:
        #Abre el archivo de la ubicacion y crea los fuente y comentarios csv de ese modulo abierto
        with open(ubicacion, "r", encoding='utf-8') as archivo_modulo, open(f'fuente_{nombre_modulo}.csv', "w") as archivo_fuente, open(f'comentarios_{nombre_modulo}.csv', "w") as archivo_comentarios:
            #Lee las lineas, las analiza y formatea y obtiene las lineas a grabar
            lineas_a_grabar, lineas_fuera_funcion = leer_modulo(archivo_modulo, nombre_modulo, info_ubicaciones, lineas_fuera_funcion)
            #Graba los csv individuales (fuente y comentarios)
            grabar_csv_individual(archivo_fuente, lineas_a_grabar[0])
            grabar_csv_individual(archivo_comentarios, lineas_a_grabar[1])
            #Guarda el nombre de los archivos en listas
            archivos_fuente.append((f'fuente_{nombre_modulo}.csv', nombre_modulo))
            archivos_comentarios.append((f'comentarios_{nombre_modulo}.csv', nombre_modulo))

    return archivos_fuente, archivos_comentarios, lineas_fuera_funcion