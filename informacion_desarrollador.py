def obtener_datos_comentarios(lineas_comentarios):
    '''[Autor: Ivan Litteri]
    [Ayuda: A esta funcion le llega por parametro una lista de lineas que pertenecen al archivo comentarios.csv
    y devuelve una lista de listas, en donde cada lista es una linea]'''

    return [linea_comentarios.split(",") for linea_comentarios in lineas_comentarios]

def obtener_datos_fuente(lineas_fuente):
    '''[Autor: Ivan Litteri]
    [Ayuda: A esta funcion le llega por parametro una lista de lineas que pertenecen al archivo fuente_unico.csv
    y devuelve una lista de listas, en donde cada lista es una linea]'''

    return [linea_funcion.split(",") for linea_funcion in lineas_fuente]

def obtener_datos_archivos_csv(archivo_fuente, archivo_comentarios):
    '''[Autor: Ivan Litteri]
    [Ayuda: Esta funcion crea las listas de lineas de cada archivo que le llega por parametro, y devuelve listas
    con los datos de cada una de las listas de lineas pero procesadas]'''

    #Crea una lista de lineas del archivo fuente_unico.csv
    lineas_fuente = archivo_fuente.readlines()
    #Crea una lista de lineas del archivo comentarios.csv
    lineas_comentarios = archivo_comentarios.readlines()
    
    return obtener_datos_fuente(lineas_fuente), obtener_datos_comentarios(lineas_comentarios)

def leer_archivos_csv(nombre_archivo_fuente, nombre_archivo_comentarios):
    '''[Autor: Ivan Litteri]
    [Ayuda: esta funcion abre los archivos cuyos nombres o ubicaciones le llegan por parametro, y devuelve
    una lista de datos por cada archivo que lee, cuando termina la lectura, los cierra]'''

    #Abre los dos archivos que le llegan por parametro para su lectura
    with open(nombre_archivo_fuente, "r") as archivo_fuente, open(nombre_archivo_comentarios, "r") as archivo_comentarios:
        datos_archivo_fuente, datos_archivo_comentarios = obtener_datos_archivos_csv(archivo_fuente, archivo_comentarios)
    
    return datos_archivo_fuente, datos_archivo_comentarios

def guardar_datos_archivo_comentarios(datos_por_autor, datos_archivo_comentarios):
    '''[Autor: Ivan Litteri]
    [Ayuda: esta funcion interpreta y organiza los datos que le llegan por parametros (los cuales son las
    listas de listas de lineas de cada archivo csv) para que luego su acceso sea mas sencillo. Recorre
    la lista de lineas de comentarios antes que la lista de lineas de fuente porque los datos por autor se
    encuentran en dicha lista, entonces para que el diccionario de datos por autor quede organizado con los
    autores como keys es necesario que se recorra primero. Cuando termina esto, empieza a recorrer la lista de
    lineas de fuente para agregar a cada autor esas lineas, comparando si ese autor fue el creador de la
    funcion a la que pertenecen esas lineas]'''
    
    #Recorre la lista de comentarios 
    for datos_comentarios_funcion in datos_archivo_comentarios:
        #Declaro a el primer elemento de la lista para que sea mas facil comprender su uso
        nombre_funcion = datos_comentarios_funcion[0]
        #Declaro a el segundo elemento de la lista para que sea mas facil comprender su uso
        autor = datos_comentarios_funcion[1]
        #Recorta la lista desde la posicion 3 hasta el final, ya que se refiere a las lineas de comentarios adicionales
        comentarios_funcion = datos_comentarios_funcion[3:]
        #Crea el diccionario que pertenece al autor si no esta el nombre en el diccionario (solo sucede una vez)
        if autor not in datos_por_autor:
            datos_por_autor[autor] = {}
        #Crea la key y le da un value si no esta el nombre en el diccionario (solo sucede una vez)
        if nombre_funcion not in datos_por_autor[autor]:
            datos_por_autor[autor][nombre_funcion] = 0
        #Una vez creado el lugar a guardar, guarda la cantidad de lineas de comentarios que pertenecen a cada funcion
        datos_por_autor[autor][nombre_funcion] += len(comentarios_funcion)

def guardar_datos_archivo_fuente(datos_por_autor, datos_archivo_fuente):
    '''[Autor: Ivan Litteri]
    [Ayuda: A partir de aca, la logica que uso es que, cada autor, se guardo como key del diccionario de datos final,
    y cada value de ese diccionario es un diccionario que contiene a la funcion que creo ese autor como key, y a
    a la cantidad de lineas que pertenecen a esa funcion como value. Entonces en el recorrido de cada autor que sigue
    es necesario ya que comparo si el autor correspondiente a la iteracion creo la funcion que tomo del recorrido
    de la lista de lineas del archivo fuente, en caso de que eso coincida, se suma la cantidad de lineas de fuente
    a la cantidad de lineas de comentarios que ya tenia cargada cada funcion de cada autor.'''

    #Recorro los keys del diccionario, que corresponden a cada autor
    for autor in datos_por_autor:
        #Recorro la lista de lineas de fuente
        for datos_lineas_funcion in datos_archivo_fuente:
            nombre_funcion = datos_lineas_funcion[0]
            lineas_funcion = datos_lineas_funcion[3:]
            #Comparo que el nombre de funcion
            if nombre_funcion not in datos_por_autor[autor]:
                datos_por_autor[autor][nombre_funcion] = 0
            #Una vez creado el lugar a guardar, guarda la cantidad de lineas de fuente que pertenecen a cada funcion
            datos_por_autor[autor][nombre_funcion] += len(lineas_funcion)

def obtener_datos_por_autor(datos_archivo_fuente, datos_archivo_comentarios):
    datos_por_autor = {}

    guardar_datos_archivo_comentarios(datos_por_autor, datos_archivo_comentarios)
    guardar_datos_archivo_fuente(datos_por_autor, datos_archivo_fuente)

    return datos_por_autor

def imprimir_datos(datos_por_autor):
    lineas_totales = 0
    print("\t\t\tInformacion de Desarrollo Por Autor\n")
    for autor in datos_por_autor:
        lineas_totales = 0
        print(f'{autor}\n\n\tFuncion{" " * (50-len("Funcion"))}Lineas\n\n\t{"=" * (50+len("Funcion"))}\n')
        for funcion, lineas in datos_por_autor[autor].items():
            lineas_totales += lineas
            print(f'\t{funcion}{" " * (50-len(funcion))}{lineas}')
        print(f'\t{len(datos_por_autor[autor])} Funciones - Lineas{" " * (47-len("Funciones - Lineas"))}{lineas_totales}')


def main():
    nombre_archivo_comentarios = "comentarios.csv"
    nombre_archivo_fuente = "fuente_unico.csv"
    datos_archivo_fuente, datos_archivo_comentarios = leer_archivos_csv(nombre_archivo_fuente, nombre_archivo_comentarios)
    datos_por_autor = obtener_datos_por_autor(datos_archivo_fuente, datos_archivo_comentarios)
    imprimir_datos(datos_por_autor)

main()