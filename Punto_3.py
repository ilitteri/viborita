
def buscar_invocaciones(archivo_fuente):
    """[Autor: Luciano Federico Aguilera]"""
    lista_funciones = []
    cuenta_lineas = 0

    #Abro el archivo creado anteriormente que contiene los datos ordenados
    with open ( archivo_fuente , "r") as invocaciones :
        #Creo un diccionario para almacenar los nombres de las funciones
        diccionario_invocaciones = {"total": {} , "indices" : {} }
        nombres = invocaciones.readline()
        #Recorro las lineas del archivo 
        while nombres :
            nombre = (nombres.split('","')[0]).replace('"','')
            lista_funciones.append(nombre)
            #Almaceno los nombres de las funciones como keys del diccionario
            #Para poder identificarlos de encontrarse entre las lineas de codigo

            nombres = invocaciones.readline()  
    
    for key in lista_funciones :
        cuenta_lineas += 1
        diccionario_invocaciones [cuenta_lineas] = {}
        
        diccionario_invocaciones [cuenta_lineas] [key] = {}
        diccionario_invocaciones ["total"] [cuenta_lineas] = 0
        diccionario_invocaciones ["indices"] [key] = cuenta_lineas

        for funcion in lista_funciones :
            diccionario_invocaciones [cuenta_lineas] [key] [funcion] = 0
    
    
    return diccionario_invocaciones , lista_funciones    

def contar_interacciones(diccionario_invocaciones , lista_funciones , archivo_fuente):  

    with open ( archivo_fuente , "r") as invocaciones :
        lineas = invocaciones.readline()
        #Recorro nuevamente el archivo para identificar invocaciones a funcione
        cuenta_linea = 0
        while lineas :
            #Identifico que funcion es la que llama a las siguientes
            nombre = (lineas.split('","')[0]).replace('"','')
            #Separo las lineas que contienen codigo
            codigo = lineas.split('","')[3:]
            funciones_llamadas = []
            cuenta_linea += 1
            funcion_en_linea = str(diccionario_invocaciones[cuenta_linea]).split(":")[0].replace("{", "").replace("'","")

            for llamadas in codigo :
                #Separo la funcion de su contenido (...)
                llamada = llamadas.split("(")[0]
                for funcion in lista_funciones :
                    if funcion in llamada :
                        funciones_llamadas.append(funcion)
            if cuenta_linea <= len(diccionario_invocaciones) :
                for invocado in diccionario_invocaciones[cuenta_linea][funcion_en_linea] :
                        if invocado in funciones_llamadas :
                            diccionario_invocaciones [cuenta_linea][funcion_en_linea][invocado] += 1

                            contador = diccionario_invocaciones ["indices"][invocado]

                            diccionario_invocaciones ["total"][contador] += 1

            lineas = invocaciones.readline()

    return diccionario_invocaciones


def creacion_formato_tabla(diccionario_invocaciones):
    """[Autor: Luciano Federico Aguilera]"""
    #Defino variables que usare mas adelante
    filas_txt = []
    indice_2 = 1
    
    filas_txt.append(str(" FUNCIONES" + " "*20 ))
    for numero in range(len (diccionario_invocaciones)-2):
        filas_txt [0] += "\t" + str(numero+1) + "\t" 
    filas_txt[0] += " \n"

    for funcion in diccionario_invocaciones :
        if funcion != "total" and funcion != "indices":
            funcion_en_linea = str(diccionario_invocaciones[funcion]).split(":")[0].replace("{", "").replace("'","")
            
            cadena_de_texto =  "\t" + " " + str(indice_2) + " " + str(funcion_en_linea) + " " + " " * (22-len(str(funcion_en_linea)) )
            if funcion <= 9 :
                cadena_de_texto += " "
            filas_txt.append(cadena_de_texto )
            indice_2 += 1  
    cadena_totales = "\n Total Invocaciones " + " "*11
    for numero in range(1,len (diccionario_invocaciones)-1) :
        cadena_totales += "\t" + str(diccionario_invocaciones ["total"] [numero]) + "\t"  
        
    filas_txt.append(cadena_totales )       

   
    
    return filas_txt

def asignacion_valores_tabla (filas_txt, diccionario_invocaciones) :

    for numero in diccionario_invocaciones :
        if str(numero).isdigit() :
            funcion_en_linea = str(diccionario_invocaciones[numero]).split(":")[0].replace("{", "").replace("'","")
            for funcion in diccionario_invocaciones[numero][funcion_en_linea]:
                if diccionario_invocaciones[numero][funcion_en_linea][funcion] > 0 :
                    filas_txt[numero] += "\t" + str(diccionario_invocaciones[numero][funcion_en_linea][funcion]) + "\t"
                else:
                    filas_txt[numero] += "\t" + " " + "\t"
    
    return filas_txt
    

def creacion_archivo_txt (filas_txt) :
    """[Autor: Luciano Federico Aguilera]"""
    # Escribo el archivo de texto txt con las lineas ordenadas
    with open("analizador.txt" , "w") as analizador :

        for linea in filas_txt:
            analizador.write(str(linea) + "\n" + "\n")

def main () :
    archivo_fuente = "fuente_unico.csv"
    diccionario_invocaciones , lista_funciones = buscar_invocaciones(archivo_fuente)
    diccionario_invocaciones = contar_interacciones(diccionario_invocaciones , lista_funciones , archivo_fuente)
    filas_txt  = creacion_formato_tabla(diccionario_invocaciones)
    filas_txt = asignacion_valores_tabla (filas_txt, diccionario_invocaciones)
    
    creacion_archivo_txt (filas_txt)

main ()


