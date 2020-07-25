
def buscar_invocaciones(datos_por_funciones):
    """[Autor: Luciano Federico Aguilera]
    [Ayuda: Busca las funciones presentes en el archivo csv creado anteriormente y las agrega en un diccionario con un numero de indice ]"""
    #Defino variables que se usaran
    
    cuenta_lineas = 0
    diccionario_invocaciones = {"total": {} , "indices" : {} }
    largo_maximo = 0 
    #Tomo las funciones recogidas en el diccionario principal de m_organizar_datos
    lista_funciones = list(datos_por_funciones.keys())
    #Creo un diccionario que servira posteriormente para el armado de la tabla
    for nombre_funcion in lista_funciones :
        # Aqui declaro la variable que estara en la tabla como indice para facilitar el manejo
        cuenta_lineas += 1
        if len(nombre_funcion) > largo_maximo :
            largo_maximo = len(nombre_funcion)
        #Defino un diccionario dentro de cada indice para organizar la informacion 
        diccionario_invocaciones [cuenta_lineas] = {}
        # Creo un  diccionario dentro del anterior para almacenar las funciones a la que pertenecen las lineas de codigo junto con sus invocaciones
        diccionario_invocaciones [cuenta_lineas] [nombre_funcion] = {}
        # Agrego una key que funciona como suma de las invocaciones para cada funcion
        diccionario_invocaciones ["total"] [cuenta_lineas] = 0
        # Agrego una key para relacionar los nombres de las variables con sus indices para ahorrar codigo
        diccionario_invocaciones ["indices"] [nombre_funcion] = cuenta_lineas
        # Seteo los contadores de las invocaciones en 0 
        for funcion in lista_funciones :
            diccionario_invocaciones [cuenta_lineas] [nombre_funcion] [funcion] = 0
    
    
    return diccionario_invocaciones , lista_funciones , largo_maximo

def contar_interacciones(diccionario_invocaciones , lista_funciones  , datos_por_funciones ):  

    """[Autor: Luciano Federico Aguilera]
    [Ayuda : Busca coincidencias entre las funciones listadas y las presentes en el archivo csv y las  ]"""
   
        #Recorro nuevamente el archivo para identificar invocaciones a funciones usando los datos recogidos en buscar_invocaciones
    lineas = 0
    cuenta_linea = 0
    while lineas < len(lista_funciones) :

        #Identifico que funcion es la que llama a las siguientes
        nombre = lista_funciones [lineas]
        cuenta_linea += 1
        #Obtengo una lista de las funciones llamadas del diccionario principal
        funciones_llamadas = datos_por_funciones[nombre]["invocaciones"]
        # Esta cadena devuelve el nombre de la funcion al poner su indice     
        funcion_en_linea = str(diccionario_invocaciones[cuenta_linea]).split(":")[0].replace("{", "").replace("'","")   
               
            # Aqui se agregan a su key correspondiente los totales y los indices mencionados anteriormente
        if cuenta_linea <= len(diccionario_invocaciones) :
            for invocado in diccionario_invocaciones[cuenta_linea][funcion_en_linea] :
                    # Cuento las veces que se invoca a las funciones 
                    if invocado in funciones_llamadas :
                        diccionario_invocaciones [cuenta_linea][funcion_en_linea][invocado] += funciones_llamadas.count(invocado)
                        
                        indices = diccionario_invocaciones ["indices"][invocado]
                        # Se cuentan todas las invocaciones por su respectivo indice 
                        diccionario_invocaciones ["total"][indices] += funciones_llamadas.count(invocado)

        lineas += 1
    
    
    # Devuelvo el diccionario actualizado
    return diccionario_invocaciones


def creacion_formato_tabla(diccionario_invocaciones , largo_maximo):
    """[Autor: Luciano Federico Aguilera]"""
    #Defino variables que usare mas adelante
    # Creo una lista cuyos elementos seran las lineas del archivo txt
    filas_txt = []
    indice_2 = 1

    # Creo la primer linea del archivo de texto  
    filas_txt.append(str("\t FUNCIONES" + "\t" + " "*(largo_maximo - 5)))
    cadena_totales = "\n\t Total Invocaciones " + "\t" + " "*(largo_maximo - 20)
    # Agrego los nombres de las funciones junto con sus indices a todas las lineas restantes
    for funcion in diccionario_invocaciones :
        # Filtro las keys que no contienen datos importantes
        if funcion != "total" and funcion != "indices":
            filas_txt [0] += "\t" + str(funcion) + "\t" 
            
            funcion_en_linea = str(diccionario_invocaciones[funcion]).split(":")[0].replace("{", "").replace("'","")
            # Hago correcciones para que la tabla quede pareja
            cadena_de_texto =  "\t" + " " + str(indice_2) + " " + str(funcion_en_linea).replace("*","") + "\t" + " " * (largo_maximo-len(str(funcion_en_linea)) )
            # Corrijo los espacios para que la tabla queda pareja
            if funcion <= 9 :
                cadena_de_texto += " "
            filas_txt.append(cadena_de_texto )
            indice_2 += 1  
            # Concateno a los totales que estaban el el diccionario a la tabla
            cadena_totales += "\t" + str(diccionario_invocaciones ["total"] [funcion]) + "\t"
    
    # Finalmente agrego la cadena a la lista
    filas_txt.append(cadena_totales )       
    # Devuelvo la lista modificada 
    return filas_txt

def asignacion_valores_tabla (filas_txt, diccionario_invocaciones) :

    """[Autor: Luciano Federico Aguilera]
    [Ayuda: Esta funcion agrega los numeros de invocaciones que hizo cada funcion]"""
    # Recorro las keys del diccionario para buscar los datos 

    for numero in diccionario_invocaciones :
        # Filtro las keys que no son funciones 
        if str(numero).isdigit() :
            funcion_en_linea = str(diccionario_invocaciones[numero]).split(":")[0].replace("{", "").replace("'","")
            # Recorro el diccionario por dentro para sacar los valores de cada funcion
            for funcion in diccionario_invocaciones[numero][funcion_en_linea]:
                # Intercambio los 0 para que la tabla quede como en el ejemplo del pdf del tp
                if diccionario_invocaciones[numero][funcion_en_linea][funcion] > 0 :
                    filas_txt[numero] += "\t" + str(diccionario_invocaciones[numero][funcion_en_linea][funcion]) + "\t"
                else:
                    filas_txt[numero] += "\t" + " " + "\t"
    # Devuelvo nuevamente la lista luego de modificarla
    return filas_txt
    

def creacion_archivo_txt (filas_txt) :
    """[Autor: Luciano Federico Aguilera]
    [Ayuda:Esta funcion crea un archivo txt llamado anatizador.txt a partir de los elementos de la lista filas_txt]"""
    # Creo un archivo txt
    with open("analizador.txt" , "w") as analizador :
        # Escribo el archivo de texto txt con las lineas ordenadas
        for linea in filas_txt:
            analizador.write(str(linea) + "\n" + "\n")
            print(str(linea) + "\n" + "\n")

def analizar_reutilizacion (datos_por_funciones) :
    """[Autor: Luciano Federico Aguilera]
    [Ayuda:Esta funcion sirve como main para llamar a las demas funciones]"""
    # Defino el nombre nombre del archivo que usamos para obtener los datos que fue creado en creador csv

    diccionario_invocaciones , lista_funciones , largo_maximo = buscar_invocaciones(datos_por_funciones )

    diccionario_invocaciones = contar_interacciones(diccionario_invocaciones , lista_funciones , datos_por_funciones )

    filas_txt  = creacion_formato_tabla(diccionario_invocaciones , largo_maximo)

    filas_txt = asignacion_valores_tabla (filas_txt, diccionario_invocaciones)

    creacion_archivo_txt (filas_txt)


