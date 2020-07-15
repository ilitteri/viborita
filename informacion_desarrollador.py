import m_organizar_datos as organizar
import m_obtener as obtener

def leer_archivos_csv(nombre_archivo_fuente, nombre_archivo_comentarios):
    '''[Autor: Ivan Litteri]
    [Ayuda: esta funcion abre los archivos cuyos nombres o ubicaciones le llegan por parametro, y devuelve
    una lista de datos por cada archivo que lee, cuando termina la lectura, los cierra]'''

    #Abre los dos archivos que le llegan por parametro para su lectura
    with open(nombre_archivo_fuente, "r") as archivo_fuente, open(nombre_archivo_comentarios, "r") as archivo_comentarios:
        datos_ordenados = organizar.por_cantidad_lineas_autor(archivo_fuente, archivo_comentarios)
    
    return datos_ordenados

def grabar_linea(archivo_datos, linea):
    '''[Autor: Ivan Litteri]'''
    archivo_datos.write(linea)

def imprimir_datos(datos_por_cantidad_lineas_autor):
    '''[Autor: Ivan Litteri]
    [Ayuda: imprime una tabla con la informacion de desarrollo por cada autor en la consola y en un archivo de texto]'''
    
    archivo_datos = open("participacion.txt", "w")
    lineas_codigo_totales = obtener.lineas_codigo_totales(datos_por_cantidad_lineas_autor)

    print("\t\t\tInformacion de Desarrollo Por Autor\n")
    grabar_linea(archivo_datos, "\t\t\tInformacion de Desarrollo Por Autor\n\n")

    for autor in datos_por_cantidad_lineas_autor:

        lineas_totales_autor = datos_por_cantidad_lineas_autor[autor]["lineas_totales"]
        columna_1 = "Funcion"
        columna_2 = "Lineas"
        separacion = " " * (50-len(columna_1))
        linea_iguales = f'\t{"=" * (50 + len(columna_1))}'

        print(f'\n{autor if "Autor" in autor else "Sin Autor"}\n\n\t{columna_1}{separacion}{columna_2}')
        print(linea_iguales)

        grabar_linea(archivo_datos, f'{autor if "Autor" in autor else "Sin Autor"}\n\n\t{columna_1}{separacion}{columna_2}\n\n{linea_iguales}\n')
        
        for funcion, cantidad_lineas in datos_por_cantidad_lineas_autor[autor]["funciones"].items():

            funcion = funcion.replace('"','')
            separacion = " " * (50-len(funcion))

            print(f'\t{funcion}{separacion}{cantidad_lineas}')

            grabar_linea(archivo_datos, f'\t{funcion}{separacion}{cantidad_lineas}\n')

        porcentaje_lineas_modulo = round(obtener.porcentaje_lineas_codigo(datos_por_cantidad_lineas_autor, autor, lineas_codigo_totales))
        columna_1 = f'{len(datos_por_cantidad_lineas_autor[autor])} Funciones - Lineas' 
        separacion = " " * (50-len(columna_1))
        
        print(f'\t{columna_1}{separacion}{lineas_totales_autor}\t{porcentaje_lineas_modulo}%\n\n')
        
        grabar_linea(archivo_datos, f'\t{columna_1}{separacion}{lineas_totales_autor}\t{porcentaje_lineas_modulo}%\n\n')
    
    archivo_datos.close()

def main():
    '''[Autor: Ivan Litteri]'''
#def main(archivo_fuente, archiv_comentarios):

    #datos_por_cantidad_lineas_autor = obtener.por_cantidad_lineas_autor(archivo_fuente, archivo_comentarios)
    datos_por_cantidad_lineas_autor = leer_archivos_csv("fuente_unico.csv", "comentarios.csv")
    imprimir_datos(datos_por_cantidad_lineas_autor)

main()