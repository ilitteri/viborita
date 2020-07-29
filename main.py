import m_csv_finales as csv_finales
import m_organizar_datos as organizar_datos
import m_panel_general_funciones as panel_general_funciones
import m_consulta_funciones as consulta_funciones
import m_analizador_reutilizacion_codigo as analizador_reutilizacion_codigo
import m_arbol_invocacion as arbol_invocacion
import m_informacion_desarrollador as informacion_desarrollador


def obtener_datos_csv(fuente, comentarios):
    '''[Autor: Ivan Litteri]
    [Ayuda: le llegan por parametro los archivos csv y devuelve un diccionario ordenado con los datos leidos de los
    mismos.]'''

    #Abre los archivos
    with open(fuente, "r") as archivo_fuente, open(comentarios, "r") as archivo_comentarios:
        #Llama a una funcion que lee y devuelve los datos ordenados
        datos_por_funciones, datos_por_autores = organizar_datos.leer_archivos_csv(archivo_fuente, archivo_comentarios)

    return datos_por_funciones, datos_por_autores

def mostrar_menu_interaccion():
    '''[Autor: Ivan Litteri]
    [Ayuda: muestra en pantalla las opciones a elegir del menu]'''

    titulo = "ANALIZADOR Y EVALUADOR DE DISEÑO MODULAR DE APLICACIONES"
    print(f'\n{"*" * len(titulo)}\n{titulo}\n{"*" * len(titulo)}')
    print("1. Panel General de Funciones")
    print("2. Consultar Funciones")
    print("3. Analizar Reutilizacion de Codigo")
    print("4. Arbol de Invocaciones")
    print("5. Informacion de Desarrollador")
    print("6. Ayuda")

def mostrar_ayuda_menu():
    '''[Autor: Ivan Litteri]
    [Ayuda: Muestra en pantalla una breve descripcion de lo que trata cada opcion del menu]'''

    titulo = "AYUDA DE OPCIONES"
    print(f'{"*" * len(titulo)}\n{titulo}\n{"*" * len(titulo)}')
    print(f'(1) - Muestra en pantalla, una tabla con la cantidad de declaraciones de la aplicacion (for, if/elif, break, exit, while, for); también genera el archivo “panel_general.csv” con esta informacion.')
    print(f'(2) - Muestra en pantalla una tabla con todas las funciones de la aplicacion y se deja a merced del usuario consultar sobre ellas, o genera un archivo con esta informacion')
    print(f'(3) - Muestra en pantalla una tabla con el analisis de la reutilzacion de codigo, y genera un archivo de texto con la misma')
    print(f'(4) - Muestra en pantalla un arbol de invocacion de funciones')
    print(f'(5) - Muestra en pantalla la informacion de cada autor que trabajo en la aplicacion, pudiendose apreciar las funciones que desarrollo, la cantidad de lineas de codigo de esa funcion y al final de cada autor un porcentaje de lineas de codigo escritas relativo a toda la aplicacion')

    return input("Presione cualquier tecla para volver al menu")

def menu_interaccion(datos_por_funciones, datos_por_autores):
    '''[Autor: Andrés Kübler]
    [Ayuda: se queda a la espera del ingreso por consola del usuario, y en base a lo que se ingresa actua.]'''

    #Muestra el menu de interaccion en consola
    mostrar_menu_interaccion()
    #Solicita al usuario el ingreso de una opcion mostrada en el menu
    opcion = input("Ingrese una opcion o presione ENTER para salir: ")
    #Imprime un enter
    print()
    #Mientras la opccion ingresada no sea un espacio o enter...
    while opcion:
        #Si la opcion ingresada es 1 o "panel general de funciones" ejecuta el main del modulo y una vez que termina eso muestra denuevo el menu
        if (opcion == "1") or (opcion.lower() == "panel general de funciones"):
            panel_general_funciones.obtener_panel_general(datos_por_funciones)
            mostrar_menu_interaccion()
        #Si la opcion ingresada es 2 o "consultar funciones" ejecuta el main del modulo y una vez que termina eso muestra denuevo el menu
        elif (opcion == "2") or (opcion.lower() == "consultar funciones"):
            consulta_funciones.consultar_funciones(datos_por_funciones)
            mostrar_menu_interaccion()
        #Si la opcion ingresada es 3 o "analizar reutilizacion de codigo" ejecuta el main del modulo y una vez que termina eso muestra denuevo el menu
        elif (opcion == "3") or (opcion.lower() == "analizar reutilizacion de codigo"):
            analizador_reutilizacion_codigo.analizar_reutilizacion(datos_por_funciones)
            mostrar_menu_interaccion()
        #Si la opcion ingresada es 4 o "arbol de invocaciones" ejecuta el main del modulo y una vez que termina eso muestra denuevo el menu
        elif (opcion == "4") or (opcion.lower() == "arbol de invocaciones"):
            arbol_invocacion.grafica_arbol_invocaciones(datos_por_funciones)
            mostrar_menu_interaccion()
        #Si la opcion ingresada es 5 o "informacion de desarrollador" ejecuta el main del modulo y una vez que termina eso muestra denuevo el menu
        elif (opcion == "5") or (opcion.lower() == "informacion de desarrollador"):
            informacion_desarrollador.obtener_informacion_desarrollador(datos_por_autores)
            mostrar_menu_interaccion()
        #Si la opcion ingresada es 6 o "ayuda" muestra en consola la ayuda para el uso del menu
        elif (opcion == "6") or (opcion.lower() == "ayuda"):
            mostrar_ayuda_menu()
            mostrar_menu_interaccion()
        #Si no se ingresa ninguna de las opciones anteriores vuelve a preguntar
        else:
            print("Opcion incorrecta!, intente denuevo...")
            print()
        #Solicita al usuario el ingreso de una opcion mostrada en el menu
        opcion = input("Ingrese una opcion o presione ENTER para salir: ")
        print()

def main():
    '''[Autor: Andrés Kübler]'''

    #Crea los archivos csv fuente_unico y comentarios
    csv_finales.crear_csv_finales("programas_ejemplo.txt")
    #Obtiene dos diccionarios que van a ser usados por el menu de interaccion
    datos_por_funciones, datos_por_autores = obtener_datos_csv("fuente_unico.csv", "comentarios.csv")
    #Abre el menu de interaccion
    menu_interaccion(datos_por_funciones, datos_por_autores)

    
main()