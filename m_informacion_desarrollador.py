import m_organizar_datos as organizar
import m_obtener as obtener
import m_grabar as grabar

def ordenar_datos(datos_por_funciones):
    '''[Autor: Ivan Litteri]
    [Ayuda: Reordena los datos del diccionario que llega del main en otro de forma descendiente respecto de la cantidad de 
    lineas de codigo que escribio cada autor]'''

    datos_por_autor = {}
    #Recorre los items del diccionario ordenado por funcion
    for funcion, datos_funcion in datos_por_funciones.items():
        #Declara la variable autor para que sea mas entendible el resto
        autor = datos_funcion["comentarios"]["autor"]
        #Si no esta en el diccionario, la agrego
        if autor not in datos_por_autor:
            datos_por_autor[autor] = {"lineas_totales": 0,
                        "funciones": {}
                        }
        #Si no esta en el diccionario, la agrego
        if funcion not in datos_por_autor[autor]["funciones"]:
            datos_por_autor[autor]["funciones"][funcion] = 0
        #Agrego los datos de interes
        datos_por_autor[autor]["funciones"][funcion] += datos_funcion["cantidad_lineas"]
        datos_por_autor[autor]["lineas_totales"] += datos_funcion["cantidad_lineas"]

    #Devuelve una lista ordenada por el total de lineas que escribio cada autor
    return sorted(datos_por_autor.items(), key=lambda x: x[1]["lineas_totales"], reverse=True)

def formatear_datos(datos_ordenados):
    '''[Autor: Ivan Litteri]
    [Ayuda: Formatea los datos del diccionario como se pide en la consigna y devuelve una cadena con los datos 
    formateados]'''
    
    #Obtiene las lineas de codigo totales de la aplicacion
    lineas_codigo_totales = sum(datos_autor["lineas_totales"] for _, datos_autor in datos_ordenados)
    #Declara el contador de funciones en 0
    funciones_totales = 0
    #Inicializa la devolucion en vacio para ir concatenando
    datos_a_imprimir = ""

    #Concatena la primera linea
    datos_a_imprimir += "\t\tInformacion de Desarrollo Por Autor\n"

    #Recorre los datos ordenados que me llegan por parametro
    for autor, datos_autor in datos_ordenados:
        #Declara esta variable, que aunque ya tenia los datos en otra, para que la impresion y el grabado se entiendan mejor
        lineas_totales_autor = datos_autor["lineas_totales"]
        #Guarda las cadenas de texto de igual forma por el mismo motivo
        columna_1 = "Funcion"
        columna_2 = "Lineas"
        separacion = " " * (50-len(columna_1))
        separacion_2 = " " * 7
        linea_iguales = f'{separacion_2}{"=" * (50 + len(columna_1))}'

        #Concatena la linea correspondiende al autor y la fila que corresponde al titulo de la tabla del autor
        datos_a_imprimir += f'\n{autor if "Autor" in autor else "Sin Autor"}\n\n{separacion_2}{columna_1}{separacion}{columna_2}\n'
        #Concatena la linea de iguales
        datos_a_imprimir += f'{linea_iguales}\n'
        
        #Recorre los datos de las funciones del autor
        for funcion, cantidad_lineas in datos_autor["funciones"].items():
            #Establece la separacion que quiero tener entre el nombre de la funcion y la cantidad de lineas de esa funcion
            separacion = " " * (50-len(funcion))
            if "*" in funcion:
                datos_a_imprimir += f'{separacion_2}{funcion[1:]}{separacion}{cantidad_lineas}\n'
            else:    
                #Concatena la linea: "Funcion" ---------- "Cantidad Lineas de Funcion"
                datos_a_imprimir += f'{separacion_2}{funcion}{separacion}{cantidad_lineas}\n'
        #Guarda el porcentaje de lineas de codigo que escribio el autor respecto del total del codigo
        porcentaje_lineas_autor = round(obtener.porcentaje_lineas_codigo(autor, datos_autor,  lineas_codigo_totales), 1)
        #Incrementa el contador de funciones
        funciones_totales += len(datos_autor["funciones"])
        #Establece la columna 1 y la separacion
        columna_1 = f'{len(datos_autor["funciones"])} Funciones - Lineas' 
        separacion = " " * (50-len(columna_1))
        #Concatena la linea que contiene la cantidad de funciones que escribio el autor y el porcentaje respecto a todo el codigo
        datos_a_imprimir += f'{separacion_2}{columna_1}{separacion}{lineas_totales_autor}\t{porcentaje_lineas_autor}%\n\n'
    #Establece la columna 1 y la separacion
    columna_1 = f'{funciones_totales} Funciones - Lineas'
    separacion = " " * (50-len(columna_1))
    #Concatena la linea final
    datos_a_imprimir += f'Total: {columna_1}{separacion}{lineas_codigo_totales}'

    return datos_a_imprimir

def imprimir_participacion(datos):
    '''[Autor: Ivan Litteri]'''
    print(datos)

def crear_archivo_txt(nombre_archivo, datos):
    '''[Autor: Ivan Litteri]
    [Ayuda: Crea y graba el archivo de participacion txt con los datos formateados]'''

    #Abre el archivo para escribir y lo cierra al finalizar la grabacion
    with open(nombre_archivo, "w") as archivo_txt:
        #Escribe en el archivo
        grabar.cadena(archivo_txt, datos)

def main(datos_archivos_csv):
    '''[Autor: Ivan Litteri]'''

    datos_ordenados = ordenar_datos(datos_archivos_csv)
    datos_formateados = formatear_datos(datos_ordenados)
    imprimir_participacion(datos_formateados)
    crear_archivo_txt("participacion.txt", datos_formateados)