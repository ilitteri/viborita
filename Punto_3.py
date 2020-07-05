"""
 Abro el .csv generado en creador_csv.py y creo un diccionario 
  que contiene una lista de las invocaciones de cada fincion
"""
def obtencion_datos(archivo_fuente):
    with open ("archivo_fuente", "r") as informacion:
        funcion = informacion.splitline()
        diccionario_invocaciones = {}
        while funcion :
            nombre = funcion.splitline(",")[0]
            diccionario_invocaciones[nombre] = []
            for linea in funcion :
                if "import" in linea :   
                    invocado = linea.splitline("import")[1]
                    diccionario_invocaciones[nombre].append(invocado)                  
            funciones = informacion.readline()
    return diccionario_invocaciones


def imprimir_ej3(archivo_fuente):
    
    largo_nombre = 0
    valores = ""
    for i in range(len(Nombres)):
        valores += str(i) + "\t"
    print ("Funciones","\t",valores)
    for i in range((len(Nombres)-1)) :
        
        if len(Nombres[i]> largo_nombre) :
            largo_nombre = len(Nombres[i]) + 4
        print (i+1, " - " , Nombres[i],"\n")
    print ("Total invocaciones","  ",)
        