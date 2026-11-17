from productos import menu_productos

def menu_principal():

    while True:

        print("\n================================")
        print("       SUPERMERCADO MI TIENDA")
        print("================================")
        print("1. Gestion de productos")
        print("2. Inventario")
        print("3. Realizar ventas")
        print("4. Facturacion")
        print("5. Devoluciones")
        print("6. Reportes")
        print("7. Gestion de caja")
        print("8. Salir")
        print("================================")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            menu_productos()

        elif opcion == "2":
            print("Inventario")

        elif opcion == "3":
            print("Realizar ventas")

        elif opcion == "4":
            print("Facturacion")

        elif opcion == "5":
            print("Devoluciones")

        elif opcion == "6":
            print("Reportes")

        elif opcion == "7":
            print("Gestion de caja")

        elif opcion == "8":
            print("Gracias por utilizar el sistema")
            break

        else:
            print("Opcion incorrecta")


menu_principal()