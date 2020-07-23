import platform
import os
import m_analizar_linea as analizar_linea

def analizar_archivo_programas(nombre_archivo):
    ubicaciones = []
    os = platform.system()
    with open(nombre_archivo, "r") as archivo_programas:
        ubicacion = archivo_programas.readline().strip()
        while ubicacion:
            if os == "Linux" or os == "Darwin":
                ubicaciones.append((ubicacion, ubicacion.split("/")[-1]))
            elif os == "Windows":
                ubicaciones.append((ubicacion, ubicacion.split("\\")[-1]))
            ubicacion = archivo_programas.readline().strip()

    return ubicaciones

def analizar_linea_codigo(linea_codigo, ubicacion, nombre_modulo, ubicaciones, datos_fuente, datos_comentarios, linea_fuente, linea_comentarios, autor, ayuda, otros_comentarios, lineas_fuera_funcion, bandera_funcion, bandera_comentario, bandera_ayuda, contador_def):
    if linea_codigo[0:3] != "def" and linea_codigo[0:3] != "   " and linea_codigo != "\n":
            lineas_fuera_funcion.append(linea_codigo)
    elif linea_codigo[0:3] == "def":
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

    linea_codigo = codigo.readline().replace('"', "'")
    while linea_codigo:
        datos_fuente, datos_comentarios, linea_fuente, linea_comentarios, autor, ayuda, otros_comentarios, lineas_fuera_funcion, bandera_funcion, bandera_comentario, bandera_ayuda, contador_def =analizar_linea_codigo(linea_codigo, ubicacion, nombre_modulo, ubicaciones, datos_fuente, datos_comentarios, linea_fuente, linea_comentarios, autor, ayuda, otros_comentarios, lineas_fuera_funcion, bandera_funcion, bandera_comentario, bandera_ayuda, contador_def)
        linea_codigo = codigo.readline().replace('"', "'")
    linea_comentarios += f',"{autor}","{ayuda}","{otros_comentarios}"\n'
    linea_fuente += "\n"
    datos_comentarios.append(linea_comentarios)
    datos_fuente.append(linea_fuente)

    return datos_fuente, datos_comentarios, lineas_fuera_funcion

def grabar_individual(archivo, datos_ordenados):
    for linea in datos_ordenados:
        archivo.write(linea)

def ordenar_datos(datos):
    return sorted(datos)

def crear_csv_individuales(ubicaciones):
    archivos_fuente = []
    archivos_comentarios = []
    for ubicacion, nombre_modulo in ubicaciones:
        with open(f'fuente_{nombre_modulo}.csv', "w") as fuente_modulo, open(f'comentarios_{nombre_modulo}.csv', "w") as comentarios_modulo, open(ubicacion, "r") as codigo:
            datos_fuente, datos_comentarios, lineas_fuera_funcion = leer_lineas_codigo(codigo, ubicacion, nombre_modulo, ubicaciones)
            #Ordena las lineas a grabar en forma alfabetica
            datos_fuente_ordenados = sorted(datos_fuente)
            datos_comentarios_ordenados = sorted(datos_comentarios)
            #Graba los datos en los archivos
            grabar_individual(fuente_modulo, datos_fuente_ordenados)
            grabar_individual(comentarios_modulo, datos_comentarios_ordenados)
            #Guarda el nombre de los archivos en listas
            archivos_fuente.append((f'fuente_{nombre_modulo}.csv', nombre_modulo))
            archivos_comentarios.append((f'comentarios_{nombre_modulo}.csv', nombre_modulo))
    
    return archivos_fuente, archivos_comentarios, lineas_fuera_funcion

def main(nombre_archivo):
    ubicaciones = analizar_archivo_programas(nombre_archivo)
    archivos_fuente, archivos_comentarios, lineas_fuera_funcion = crear_csv_individuales(ubicaciones)

    return archivos_fuente, archivos_comentarios, lineas_fuera_funcion

    