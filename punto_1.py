'''Mediante esta opción se debe mostrar por pantalla, una tabla con la siguiente información
por columna:

Nombre de la Función.Módulo (FUNCION) – nombre función seguido de un punto y el nombre del módulo
Cantidad de Parámetros Formales (Parámetros)
Cantidad de líneas de código (Líneas) – no contabilizar las líneas vacías
Cantidad de invocaciones a la función (Invocaciones)
Cantidad de Puntos de Salida (Returns)
Cantidad de If, contabilizar los anidamientos elif (If/elif)
Cantidad de For (for)
Cantidad de While (while)
Cantidad de Break (Break)
Cantidad de Exit (Exit)
Cantidad de líneas de comentarios (Coment) – sólo los extra descripción
Indicador de Descripción Función (Ayuda) – Si/No indicando que hay descripción de uso de la función, para lo cual se debe evaluar si inmediatamente después de la firma de la función, existe comentario entre comillas triples.
Autor/Responsable (Autor)
Utilice como nombre de las columnas, los nombres que figuran entre paréntesis en cada
caso.

Este punto también debe generar el archivo “panel_general.csv”, en el cual cada línea del
archivo contenga la información descripta en cada uno de los puntos.
La primera línea del archivo, debe contener los nombres que figuran entre paréntesis.'''

def main():
    from m_organizar_datos import por_cantidad_declaraciones_funcion
    with open ("fuente_unico.csv", "r") as fuente_unico, open ("comentarios.csv", "r") as comentarios: 
        diccionario = por_cantidad_declaraciones_funcion(fuente_unico, comentarios)
    grabar(diccionario)








'''def grabar(datos_ordenados_cantidad_declaraciones):
    with open("panel_general.csv", "w") as panel_general
        panel_general.write("funcion, parametros, lineas, invocaciones, returns, if/elif, for, while, break, exit, coment, ayuda, autor \n")
        panel_general.write(f'{nombre_funcion}.{modulo_funcion},{cant_parametros},{cant_invocaciones},{returns},{ifelif},{cant_for},{cant_while},{cant_break},{cant_exit},{cant_comentarios},{ayuda},{autor}')
'''