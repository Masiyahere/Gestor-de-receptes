import os
import csv
import json

#--OPCION 1: AFEGIR UNA NOVA RECETA

def JSON():
    print("Nom de la receta:")
    titol=input()
    print("Nom:")
    nom=input()
    print("Ingredients:")
    ingredients=input()
    data = {"Titol":titol,"nom":nom,"ingredients":ingredients}

    with open(titol+".json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        try:
            os.mkdir(titol)
            print("Carpeta creada exitosament")
        except FileExistsError:
            print("La carpeta ja existeix")


def CSV():
    print("Nom recepta")
    Titol=input()
    print("Nom")
    Nom=input()
    print("Ingredients:")
    Ingredients=input()
    with open(Titol+".csv", "w", newline="", encoding="utf-8") as f:
        escriptor = csv.writer(f)
        escriptor.writerow(["Nom:"+Nom])
        escriptor.writerow(["Ingredients:"+Ingredients])
        try:
            os.mkdir(Titol)
            print("Carpeta creada exitosament")
        except FileExistsError:
            print("La carpeta ja existeix")


def TXT():
    print("Nom recepta")
    Titol=input()
    print("Nom")
    Nom=input()
    print("Ingredients")
    Ingredients=input()
    with open(Titol+".txt", "w", encoding="utf-8") as f:
        f.write("Titol:"+Titol+"\n")
        f.write("Nom:"+Nom+"\n")
        f.write("Ingredients:"+Ingredients)
        try:
            os.mkdir(Titol)
            print("Carpeta creada exitosamente")
        except FileExistsError:
            print("La carpeta ya existe")

#--OPCION 2: LLISTAR LES RECEPTES

def llista():
    print("---El meu llibre de receptes---")
    for archivo in os.listdir():
        if archivo.endswith(".csv") or archivo.endswith(".txt") or archivo.endswith(".json"):
            print("-"+archivo)

#--OPCION 3: EXPORTAR/IMPORTAR

def exportar():
    print("Nom del fitxer sense extensió:")
    nom=input()

    data={
        "Titol":nom,
        "Nom":"Exportat",
        "Ingredients":"..."
    }

    try:
        # JSON
        with open(nom+".json","w",encoding="utf-8") as f:
            json.dump(data,f,indent=4,ensure_ascii=False)

        # CSV
        with open(nom+".csv","w",newline="",encoding="utf-8") as f:
            w=csv.writer(f)
            w.writerow(["Titol","Nom","Ingredients"])
            w.writerow([data["Titol"],data["Nom"],data["Ingredients"]])

        # TXT
        with open(nom+".txt","w",encoding="utf-8") as f:
            f.write(str(data))

        print("Exportació completada")

    except Exception as e:
        print("Error exportant:",e)


def importar():
    print("Nom del fitxer a importar:")
    archivo=input()

    if not os.path.exists(archivo):
        print("Error: fitxer no trobat")
        return

    try:
        if archivo.endswith(".json"):
            with open(archivo,"r",encoding="utf-8") as f:
                data=json.load(f)
                print("JSON carregat:",data)

        elif archivo.endswith(".csv"):
            with open(archivo,"r",encoding="utf-8") as f:
                r=csv.reader(f)
                for linea in r:
                    print(linea)

        elif archivo.endswith(".txt"):
            with open(archivo,"r",encoding="utf-8") as f:
                print(f.read())

        else:
            print("Format incorrecte")

    except json.JSONDecodeError:
        print("Error: JSON mal formatat")
    except Exception as e:
        print("Error llegint el fitxer:",e)


def gestio_arxius():
    print("1.Exportar receptes")
    print("2.Importar receptes")
    op=input("Escoge opción:")

    if op=="1":
        exportar()
    elif op=="2":
        importar()

#--MENU:

def menu():
    while True:
        print("")
        print("Receptes")
        print("1.Afegir nova recepta")
        print("2.Llistar receptes")
        print("3.Exportar/Importar JSON,CSV,TXT")
        print("4.Buscar receptes en API")
        print("5.Eixir del programa")

        opcion=int(input("Escoge entre el 1-5: "))

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
        elif opcion==3:
            print("")
            gestio_arxius()
        elif opcion==5:
            print("")
            print("Cerrant llibreria...")
            print("Llibreria tancada.")
            break
        else:
            print("")
            print("Opció no vàlida, prova altre número.")

menu()
print("")
