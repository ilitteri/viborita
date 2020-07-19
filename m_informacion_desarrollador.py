import m_organizar_datos as organizar
import m_obtener as obtener

def ordenar_datos(datos):
    '''[Autor: Ivan Litteri]
    [Ayuda: Ordena los datos del diccionario de forma descendiente respecto de la cantidad de lineas de codigo que
    escribio cada autor]'''
    return sorted(datos.items(), key=lambda x: x[1]["lineas_totales"], reverse=True)

def leer_archivos_csv(nombre_archivo_fuente, nombre_archivo_comentarios):
    '''[Autor: Ivan Litteri]
    [Ayuda: esta funcion abre los archivos cuyos nombres o ubicaciones le llegan por parametro, y devuelve
    una lista de datos por cada archivo que lee, cuando termina la lectura, los cierra]'''

    #Abre los dos archivos que le llegan por parametro para su lectura
    with open(nombre_archivo_fuente, "r") as archivo_fuente, open(nombre_archivo_comentarios, "r") as archivo_comentarios:
        datos_csv = organizar.por_cantidad_lineas_autor(archivo_fuente, archivo_comentarios)
        
    #Obtiene la cantidad de lineas de codigo totales de todos los modulos juntos
    lineas_codigo_totales = obtener.lineas_codigo_totales(datos_csv)
    return datos_csv, lineas_codigo_totales

def grabar_txt(archivo_datos, linea):
    '''[Autor: Ivan Litteri]'''
    archivo_datos.write(linea)

def imprimir_datos(datos_ordenados, lineas_codigo_totales):
    '''[Autor: Ivan Litteri]
    [Ayuda: imprime una tabla con la informacion de desarrollo por cada autor en la consola y en un archivo de texto]'''
    
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
        porcentaje_lineas_autor = round(obtener.porcentaje_lineas_codigo(autor, datos_autor,  lineas_codigo_totales))
        #Establece la columna 1 y la separacion
        columna_1 = f'{len(datos_autor["funciones"])} Funciones - Lineas' 
        separacion = " " * (50-len(columna_1))
        #Imprime y graba la linea que contiene la cantidad de funciones que escribio el autor y el porcentaje respecto a todo el codigo
        print(f'\t{columna_1}{separacion}{lineas_totales_autor}\t{porcentaje_lineas_autor}%\n\n')
        grabar_txt(archivo_datos, f'\t{columna_1}{separacion}{lineas_totales_autor}\t{porcentaje_lineas_autor}%\n\n')

    #Cierra el archivo de texto que se creo ya que se grabo todo lo que se queria grabar
    archivo_datos.close()

def main():
    '''[Autor: Ivan Litteri]'''
#def main(archivo_fuente, archiv_comentarios):

    #datos_por_cantidad_lineas_autor = obtener.por_cantidad_lineas_autor(archivo_fuente, archivo_comentarios)
    datos_csv, lineas_codigo_totales = leer_archivos_csv("fuente_unico.csv", "comentarios.csv")
    datos_ordenados = ordenar_datos(datos_csv)
    imprimir_datos(datos_ordenados, lineas_codigo_totales)

main()