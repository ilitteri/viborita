def leer_codigo(codigo, datos_ordenados, nombre_modulo, imports, bandera_funcion = False, bandera_comentario = False, bandera_ayuda = False, nombre_funcion = None):
    '''[Autor: Ivan Litteri]
    [Ayuda: Lee el codigo que le llega por parametro, lo analiza con distintas funciones y actualiza el 
    diccionario donde se guardan los datos analizados cada vez que se llama.]'''

    #Importo las funciones del modulo m_analizar_linea.py.
    import m_analizar_linea as analizar

    linea_codigo = codigo.readline().replace('"', "'")
    while linea_codigo:
        #Se habilita esta bandera cuando en el codigo a leer empieza una funcion, se deshabilita cuando termina o empieza otra.
        if bandera_funcion:
            #Se habilita esta bandera cuando se detecta un comentario multilinea que no se cierra en la misma linea.
            if bandera_comentario:
                ayuda_funcion, bandera_ayuda = analizar.ayuda_funcion(linea_codigo, bandera_ayuda)
                datos_ordenados[nombre_funcion]["comentarios"]["ayuda"] += ayuda_funcion
                #Se deshabilita la bandera cuando se detecta que se cierra el comentario multilinea.
                if "'''" in linea_codigo:
                    bandera_comentario = False
            #Guarda otro tipo de comentarios
            elif "#" in linea_codigo:
                #Si es None, cambia su valor a una lista vacia para que se pueda hacer append.
                if datos_ordenados[nombre_funcion]["comentarios"]["otros"] == None:
                    datos_ordenados[nombre_funcion]["comentarios"]["otros"] = []
                otro_comentario = analizar.comentario_numeral(linea_codigo)
                datos_ordenados[nombre_funcion]["comentarios"]["otros"].append(f'"{otro_comentario}"')
            #Si un comentario multilinea se abre y cierra en la misma linea, analiza la linea y guarda los datos del autor.
            elif linea_codigo.count("'''") == 2:
                autor_funcion = analizar.autor_funcion(linea_codigo)
                datos_ordenados[nombre_funcion]["comentarios"]["autor"] = autor_funcion
            #Si la linea empieza con un comentario multilinea, y no se cierra en la misma linea, se analiza esta primera linea que corresponde
            #al autor, y luego habilita la bandera de comentario multilinea para que se analicen las lineas siguientes hasta que se cierre
            #el comentario multilinea.
            elif linea_codigo.strip().startswith("'''"):
                bandera_comentario = True
                autor_funcion = analizar.autor_funcion(linea_codigo)
                datos_ordenados[nombre_funcion]["comentarios"]["autor"] = autor_funcion
            #Si ninguna linea es un comentario guarda la linea en lineas de codigo.
            else:
                if not linea_codigo.isspace():
                    datos_ordenados[nombre_funcion]["lineas"].append(f'"{linea_codigo.strip()}"')

        if linea_codigo.strip().startswith("return"):
            bandera_funcion = False
        if linea_codigo.startswith("def"):
            bandera_funcion = True
            nombre_funcion, parametros_funcion = analizar.declaracion_funcion(linea_codigo)
            datos_ordenados[nombre_funcion] = {"modulo": nombre_modulo, 
                                                "parametros": parametros_funcion, 
                                                "lineas": [], 
                                                "comentarios": {"autor": "", 
                                                                "ayuda": "",
                                                                "otros": None
                                                                }
                                                }
        #Almaceno las lineas de imports.
        if linea_codigo.startswith("import"):
            #Si el nombre del modulo no esta como key, entonces lo agrega (Esto ocurre una vez sola).
            if nombre_modulo not in imports:
                imports[nombre_modulo] = []
            imports[nombre_modulo].append(linea_codigo)
        #Lee la siguiente linea del codigo.
        linea_codigo = codigo.readline().replace('"', "'")

    #Devuelvo un diccionario de datos de todos los modulos, y uno de imports.
    return datos_ordenados, imports

def crear_archivos_csv_individuales(ubicaciones_modulos):
    '''[Autor: Ivan Litteri]
    [Ayuda: Abre los archivos a crear (los csv finales), y para cada ubicacion abre el archivo perteneciente
    a esa ubicacion, lo lee, extrae los datos, y los guarda en un diccionario para que luego se graben de la
    forma en la que se pide en cada uno de los csv, luego se cierran.]'''

    #Importo las funciones del modulo grabar.py.
    import m_grabar as grabar

    datos_modulos = {}
    imports = {}

    with open(f'fuente_unico.csv', "w") as archivo_fuente, open(f'comentarios.csv', "w") as archivo_comentarios:
        for ubicacion_modulo in ubicaciones_modulos:
            nombre_modulo = ubicacion_modulo.split("\\")[-1]
            #Abre un archivo para leer y dos para escribir, al mismo tiempo.
            with open(ubicacion_modulo, "r") as codigo:
                datos_modulos, imports = leer_codigo(codigo, datos_modulos, nombre_modulo, imports)
        nombres_funcion_ordenados = sorted(list(datos_modulos.keys()))
        for nombre_funcion in nombres_funcion_ordenados:
            grabar.fuente(archivo_fuente, nombre_funcion, datos_modulos[nombre_funcion]["parametros"], datos_modulos[nombre_funcion]["modulo"], datos_modulos[nombre_funcion]["lineas"])
            grabar.comentarios(archivo_comentarios, nombre_funcion, datos_modulos[nombre_funcion]["comentarios"])

def main():
    '''[Autor: Ivan Litteri]'''

    #Importo las funciones del modulo obtener.py.
    from m_obtener import ubicaciones_modulos

    #Crea los archivos csv.
    archivo_principal = "programas.txt"
    ubicaciones_modulos = ubicaciones_modulos(archivo_principal)
    crear_archivos_csv_individuales(ubicaciones_modulos)

main()