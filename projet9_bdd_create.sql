CREATE TABLE TypeVehicule(
   idTypeVehicule INT,
   LibelleTypeVehicule VARCHAR(50) NOT NULL,
   CapaciteKg DOUBLE NOT NULL,
   AutonomieKm DOUBLE NOT NULL,
   nbVehicule INT NOT NULL,
   PRIMARY KEY(idTypeVehicule)
)engine = innodb;

CREATE TABLE Livreur(
   idLivreur INT,
   PrenomLivreur VARCHAR(50) NOT NULL,
   nomLivreur VARCHAR(50) NOT NULL,
   DateEmbauche DATE NOT NULL,
   PRIMARY KEY(idLivreur)
)engine = innodb;

CREATE TABLE EmissionCo2(
   idEmission INT,
   annee INT NOT NULL,
   QuantiteCo2 DOUBLE NOT NULL,
   idTypeVehicule INT NOT NULL,
   PRIMARY KEY(idEmission),
   FOREIGN KEY(idTypeVehicule) REFERENCES TypeVehicule(idTypeVehicule)
)engine = innodb;

CREATE TABLE Partenaire(
   idPartenaire INT,
   nomPartenaire VARCHAR(50) NOT NULL,
   ruePartenaire VARCHAR(50) NOT NULL,
   cpPartenaire VARCHAR(5) NOT NULL,
   villePartenaire VARCHAR(50) NOT NULL,
   PRIMARY KEY(idPartenaire)
)engine = innodb;

CREATE TABLE LivraisonEntrante(
   idLivraisonEntrante INT,
   nbColis INT NOT NULL,
   dateReception DATE NOT NULL,
   idPartenaire INT NOT NULL,
   PRIMARY KEY(idLivraisonEntrante),
   FOREIGN KEY(idPartenaire) REFERENCES Partenaire(idPartenaire)
)engine = innodb;

CREATE TABLE Client(
   idClient INT,
   rueClient VARCHAR(50) NOT NULL,
   cpClient VARCHAR(5) NOT NULL,
   villeClient VARCHAR(50) NOT NULL,
   PRIMARY KEY(idClient)
)engine = innodb;

CREATE TABLE Tournee(
   idTournee INT,
   DateTournee DATE NOT NULL,
   DistanceEstimeeKm DOUBLE NOT NULL,
   idTypeVehicule INT NOT NULL,
   idLivreur INT NOT NULL,
   PRIMARY KEY(idTournee),
   FOREIGN KEY(idTypeVehicule) REFERENCES TypeVehicule(idTypeVehicule),
   FOREIGN KEY(idLivreur) REFERENCES Livreur(idLivreur)
)engine = innodb;

CREATE TABLE LivraisonSortante(
   idLivraisonS INT,
   DateLivraison DATE NOT NULL,
   Poids DOUBLE NOT NULL,
   nbColis INT NOT NULL,
   idTournee INT NOT NULL,
   idClient INT NOT NULL,
   PRIMARY KEY(idLivraisonS),
   FOREIGN KEY(idTournee) REFERENCES Tournee(idTournee),
   FOREIGN KEY(idClient) REFERENCES Client(idClient)
)engine = innodb;

CREATE TABLE Collecter(
   idTournee INT,
   idLivraisonEntrante INT,
   dateProvenance DATE,
   PRIMARY KEY(idTournee, idLivraisonEntrante),
   FOREIGN KEY(idTournee) REFERENCES Tournee(idTournee),
   FOREIGN KEY(idLivraisonEntrante) REFERENCES LivraisonEntrante(idLivraisonEntrante)
)engine = innodb;