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

def guardar_datos():
    datos = leer_programas("programas.txt")
    nombres_funciones = list(datos.keys())
    modulos = list(set([datos[nombre_funcion]["modulo"] for nombre_funcion in nombres_funciones]))
    for modulo in modulos:
        with open(f'fuente_{modulo}.csv', "w") as archivo_fuente, open(f'comentarios_{modulo}.csv', "w") as archivo_comentarios:
            for nombre_funcion in nombres_funciones:
                if modulo == datos[nombre_funcion]["modulo"]:
                    archivo_fuente.write(f'{nombre_funcion},{datos[nombre_funcion]["parametros"]},{datos[nombre_funcion]["modulo"]},{datos[nombre_funcion]["lineas"]}\n')
                    if len(datos[nombre_funcion]["comentarios"]) > 0:
                        archivo_comentarios.write(f'{nombre_funcion},nombre de autor,ayuda,{datos[nombre_funcion]["comentarios"]}\n')

guardar_datos()