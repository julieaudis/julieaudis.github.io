--- LES REQUETES CLASSIQUES ---

# Nombre de livraisons par client: 
SELECT C.idClient, C.villeClient, COUNT(LS.idLivraisonS) AS nb_livraisons
FROM Client C
JOIN LivraisonSortante LS ON LS.idClient = C.idClient
GROUP BY C.idClient, C.villeClient
ORDER BY nb_livraisons DESC;

# Liste des livreurs avec plus de 3 livraisons:
SELECT L.idLivreur, L.PrenomLivreur, L.nomLivreur, COUNT(T.idTournee) AS nb_livraisons
FROM Livreur L
JOIN Tournee T ON T.idLivreur = L.idLivreur
GROUP BY L.idLivreur, L.PrenomLivreur, L.nomLivreur
HAVING COUNT(T.idTournee) > 3
ORDER BY nb_livraisons DESC;

# Distance totale par tournée :
SELECT T.idTournee, T.DateTournee, SUM(T.DistanceEstimeeKm) AS distance_totale_km
FROM Tournee T
GROUP BY T.idTournee, T.DateTournee
ORDER BY distance_totale_km DESC;

# Écart entre l’autonomie restante et le trajet à effectuer : 
SELECT T.idTournee, T.DateTournee, T.DistanceEstimeeKm,
       TV.LibelleTypeVehicule, TV.AutonomieKm,
       (TV.AutonomieKm - T.DistanceEstimeeKm) AS marge_autonomie_km
FROM Tournee T
JOIN TypeVehicule TV ON TV.idTypeVehicule = T.idTypeVehicule
ORDER BY marge_autonomie_km ASC;

# Liste des livreurs sans livraison : 
SELECT idLivreur, PrenomLivreur, nomLivreur
FROM LIVREUR
WHERE idLivreur NOT IN (SELECT idLivreur FROM TOURNEE);

# Émissions CO2 par véhicule et par année :
SELECT TV.LibelleTypeVehicule, EC.annee, SUM(EC.QuantiteCo2) AS total_co2
FROM TYPEVEHICULE TV
JOIN EMISSIONCO2 EC USING (idTypeVehicule)
GROUP BY TV.idTypeVehicule, TV.LibelleTypeVehicule, EC.annee
ORDER BY total_co2 DESC;

# Liste des livreurs et de ses tournées associées :
SELECT L.idLivreur, L.PrenomLivreur, L.nomLivreur,
       T.idTournee, T.DateTournee, T.DistanceEstimeeKm
FROM LIVREUR L
JOIN TOURNEE T ON T.idLivreur = L.idLivreur
ORDER BY L.nomLivreur;

# Nombre de tournées et distance totale effectuée pour chaque livreur :
SELECT L.idLivreur, L.PrenomLivreur, L.nomLivreur,
       COUNT(T.idTournee) AS nb_tournees,
       SUM(T.DistanceEstimeeKm) AS distance_totale_km
FROM LIVREUR L
JOIN TOURNEE T ON T.idLivreur = L.idLivreur
GROUP BY L.idLivreur, L.PrenomLivreur, L.nomLivreur
ORDER BY distance_totale_km DESC;

# Nombre de livraisons entrantes par partenaire :
SELECT P.nomPartenaire, P.villePartenaire, COUNT(LE.idLivraisonEntrante) AS nb_livraisons,
       SUM(LE.nbColis) AS total_colis
FROM Partenaire P
JOIN LivraisonEntrante LE ON LE.idPartenaire = P.idPartenaire
GROUP BY P.idPartenaire, P.nomPartenaire, P.villePartenaire
ORDER BY total_colis DESC;

# Véhicules dépassant leur autonomie :
SELECT T.idTournee, T.DateTournee, T.DistanceEstimeeKm,
       TV.LibelleTypeVehicule, TV.AutonomieKm
FROM Tournee T
JOIN TypeVehicule TV ON TV.idTypeVehicule = T.idTypeVehicule
WHERE T.DistanceEstimeeKm > TV.AutonomieKm
ORDER BY (T.DistanceEstimeeKm - TV.AutonomieKm) DESC;

--- LES VUES ---

# Vue des émissions CO2 par véhicule et par année
CREATE OR REPLACE VIEW Vue_Vehicule_Emissions AS
SELECT 
    TV.idTypeVehicule, 
    TV.LibelleTypeVehicule, 
    EC.annee, 
    SUM(EC.QuantiteCo2) AS total_co2
FROM TYPEVEHICULE TV
JOIN EMISSIONCO2 EC USING (idTypeVehicule)
GROUP BY 
    TV.idTypeVehicule, 
    TV.LibelleTypeVehicule, 
    EC.annee;
# Requête de consultation
SELECT * 
FROM Vue_Vehicule_Emissions
ORDER BY annee DESC, total_co2 DESC;


# Vue : Association des tournées avec les livreurs
CREATE OR REPLACE VIEW Vue_Tournees_Livreurs AS
SELECT 
    L.idLivreur, 
    L.PrenomLivreur, 
    L.nomLivreur, 
    T.idTournee, 
    T.DateTournee, 
    T.DistanceEstimeeKm
FROM LIVREUR L
JOIN TOURNEE T ON T.idLivreur = L.idLivreur
GROUP BY 
    L.idLivreur, 
    L.PrenomLivreur, 
    L.nomLivreur, 
    T.idTournee, 
    T.DateTournee, 
    T.DistanceEstimeeKm;
# Requête de consultation
SELECT 
    idLivreur, 
    PrenomLivreur, 
    nomLivreur,
    COUNT(idTournee) AS nb_tournees, 
    SUM(DistanceEstimeeKm) AS distance_totale_km
FROM Vue_Tournees_Livreurs
GROUP BY 
    idLivreur, 
    PrenomLivreur, 
    nomLivreur
ORDER BY distance_totale_km DESC;