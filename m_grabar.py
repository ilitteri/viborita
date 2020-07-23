def cadena(archivo, linea):
    '''[Autores: Ivan Litteri]
    [Ayuda: Graba una linea en el archivo que le llega por parametro]'''
    archivo.write(linea)

def cadenas(archivo, lineas):
    '''[Autor: Ivan Litteri]
    [Ayuda: Graba una lista de lineas en el archivo que le llega por parametro]'''
    for linea in lineas:
        archivo.write(linea)