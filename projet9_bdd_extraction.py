import csv 
import mysql.connector 
import re

db = mysql.connector.connect(host="localhost",user="root",password="",database="sae", port=3306) 
c = db.cursor() 
db.autocommit = True
# c.execute("insert into client values (NULL, 'bus', 79000, 'François','Niort', 'bh')") 
# c.execute("delete from client where idClient = 12")

def changement(date, separateur):
    """Transforme les dates anglaises (YYYY-MM-DD) en dates françaises (DD-MM-YYYY)"""
    jour, mois, annee = date.split(f"{separateur}")
    return f"{annee}-{mois}-{jour}" # Alternative : return str(jour) + "/" + str(mois) + "/" + str(annee)

def normaliser_nom(nom):
    nom = nom.strip()
    nom = nom.replace("_", " ")
    nom = nom.lower()
    nom = re.sub(r"\s+", " ", nom)  # remplace espaces multiples par un seul
    return nom

def _normaliser_libelle_vehicule(libelle_brut: str) -> str:
    """Uniformise le libellé du type de véhicule (sans accents, sans tiret)."""
    if not libelle_brut:
        return ""
    mapping = {
        "velo-cargo":             "VeloCargo",
        "velo cargo":             "VeloCargo",
        "triporteur":             "Triporteur",
        "utilitaireelectrique":   "UtilitaireElectrique",
        "utilitaire electrique":  "UtilitaireElectrique",
        "utilitaire elec":        "UtilitaireElectrique",
        "tri porteur":            "Triporteur",
    }
    cle = libelle_brut.strip().lower().replace("-", " ")
    return mapping.get(cle, libelle_brut.strip())

def decouper_adresse(adresse: str):
    """
    Retourne (rue, cp, ville) à partir d'une adresse complète.
    Si l'adresse ne correspond pas au format attendu, renvoie des valeurs par défaut.
    """
    adresse = adresse.strip()

    # Regex : (rue) (CP) (ville)
    m = re.match(r"^(.*?)[ ,]+(\d{5})[ ,]+(.+)$", adresse)
    if m:
        rue  = m.group(1).strip()
        cp   = m.group(2).strip()
        ville = m.group(3).strip()
        return rue, cp, ville

    # Si pas de match → valeurs fallback
    return adresse, "", ""


def inserer_collecter():
    """
    Associe chaque livraison entrante à une tournée correspondant à sa date
    et insère les liens dans la table COLLECTER.
    """

    # Récupération des livraisons entrantes
    c.execute("""SELECT idLivraisonEntrante, nbColis, dateReception, idPartenaire FROM livraisonentrante""")
    livraisons_entrantes = c.fetchall()

    # Récupération des tournées existantes
    c.execute("""SELECT idTournee, DateTournee, idLivreur FROM tournee""")
    tournees = c.fetchall()

    # Mapping : date SQL → idTournee
    mapping_tournee_par_date = {
        str(dateTournee): idTournee
        for (idTournee, dateTournee, idLivreur) in tournees
    }

    lignes_collecter = []

    # Construction des lignes à insérer
    for (idLivEntrante, nbColis, dateReception, idPartenaire) in livraisons_entrantes:
        dateReception_str = str(dateReception)

        if dateReception_str not in mapping_tournee_par_date:
            continue

        idTournee = mapping_tournee_par_date[dateReception_str]

        lignes_collecter.append((idTournee, idLivEntrante, dateReception_str, idPartenaire))

    # Insertion dans collecter
    c.execute("SET FOREIGN_KEY_CHECKS = 0")  # sécurité optionnelle
    sql_collect = """INSERT IGNORE INTO collecter (idTournee, idLivraisonEntrante, dateProvenance, idPartenaire)VALUES (%s, %s, %s, %s)"""
    c.executemany(sql_collect, lignes_collecter)
    c.execute("SET FOREIGN_KEY_CHECKS = 1")

    print(f"[Collecter] {c.rowcount} ligne(s) insérée(s).")


def ajout_partenaire(nom:str, rue:str, CP:int, ville:str) : 
    c.execute("SELECT COUNT(*) FROM partenaire WHERE nomPartenaire = %s AND villePartenaire = %s", (nom, ville))
    existe = c.fetchone()[0]
    if existe == 0 :
        sql = "INSERT INTO partenaire VALUES (NULL, %s, %s, %s, %s)"
        c.execute(sql, (nom, rue, CP, ville))
    else : 
        print("ligne existante")

def extraction_partenaire():
    fichier = open("partenaire.csv", encoding="latin-1") 
    #Ouverture du lecteur CSV en lui fournissant le caractère séparateur (ici ";") 
    lecteurCSV = csv.reader(fichier,delimiter=";")
    for ligne in lecteurCSV: 
        if ligne[0] != "nomPartenaire" :
            nom = str(ligne[0]).strip()
            ville = str(ligne[1]).strip()
            rue = input("Quelle est la rue du partanire : " + str(nom) + " ? ").strip()
            CP = input("Quelle est le code postal du partanire : " + str(nom) + " ? ").strip()
            ajout_partenaire(nom,rue,CP,ville)

def ajout_entree(qte, date, idPartenaire):
    c.execute("SELECT idPartenaire FROM partenaire WHERE nomPartenaire = %s", (idPartenaire,))
    row = c.fetchone()
    # 2. Si le partenaire n'existe pas → erreur ou insertion automatique
    if row is None:
        raise ValueError(f"Partenaire inconnu dans la base : {idPartenaire}")
    id_partenaire = row[0]
    # 3. Insérer la ligne dans livraisonentrante
    sql = "INSERT INTO livraisonentrante VALUES (NULL, %s, %s, %s)"
    c.execute(sql, (qte, date, id_partenaire))

def extraction_entree():
    fichier = open("entree.csv", encoding="latin-1") 
    # Ouverture du lecteur CSV en lui fournissant le caractère séparateur (ici ";") 
    lecteurCSV = csv.reader(fichier,delimiter=";")
    for ligne in lecteurCSV:
        if ligne[0] != "date_entree":
            date = str(ligne[0]).strip()
            date = changement(date, "/")
            qte = str(ligne[1]).strip()
            idPartenaire = str(ligne[2]).strip()
            idPartenaire = normaliser_nom(idPartenaire)
            ajout_entree(qte, date, idPartenaire)

def ajout_livreur(prenomLivreur, nomLivreur, date):
    # Vérifier si un livreur identique existe déjà
    c.execute(
        "SELECT COUNT(*) FROM livreur "
        "WHERE PrenomLivreur = %s AND NomLivreur = %s AND DateEmbauche = %s",
        (prenomLivreur, nomLivreur, date)
    )
    existe = c.fetchone()[0]

    if existe == 0:
        # Ajouter le livreur
        sql = "INSERT INTO livreur VALUES (NULL, %s, %s, %s)"
        c.execute(sql, (prenomLivreur, nomLivreur, date))
        return True  # insertion effectuée
    else:
        return False  # doublon détecté


def ajout_vehicule(typeVeh, capacite, autonomie, nb):
    c.execute("SELECT COUNT(*) FROM typevehicule WHERE LibelleTypeVehicule = %s AND CapaciteKg = %s AND AutonomieKm = %s" , (typeVeh, capacite, autonomie))
    existe = c.fetchone()[0]
    if existe == 0 :
        sql = "INSERT INTO typevehicule VALUES (NULL, %s, %s, %s, %s)"
        c.execute(sql, (typeVeh, capacite, autonomie, nb))


def extraction_vehicule_livreur():
    fichier = open("vehicule_livreur.csv", encoding="latin-1") 
    # Ouverture du lecteur CSV en lui fournissant le caractère séparateur (ici ";") 
    lecteurCSV = csv.reader(fichier,delimiter=";")
    for ligne in lecteurCSV: 
        if ligne[0] != "typeVeh" :
            if ligne[0] != "":
                typeVeh = str(ligne[0]).strip()
                autonomie = str(ligne[1]).strip()
                capacite = str(ligne[2]).strip()
                nb = str(ligne[3]).strip()
                ajout_vehicule(typeVeh, capacite, autonomie, nb)
            else:
                nomLivreur = str(ligne[4]).strip()
                prenomLivreur = str(ligne[5]).strip()
                date = str(ligne[6]).strip()
                date = changement(date, "/")
                ajout_livreur(prenomLivreur, nomLivreur, date)

def extraction_tournee():
    fichier = open("tournee.csv", encoding="latin-1")
    lecteurCSV = csv.reader(fichier, delimiter=";")

    for ligne in lecteurCSV:
        if ligne[0] != "dateTour":

            date = changement(str(ligne[0]).strip(), "/")
            vehicule = str(ligne[1]).strip()
            autonomie = str(ligne[2]).strip()
            capacite = str(ligne[3]).strip()
            livreur = normaliser_nom(ligne[4].strip())
            # Normalisation du véhicule
            if vehicule == "UTILITAIRE ELEC":
                vehicule = "UtilitaireElectrique"
            ajout_tournee(date, autonomie, vehicule, livreur, capacite)


def ajout_tournee(date, autonomie, vehicule, livreur, capacite):
    c.execute(
        "SELECT idLivreur FROM livreur WHERE LOWER(nomLivreur) = %s",
        (livreur.lower(),)
    )
    rows = c.fetchall()

    if len(rows) == 0:
        raise ValueError(f"Livreur inconnu dans la base : {livreur}")

    idLivreur = rows[0][0]

    # --- Récupération du type de véhicule ---
    c.execute(
        "SELECT idTypeVehicule FROM typevehicule WHERE LibelleTypeVehicule = %s",
        (vehicule,)
    )
    rows = c.fetchall()

    if len(rows) == 0:
        nb = input(f"Véhicule inconnu dans la base : {vehicule}, combien y'en a t'il ? ")
        ajout_vehicule(vehicule, capacite, autonomie, nb)
        c.execute("SELECT idTypeVehicule FROM typevehicule WHERE LibelleTypeVehicule = %s",(vehicule,))
        rows = c.fetchall()
    idTypeVehicule = rows[0][0]

    # --- Insertion de la tournée ---
    sql = """INSERT INTO tournee (DateTournee, DistanceEstimeeKm, idTypeVehicule, idLivreur) VALUES (%s, %s, %s, %s)"""
    c.execute(sql, (date, autonomie, idTypeVehicule, idLivreur))

def extraire_livraison():
    """
    Lit livraison.csv et retourne :
      - clients   : liste (nomClient, rueClient, cpClient, villeClient)
      - livraisons: liste (date_sql, poids, nb_colis, nom_client, vehicule, livreur)
    """
    fichier = open("livraison.csv", encoding="latin-1")
    lecteurCSV = csv.reader(fichier, delimiter=";")

    clients_vus = {}
    livraisons  = []

    for ligne in lecteurCSV:
        if ligne[0] == "date_sortie":
            continue

        # Extraction brute
        date_raw   = ligne[0].strip()
        client_raw = ligne[1].strip()
        ville  = ligne[2].strip()
        vehicule   = ligne[3].strip()
        poids_raw  = ligne[4].strip()
        adresse    = ligne[5].strip()
        nb_raw     = ligne[6].strip()
        livreur_raw = ligne[7].strip()

        # Normalisation
        nom_client = normaliser_nom(client_raw)
        livreur    = livreur_raw.capitalize()
        vehicule = _normaliser_libelle_vehicule(vehicule)

        # Poids vide → None
        poids = poids_raw if poids_raw not in ("", " ", "-", "null", "NULL") else None

        # nb colis
        try:
            nb_colis = int(nb_raw)
        except:
            nb_colis = 1

        # Date SQL
        try:
            date_sql = changement(date_raw, "/")
        except:
            date_sql = date_raw

        # Découpage adresse
        rue, cp, ville = decouper_adresse(adresse)

        # Ajout client unique
        if nom_client not in clients_vus:
            clients_vus[nom_client] = (nom_client, rue, cp, ville)

        # Ajout livraison
        livraisons.append((date_sql, poids, nb_colis, nom_client, vehicule, livreur))

    return list(clients_vus.values()), livraisons
 
 
def inserer_livraison(clients: list, livraisons: list):

    # ───────────────────────────────
    #  INSERTION CLIENT
    # ───────────────────────────────
    sql_cl = """INSERT IGNORE INTO Client (rueClient, cpClient, villeClient) VALUES (%s, %s, %s)"""

    lignes_cl = [(rue, cp, ville) for (nom, rue, cp, ville) in clients]
    c.executemany(sql_cl, lignes_cl)


    # Mapping client
    c.execute("SELECT idClient, rueClient, cpClient, villeClient FROM Client")
    map_client = {(r or "", cp or "", v or ""): idc for (idc, r, cp, v) in c.fetchall()}

    nom_vers_adresse = {nom: (rue, cp, ville) for (nom, rue, cp, ville) in clients}

    # Mapping TypeVehicule
    c.execute("SELECT idTypeVehicule, LibelleTypeVehicule FROM TypeVehicule")
    map_veh = {lib: idf for (idf, lib) in c.fetchall()}

    # Mapping Livreur
    c.execute("SELECT idLivreur, nomLivreur FROM Livreur")
    map_livr = {nom.capitalize(): idl for (idl, nom) in c.fetchall()}

    # Mapping Tournee
    c.execute("SELECT idTournee, DateTournee, idLivreur FROM Tournee")
    map_tournee = {(str(dt), idl): idt for (idt, dt, idl) in c.fetchall()}

    # ───────────────────────────────
    #  INSERTION LIVRAISON SORTANTE
    # ───────────────────────────────
    lignes_ls = []

    for (date_sql, poids, nb_colis, nom_client, vehicule, livreur) in livraisons:

        # idClient
        adresse = nom_vers_adresse.get(nom_client, ("", "", ""))
        id_client = map_client.get(adresse)
        if id_client is None:
            continue

        # idLivreur
        id_livreur = map_livr.get(livreur)
        if id_livreur is None:
            continue

        # idTournee
        id_tournee = map_tournee.get((date_sql, id_livreur))
        if id_tournee is None:
            continue

        # idVehicule
        id_vehicule = map_veh.get(vehicule)
        if id_vehicule is None:
            continue

        # Ajout ligne
        lignes_ls.append((date_sql, poids, nb_colis, id_tournee, id_client))

    sql_ls = """
        INSERT IGNORE INTO livraisonsortante
            (DateLivraison, Poids, nbColis, idTournee, idClient)
        VALUES (%s, %s, %s, %s, %s)
    """

    c.executemany(sql_ls, lignes_ls)





extraction_partenaire()
extraction_entree()
extraction_vehicule_livreur()
extraction_tournee()
clients, livraisons = extraire_livraison()
inserer_livraison(clients, livraisons)

# Appel unique
inserer_collecter()

# Fermeture propre
c.close()
db.close()


db.close()



