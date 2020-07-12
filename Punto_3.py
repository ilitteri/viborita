
def buscar_invocaciones(diccionario_invocaciones , lineas):
    """[Autor: Luciano Federico Aguilera]"""
    #Abro el archivo creado anteriormente que contiene los datos ordenados
    with open ("archivo_fuente", "r") as invocaciones :
        #Creo un diccionario para almacenar los nombres de las funciones
        diccionario_invocaciones = {}
        nombres = invocaciones.readline()
        #Recorro las lineas del archivo 
        while nombres :
            nombre = nombres.splitline('","')[0]
            #Almaceno los nombres de las funciones como keys del diccionario
            #Para poder identificarlos de encontrarse entre las lineas de codigo
            diccionario_invocaciones[nombre] = []
    
            funciones = invocaciones.readline()  
        
        lineas = invocaciones.readline()
        #Recorro nuevamente el archivo para identificar invocaciones a funcione
        while lineas :
            #Identifico que funcion es la que llama a las siguientes
            nombre = lineas.splitline('","')[0]
            #Separo las lineas que contienen codigo
            llamadas = lineas.splitline('","')[3:]

            for llamada in llamadas :
                #Separo la funcion de su contenido (...)
                funcion = llamada.splitlines("(")[0]
                if " " in funcion :
                    funcion_limpia = funcion.replace(" ","")

                #Busco funciones con nombres existentes en el diccionario
                if funcion_limpia in diccionario_invocaciones:
                    #Creo listas dentro del diccionario 
                    diccionario_invocaciones[nombre] = []
                    #Agrego las funciones encontradas en una lista para facilitar operaciones
                    diccionario_invocaciones[nombre].append(funcion_limpia)
            lineas = invocaciones.readline()
    return diccionario_invocaciones

def contar_interacciones(diccionario_invocaciones):
    """[Autor: Luciano Federico Aguilera]"""
    
    #Creo un nuevo diccionario que tiene las funciones sin repetir 
    diccionario_funciones = {}
    for funcion in diccionario_invocaciones :
        #Cuento su numero de llamadas
        for invocacion in diccionario_invocaciones[funcion]:
            numero_llamadas = diccionario_invocaciones[funcion].count(invocacion)
            diccionario_funciones[funcion][invocacion] =  numero_llamadas
    return diccionario_funciones

def creacion_formato_tabla(diccionario_funciones):
    """[Autor: Luciano Federico Aguilera]"""
    #Defino variables que usare mas adelante
    texto_max = 0
    numero_tabla = 1
    filas_txt = []
    filas_txt [0] = ""
    indice = 1
    indice_2 = 0
    total_invocado = []
    #Esta funcion sirve para que los nommbres no queden demaciado largos para el formato que se quiere
    for funcion in diccionario_funciones.keys():
        if len(funcion+"\t") > texto_max :
            texto_max = len(funcion)
            correccion_espaciado = " " * (texto_max - len(funcion))
            numero_tabla += 1
        filas_txt.append(str( " ",numero_tabla," - ",funcion,correccion_espaciado, "\t"*2 ))
        while indice < len (diccionario_funciones[funcion]) :
            if diccionario_funciones[funcion][indice_2] != 0 :
                filas_txt[indice_2+1] = " " * 3
                total_invocado.append(0)
            else :
                filas_txt[indice_2+1] = " " + str(diccionario_funciones[funcion][indice_2]) + " "
                total_invocado.append(diccionario_funciones[funcion][indice_2])
            indice_2 += 1
    filas_txt [0] = (str(" ","FUNCIONES",correccion_espaciado, "\t"*2))

    while indice <= numero_tabla :
        filas_txt[0] += " "+str(indice)+" "
        indice += 1 
    correccion_espaciado_total = texto_max
    filas_txt [numero_tabla+1] = str("Total Invocaciones",correccion_espaciado,"\t"*2 )
    for invocaciones_count in total_invocado :
        filas_txt [numero_tabla+1] = filas_txt[numero_tabla+1] + " " + invocaciones_count + " "
    return filas_txt

def creacion_archivo_txt (filas_txt) :
    """[Autor: Luciano Federico Aguilera]"""
    # Escribo el archivo de texto txt con las lineas ordenadas
    with open("analizador.txt" , "w") as analizador :
        for linea in filas_txt:
            analizador.write(linea)

    