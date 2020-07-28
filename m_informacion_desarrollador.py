import m_obtener as obtener

def ordenar_diccionario_autores(datos_csv):
    '''[Autor: Ivan Litteri]
    [Ayuda: Reordena los datos del diccionario que llega del main en otro de forma descendiente respecto de la cantidad de 
    lineas de codigo que escribio cada autor]'''

    #Devuelve una lista ordenada por el total de lineas que escribio cada autor
    return sorted(datos_csv.items(), key=lambda x: x[1]["lineas_totales"], reverse=True)

def formatear_participacion(datos_ordenados):
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
            if ("*" in funcion):
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

def mostrar_participacion(datos_formateados):
    '''[Autor: Ivan Litteri]'''
    print(datos_formateados)

def crear_participacion_txt(nombre_archivo, datos_formateados):
    '''[Autor: Ivan Litteri]
    [Ayuda: Crea y graba el archivo de participacion txt con los datos formateados]'''

    #Abre el archivo para escribir y lo cierra al finalizar la grabacion
    with open(nombre_archivo, "w") as archivo_txt:
        #Escribe en el archivo
        archivo_txt.write(datos_formateados)

def obtener_informacion_desarrollador(datos_csv):
    '''[Autor: Ivan Litteri]'''

    datos_ordenados = ordenar_diccionario_autores(datos_csv)
    datos_formateados = formatear_participacion(datos_ordenados)
    mostrar_participacion(datos_formateados)
    crear_participacion_txt("participacion.txt", datos_formateados)