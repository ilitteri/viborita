
def obtencion_datos(archivo_fuente):
    """[Autor: Luciano Federico Aguilera]"""
    #Abro el .csv generado en creador_csv.py 
    with open ("archivo_fuente", "r") as informacion:
        funciones = informacion.readline()
        diccionario_invocaciones = {}
        #Creo un diccionario que contiene una lista de las invocaciones de cada funcion
        while funciones :
            nombre = funciones.splitline('","')[0]
            diccionario_invocaciones[nombre] = []
            #Filtro las lineas que no son de codigo
            lineas = funciones.splitline('","')[3:]
            for linea in lineas :
                for funcion in linea :
                    if "import" in funcion :
                        #Busco las invocaciones dentro de las lineas de codigo   
                        invocado = linea.splitline("import")[1]
                        #Agrego un if para agregar invocaciones de varias funciones en un mismo import
                        if "," in invocado :
                            invocaciones = invocado.split(",")
                            for funcion_invocada in invocaciones :
                                diccionario_invocaciones[nombre].append(funcion_invocada) 
                        else :
                                diccionario_invocaciones[nombre].append(invocaciones)                  
            funciones = informacion.readline()
            #Devuelvo el diccionario 
    return diccionario_invocaciones

def buscar_invocaciones(diccionario_invocaciones):
    """[Autor: Luciano Federico Aguilera]"""

    with open ("archivo_fuente", "r") as invocaciones :
        lineas = invocaciones.readline()
        while lineas :
            nombre = lineas.splitline('","')[0]
            llamadas = lineas.splitline('","')[3:]
            for llamada in llamadas :
                if llamada not in diccionario_invocaciones:
                    diccionario_invocaciones[nombre] = []
                diccionario_invocaciones[nombre].append(llamada)
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

    texto_max = 0
    numero_tabla = 1
    filas_txt = []
    filas_txt [0] = ""
    indice = 1
    indice_2 = 0
    total_invocado = []
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
    
    with open("analizador.txt" , "w") as analizador :
        for linea in filas_txt:
            analizador.write(linea)

    