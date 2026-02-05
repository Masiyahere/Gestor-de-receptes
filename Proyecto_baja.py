import os
import csv
import json
import requests


def JSON():
    with open("recepta.json", "w", encoding="utf-8") as f:
        json.dump(f, indent=4)
        try:
            os.mkdir("Llista_JSON")
            print("Carpeta creada exitosamente")
        except FileExistsError:
            print("La carpeta ya existe")


def CSV():
    print("Nom recepta")
    Titol=input()
    print("Nom")
    Nom=input()
    print("Ingredients:")
    Ingredients=input()
    with open("recepta.csv", "w", newline="", encoding="utf-8") as f:
        escriptor = csv.writer(f)
        escriptor.writerow(["Nom","Ingredients"])
        escriptor.writerow([Nom, Ingredients])
        try:
            os.mkdir(Titol)
            print("Carpeta creada exitosamente")
        except FileExistsError:
            print("La carpeta ya existe")


def TXT():
    print("Nom recepta")
    Titol=input()
    print("Nom")
    Nom=input()
    print("Ingredients")
    Ingredients=input()
    with open("recepta.txt", "w", encoding="utf-8") as f:
        
        try:
            os.mkdir(Titol)
            print("Carpeta creada exitosamente")
            f.write(Nom)
            f.write(Ingredients)
        except FileExistsError:
            print("La carpeta ya existe")
            
def llista():
    print("---El meu llibre de receptes---")
    print("")
    receptas=["recepta.csv","recepta.txt"]
    for recepta in receptas:
        print("-"+ recepta)

def menu():
    while True:
        print("")
        print("Receptes")
        print("1.Afegir nova recepta")
        print("2.Llistar receptes")
        print("3.Exportar/Importar JSON,CSV,TXT")
        print("4.Buscar receptes en API")
        print("5.Veure estadístiques")
        print("6.Eixir del programa")

        opcion=int(input("Escoge entre el 1-3: "))

        if opcion==1:
            print("")
            print("1.Format JSON")
            print("2.Format CSV")
            print("3.Format TXT")
            tipus_text=int(input("Escoge el format a escriure:"))
            if tipus_text==1:
                JSON()
            elif tipus_text==2:
                CSV()
            elif tipus_text==3:
                TXT()


        elif opcion==2:
            print("")
                 
            llista()   
        elif opcion==6:
            print("")
            print("Cerrando libreria...")
            print("Libreria cerrada.")
            break
        else:
            print("")
            print("Opción no válida, pruebe otro número.")

menu()
print("")
