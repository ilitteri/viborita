import creador_csv
import m_panel_general_funciones
import m_consulta_funciones
import m_analizador_reutilizacion_codigo
import m_arbol_invocacion
import m_informacion_desarrollador

def menu_interactivo():
    '''[Autor: Andres Kubler]
    [Ayuda: Imrimie un menú interactivo para el usuario, y asi desplazarse al punto que elija]'''

    bandera = True
    while bandera:
        print("Menú de interacción\n1. Panel general de funciones\n2. Consulta de funciones\n3. Analizador de reutilización de codigo\n4. Arbol de invocación\n5. Información por desarrollador\n6. Salir")

        opcion_usuario = input("Ingrese una opcion_usuario:")
        if opcion_usuario == "1":
            print("Aca va el punto 1\n")
        elif opcion_usuario == "2":
            print("Aca va el punto 2\n")
        elif opcion_usuario == "3":
            m_analizador_codigo.main()
        elif opcion_usuario == "4":
            m_arbol_invocacion.main()
        elif opcion_usuario == "5":
            print("Aca va el punto 5\n")
        elif opcion_usuario == "6":
            print("\nGracias, vuelva pronto!")
            bandera = False
        else:
            print("\n¡LA OPCION INGRESADA ES INCORRECTA!\n")

def main():
    '''[Autor: Andres Kubler]
    [Ayuda: Ejecuta el archivo para crear el csv, luego ejecua el menu interativo]'''

    creador_csv.main()
    menu_interactivo()

main()