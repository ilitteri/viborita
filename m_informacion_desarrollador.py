import m_organizar_datos as organizar
import m_obtener as obtener

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

def grabar_txt(archivo_datos, linea):
    '''[Autor: Ivan Litteri]'''
    archivo_datos.write(linea)

def imprimir_datos(datos_ordenados):
    '''[Autor: Ivan Litteri]
    [Ayuda: imprime una tabla con la informacion de desarrollo por cada autor en la consola y en un archivo de texto]'''
    
    lineas_codigo_totales = sum(datos_autor["lineas_totales"] for _, datos_autor in datos_ordenados)

    #Crea el archivo de texto para grabar lineas
    archivo_datos = open("participacion.txt", "w")

    #Imprime y graba la primera linea
    print("\t\t\tInformacion de Desarrollo Por Autor\n")
    grabar_txt(archivo_datos, "\t\t\tInformacion de Desarrollo Por Autor\n\n")

    #Recorre los datos ordenados que me llegan por parametro
    for autor, datos_autor in datos_ordenados:
        #Declara esta variable, que aunque ya tenia los datos en otra, para que la impresion y el grabado se entiendan mejor
        lineas_totales_autor = datos_autor["lineas_totales"]
        #Guarda las cadenas de texto de igual forma por el mismo motivo
        columna_1 = "Funcion"
        columna_2 = "Lineas"
        separacion = " " * (50-len(columna_1))
        linea_iguales = f'\t{"=" * (50 + len(columna_1))}'

        #Imprime y graba la linea correspondiende al autor y la fila que corresponde al titulo de la tabla del autor
        print(f'\n{autor if "Autor" in autor else "Sin Autor"}\n\n\t{columna_1}{separacion}{columna_2}')
        print(linea_iguales)
        grabar_txt(archivo_datos, f'{autor if "Autor" in autor else "Sin Autor"}\n\n\t{columna_1}{separacion}{columna_2}\n{linea_iguales}\n')
        
        #Recorre los datos de las funciones del autor
        for funcion, cantidad_lineas in datos_autor["funciones"].items():
            #Establece la separacion que quiero tener entre el nombre de la funcion y la cantidad de lineas de esa funcion
            separacion = " " * (50-len(funcion))
            #Imprime y graba la linea: "Funcion" ---------- "Cantidad Lineas de Funcion"
            print(f'\t{funcion}{separacion}{cantidad_lineas}')
            grabar_txt(archivo_datos, f'\t{funcion}{separacion}{cantidad_lineas}\n')
        #Guarda el porcentaje de lineas de codigo que escribio el autor respecto del total del codigo
        porcentaje_lineas_autor = round(obtener.porcentaje_lineas_codigo(autor, datos_autor,  lineas_codigo_totales), 1)
        #Establece la columna 1 y la separacion
        columna_1 = f'{len(datos_autor["funciones"])} Funciones - Lineas' 
        separacion = " " * (50-len(columna_1))
        #Imprime y graba la linea que contiene la cantidad de funciones que escribio el autor y el porcentaje respecto a todo el codigo
        print(f'\t{columna_1}{separacion}{lineas_totales_autor}\t{porcentaje_lineas_autor}%\n\n')
        grabar_txt(archivo_datos, f'\t{columna_1}{separacion}{lineas_totales_autor}\t{porcentaje_lineas_autor}%\n\n')

    #Cierra el archivo de texto que se creo ya que se grabo todo lo que se queria grabar
    archivo_datos.close()

def main(datos_archivos_csv):
    '''[Autor: Ivan Litteri]'''

    datos_ordenados = ordenar_datos(datos_archivos_csv)
    imprimir_datos(datos_ordenados)