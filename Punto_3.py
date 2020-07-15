
def buscar_invocaciones(archivo_fuente):
    """[Autor: Luciano Federico Aguilera]"""
    #Abro el archivo creado anteriormente que contiene los datos ordenados
    with open ( archivo_fuente , "r") as invocaciones :
        #Creo un diccionario para almacenar los nombres de las funciones
        diccionario_invocaciones = {}
        nombres = invocaciones.readline()
        #Recorro las lineas del archivo 
        while nombres :
            nombre = (nombres.split('","')[0]).replace('"','')
            #Almaceno los nombres de las funciones como keys del diccionario
            #Para poder identificarlos de encontrarse entre las lineas de codigo
            diccionario_invocaciones[nombre] = [nombre]
        

    
            nombres = invocaciones.readline()  
    print("\n" , diccionario_invocaciones , "\n")    

    with open ( archivo_fuente , "r") as invocaciones :
        lineas = invocaciones.readline()
        #Recorro nuevamente el archivo para identificar invocaciones a funcione
        while lineas :
            #Identifico que funcion es la que llama a las siguientes
            nombre = (lineas.split('","')[0]).replace('"','')
            #Separo las lineas que contienen codigo
            llamadas = lineas.split('","')[3:]
            for llamada in llamadas :
                #Separo la funcion de su contenido (...)
                for funcion in diccionario_invocaciones :
                    if funcion in llamada and funcion != nombre :
                        
                        diccionario_invocaciones[nombre].append(funcion)
            
            lineas = invocaciones.readline()
    print ("\n" , diccionario_invocaciones , "\n" )

    return diccionario_invocaciones

def contar_interacciones(diccionario_invocaciones):
    """[Autor: Luciano Federico Aguilera]"""
    
    #Creo un nuevo diccionario que tiene las funciones sin repetir 
    diccionario_funciones = {}
    for key in diccionario_invocaciones :

        #Cuento su numero de llamadas
    
        for invocacion in diccionario_invocaciones[key]:
            if invocacion is not key :
                diccionario_funciones [key] = {invocacion : diccionario_invocaciones[key].count(invocacion)}
            else :
                diccionario_funciones [key] = {invocacion : 0}
    print (diccionario_funciones)
    return diccionario_funciones

def creacion_formato_tabla(diccionario_funciones):
    """[Autor: Luciano Federico Aguilera]"""
    #Defino variables que usare mas adelante
    texto_max = 0
    numero_tabla = 1
    filas_txt = []
    indice = 1
    indice_2 = 1
    indice_3 = 1
    invocacion = 0
    total_invocado = []
    relacion_indices = {}
    #Esta funcion sirve para que los nommbres no queden demaciado largos para el formato que se quiere
    filas_txt.append(str(" FUNCIONES" + " "*20 ))
    for numero in range(len (diccionario_funciones)):
        filas_txt [0] += "\t" + str(numero+1) + "\t" 
    filas_txt[0] += " \n"

    for funcion in diccionario_funciones :
        relacion_indices [indice_3] = str(funcion)
        indice_3 += 1
        for invocacion in diccionario_funciones[funcion] : 
            cadena_de_texto =  "\t" + " " + str(indice_2) + " " + str(invocacion) + " " + " " * (20-len(str(invocacion)) )
            filas_txt.append(cadena_de_texto )
            indice_2 += 1  
        
    #print(relacion_indices)  
    
    return filas_txt , relacion_indices

def asignacion_valores_tabla (filas_txt, relacion_indices , diccionario_funciones) : 
    suma_filas = {}
    for fila in range (1,len(filas_txt)) :
        for funcion in diccionario_funciones[relacion_indices[fila]] :
        
            cantidad = int(diccionario_funciones[relacion_indices[fila]][funcion])
            
            filas_txt [fila] += ("\t" + str(cantidad) + "\t") 
            suma_filas = {fila : cantidad}
    return filas_txt
    
def creacion_archivo_txt (filas_txt) :
    """[Autor: Luciano Federico Aguilera]"""
    # Escribo el archivo de texto txt con las lineas ordenadas
    with open("analizador.txt" , "w") as analizador :

        for linea in filas_txt:
            analizador.write(linea + "\n")

def main () :
    archivo_fuente = "fuente_unico.csv"
    diccionario_invocaciones = buscar_invocaciones(archivo_fuente)
    diccionario_funciones = contar_interacciones(diccionario_invocaciones)
    filas_txt , relacion_indices = creacion_formato_tabla(diccionario_funciones)
    filas_txt = asignacion_valores_tabla (filas_txt, relacion_indices , diccionario_funciones)
    creacion_archivo_txt (filas_txt)

main ()


