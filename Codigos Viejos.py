#Primer intento de organizador de datos
'''
funciones = {}
contador_funciones = 0
with open("test.py", "r") as archivo:
    linea = archivo.readline()
    while linea:
        if linea.startswith("def"):
            contador_funciones += 1
        if contador_funciones > 0:
            if not contador_funciones in funciones:
                funciones[contador_funciones] = [linea.rstrip("\n")]
            else:
                funciones[contador_funciones].append(linea.rstrip("\n"))
        linea = archivo.readline()
    print(funciones)
'''
#Forma de guardar los datos
'''
def guardar_datos():
    datos = organizar_datos()
    modulos = list(datos.keys())
    for modulo in modulos:
        with open(f'fuente_{modulo}.csv', "w") as nuevo_archivo:
            for nombre_funcion in datos[modulo].keys():
                nuevo_archivo.write(f'{nombre_funcion},{datos[modulo][nombre_funcion]["parametros"]},{modulo},{datos[modulo][nombre_funcion]["lineas"]}\n')
'''
