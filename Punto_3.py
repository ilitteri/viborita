
def obtencion_datos(archivo_fuente):
    """
    Abro el .csv generado en creador_csv.py y creo un diccionario 
    que contiene una lista de las invocaciones de cada fincion
    """
    with open ("archivo_fuente", "r") as informacion:
        funcion = informacion.splitline()
        diccionario_invocaciones = {}
        while funcion :
            nombre = funcion.splitline(",")[0]
            diccionario_invocaciones[nombre] = []
            for linea in funcion :
                if "import" in linea :   
                    invocado = linea.splitline("import")[1]
                    if "," in invocado :
                        invocaciones = invocado.split(",")
                    diccionario_invocaciones[nombre].append(invocado)                  
            funciones = informacion.readline()
    return diccionario_invocaciones

def contar_interacciones(diccionario_invocaciones):
    """
    Creo un nuevo diccionario que tiene las funciones sin repetir 
    y su numero de llamadas
    """
    diccionario_funciones = {}
    for funcion in diccionario_invocaciones :
        for invocacion in diccionario_invocaciones[funcion]:
            numero_llamadas = diccionario_invocaciones[funcion].count(invocacion)
            diccionario_funciones[funcion][invocacion] =  numero_llamadas
    return diccionario_funciones

"""
En proceso....

def imprimir_ej3(archivo_fuente):
    
    largo_nombre = 0
    valores = ""
    for i in range(len(nombres)):
        valores += str(i) + "\t"
    print ("Funciones","\t",valores)
    for i in range((len(nombres)-1)) :
        
        if len(nombres[i]> largo_nombre) :
            largo_nombre = len(Nombres[i]) + 4
        print (i+1, " - " , Nombres[i],"\n")
    print ("Total invocaciones","  ",)
"""