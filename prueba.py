datos_por_funciones = {'es_primo': {'parametros': '(valor)', 'modulo': 'lib_matematica.py', 'lineas': ['devolver = True', 'if valor <= 1:', 'devolver = False', 'else:', '', 'divisor = 2', 'while (((valor % divisor)!=0) and (divisor <= valor/2)):', 'divisor += 1', 'if divisor <= valor/2:', 'devolver = False', 'return devolver"\n'], 'cantidad_lineas': 11, 'invocaciones': [], 'cantidad_invocaciones': 1, 'cantidad_parametros': 1, 'cantidad_comentarios': 1, 'comentarios': {'autor': 'Autor: Juan Perez', 'ayuda': 'Ayuda: Evlua si el numero recibido es primo o no, devolviendo True encaso de serlo, y False en caso contrario.', 'otros': ['# Evaluacion de si el numero es primo"\n']}, 'cantidad_declaraciones': {'returns': 1, 'if/elif': 2, 'for': 0, 'while': 1, 'break': 0, 'exit': 0}}, 'factorial': {'parametros': '(n)', 'modulo': 'lib_matematica.py', 'lineas': ['resultado = 1', 'for i in range(2, n+1):', 'resultado = resultado * i', 'return resultado"\n'], 'cantidad_lineas': 4, 'invocaciones': [], 'cantidad_invocaciones': 1, 'cantidad_parametros': 1, 'cantidad_comentarios': 0, 'comentarios': {'autor': 'Autor: Juan Perez', 'ayuda': 'Ayuda: Calcula el factorial de el numero recibido, que debe sermayor o igual a cero', 'otros': None}, 'cantidad_declaraciones': {'returns': 1, 'if/elif': 0, 'for': 1, 'while': 0, 'break': 0, 'exit': 0}}, 'mcd': {'parametros': '(nro_1, nro_2)', 'modulo': 'lib_matematica.py', 'lineas': ['if abs(nro_1) < abs(nro_2):', 'menor = abs(nro_1)', 'mayor = abs(nro_2)', 'else:', 'menor = abs(nro_2)', 'mayor = abs(nro_1)', 'if menor == mayor == 0:', 'devovler = -1', 'elif menor == 0:', 'devolver = mayor', 'else:', 'dividendo = mayor', 'divisor = menor', 'resto = mayor % divisor', 'while resto != 0:', 'dividendo = divisor', 'divisor = resto', 'resto = dividendo % divisor', 'devolver = divisor', 'return devolver"\n'], 'cantidad_lineas': 20, 'invocaciones': [], 'cantidad_invocaciones': 2, 'cantidad_parametros': 2, 'cantidad_comentarios': 2, 'comentarios': {'autor': 'Autor: Ana Garcia', 'ayuda': 'Ayuda: Calcula el MCD entre los dos numeros recibidos, utilizando elmetodo de Euclides. En caso de no existir MCD, devolverÃ¡ -1.', 'otros': ['# Si ambos iguales a 0 no es posible mcd', '# Implementacion del algoritmo de Euclides"\n']}, 'cantidad_declaraciones': {'returns': 1, 'if/elif': 3, 'for': 0, 'while': 1, 'break': 0, 'exit': 0}}, 'mcm': {'parametros': '(nro_1, nro_2)', 'modulo': 'lib_matematica.py', 'lineas': ['return (nro_1 * nro_2)//mcd(nro_1, nro_2)"\n'], 'cantidad_lineas': 1, 'invocaciones': ['mcd'], 'cantidad_invocaciones': 1, 'cantidad_parametros': 2, 'cantidad_comentarios': 0, 'comentarios': {'autor': 'Autor: Ana Garcia', 'ayuda': 'Ayuda: Calcula el MCM (minimo comun multiplo) entre los dos numerosrecibidos. En caso de no existir, devolverÃ¡ -1.Para el calculo se utiliza mcm(a,b) = (a*b)/MCD(a,b)', 'otros': None}, 'cantidad_declaraciones': {'returns': 1, 'if/elif': 0, 'for': 0, 'while': 0, 'break': 0, 'exit': 0}}, 'menu_MCD': {'parametros': None, 'modulo': 'app_matematica.py', 'lineas': ["print('\\nMCD (Maximo comun divisor)')", "valor_1 = solicitar_valor('Numero 1: ', -100000, 100000 )", "valor_2 = solicitar_valor('Numero 2: ', -100000, 100000 )", 'print(\'El MCD es: \', lib_matematica.mcd(valor_1, valor_2), \'\\n\')"\n'], 'cantidad_lineas': 4, 'invocaciones': ['solicitar_valor', 'solicitar_valor', 'mcd'], 'cantidad_invocaciones': 1, 'cantidad_parametros': 1, 'cantidad_comentarios': 0, 'comentarios': {'autor': 'Autor: Juan Perez', 'ayuda': 'Ayuda: submenu de la opcion mcd', 'otros': None}, 'cantidad_declaraciones': {'returns': 0, 'if/elif': 0, 'for': 0, 'while': 0, 'break': 0, 'exit': 0}}, 'menu_MCM': {'parametros': None, 'modulo': 'app_matematica.py', 'lineas': ["print('\\nMCM (Minimo comun multiplo)')", "valor_1 = solicitar_valor('Numero 1: ', -100000, 100000 )", "valor_2 = solicitar_valor('Numero 2: ', -100000, 100000 )", 'print(\'El MCM es: \', lib_matematica.mcm(valor_1, valor_2), \'\\n\')"\n'], 'cantidad_lineas': 4, 'invocaciones': ['solicitar_valor', 'solicitar_valor', 'mcm'], 'cantidad_invocaciones': 1, 'cantidad_parametros': 1, 'cantidad_comentarios': 0, 'comentarios': {'autor': 'Autor: Juan Perez', 'ayuda': 'Ayuda: submenu de la opcion mcm', 'otros': None}, 'cantidad_declaraciones': {'returns': 0, 'if/elif': 0, 'for': 0, 'while': 0, 'break': 0, 'exit': 0}}, '*menu_elegir': {'parametros': None, 'modulo': 'app_matematica.py', 'lineas': ['menu_opciones()', "opcion = solicitar_valor('Opcion: ', 1, 6)", "print('-------------------------------')", 'while opcion != 6:', 'if opcion == 1:', 'menu_factorial()', 'elif opcion == 2:', 'menu_potencia()', 'elif opcion == 3:', 'menu_primo()', 'elif opcion == 4:', 'menu_MCD()', 'else:', 'menu_MCM()', 'menu_opciones()', "opcion = solicitar_valor('Opcion: ', 1, 6)", "print('-------------------------------')"], 'cantidad_lineas': 18, 'invocaciones': ['menu_opciones', 'solicitar_valor', 'menu_factorial', 'menu_potencia', 'menu_primo', 'menu_MCD', 'menu_MCM', 'menu_opciones', 'solicitar_valor'], 'cantidad_invocaciones': 1, 'cantidad_parametros': 1, 'cantidad_comentarios': 0, 'comentarios': {'autor': '', 'ayuda': None, 'otros': None}, 'cantidad_declaraciones': {'returns': 0, 'if/elif': 4, 'for': 0, 'while': 1, 'break': 0, 'exit': 0}}, 'menu_factorial': {'parametros': None, 'modulo': 'app_matematica.py', 'lineas': ["print('\\nCalculo de Factorial')", "valor = solicitar_valor('Numero: ', 0, 20)", 'print(\'El factorial es: \', lib_matematica.factorial(valor), \'\\n\')"\n'], 'cantidad_lineas': 3, 'invocaciones': ['solicitar_valor', 'factorial'], 'cantidad_invocaciones': 1, 'cantidad_parametros': 1, 'cantidad_comentarios': 0, 'comentarios': {'autor': 'Autor: Alan Gonzalez', 'ayuda': 'Ayuda: submenu de la opcion factorial', 'otros': None}, 'cantidad_declaraciones': {'returns': 0, 'if/elif': 0, 'for': 0, 'while': 0, 'break': 0, 'exit': 0}}, 'menu_opciones': {'parametros': None, 'modulo': 'app_matematica.py', 'lineas': ["print('-------------------------------')", "print('MENU DE OPERACIONES MATEMATICAS')", 'print()', "print('1. Factorial')", "print('2. Potencia')", "print('3. Primo')", "print('4. MCD (Maximo Comun Divisor)')", "print('5. MCM (Minimo Comun Multiplo)')", "print('6. Terminar')", 'print()"\n'], 'cantidad_lineas': 10, 'invocaciones': [], 'cantidad_invocaciones': 2, 'cantidad_parametros': 1, 'cantidad_comentarios': 0, 'comentarios': {'autor': 'Autor: Alan Gonzalez', 'ayuda': 'Ayuda: Menu de opciones', 'otros': None}, 'cantidad_declaraciones': {'returns': 0, 'if/elif': 0, 'for': 0, 'while': 0, 'break': 0, 'exit': 0}}, 'menu_potencia': {'parametros': None, 'modulo': 'app_matematica.py', 'lineas': ["print('\\nCalculo de Potencia')", "base = solicitar_valor('Base: ', -100, 100)", "exponente = solicitar_valor('Exponente: ', -100, 100)", 'print(\'La potencia es: \', lib_matematica.potencia(base, exponente), \'\\n\')"\n'], 'cantidad_lineas': 4, 'invocaciones': ['solicitar_valor', 'solicitar_valor', 'potencia'], 'cantidad_invocaciones': 1, 'cantidad_parametros': 1, 'cantidad_comentarios': 0, 'comentarios': {'autor': 'Autor: Juan Perez', 'ayuda': 'Ayuda: submenu de la opcion Potencia', 'otros': None}, 'cantidad_declaraciones': {'returns': 0, 'if/elif': 0, 'for': 0, 'while': 0, 'break': 0, 'exit': 0}}, 'menu_primo': {'parametros': None, 'modulo': 'app_matematica.py', 'lineas': ["print('\\nEvaluar Primo')", "valor = solicitar_valor('Numero: ', -100000, 100000)", 'print(\'Es Primo\\n\' if lib_matematica.es_primo(valor) else \'No es primo\\n\')"\n'], 'cantidad_lineas': 3, 'invocaciones': ['solicitar_valor', 'es_primo'], 'cantidad_invocaciones': 1, 'cantidad_parametros': 1, 'cantidad_comentarios': 0, 'comentarios': {'autor': 'Autor: Alan Gonzalez', 'ayuda': 'Ayuda: submenu de la opcion primo', 'otros': None}, 'cantidad_declaraciones': {'returns': 0, 'if/elif': 1, 'for': 0, 'while': 0, 'break': 0, 'exit': 0}}, 'potencia': {'parametros': '(base, exponente)', 'modulo': 'lib_matematica.py', 'lineas': ['resultado = base', 'for i in range(2, abs(exponente) +1):', 'resultado *= base', 'if exponente == 0:', 'resultado = 1', 'elif exponente < 0:', 'resultado = 1 / resultado', 'return resultado"\n'], 'cantidad_lineas': 8, 'invocaciones': [], 'cantidad_invocaciones': 1, 'cantidad_parametros': 2, 'cantidad_comentarios': 0, 'comentarios': {'autor': 'Autor: Ana Garcia', 'ayuda': 'Ayuda: Calcula la potencia de la base elevada al exponente reibidopor parametros', 'otros': None}, 'cantidad_declaraciones': {'returns': 1, 'if/elif': 2, 'for': 1, 'while': 0, 'break': 0, 'exit': 0}}, 'solicitar_valor': {'parametros': '(mensaje, minimo, maximo)', 'modulo': 'app_matematica.py', 'lineas': ['valor = input(mensaje)', 'while (not valor.isdigit()) or ((int(valor) < minimo) or (int(valor) > maximo)):', "print('Error: Valor debe estar entre', minimo, 'y', maximo)", 'valor = input(mensaje)', 'return int(valor)"\n'], 'cantidad_lineas': 5, 'invocaciones': [], 'cantidad_invocaciones': 10, 'cantidad_parametros': 3, 'cantidad_comentarios': 0, 'comentarios': {'autor': 'Autor: Juan Perez', 'ayuda': 'Ayuda: Solicitar el ingreso de un valor y devolverlo, asegurando queestara entre el minimo y el maximo pasado por parametro', 'otros': None}, 'cantidad_declaraciones': {'returns': 1, 'if/elif': 0, 'for': 0, 'while': 1, 'break': 0, 'exit': 0}}}
def buscar_invocaciones(datos_por_funciones):
    """[Autor: Luciano Federico Aguilera]
    [Ayuda: Busca las funciones presentes en el archivo csv creado anteriormente y las agrega en un diccionario con un numero de indice ]"""
    #Defino variables que se usaran
    
    cuenta_lineas = 0
    diccionario_invocaciones = {"total": {} , "indices" : {} , "nombres" : {} }
    largo_maximo = 0 
    #Tomo las funciones recogidas en el diccionario principal de m_organizar_datos
    tupla_funciones = tuple(datos_por_funciones.keys())
    #Creo un diccionario que servira posteriormente para el armado de la tabla
    for nombre_funcion in tupla_funciones :
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
        diccionario_invocaciones ["nombres"] [cuenta_lineas] = nombre_funcion
        
        # Seteo los contadores de las invocaciones en 0 
        for funcion in tupla_funciones :
            diccionario_invocaciones [cuenta_lineas] [nombre_funcion] [funcion] = 0
    
    
    return diccionario_invocaciones , tupla_funciones , largo_maximo

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
        
        #funcion_en_linea = str(diccionario_invocaciones[cuenta_linea]).split(":")[0].replace("{", "").replace("'","")   
        funcion_en_linea = diccionario_invocaciones["nombres"][cuenta_linea]       
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
    """[Autor: Luciano Federico Aguilera]
    [Ayuda: Esta funcion recive el diccionario y largo de la funcion con mas caracteres para armar el formato de la tabla y devuelve una lista de lineas del archivo txt final]"""
    #Defino variables que usare mas adelante
    # Creo una lista cuyos elementos seran las lineas del archivo txt
    filas_txt = []
    indice_2 = 1

    # Creo la primer linea del archivo de texto  
    filas_txt.append(f'\t FUNCIONES\t{" "*(largo_maximo - 5)}')
    cadena_totales = (f'\n\t Total Invocaciones{" "*(largo_maximo - 30)}')
    # Agrego los nombres de las funciones junto con sus indices a todas las lineas restantes
    for funcion in diccionario_invocaciones :
        # Filtro las keys que no contienen datos importantes
        if str(funcion).isdigit() :
            
            filas_txt [0] += (f'\t{funcion}\t') 
            
            #funcion_en_linea = str(diccionario_invocaciones[funcion]).split(":")[0].replace("{", "").replace("'","")
            
            funcion_en_linea = diccionario_invocaciones["nombres"][funcion]
            
            if "*" in funcion_en_linea :
                funcion_en_linea = funcion_en_linea.replace("*","")
            # Hago correcciones para que la tabla quede pareja
            cadena_de_texto =  f'\t {indice_2} {funcion_en_linea}\t{" " * (largo_maximo-len(str(funcion_en_linea)) )}'
            # Corrijo los espacios para que la tabla queda pareja
            if funcion <= 9 :
                cadena_de_texto += " "
            filas_txt.append(cadena_de_texto )
            indice_2 += 1  
            # Concateno a los totales que estaban el el diccionario a la tabla
            cadena_totales += (f'\t{diccionario_invocaciones ["total"] [funcion]}\t')
    
    # Finalmente agrego la cadena a la lista
    filas_txt.append(cadena_totales )       
    # Devuelvo la lista modificada 
    return filas_txt

def asignacion_valores_tabla (filas_txt, diccionario_invocaciones , lista_funciones) :

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
                    filas_txt[numero] +=(f'\t{diccionario_invocaciones[numero][funcion_en_linea][funcion]}\t')

                else:
                    indice = diccionario_invocaciones["indices"][funcion]
                    if diccionario_invocaciones[indice][funcion][funcion_en_linea] > 0  :
                        filas_txt[numero] += (f'\tX\t')
                    else :
                        filas_txt[numero] += (f'\t \t')

    # Devuelvo nuevamente la lista luego de modificarla
    return filas_txt
    

def creacion_archivo_txt (filas_txt) :
    """[Autor: Luciano Federico Aguilera]
    [Ayuda:Esta funcion crea un archivo txt llamado anatizador.txt a partir de los elementos de la lista filas_txt]"""
    # Creo un archivo txt
    with open("analizador.txt" , "w") as analizador :
        # Escribo el archivo de texto txt con las lineas ordenadas
        for linea in filas_txt:
            analizador.write(f'{linea}\n\n')
            print(f'{linea}\n\n')

def analizar_reutilizacion (datos_por_funciones) :
    """[Autor: Luciano Federico Aguilera]
    [Ayuda:Esta funcion sirve como main para llamar a las demas funciones]"""
    # Defino el nombre nombre del archivo que usamos para obtener los datos que fue creado en creador csv

    diccionario_invocaciones , lista_funciones , largo_maximo = buscar_invocaciones(datos_por_funciones )

    diccionario_invocaciones = contar_interacciones(diccionario_invocaciones , lista_funciones , datos_por_funciones )

    filas_txt  = creacion_formato_tabla(diccionario_invocaciones , largo_maximo)

    filas_txt = asignacion_valores_tabla (filas_txt, diccionario_invocaciones , lista_funciones)

    creacion_archivo_txt (filas_txt)


analizar_reutilizacion(datos_por_funciones)