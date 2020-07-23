def declaracion_funcion(line, bandera_nombre = True, bandera_parametro = False):
    '''[Autor: Ivan Litteri]
    [Ayuda: esta funcion analiza la linea que le entra por parametro, previamente filtrada como linea de declaracion de funcion, de esta forma
    se recorre caracter a caracter la linea para ver cuando guardar los caracteres en la cadena de nombre, y cuando guardar los caracteres en 
    la cadena de parametros]'''

    #Declara inicialmente cadenas vacias para luego llenarla desde 0
    nombre_funcion = ""
    parametros_funcion = ""

    #Recorre caracter a caracter desde "def" en adelante la linea que le llega por parametro
    for caracter in line[3:]:
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
    [Ayuda: Esta funcion analiza la linea de codigo que anteriormente fue filtrada como posible contenedora de datos del autor de la funcion.
    Se analiza caracter a caracter la linea, y se habilita la bandera que permite que se empiecen a almacenar los caracteres que son parte de
    la informacion requerida.]'''

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
    [Ayuda: Esta funcion analiza la linea de codigo que le llega por parametro (sabiendo que se trata de una linea de ayuda de funcion;
    se recorre la linea caracter por caracter hasta hayar la apertura de un corchete que al mismo tiempo en esa linea este la palabra ayuda,
    si ese fuera el caso, se habilita la bandera para que cada caracter se sume a la cadena inicializada al principio como vacia. Esta funcion
    en particular, tambien devuelve el ultimo estado de la bandera de ayuda, porque al tratarse de comentarios multilinea, cuando se vuelva
    a llamar a esta funcion, puede ser que este comentario multilinea no haya sido cerrado, en esta caso, deben seguir siendo almacenadas
    las proximas lineas que vengan a ella por parametro hasta que se cierre el comentario.]'''

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

    if not linea_codigo.startswith("#"):
        #Recorre caracter a caracter la linea que entra por parametro
        for caracter in linea_codigo.strip(): 
            #Cuando el caracter se trate del numeral, se habilita la bandera para que se empiece a guardar caracteres en la cadena inicializada anteriormente
            if caracter == "#":
                bandera_linea = False
                bandera_otro_comentario = True
            if bandera_linea:
                posible_linea += caracter
            if bandera_otro_comentario:
                otro_comentario += caracter
    else:
        otro_comentario = linea_codigo

    return otro_comentario, posible_linea

def imports(linea_codigo, bandera_import = False):
    '''[Autor: Ivan Litteri]
    [Ayuda: esta funcion analiza la linea que le llega por parametro que anteriormente fue filtrada como
    linea de import, devuelve en caso de ser un import general un diccionario con el modulo importado como
    value; y un diccionario con una lista como value cuyo primer elemento es el modulo importado, y el segundo
    elemento es una lista de las funciones que se importaron de ese modulo.]'''

    datos_import = {}

    #Si la linea es del estilo import modulo...
    if linea_codigo.startswith("import"):
        datos["modulo_importado"] = [linea_codigo.split(" ")[1]]
    #Si la linea es del estilo from modulo import...
    elif linea_codigo.startswith("from"):
        recorte = linea_codigo.split(" ")
        datos["modulo_importado"] = [recorte[1], recorte[3:]]
    
    return datos_import

def largo_ayuda(ayuda):
    '''[Autor: Joel Glauber]
    [Ayuda: analiza un comentario de ayuda con mas de 80 caracteres, y devuelve el mismo, pero cada 80 caracteres, agrega
    un enter (para la grabacion del archivo de ayuda de funcion del punto 2)]'''

    #Declara una cadena vacia para llenar con los caracteres de el comentario de ayuda
    ayuda_recortada = ""
    #Declaro una variable global como 0 para usarla de indice
    i = 0
    while i < len(ayuda):
        #Si se llega a una posicion que es multiplo de 79 (cada vez que se llega a 80 caracteres de longitud) y agrega un enter
        if i % 79 == 0:
            ayuda_recortada += "\n"
        #Agregar el caracter a la cadena final
        ayuda_recortada += ayuda[i]
        #Incrementa el indice
        i += 1

    return ayuda_recortada

