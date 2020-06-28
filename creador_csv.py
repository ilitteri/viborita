def leer_archivo_principal(archivo_principal):
    with open(archivo_principal, "r") as archivo:
        lineas = archivo.read().splitlines()
    return lineas