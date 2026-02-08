import os
import json
import csv
import requests

# ────────────────────────────────────────────────
# CONFIGURACIÓ
# ────────────────────────────────────────────────

FITXER_RECEPTES = "receptes.json"


# ────────────────────────────────────────────────
# FUNCIONS BÀSIQUES DE GESTIÓ DE RECEPTES
# ────────────────────────────────────────────────

def carregar_receptes():
    if not os.path.exists(FITXER_RECEPTES):
        return []
    try:
        with open(FITXER_RECEPTES, "r", encoding="utf-8") as f:
            dades = json.load(f)
            if isinstance(dades, list):
                return dades
            return []
    except Exception:
        print("Error carregant receptes.json → es crea fitxer nou")
        return []


def guardar_receptes(receptes):
    try:
        with open(FITXER_RECEPTES, "w", encoding="utf-8") as f:
            json.dump(receptes, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error guardant receptes: {e}")


def afegir_recepta_manual(receptes):
    print("\nAfegir nova recepta (manual)")
    titol = input("Títol / Nom de la recepta: ").strip()
    if not titol:
        print("El títol és obligatori.")
        return

    ingredients = []
    print("Introdueix ingredients (un per línia). En blanc per acabar:")
    while True:
        ing = input("  - ").strip()
        if not ing:
            break
        ingredients.append(ing)

    if not ingredients:
        print("Cal almenys un ingredient.")
        return

    recepta = {
        "titol": titol,
        "ingredients": ingredients
    }
    receptes.append(recepta)
    guardar_receptes(receptes)
    print(f"Recepta '{titol}' afegida correctament.")


def llistar_receptes(receptes):
    if not receptes:
        print("\nEncara no hi ha receptes guardades.")
        return

    print("\n--- Llibre de receptes ---")
    for i, r in enumerate(receptes, 1):
        print(f"{i:3d}. {r['titol']}")
        print("   Ingredients:", ", ".join(r['ingredients'][:6]) + ("..." if len(r['ingredients']) > 6 else ""))
    print()


# ────────────────────────────────────────────────
# EXPORTAR / IMPORTAR
# ────────────────────────────────────────────────

def exportar(receptes):
    if not receptes:
        print("No hi ha receptes per exportar.")
        return

    nom_base = input("\nNom del fitxer (sense extensió): ").strip()
    if not nom_base:
        nom_base = "export_receptes"

    # JSON
    try:
        with open(f"{nom_base}.json", "w", encoding="utf-8") as f:
            json.dump(receptes, f, ensure_ascii=False, indent=2)
        print(f"→ Exportat: {nom_base}.json")
    except Exception as e:
        print(f"Error JSON: {e}")

    # CSV
    try:
        with open(f"{nom_base}.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Títol", "Ingredients"])
            for r in receptes:
                ingredients_str = ", ".join(r["ingredients"])
                writer.writerow([r["titol"], ingredients_str])
        print(f"→ Exportat: {nom_base}.csv")
    except Exception as e:
        print(f"Error CSV: {e}")

    # TXT
    try:
        with open(f"{nom_base}.txt", "w", encoding="utf-8") as f:
            for i, r in enumerate(receptes, 1):
                f.write(f"{i}. {r['titol']}\n")
                f.write("Ingredients:\n")
                for ing in r["ingredients"]:
                    f.write(f"  • {ing}\n")
                f.write("\n")
        print(f"→ Exportat: {nom_base}.txt")
    except Exception as e:
        print(f"Error TXT: {e}")


def importar():
    print("\nFormats suportats: .json  .csv  .txt")
    nom_fitxer = input("Nom del fitxer a importar (amb extensió): ").strip()

    if not os.path.exists(nom_fitxer):
        print("Error: fitxer no trobat.")
        return None

    receptes_noves = []

    try:
        if nom_fitxer.endswith(".json"):
            with open(nom_fitxer, "r", encoding="utf-8") as f:
                dades = json.load(f)
                if isinstance(dades, list):
                    receptes_noves = dades
                else:
                    print("El JSON ha de ser una llista d'objectes.")
                    return None

        elif nom_fitxer.endswith(".csv"):
            with open(nom_fitxer, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    titol = row.get("Títol", "").strip()
                    ingredients_str = row.get("Ingredients", "").strip()
                    if titol and ingredients_str:
                        ingredients = [i.strip() for i in ingredients_str.split(",") if i.strip()]
                        receptes_noves.append({"titol": titol, "ingredients": ingredients})

        elif nom_fitxer.endswith(".txt"):
            with open(nom_fitxer, "r", encoding="utf-8") as f:
                contingut = f.read()
                print("Contingut TXT carregat (però no s'ha parsejat automàticament)")
                print("Si vols importar manualment, edita el fitxer o usa JSON/CSV.")
                return None   # Simplificat: TXT només visualització

        else:
            print("Format no suportat.")
            return None

        print(f"Importades {len(receptes_noves)} receptes.")
        return receptes_noves

    except Exception as e:
        print(f"Error important: {e}")
        return None


# ────────────────────────────────────────────────
# API TheMealDB
# ────────────────────────────────────────────────

def buscar_api(ingredient):
    url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json().get("meals", [])
    except Exception as e:
        print(f"Error connectant a l'API: {e}")
        return []


def obtenir_detall_api(meal_id):
    url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        meals = r.json().get("meals", [])
        if not meals:
            return None
        meal = meals[0]

        ingredients = []
        for i in range(1, 21):
            ing = meal.get(f"strIngredient{i}", "").strip()
            mesura = meal.get(f"strMeasure{i}", "").strip()
            if ing:
                text = f"{mesura} {ing}".strip() if mesura else ing
                ingredients.append(text)

        return {
            "titol": meal.get("strMeal", "Recepta sense nom"),
            "ingredients": ingredients
        }
    except Exception:
        return None


def buscar_i_afegir_api(receptes):
    ingredient = input("\n Ingredient en anglés per buscar(ex: chicken, rice, egg...): ").strip()
    if not ingredient:
        return

    print(f"Cercant receptes amb '{ingredient}'...")
    resultats = buscar_api(ingredient)

    if not resultats:
        print("No s'han trobat receptes.")
        return

    print(f"\nTrobades {len(resultats)} receptes:")
    for i, meal in enumerate(resultats, 1):
        print(f"  {i:3d}  {meal['strMeal']}")

    try:
        num = int(input("\nNúmero de recepta a veure/afegir (0 = cancel·lar): "))
        if num < 1 or num > len(resultats):
            print("Cancel·lat o número incorrecte.")
            return

        detall = obtenir_detall_api(resultats[num-1]["idMeal"])
        if not detall:
            print("No s'han pogut obtenir els detalls.")
            return

        print("\n" + "─" * 70)
        print(detall["titol"])
        print("Ingredients:")
        for ing in detall["ingredients"]:
            print(f"  • {ing}")
        print("─" * 70)

        if input("\nVols afegir aquesta recepta? (s/n): ").strip().lower() == "s":
            receptes.append(detall)
            guardar_receptes(receptes)
            print("Recepta afegida al teu llibre!")

    except ValueError:
        print("Has d'introduir un número.")


# ────────────────────────────────────────────────
# MENÚ PRINCIPAL
# ────────────────────────────────────────────────

def menu():
    receptes = carregar_receptes()

    while True:
        print("\n" + "═" * 45)
        print("       LLIBRE DE RECEPTES")
        print("═" * 45)
        print("  1. Afegir nova recepta (manual)")
        print("  2. Llistar receptes guardades")
        print("  3. Exportar / Importar (JSON, CSV, TXT)")
        print("  4. Buscar receptes online (TheMealDB API)")
        print("  5. Eixir del programa")
        print("═" * 45)

        try:
            opcio = int(input("Opció (1-5): "))
        except ValueError:
            print("Introdueix un número vàlid.")
            continue

        if opcio == 1:
            afegir_recepta_manual(receptes)

        elif opcio == 2:
            llistar_receptes(receptes)

        elif opcio == 3:
            print("\n  a. Exportar totes les receptes")
            print("  b. Importar receptes des d'un fitxer")
            sub = input("   → ").strip().lower()
            if sub in ("a", "exportar"):
                exportar(receptes)
            elif sub in ("b", "importar"):
                noves = importar()
                if noves:
                    receptes.extend(noves)
                    guardar_receptes(receptes)
                    print(f"S'han afegit {len(noves)} receptes noves.")

        elif opcio == 4:
            buscar_i_afegir_api(receptes)

        elif opcio == 5:
            print("\nFins aviat! Les receptes s'han guardat.")
            break

        else:
            print("Opció no vàlida.")

menu()