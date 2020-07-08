
def obtencion_datos(archivo_fuente):
    
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
    with open ("archivo_fuente", "r") as invocaciones :
        lineas = invocaciones.readline()
        while lineas :
            nombre = lineas.splitline('","')[0]
            llamadas = lineas.splitline('","')[3:]
            for llamada in llamadas :
                if  llamadas in diccionario_invocaciones.keys():
                    diccionario_invocaciones[nombre].append(llamada)
                else :
                    diccionario_invocaciones[nombre] = []
    return diccionario_invocaciones

def contar_interacciones(diccionario_invocaciones):
    
    #Creo un nuevo diccionario que tiene las funciones sin repetir 
    diccionario_funciones = {}
    for funcion in diccionario_invocaciones :
        #Cuento su numero de llamadas
        for invocacion in diccionario_invocaciones[funcion]:
            numero_llamadas = diccionario_invocaciones[funcion].count(invocacion)
            diccionario_funciones[funcion][invocacion] =  numero_llamadas
    return diccionario_funciones

def creacion_archivo_txt_p3(diccionario_funciones):
    texto_max = 0
    numero_tabla = 1
    filas_txt = []
    columnas_txt = []
    lineas_txt[0] = filas_txt
    lineas_txt[1] = columnas_txt
    filas_txt [0] = None
    indice = 1
    indice_2 = 0
    
    for funcion in diccionario_funciones.keys():
        if len(funcion+"\t") > texto_max :
            texto_max = len(funcion)
            correccion_espaciado = texto_max - len(funcion)
            numero_tabla += 1
        filas_txt.append(str( " ",numero_tabla," - ",funcion,correccion_espaciado, "\t"*2 ))
        while indice < len (diccionario_funciones[funcion]) :
            if diccionario_funciones[funcion][indice_2] != 0 :
                filas_txt[indice_2+1] = " " * 3
            else :
                filas_txt[indice_2+1] = " " + str(diccionario_funciones[funcion][indice_2]) + " "
            indice_2 += 1
    filas_txt [0] = (str(" ","FUNCIONES",correccion_espaciado, "\t"*2))
    while indice <= numero_tabla :
        filas_txt[0] += " "+str(indice)+" "
        indice += 1 
       
    