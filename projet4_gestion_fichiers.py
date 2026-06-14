import csv
import json

contenu_filtre = []
liste_dict = []

def ouverture_json(nom_fichier):
    """Ouverture et téléchargement du fichier JSON"""
    try : 
        # Vérification de l'emplacement du fichier
        fichier = open(f"{nom_fichier}", "r", encoding = "utf-8")
        contenu = json.load(fichier)
        return contenu
        
    except FileNotFoundError : 
        print("Fichier introuvable") 

def transformer_date_francais(date, separateur):
    """Transforme les dates anglaises (YYYY-MM-DD) en dates françaises (DD-MM-YYYY)"""
    annee, mois, jour = date.split(f"{separateur}")
    return f"{jour}/{mois}/{annee}" # Alternative : return str(jour) + "/" + str(mois) + "/" + str(annee)

def isole_heure(date):
    """Isole l'heure afin de garder que la partie lisible"""
    heure = date[11:23]
    return f"{heure}"

def transforme_unite(unite):
    unite = unite.replace("u" , "µ")
    return unite

def transforme_csv(contenu):
    """Supprime les lignes qui n'ont pas les données essentielles à notre étude et créer le csv"""
    # Vérification des lignes completes et ajout à la liste 
    for dico in contenu:
        if (
            dico["fields"]["nom_station"] is not None
            and dico["record_timestamp"] is not None
            and dico["fields"]["date_fin"] is not None
            and dico["fields"]["nom_poll"] is not None
            # Les valeurs de la clé valeur ne sont pas forcément codées, on ne peut pas utiliser None
            and "valeur" in dico["fields"].keys()
            and dico["fields"]["unite"] is not None
            and dico["geometry"]["coordinates"][0] is not None
            and dico["geometry"]["coordinates"][1] is not None
        ):
            # Ajout des lignes complètes à la liste contenu_filtre
            contenu_filtre.append([
                dico["fields"]["nom_station"],
                dico["geometry"]["coordinates"][1],
                dico["geometry"]["coordinates"][0],
                dico["fields"]["date_fin"],
                transformer_date_francais(dico["record_timestamp"][:10], "-"),
                isole_heure(dico["record_timestamp"]),
                dico["fields"]["nom_poll"],
                dico["fields"]["valeur"],
                transforme_unite(dico["fields"]["unite"])
                ])
    # Création du csv
    cles = ["Nom_Station", "Latitude", "Londitude", "Date de fin", "Date de prélèvement", "Heure du prélèvement", "Nom_Polluant", "Valeur", "Unité"]
    for ligne in contenu_filtre:
        dico = {}
        for i in range(len(cles)):
            dico[cles[i]] = ligne[i]
        liste_dict.append(dico)
    fichier = open("CSV.csv", "wt", newline = "", encoding = "utf-8-sig")
    ecritCSV = csv.DictWriter(fichier, delimiter=";", fieldnames = liste_dict[0].keys())
    ecritCSV.writeheader()
    # Remplissage du csv ligne par ligne
    for ligne in liste_dict:
        ecritCSV.writerow(ligne)
    fichier.close()
    
if __name__ == "__main__":
    fichier_json = ouverture_json("fichier.json") 
    fichier_csv = transforme_csv(fichier_json)
