# coding=utf-8

def menu_interactivo():
    '''[Autor: Andres Kubler]
    [Ayuda: Imrimie un menu interactivo para el usuario, y asi desplazarse al punto que elija]'''
    bandera = True
    while bandera:
        print("Menú de interacción\n1. Panel general de funciones\n2. Consulta de funciones\n3. Analizador de reutilización de codigo\n4. Arbol de invocación\n5. Información por desarrollador\n6. Salir")

        opcion_usuario = input("Ingrese una opcion_usuario:")
        if opcion_usuario == "1":
            print("Aca va el punto 1\n")
        elif opcion_usuario == "2":
            print("Aca va el punto 2\n")
        elif opcion_usuario == "3":
            print("Aca va el punto 3\n")
        elif opcion_usuario == "4":
            print("Aca va el punto 4\n")
        elif opcion_usuario == "5":
            print("Aca va el punto 5\n")
        elif opcion_usuario == "6":
            print("\nGracias, vuelva pronto!")
            bandera = False
        else:
            print("\n¡LA OPCION INGRESADA ES INCORRECTA!\n")

def main():
    '''[Autor: Andres Kubler]
    [Ayuda: Importamos el modulo para crear los archivos csv, y así correrlo antes del menú]'''
    import creador_csv_v2

    creador_csv_v2.main()
    menu_interactivo()
