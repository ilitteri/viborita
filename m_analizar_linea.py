def declaracion_funcion(linea_codigo, bandera_nombre = True, bandera_parametro = False):
    '''[Autor: Ivan Litteri]
    [Ayuda: le llega una linea de codigo filtrada como declaracion de funcion y devuelve el nombre de la funcion declarada y sus parametros por separado]'''

    #Declara inicialmente cadenas vacias para luego llenarla desde 0
    nombre_funcion = ""
    parametros_funcion = ""

    #Recorre caracter a caracter desde "def" en adelante la linea que le llega por parametro
    for caracter in linea_codigo[3:]:
        #Se guardan los caracteres en la cadena de parametros cuando esta habilitada la bandera
        if bandera_parametro:
            parametros_funcion += caracter
        #Se guardan los caracteres en la cadena de nombre cuando esta habilitada la bandera y siempre y cuando no se trate de espacios
        if not caracter.isspace() and caracter != "(" and bandera_nombre:
            nombre_funcion += caracter
        #Cuando aparece el caracter evaluado, se habilita la bandera para empezar a guardar los caracteres en la cadena de parametros y se deshabilita la bandera que permitia el almacenamiento de caracteres en la cadena de nombre
        elif caracter == "(":
            parametros_funcion += caracter
            bandera_nombre = False
            bandera_parametro = True
        #Se deshabilita la bandera que permitia el almacenamiento de caracteres en la cadena de parametros cuando se detecta que ya no se trata mas de uno
        elif caracter == ")":
            bandera_parametro = False

    return nombre_funcion, parametros_funcion

def autor_funcion(linea_codigo, bandera_autor = False):
    '''[Autor: Ivan Litteri]
    [Ayuda: Esta funcion analiza la linea de codigo que anteriormente fue filtrada como posible contenedora de datos del autor de la funcion. Se analiza 
    caracter a caracter la linea, y se habilita la bandera que permite que se empiecen a almacenar los caracteres que son parte de la informacion requerida.]'''

    #Declara inicialmente como una cadena vacia para luego llenarla desde 0
    autor_funcion = ""

    #Recorre caracter a caracter la linea que le entra por parametro
    for caracter in linea_codigo.strip():
        #Cuando se termine el comentario de autor, se deshabilita la bandera para que no se continuen guardando caracteres en la cadena.
        if caracter == "]" and bandera_autor:
            bandera_autor = False
        if bandera_autor:
            autor_funcion += caracter
        #Cuando el caracter se trate de una apertura de corchete y al mismo tiempo esa linea tenga la palabra autor, se habilita la bandera para que se almacenen caracteres en la cadena de autor.
        if caracter == "[" and ("Autor" in linea_codigo or "Autores" in linea_codigo):
            bandera_autor = True

    return autor_funcion

def ayuda_funcion(linea_codigo, bandera_ayuda):
    '''[Autor: Ivan Litteri]
    [Ayuda: le llega una linea de codigo, en caso de que la bandera este levantada directamente la concatena al string de ayuda y lo devuelve, si se encontrase baja
    se analiza, en caso verdadero se levanta. Tambien analiza si esta bandera se tiene que bajar.]'''

    #Declara inicialmente como una cadena vacia para luego llenarla desde 0
    ayuda_funcion = ""

    #Recorre caracter a caracter la linea que entra por parametro
    for caracter in linea_codigo.strip():
        #Cuando se termine el comentario de ayuda, se deshabilita la bandera para que no se continuen guardando caracteres en la cadena.
        if caracter == "]" and bandera_ayuda:
            bandera_ayuda = False
        if bandera_ayuda:
            ayuda_funcion += caracter
        #Cuando el caracter se trate de una apertura de corchete y al mismo tiempo esa linea tenga la palabra ayuda, se habilita la bandera para que se almacenen caracteres en la cadena de ayuda.
        if caracter == "[" and "Ayuda" in linea_codigo:
            bandera_ayuda = True

    return ayuda_funcion, bandera_ayuda

def comentario_numeral(linea_codigo, bandera_otro_comentario = False, bandera_linea = True):
    '''[Autor: Ivan Litteri]
    [Ayuda: Esta funcion analiza la linea que le llega por parametro (sabiendo que se trata de una linea que posiblemente tenga un comentario
    de linea simple, y devuelve solo desde el "#" en adelante)]'''

    #Declara inicialmente como una cadena vacia para luego llenarla desde 0
    otro_comentario = ""
    posible_linea = ""
    i = 0
    linea = linea_codigo.strip()

    if not linea_codigo.startswith("#"):
        #Recorre caracter a caracter la linea que entra por parametro
        while i < len(linea):
            #Cuando el caracter se trate del numeral, se habilita la bandera para que se empiece a guardar caracteres en la cadena inicializada anteriormente
            if linea[i] == "#":
                bandera_linea = False
                bandera_otro_comentario = True
            if bandera_linea:
                posible_linea += linea[i]
            if bandera_otro_comentario:
                otro_comentario += linea[i]
            i += 1
    else:
        otro_comentario = linea_codigo

    return otro_comentario, posible_linea

def largo_linea(linea):
    '''[Autor: Joel Glauber]
    [Ayuda: analiza una linea con mas de 80 caracteres, y devuelve el mismo, pero cada 80 caracteres, agrega
    un enter (para la grabacion del archivo de ayuda de funcion del punto 2)]'''

    #Declara una cadena vacia para llenar con los caracteres de el comentario de ayuda
    linea_formateada = ""
    #Declaro una variable global como 0 para usarla de indice
    i = 0
    while (i < len(linea)):
        #Si se llega a una posicion que es multiplo de 79 (cada vez que se llega a 80 caracteres de longitud) y agrega un enter
        if( i % 78 == 0) and (i != 0):
            if linea[i].isalpha():
                linea_recortada += "-\n"
            else:
                linea_recortada += "\n"
        #Agregar el caracter a la cadena final
        linea_recortada += linea[i]
        #Incrementa el indice
        i += 1

    return linea_formateada