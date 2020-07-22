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

def analizar_linea_codigo(linea_codigo, ubicacion, nombre_modulo, ubicaciones, datos_fuente, datos_comentarios, autor, ayuda, otros_comentarios, lineas_fuera_funcion, bandera_funcion, bandera_comentario, bandera_ayuda, contador_def):
    if linea_codigo[0:3] != "def" and linea_codigo[0:3] != "   " and linea_codigo != "\n":
            lineas_fuera_funcion.append(linea_codigo)
    elif linea_codigo[0:3] == "def":
        contador_def += 1
        bandera_funcion = True
        if contador_def > 1:
            datos_fuente += "\n"
            datos_comentarios += f',"{autor}","{ayuda}","{otros_comentarios}"\n'
            autor = ""
            ayuda = ""
        funcion, parametros = analizar_linea.declaracion_funcion(linea_codigo)
        if ubicacion == ubicaciones[0][0]:
            datos_fuente += f'"{funcion}","{parametros}","*{nombre_modulo}"'
        else:
            datos_fuente += f'"{funcion}","{parametros}","{nombre_modulo}"'
        datos_comentarios += f'"{funcion}"'
    elif bandera_funcion:
        if "return" in linea_codigo:
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
                if linea != "":
                    datos_fuente += f',"{linea}",'
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
            elif linea_codigo:
                datos_fuente += f',"{linea_codigo.strip()}"'
    else:
        lineas_fuera_funcion.append(linea_codigo.strip())
    
    return datos_fuente, datos_comentarios, autor, ayuda, otros_comentarios, lineas_fuera_funcion, bandera_funcion, bandera_comentario, bandera_ayuda, contador_def

def leer_lineas_codigo(codigo, ubicacion, nombre_modulo, ubicaciones, datos_fuente="", datos_comentarios="", autor="", ayuda="", otros_comentarios="", lineas_fuera_funcion=[], bandera_funcion=False, bandera_comentario=False, bandera_ayuda=False, contador_def=0):

    linea_codigo = codigo.readline().replace('"', "'")
    while linea_codigo:
        datos_fuente, datos_comentarios, autor, ayuda, otros_comentarios, lineas_fuera_funcion, bandera_funcion, bandera_comentario, bandera_ayuda, contador_def =analizar_linea_codigo(linea_codigo, ubicacion, nombre_modulo, ubicaciones, datos_fuente, datos_comentarios, autor, ayuda, otros_comentarios, lineas_fuera_funcion, bandera_funcion, bandera_comentario, bandera_ayuda, contador_def)
        linea_codigo = codigo.readline().replace('"', "'")
    datos_comentarios += f',"{autor}","{ayuda}","{otros_comentarios}"'

    return datos_fuente, datos_comentarios

def grabar(archivo, datos):
    archivo.write(datos)

def crear_csv_individuales(ubicaciones):
    archivos_fuente = []
    archivos_comentarios = []
    for ubicacion, nombre_modulo in ubicaciones:
        with open(f'fuente_{nombre_modulo}.csv', "w") as fuente_modulo, open(f'comentarios_{nombre_modulo}.csv', "w") as comentarios_modulo, open(ubicacion, "r") as codigo:
            datos_fuente, datos_comentarios = leer_lineas_codigo(codigo, ubicacion, nombre_modulo, ubicaciones)
            grabar(fuente_modulo, datos_fuente)
            grabar(comentarios_modulo, datos_comentarios)
            archivos_fuente.append(f'fuente_{nombre_modulo}.csv')
            archivos_comentarios.append(f'comentarios_{nombre_modulo}.csv')
    
    return archivos_fuente, archivos_comentarios

def borrar_archivos_csv_individuales(nombres_archivos_csv_individuales):
    '''[Autor: Ivan Litteri]
    [Ayuda: Borra los archivos .csv individuales (que se encuentran en el repositorio actual) cuyas ubicaciones se obtienen 
    de una funcion a la que le llega por parametro los nombres de los archivos .csv individuales.]'''

    #Obtengo las ubicaciones y las recorro para borrar el archivo que se encuentra en ella.
    for ubicacion_archivo_csv_individual in obtener.ubicaciones_archivos_csv_individuales(nombres_archivos_csv_individuales):
        #Borro el archivo que se encuentra en esa ubicacion.
        os.remove(ubicacion_archivo_csv_individual)

def main(nombre_archivo):
    ubicaciones = analizar_archivo_programas(nombre_archivo)
    crear_csv_individuales(ubicaciones)
    #borrar_archivos_csv_individuales(list(zip(*ubicaciones))[1])

main("programas.txt")