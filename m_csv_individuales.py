import m_analizar_linea as analizar_linea
import m_obtener as obtener

def grabar_csv_final(archivo, lineas):
    for linea in lineas:
        archivo.write(linea)

def analizar_linea_codigo(linea_codigo, nombre_modulo, lineas_a_grabar, banderas, cadenas, info_lineas):
    if banderas[0]:
        if banderas[1]:
            if "Ayuda" in linea_codigo and not banderas[2]:
                info_lineas[2], banderas[2] = analizar_linea.ayuda_funcion(linea_codigo, banderas[2])
            if "'''\n" in linea_codigo or '"""\n' in linea_codigo:
                banderas[1] = False
                banderas[2] = False
        else:
            if linea_codigo[0:3] == "def":
                banderas[1] = banderas[2] =  False
                lineas_a_grabar[0].append(cadenas[0]+"\n")
                lineas_a_grabar[1].append(f'"{info_lineas[0]}","{info_lineas[1]}","{info_lineas[2]}","{info_lineas[3]}"\n')
                cadenas[0] = cadenas[1] = info_lineas[1] = info_lineas[2] = info_lineas[3] = ""
                info_lineas[0], param = analizar_linea.declaracion_funcion(linea_codigo)
                cadenas[0] += f'"{info_lineas[0]}","{param}","{nombre_modulo}"'
            elif linea_codigo.strip().startswith("return"):
                banderas[0] = banderas[1] = banderas[2] =  False
                cadenas[0] += f',"{linea_codigo.strip()}"'
                lineas_a_grabar[0].append(cadenas[0]+"\n")
                lineas_a_grabar[1].append(f'"{info_lineas[0]}","{info_lineas[1]}","{info_lineas[2]}","{info_lineas[3]}"\n')
                cadenas[0] = cadenas[1] = info_lineas[0] = info_lineas[1] = info_lineas[2] = info_lineas[3] = ""
            elif "#" in linea_codigo and not("'#" in linea_codigo or "('#" in linea_codigo) and "#todo" not in linea_codigo:
                coment, seudo_line = analizar_linea.comentario_numeral(linea_codigo)
                if info_lineas[3] == "":
                    info_lineas[3] = f'{coment}'
                else:
                    info_lineas[3] += f'","{coment}'
                if seudo_line:
                    cadenas[0] += f',"{seudo_line}"'
                banderas[1] = False
            elif linea_codigo.strip().startswith("'''"):
                if linea_codigo.count("'''") == 2:
                    if "Autor" in linea_codigo:
                        info_lineas[1] = analizar_linea.autor_funcion(linea_codigo)
                    elif "Ayuda" in linea_codigo:
                        info_lineas[2] = linea_codigo[4:-4]
                else:
                    banderas[1] = True
                    if "Autor" in linea_codigo:
                        info_lineas[1] = analizar_linea.autor_funcion(linea_codigo)
            elif linea_codigo.strip() != "":
                cadenas[0] += f',"{linea_codigo.strip()}"'
    elif linea_codigo[0:3] == "def":
        banderas[0] = True
        banderas[1] = False
        info_lineas[0], param = analizar_linea.declaracion_funcion(linea_codigo)
        cadenas[0] += f'"{info_lineas[0]}","{param}","{nombre_modulo}"'
    else:
        lineas_a_grabar[2].append(linea_codigo.strip())
        banderas[1] = False

    return lineas_a_grabar, banderas, cadenas, info_lineas

def formatear_lineas_csv(archivo_modulo, nombre_modulo, lineas_a_grabar, banderas, cadenas, info_lineas):
    linea_codigo = archivo_modulo.readline().replace('"', "'")

    while linea_codigo:
        lineas_a_grabar, banderas, cadenas, info_lineas = analizar_linea_codigo(linea_codigo, nombre_modulo, lineas_a_grabar, banderas, cadenas, info_lineas)
        linea_codigo = archivo_modulo.readline().replace('"', "'")
    
    return lineas_a_grabar, banderas, cadenas, info_lineas 
    
def leer_modulo(archivo_modulo, archivo_fuente, archivo_comentarios, nombre_modulo):
    '''lineas_fuente = lineas_a_grabar[0], lineas_comentarios = lineas_a_grabar[1], lineas_fuera_funcion = lineas_a_grabar[2]],
    bandera_funcion = banderas[0], bandera_comentarios = banderas[1], bandera_ayuda = banderas[2],
    linea_fuente = cadenas[0], linea_comentario = cadenas[1], funcion = info_lineas[0], autor = info_lineas[1],
    ayuda = info_lineas[2], otros_comentarios = info_lineas[3]'''
    lineas_a_grabar = [[],[],[]]
    banderas = [False, False, False]
    cadenas = ["",""]
    info_lineas = ["", "", "", ""]

    lineas_a_grabar, banderas, cadenas, info_lineas  = formatear_lineas_csv(archivo_modulo, nombre_modulo, lineas_a_grabar, banderas, cadenas, info_lineas)

    if f'"{info_lineas[0]}","{info_lineas[1]}","{info_lineas[2]}","{info_lineas[3]}"\n' != '"","","",""\n':
        lineas_a_grabar[1].append(f'"{info_lineas[0]}","{info_lineas[1]}","{info_lineas[2]}","{info_lineas[3]}"\n')
    if cadenas[0] != "":
        lineas_a_grabar[0].append(cadenas[0]+"\n")
    
    return lineas_a_grabar

def crear_csv_individuales(ubicaciones):
    '''[Autor: Ivan Litteri]
    [Ayuda: ]'''

    archivos_fuente = []
    archivos_comentarios = []
    
    for ubicacion, nombre_modulo in ubicaciones:
        with open(ubicacion, "r", encoding='utf-8') as archivo_modulo, open(f'fuente_{nombre_modulo}.csv', "w") as archivo_fuente, open(f'comentarios_{nombre_modulo}.csv', "w") as archivo_comentarios:
            lineas_a_grabar = leer_modulo(archivo_modulo, archivo_fuente, archivo_comentarios, nombre_modulo)
            grabar_csv_final(archivo_fuente, lineas_a_grabar[0])
            grabar_csv_final(archivo_comentarios, lineas_a_grabar[1])
            #Guarda el nombre de los archivos en listas
            archivos_fuente.append((f'fuente_{nombre_modulo}.csv', nombre_modulo))
            archivos_comentarios.append((f'comentarios_{nombre_modulo}.csv', nombre_modulo))

    return archivos_fuente, archivos_comentarios, lineas_a_grabar[2]

#ubicaciones = obtener.ubicaciones_modulos("programas.txt")
#crear_csv_individuales(ubicaciones)