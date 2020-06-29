import creador_csv

def menu_interactivo():
    bandera = True
    while bandera:
        print("Menú de interacción\n1. Panel general de funciones\n2. Consulta de funciones\n3. Analizador de reutilización de codigo\n4. Arbol de invocación\n5. Información por desarrollador\n6. Salir")

        opcion = input("Ingrese una opcion:")
        if opcion == "1":
            print("Aca va el punto 1\n")
        elif opcion == "2":
            print("Aca va el punto 2\n")
        elif opcion == "3":
            print("Aca va el punto 3\n")
        elif opcion == "4":
            print("Aca va el punto 4\n")
        elif opcion == "5":
            print("Aca va el punto 5\n")
        elif opcion == "6":
            print("\nGracias, vuelva pronto!")
            bandera = False
        else:
            print("\n¡LA OPCION INGRESADA ES INCORRECTA!\n")

def main():
    creador_csv.main()
    menu_interactivo()