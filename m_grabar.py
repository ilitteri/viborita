def cadena(archivo, linea):
    '''[Autores: Ivan Litteri]
    [Ayuda: Graba una linea en el archivo que le llega por parametro]'''

    archivo.write(linea)

def cadenas(archivo, lineas):
    '''[Autor: Ivan Litteri]
    [Ayuda: Graba una lista de lineas en el archivo que le llega por parametro]'''

    for linea in lineas:
        archivo.write(linea)

def panel_control_csv(archivo, lineas):
    '''[Autor: Santiago Vaccarelli]
    [Ayuda: graba las lineas que le llegan por parametro al archivo]'''

    for linea in lineas:
        archivo.write(f'{",".join(linea)}\n')