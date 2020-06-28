comentarios = {}
codigo = []

def proceso_de_archivos():
    with open('programas.txt', 'r') as archivo:
        filas = archivo.readlines()
        for fila in filas:
            ubicacion_modulo = fila.replace("\n", "")
            with open(ubicacion_modulo, "r") as modulo:
                for linea in modulo.readlines():
                    if ("#" in linea):
                        comentarios.append(linea)
#                    elif ("'''" in linea):
#                        if "Autor" in linea:
#                            comentarios["Autor"] = 
                    else:
                        codigo.append(linea)

                
