#Abro el .csv generado en creador_csv.py y tomo los nombres de las funciones
def desempaquetado(archivo_fuente):
    with open ("archivo_fuente", "r") as informacion:
        funciones = informacion.splitlines()
        Nombres = list(zip(informacion))
    return funciones, Nombres
"""
def analisis_funciones(archivo_fuente):
    funciones , Nombres = desempaquetado(archivo_fuente)
    numero = 0
    lista =  []
    Nombres = []
    for funcion in funciones:
        lista[numero] =  funciones[funcion].split(",")
        numero += 1
"""    
    
def imprimir_ej3(archivo_fuente):
    funciones , Nombres = desempaquetado(archivo_fuente)
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
        