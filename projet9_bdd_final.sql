-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le :  jeu. 02 avr. 2026 à 15:40
-- Version du serveur :  5.7.17
-- Version de PHP :  5.6.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `sae`
--

-- --------------------------------------------------------

--
-- Structure de la table `client`
--

CREATE TABLE `client` (
  `idClient` int(11) NOT NULL,
  `rueClient` varchar(50) NOT NULL,
  `cpClient` varchar(5) NOT NULL,
  `villeClient` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `client`
--

INSERT INTO `client` (`idClient`, `rueClient`, `cpClient`, `villeClient`) VALUES
(1, '7 Rue Des Lilas', '64000', 'Pau'),
(2, '14 Impasse Du Moulin', '64000', 'Pau'),
(3, '3 Avenue Peplum', '64100', 'Bayonne'),
(4, '22 Chemin Des Bois', '64200', 'Biarritz'),
(5, '9 Rue Victor Hugo', '64000', 'Pau'),
(6, '1 Allée Des Roses', '64300', 'Orthez'),
(7, '5 Rue Du Gave', '64110', 'Jurançon'),
(8, '18 Boulevard Pyrénées', '64000', 'Pau'),
(9, '30 Route De Tarbes', '65000', 'Tarbes'),
(10, '12 Rue Samonzet', '64000', 'Pau'),
(11, '6 Impasse Du Gave', '64100', 'Bayonne');

-- --------------------------------------------------------

--
-- Structure de la table `collecter`
--

CREATE TABLE `collecter` (
  `idTournee` int(11) NOT NULL,
  `idLivraisonEntrante` int(11) NOT NULL,
  `dateProvenance` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `collecter`
--

INSERT INTO `collecter` (`idTournee`, `idLivraisonEntrante`, `dateProvenance`) VALUES
(1, 1, '2024-01-08'),
(1, 2, '2024-01-08'),
(2, 2, '2024-01-08'),
(3, 3, '2024-01-09'),
(3, 4, '2024-01-09'),
(4, 5, '2024-01-10'),
(4, 6, '2024-01-10'),
(5, 6, '2024-01-10'),
(6, 7, '2024-01-11'),
(7, 8, '2024-01-12'),
(8, 9, '2024-01-15'),
(9, 10, '2024-01-16'),
(10, 11, '2024-01-17');

-- --------------------------------------------------------

--
-- Structure de la table `emissionco2`
--

CREATE TABLE `emissionco2` (
  `idEmission` int(11) NOT NULL,
  `annee` int(11) NOT NULL,
  `QuantiteCo2` double NOT NULL,
  `idTypeVehicule` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `emissionco2`
--

INSERT INTO `emissionco2` (`idEmission`, `annee`, `QuantiteCo2`, `idTypeVehicule`) VALUES
(1, 2025, 4, 1),
(2, 2025, 9, 2),
(3, 2025, 21, 3),
(4, 2026, 3, 1),
(5, 2026, 7, 2),
(6, 2026, 18, 3),
(7, 2025, 4, 4),
(8, 2025, 9, 5),
(9, 2026, 18, 6),
(10, 2026, 7, 2);

-- --------------------------------------------------------

--
-- Structure de la table `livraisonentrante`
--

CREATE TABLE `livraisonentrante` (
  `idLivraisonEntrante` int(11) NOT NULL,
  `nbColis` int(11) NOT NULL,
  `dateReception` date NOT NULL,
  `idPartenaire` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `livraisonentrante`
--

INSERT INTO `livraisonentrante` (`idLivraisonEntrante`, `nbColis`, `dateReception`, `idPartenaire`) VALUES
(1, 15, '2024-01-08', 1),
(2, 8, '2024-01-08', 2),
(3, 20, '2024-01-09', 3),
(4, 5, '2024-01-09', 1),
(5, 12, '2024-01-10', 4),
(6, 3, '2024-01-10', 5),
(7, 18, '2024-01-11', 2),
(8, 7, '2024-01-12', 3),
(9, 10, '2024-01-15', 1),
(10, 6, '2024-01-16', 4),
(11, 9, '2024-01-17', 5);

-- --------------------------------------------------------

--
-- Structure de la table `livraisonsortante`
--

CREATE TABLE `livraisonsortante` (
  `idLivraisonS` int(11) NOT NULL,
  `DateLivraison` date NOT NULL,
  `Poids` double NOT NULL,
  `nbColis` int(11) NOT NULL,
  `idTournee` int(11) NOT NULL,
  `idClient` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `livraisonsortante`
--

INSERT INTO `livraisonsortante` (`idLivraisonS`, `DateLivraison`, `Poids`, `nbColis`, `idTournee`, `idClient`) VALUES
(1, '2024-01-08', 4.5, 2, 1, 1),
(2, '2024-01-08', 2, 1, 1, 2),
(3, '2024-01-08', 7.8, 3, 2, 3),
(4, '2024-01-09', 15, 4, 3, 4),
(5, '2024-01-09', 1.2, 1, 3, 5),
(6, '2024-01-10', 9, 2, 4, 6),
(7, '2024-01-10', 3.5, 2, 5, 7),
(8, '2024-01-10', 6, 3, 5, 8),
(9, '2024-01-11', 22, 5, 6, 1),
(10, '2024-01-11', 5.5, 2, 6, 9),
(11, '2024-01-12', 0.8, 1, 7, 10),
(12, '2024-01-15', 11, 3, 8, 2),
(13, '2024-01-16', 4, 2, 9, 3),
(14, '2024-01-17', 8.5, 4, 10, 4);

-- --------------------------------------------------------

--
-- Structure de la table `livreur`
--

CREATE TABLE `livreur` (
  `idLivreur` int(11) NOT NULL,
  `PrenomLivreur` varchar(50) NOT NULL,
  `nomLivreur` varchar(50) NOT NULL,
  `DateEmbauche` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `livreur`
--

INSERT INTO `livreur` (`idLivreur`, `PrenomLivreur`, `nomLivreur`, `DateEmbauche`) VALUES
(1, 'Thomas', 'Martin', '2021-03-15'),
(2, 'Julie', 'Bernard', '2020-07-01'),
(3, 'Karim', 'Benali', '2022-01-10'),
(4, 'Sophie', 'Dupont', '2019-11-20'),
(5, 'Paul', 'Dupont', '2019-11-20'),
(6, 'Suzanne', 'Dupont', '2019-11-20'),
(7, 'François', 'Dupont', '2019-11-20'),
(8, 'Mohamed', 'Dupont', '2019-11-20'),
(9, 'Sofia', 'Dupont', '2019-11-20'),
(10, 'Lucas', 'Petit', '2023-04-05');

-- --------------------------------------------------------

--
-- Structure de la table `partenaire`
--

CREATE TABLE `partenaire` (
  `idPartenaire` int(11) NOT NULL,
  `nomPartenaire` varchar(50) NOT NULL,
  `ruePartenaire` varchar(50) NOT NULL,
  `cpPartenaire` varchar(5) NOT NULL,
  `villePartenaire` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `partenaire`
--

INSERT INTO `partenaire` (`idPartenaire`, `nomPartenaire`, `ruePartenaire`, `cpPartenaire`, `villePartenaire`) VALUES
(1, 'Amazon', '12 Rue De La Logistique', '75001', 'Paris'),
(2, 'Cdiscount', '5 Avenue Du Commerce', '33000', 'Bordeaux'),
(3, 'Decathlon', '8 Rue Du Sport', '59000', 'Lille'),
(4, 'Fnac', '3 Boulevard Des Medias', '69001', 'Lyon'),
(5, 'Boulanger', '20 Rue De L Electronique', '31000', 'Toulouse'),
(6, 'Carrefour', '2 Rue Du Supermarché', '98000', 'Paris'),
(7, 'Super U', '5 Avenue Du Marais Poitevin', '79460', 'Magné'),
(8, 'Chronopost', '8 Rue Du Grand Port', '17000', 'La Rochelle'),
(9, 'La Poste', '3 Boulevard Des Dragons', '79000', 'Niort'),
(10, 'Leclerc', '20 Rue Du Magasin', '67000', 'Marigny');

-- --------------------------------------------------------

--
-- Structure de la table `tournee`
--

CREATE TABLE `tournee` (
  `idTournee` int(11) NOT NULL,
  `DateTournee` date NOT NULL,
  `DistanceEstimeeKm` double NOT NULL,
  `idTypeVehicule` int(11) NOT NULL,
  `idLivreur` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `tournee`
--

INSERT INTO `tournee` (`idTournee`, `DateTournee`, `DistanceEstimeeKm`, `idTypeVehicule`, `idLivreur`) VALUES
(1, '2024-01-08', 35, 1, 1),
(2, '2024-01-08', 42, 2, 2),
(3, '2024-01-09', 110, 3, 3),
(4, '2024-01-10', 28, 1, 4),
(5, '2024-01-10', 55, 2, 5),
(6, '2024-01-11', 130, 3, 1),
(7, '2024-01-12', 40, 1, 2),
(8, '2024-01-15', 95, 3, 3),
(9, '2024-01-16', 33, 2, 4),
(10, '2024-01-17', 22, 1, 5);

-- --------------------------------------------------------

--
-- Structure de la table `typevehicule`
--

CREATE TABLE `typevehicule` (
  `idTypeVehicule` int(11) NOT NULL,
  `LibelleTypeVehicule` varchar(50) NOT NULL,
  `CapaciteKg` double NOT NULL,
  `AutonomieKm` double NOT NULL,
  `nbVehicule` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `typevehicule`
--

INSERT INTO `typevehicule` (`idTypeVehicule`, `LibelleTypeVehicule`, `CapaciteKg`, `AutonomieKm`, `nbVehicule`) VALUES
(1, 'VeloCargo', 80, 60, 4),
(2, 'Triporteur', 120, 45, 3),
(3, 'UtilitaireElectrique', 500, 150, 2),
(4, 'Triporteur Pro', 350, 75, 4),
(5, 'Vélo cargo XL', 250, 90, 5),
(6, 'Utilitaire électrique XL', 1200, 320, 3),
(7, 'Mini utilitaire', 800, 250, 7),
(8, 'Scooter électrique', 150, 100, 9),
(9, 'Fourgon léger', 900, 280, 6),
(10, 'Camionnette électrique', 1500, 350, 2);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`idClient`);

--
-- Index pour la table `collecter`
--
ALTER TABLE `collecter`
  ADD PRIMARY KEY (`idTournee`,`idLivraisonEntrante`),
  ADD KEY `idLivraisonEntrante` (`idLivraisonEntrante`);

--
-- Index pour la table `emissionco2`
--
ALTER TABLE `emissionco2`
  ADD PRIMARY KEY (`idEmission`),
  ADD KEY `idTypeVehicule` (`idTypeVehicule`);

--
-- Index pour la table `livraisonentrante`
--
ALTER TABLE `livraisonentrante`
  ADD PRIMARY KEY (`idLivraisonEntrante`),
  ADD KEY `idPartenaire` (`idPartenaire`);

--
-- Index pour la table `livraisonsortante`
--
ALTER TABLE `livraisonsortante`
  ADD PRIMARY KEY (`idLivraisonS`),
  ADD KEY `idTournee` (`idTournee`),
  ADD KEY `idClient` (`idClient`);

--
-- Index pour la table `livreur`
--
ALTER TABLE `livreur`
  ADD PRIMARY KEY (`idLivreur`);

--
-- Index pour la table `partenaire`
--
ALTER TABLE `partenaire`
  ADD PRIMARY KEY (`idPartenaire`);

--
-- Index pour la table `tournee`
--
ALTER TABLE `tournee`
  ADD PRIMARY KEY (`idTournee`),
  ADD KEY `idTypeVehicule` (`idTypeVehicule`),
  ADD KEY `idLivreur` (`idLivreur`);

--
-- Index pour la table `typevehicule`
--
ALTER TABLE `typevehicule`
  ADD PRIMARY KEY (`idTypeVehicule`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `client`
--
ALTER TABLE `client`
  MODIFY `idClient` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
--
-- AUTO_INCREMENT pour la table `emissionco2`
--
ALTER TABLE `emissionco2`
  MODIFY `idEmission` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT pour la table `livraisonentrante`
--
ALTER TABLE `livraisonentrante`
  MODIFY `idLivraisonEntrante` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
--
-- AUTO_INCREMENT pour la table `livraisonsortante`
--
ALTER TABLE `livraisonsortante`
  MODIFY `idLivraisonS` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
--
-- AUTO_INCREMENT pour la table `livreur`
--
ALTER TABLE `livreur`
  MODIFY `idLivreur` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT pour la table `partenaire`
--
ALTER TABLE `partenaire`
  MODIFY `idPartenaire` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT pour la table `tournee`
--
ALTER TABLE `tournee`
  MODIFY `idTournee` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT pour la table `typevehicule`
--
ALTER TABLE `typevehicule`
  MODIFY `idTypeVehicule` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `collecter`
--
ALTER TABLE `collecter`
  ADD CONSTRAINT `collecter_ibfk_1` FOREIGN KEY (`idTournee`) REFERENCES `tournee` (`idTournee`),
  ADD CONSTRAINT `collecter_ibfk_2` FOREIGN KEY (`idLivraisonEntrante`) REFERENCES `livraisonentrante` (`idLivraisonEntrante`);

--
-- Contraintes pour la table `emissionco2`
--
ALTER TABLE `emissionco2`
  ADD CONSTRAINT `emissionco2_ibfk_1` FOREIGN KEY (`idTypeVehicule`) REFERENCES `typevehicule` (`idTypeVehicule`);

--
-- Contraintes pour la table `livraisonentrante`
--
ALTER TABLE `livraisonentrante`
  ADD CONSTRAINT `livraisonentrante_ibfk_1` FOREIGN KEY (`idPartenaire`) REFERENCES `partenaire` (`idPartenaire`);

--
-- Contraintes pour la table `livraisonsortante`
--
ALTER TABLE `livraisonsortante`
  ADD CONSTRAINT `livraisonsortante_ibfk_1` FOREIGN KEY (`idTournee`) REFERENCES `tournee` (`idTournee`),
  ADD CONSTRAINT `livraisonsortante_ibfk_2` FOREIGN KEY (`idClient`) REFERENCES `client` (`idClient`);

--
-- Contraintes pour la table `tournee`
--
ALTER TABLE `tournee`
  ADD CONSTRAINT `tournee_ibfk_1` FOREIGN KEY (`idTypeVehicule`) REFERENCES `typevehicule` (`idTypeVehicule`),
  ADD CONSTRAINT `tournee_ibfk_2` FOREIGN KEY (`idLivreur`) REFERENCES `livreur` (`idLivreur`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
