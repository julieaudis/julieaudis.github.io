INSERT INTO typevehicule (LibelleTypeVehicule, CapaciteKg, AutonomieKm, nbVehicule) VALUES
('VeloCargo', 80, 60, 4),
('Triporteur', 120,  45,  3),
('UtilitaireElectrique', 500, 150,  2),
('Triporteur Pro', 350, 75, 4),
('Vélo cargo XL', 250, 90, 5),
('Utilitaire électrique XL', 1200, 320, 3),
('Mini utilitaire', 800, 250, 7),
('Scooter électrique', 150, 100, 9),
('Fourgon léger', 900, 280, 6),
('Camionnette électrique', 1500, 350, 2);
 

INSERT INTO emissionco2 (annee, QuantiteCo2, idTypeVehicule) VALUES
(2025, 4, 1),
(2025, 9, 2),
(2025, 21, 3),
(2026, 3, 1),
(2026, 7, 2),
(2026, 18, 3),
(2025, 4, 4),
(2025, 9, 5),
(2026, 18, 6),
(2026, 7, 2);
 
INSERT INTO partenaire (nomPartenaire, ruePartenaire, cpPartenaire, villePartenaire) VALUES
('Amazon', '12 Rue De La Logistique', '75001', 'Paris'),
('Cdiscount', '5 Avenue Du Commerce', '33000', 'Bordeaux'),
('Decathlon', '8 Rue Du Sport', '59000', 'Lille'),
('Fnac', '3 Boulevard Des Medias', '69001', 'Lyon'),
('Boulanger', '20 Rue De L Electronique', '31000', 'Toulouse'),
('Carrefour', '2 Rue Du Supermarché', '98000', 'Paris'),
('Super U', '5 Avenue Du Marais Poitevin', '79460', 'Magné'),
('Chronopost', '8 Rue Du Grand Port', '17000', 'La Rochelle'),
('La Poste', '3 Boulevard Des Dragons', '79000', 'Niort'),
('Leclerc', '20 Rue Du Magasin', '67000', 'Marigny');
 

INSERT INTO livreur (PrenomLivreur, nomLivreur, DateEmbauche) VALUES
('Thomas', 'Martin', '2021-03-15'),
('Julie', 'Bernard', '2020-07-01'),
('Karim', 'Benali', '2022-01-10'),
('Sophie', 'Dupont', '2019-11-20'),
('Paul', 'Dupont', '2019-11-20'),
('Suzanne', 'Dupont', '2019-11-20'),
('François', 'Dupont', '2019-11-20'),
('Mohamed', 'Dupont', '2019-11-20'),
('Sofia', 'Dupont', '2019-11-20'),
('Lucas', 'Petit', '2023-04-05');
 

INSERT INTO tournee (DateTournee, DistanceEstimeeKm, idTypeVehicule, idLivreur) VALUES
('2025-01-08', 35, 1, 1),
('2025-01-08', 42, 2, 2),
('2025-01-09', 110, 3, 3),
('2025-01-10', 28, 1, 4),
('2025-01-10', 55, 2, 5),
('2026-01-11', 130, 3, 1),
('2026-01-12', 40, 1, 2),
('2026-01-15', 95, 3, 3),
('2026-01-16', 33, 2, 2),
('2026-01-17', 22, 1, 2);
 

INSERT INTO client (rueClient, cpClient, villeClient) VALUES
('7 Rue Des Lilas', '64000', 'Pau'),
('14 Impasse Du Moulin', '64000', 'Pau'),
('3 Avenue Peplum', '64100', 'Bayonne'),
('22 Chemin Des Bois', '64200', 'Biarritz'),
('9 Rue Victor Hugo', '64000', 'Pau'),
('1 Allée Des Roses', '64300', 'Orthez'),
('5 Rue Du Gave', '64110', 'Jurançon'),
('18 Boulevard Pyrénées', '64000', 'Pau'),
('30 Route De Tarbes', '65000', 'Tarbes'),
('12 Rue Samonzet', '64000', 'Pau'),
('6 Impasse Du Gave', '64100', 'Bayonne');

INSERT INTO livraisonentrante (nbColis, dateReception, idPartenaire) VALUES
(15, '2025-01-08', 1),
(8, '2025-01-08', 2),
(20, '2025-01-09', 3),
(5, '2025-01-09', 1),
(12, '2025-01-10', 4),
(3, '2025-01-10', 5),
(18, '2026-01-11', 2),
(7, '2026-01-12', 3),
(10, '2026-01-15', 1),
(6, '2026-01-16', 4),
(9, '2026-01-17', 5);
 

INSERT INTO collecter (idTournee, idLivraisonEntrante, dateProvenance) VALUES
(1, 1, '2025-01-08'),
(1, 2, '2025-01-08'),
(2, 2, '2025-01-08'),
(3, 3, '2025-01-09'),
(3, 4, '2025-01-09'),
(4, 5, '2025-01-10'),
(4, 6, '2025-01-10'),
(5, 6, '2025-01-10'),
(6, 7, '2026-01-11'),
(7, 8, '2026-01-12'),
(8, 9, '2026-01-15'),
(9, 10, '2026-01-16'),
(10, 11, '2026-01-17');
 

INSERT INTO livraisonsortante (DateLivraison, Poids, nbColis, idTournee, idClient) VALUES
('2024-01-08', 4.50,  2, 1,  1),
('2025-01-08', 2.00,  1, 1,  2),
('2025-01-08', 7.80,  3, 2,  3),
('2025-01-09', 15.00, 4, 3,  4),
('2025-01-09', 1.20,  1, 3,  5),
('2025-01-10', 9.00,  2, 4,  6),
('2025-01-10', 3.50,  2, 5,  7),
('2026-01-10', 6.00,  3, 5,  8),
('2026-01-11', 22.00, 5, 6,  1),
('2026-01-11', 5.50,  2, 6,  9),
('2026-01-12', 0.80,  1, 7,  10),
('2026-01-15', 11.00, 3, 8,  2),
('2026-01-16', 4.00,  2, 9,  3),
('2026-01-17', 8.50,  4, 10, 4);
 
