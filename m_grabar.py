def fuente(archivo_fuente, nombre_funcion, parametros_funcion, nombre_modulo, lineas_codigo):
    '''[Autor: Ivan Litteri]'''

    #Escribe una linea en el archivo de fuente del modulo correspondiente
    archivo_fuente.write(f'{nombre_funcion},"{parametros_funcion}",{nombre_modulo},{",".join(linea_codigo for linea_codigo in lineas_codigo)}\n')

def comentarios(archivo_comentarios, nombre_funcion, comentarios):
    '''[Autor: Ivan Litteri]'''

    #Extraigo el nombre del autor del diccionario comentarios
    nombre_autor = comentarios["autor"]
    #Extraigo la ayuda de funcion del diccionario comentarios
    ayuda = comentarios["ayuda"]
    #Extraigo otros comentrios del diccionario comentarios
    otros_comentarios = comentarios["otros"]
    #Escribe una linea en el archivo de comentarios del modulo correspondiente
    archivo_comentarios.write(f'{nombre_funcion},"{nombre_autor}","{ayuda}",{",".join(comentario for comentario in otros_comentarios) if otros_comentarios is not None else ""}\n')