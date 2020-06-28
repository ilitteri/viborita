def leer_archivo_principal(archivo_principal):
    with open(archivo_principal, "r") as archivo:
        lineas = archivo.read().splitlines()
    return lineas

def leer_programas(archivo_principal):
    ubicaciones = leer_archivo_principal(archivo_principal)
    u_programa_principal = ubicaciones[0]
    datos_programas = {}

    for ubicacion in ubicaciones:
        nombre_modulo = ubicacion.split("\\")[-1]
        with open(ubicacion, "r") as codigo:
            linea = codigo.readline()
            while linea:
                if linea.startswith("def"):
                    recorte = linea.strip()[4:-1]
                    nombre_funcion = recorte.split("(")[0]
                    parametros = recorte.split("(")[1].split(")")[0]
                    datos_programas[nombre_funcion] = {"modulo": nombre_modulo, "parametros": f'({parametros})', "lineas": [], "comentarios": []}
                if (len(datos_programas) > 0) and linea.startswith("    ") and ("#" not in linea or "'''" not in linea):
                    datos_programas[nombre_funcion]["lineas"].append(linea.strip())
                elif linea.strip().startswith("#") or linea.strip().startswith("'''"):
                    datos_programas[nombre_funcion]["comentarios"].append(linea.strip())
                linea = codigo.readline()

    return datos_programas