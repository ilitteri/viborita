def buscar_invocaciones(datos_por_funciones):
    '''[Autor: Luciano Federico Aguilera]
    [Ayuda: Busca las funciones presentes en el diccionario creado anteriormente y las agrega en un diccionario con un numero de indice ]'''
    
    cuenta_lineas = 0
    diccionario_invocaciones = {"total": {} , "indices" : {} , "nombres" : {} }
    largo_maximo = 0 
    #Guardo las keys del diccionario como una tupla
    tupla_funciones = tuple(datos_por_funciones.keys())

    #Recorro la tupla de funciones
    for nombre_funcion in tupla_funciones:
        cuenta_lineas += 1
        #Guardo la funcion con mayor cantidad de caracteres
        if (len(nombre_funcion) > largo_maximo):
            largo_maximo = len(nombre_funcion)
        diccionario_invocaciones[cuenta_lineas] = {}
        diccionario_invocaciones[cuenta_lineas][nombre_funcion] = {}
        #Defino los totales para agregarlos posteriormente a la tabla
        diccionario_invocaciones["total"][cuenta_lineas] = 0
        # Agrego una key para relacionar los nombres de las variables con sus indices para ahorrar codigo
        diccionario_invocaciones["indices"][nombre_funcion] = cuenta_lineas
        # Tambien hago lo mismo para relacionar los indices con sus variables
        diccionario_invocaciones["nombres"][cuenta_lineas] = nombre_funcion
        #Una vez creado el diccionario defino en 0 las invocaciones de cada funcion dentro de las demas 
        for funcion in tupla_funciones :
            diccionario_invocaciones[cuenta_lineas][nombre_funcion][funcion] = 0
    largo_maximo += 3
    return diccionario_invocaciones, tupla_funciones, largo_maximo

def contar_interacciones(diccionario_invocaciones, tupla_funciones, datos_por_funciones):  
    '''[Autor: Luciano Federico Aguilera]
    [Ayuda : Busca coincidencias entre las funciones listadas en tupla_funciones y las presentes en la lista datos_por_funcion para su correspondiente funcion y agrego esa informacion en diccionario_invocaciones ]'''
   
    lineas = 0
    cuenta_linea = 0

    #Recorro los indices de las funciones listadas
    while (lineas < len(tupla_funciones)):
        nombre = tupla_funciones [lineas]
        cuenta_linea += 1
        funciones_llamadas = datos_por_funciones[nombre]["invocaciones"]
        # Esta cadena devuelve el nombre de la funcion al poner su indice     
        funcion_en_linea = diccionario_invocaciones["nombres"][cuenta_linea]
        # Aqui se agregan a su key correspondiente los totales de los indices mencionados anteriormente
        if (cuenta_linea <= len(diccionario_invocaciones)):
            for invocado in diccionario_invocaciones[cuenta_linea][funcion_en_linea]:
                    # Cuento las veces que se invoca a las funciones 
                    if (invocado in funciones_llamadas):
                        diccionario_invocaciones[cuenta_linea][funcion_en_linea][invocado] += funciones_llamadas.count(invocado)
                        # Esta cadena devuelve el nombre de la funcion al poner su indice correspondiente
                        indices = diccionario_invocaciones["indices"][invocado]
                        # Se cuentan todas las invocaciones por su respectivo indice 
                        diccionario_invocaciones["total"][indices] += funciones_llamadas.count(invocado)
        lineas += 1

    return diccionario_invocaciones


def creacion_formato_tabla(diccionario_invocaciones, largo_maximo):
    '''[Autor: Luciano Federico Aguilera]
    [Ayuda: Esta funcion recive el diccionario y largo de la funcion con mas caracteres para armar el formato de la tabla y devuelve una lista de lineas del archivo txt final]'''
    
    # Creo una lista cuyos elementos seran las lineas del archivo txt
    filas_txt = []
    indice_de_lineas = 1
    # Creo la primer y ultima linea del archivo de texto  
    filas_txt.append(f'\t FUNCIONES    {" " * (largo_maximo - 9)}|')
    cadena_totales = (f'\n\t Total Invocaciones   {" " * (largo_maximo-17)}|')

    # Agrego los nombres de las funciones junto con sus indices a todas las lineas restantes
    for funcion in diccionario_invocaciones:
        if str(funcion).isdigit():
            if funcion < 10 :
                filas_txt [0] += (f'   {funcion}  |') 
            else :
                filas_txt [0] += (f'  {funcion}  |') 
            funcion_en_linea = diccionario_invocaciones["nombres"][funcion]
            #Filtro el caracter "*" que fue usado para identificar a la funcion principal en otros modulos
            if ("*" in funcion_en_linea):
                funcion_en_linea = funcion_en_linea.replace("*","")
            #Apendeo la cadena de texto que corresponde al lateral izquierdo de la tabla e incluye a laas funciones y sus indices
            #fixed
            diferencia = largo_maximo - len(funcion_en_linea)
            if funcion < 10 :
                cadena_de_texto =  (f'\t   {indice_de_lineas} {funcion_en_linea}')
            else :
                cadena_de_texto =  (f'\t  {indice_de_lineas} {funcion_en_linea}')
            cadena_de_texto += " " * diferencia + "|"
            filas_txt.append(cadena_de_texto)
            indice_de_lineas += 1  

            # Concateno a los totales que estaban el el diccionario a la tabla
            if diccionario_invocaciones["total"][funcion] < 10 :
                cadena_totales += (f'   {diccionario_invocaciones["total"][funcion]}  |')
            else :
                cadena_totales += (f'  {diccionario_invocaciones["total"][funcion]}  |')
            
            
            #Corrijo el espaciado en caso de que el numero de funciones sea muy elevado
            
    filas_txt.append(cadena_totales)       

    return filas_txt

def asignacion_valores_tabla(filas_txt, diccionario_invocaciones):
    '''[Autor: Luciano Federico Aguilera]
    [Ayuda: Esta funcion recive filas_txt y agrega a las lineas el valor correspondiente a cada funcion tambien recibe diccionario_invocaciones ]'''

    for numero in diccionario_invocaciones:
        if str(numero).isdigit():
            # Esta cadena devuelve el nombre de la funcion si se ingresa su indice correspondiente
            funcion_en_linea = diccionario_invocaciones["nombres"][numero]
        
            for funcion in diccionario_invocaciones[numero][funcion_en_linea]:
                # Aqui agrego el caracteres correspondientes a cada funcion ("X", "numero" o "vacio")
                
                if (diccionario_invocaciones[numero][funcion_en_linea][funcion] > 0):
                    filas_txt[numero] +=(f'   {diccionario_invocaciones[numero][funcion_en_linea][funcion]}  |')
                else:
                    indice = diccionario_invocaciones["indices"][funcion]
                    if (diccionario_invocaciones[indice][funcion][funcion_en_linea] > 0):
                        filas_txt[numero] += ("   x  |")
                    else:
                        filas_txt[numero] += ("      |")
                #Corrijo el espaciado en caso de que el numero de funciones sea muy elevado
            
    return filas_txt
    

def creacion_archivo_txt(filas_txt):
    '''[Autor: Luciano Federico Aguilera]
    [Ayuda:Esta funcion crea un archivo txt llamado anatizador.txt e imprime las lineas por consola a partir de los elementos de la lista filas_txt]'''
    
    #Escribo el archivo txt a la vez que imprimo por pantalla
    with open("analizador.txt", "w") as analizador:
        separador = "_" * (len(filas_txt[0]))
        for linea in filas_txt:
            analizador.write(f'{linea}\n')
            analizador.write(f'    {separador}\n')
            print(f'{linea}')
            print("\t",separador)

def analizar_reutilizacion(datos_por_funciones):
    '''[Autor: Luciano Federico Aguilera]
    [Ayuda:Esta funcion sirve como main para llamar a las demas funciones]'''
    
    # Defino el nombre nombre del archivo que usamos para obtener los datos que fue creado en creador csv
    diccionario_invocaciones, tupla_funciones, largo_maximo = buscar_invocaciones(datos_por_funciones)
    diccionario_invocaciones = contar_interacciones(diccionario_invocaciones, tupla_funciones, datos_por_funciones)
    filas_txt = creacion_formato_tabla(diccionario_invocaciones, largo_maximo)
    filas_txt = asignacion_valores_tabla(filas_txt, diccionario_invocaciones)
    creacion_archivo_txt(filas_txt)