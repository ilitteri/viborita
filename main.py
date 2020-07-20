import creador_csv
import m_organizar_datos as organizar_datos
import m_panel_general_funciones as panel_general_funciones
import m_consulta_funciones as consulta_funciones
import m_analizador_reutilizacion_codigo as analizador_reutilizacion_codigo
import m_arbol_invocacion as arbol_invocacion
import m_informacion_desarrollador as informacion_desarrollador

def leer_archivos_csv(fuente, comentarios):
    with open(fuente, "r") as archivo_fuente, open(comentarios, "r") as archivo_comentarios:
        datos_por_funciones = organizar_datos.por_funciones(archivo_fuente, archivo_comentarios)

    return datos_por_funciones

def imprimir_menu_interaccion():
    titulo = "ANALIZADOR Y EVALUADOR DE DISEÑO MODULAR DE APLICACIONES"
    print(f'{"*" * len(titulo)}\n{titulo}\n{"*" * len(titulo)}')
    print("1. Panel General de Funciones")
    print("2. Consultar Funciones")
    print("3. Analizar Reutilizacion de Codigo")
    print("4. Arbol de Invocaciones")
    print("5. Informacion de Desarrollador")
    print("6. Ayuda")

def ayuda_menu(opcion):
    titulo = "AYUDA DE OPCIONES"
    print(f'{"*" * len(titulo)}\n{titulo}\n{"*" * len(titulo)}')
    print(f'(1) - Muestra en pantalla, una tabla con la cantidad de declaraciones de la aplicacion (for, if/elif, break, exit, while, for); también genera el archivo “panel_general.csv” con esta informacion.')
    print(f'(2) - Muestra en pantalla una tabla con todas las funciones de la aplicacion y se deja a merced del usuario consultar sobre ellas, o genera un archivo con esta informacion')
    print(f'(3) - Muestra en pantalla una tabla con el analisis de la reutilzacion de codigo, y genera un archivo de texto con la misma')
    print(f'(4) - Muestra en pantalla un arbol de invocacion de funciones')
    print(f'(5) - Muestra en pantalla la informacion de cada autor que trabajo en la aplicacion, pudiendose apreciar las funciones que desarrollo, la cantidad de lineas de codigo de esa funcion y al final de cada autor un porcentaje de lineas de codigo escritas relativo a toda la aplicacion')

    return input("Presione cualquier tecla para volver al menu")

def menu_interaccion(datos_por_funciones):
    imprimir_menu_interaccion()
    opcion = input("Ingrese una opcion o presione ENTER para salir: ")
    while opcion:
        if opcion == "1" or opcion.lower() == "panel general de funciones":
            panel_general_funciones.main(datos_por_funciones)
            imprimir_menu_interaccion()
        elif opcion == "2" or opcion.lower() == "consultar funciones":
            consulta_funciones.main(datos_por_funciones)
            imprimir_menu_interaccion()
        elif opcion == "3" or opcion.lower() == "analizar reutilizacion de codigo":
            analizador_reutilizacion_codigo.main(datos_por_funciones)
            imprimir_menu_interaccion()
        elif opcion == "4" or opcion.lower() == "arbol de invocaciones":
            arbol_invocacion.main(datos_por_funciones)
            imprimir_menu_interaccion()
        elif opcion == "5" or opcion.lower() == "informacion de desarrollador":
            informacion_desarrollador.main(datos_por_funciones)
            imprimir_menu_interaccion()
        elif opcion == "6" or opcion.lower() == "ayuda":
            ayuda_menu(opcion)
            imprimir_menu_interaccion()
        else:
            print("Opcion incorrecta!, intente denuevo...")
        opcion = input("Ingrese una opcion o presione ENTER para salir: ")

def main():
    creador_csv.main("programas.txt")
    datos_por_funciones = leer_archivos_csv("fuente_unico.csv", "comentarios.csv")
    menu_interaccion(datos_por_funciones)
    
main()