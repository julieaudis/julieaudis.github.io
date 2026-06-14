-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le :  jeu. 02 avr. 2026 à 15:03
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
-- Base de données :  `saz`
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

-- --------------------------------------------------------

--
-- Structure de la table `collecter`
--

CREATE TABLE `collecter` (
  `idTournee` int(11) NOT NULL,
  `idLivraisonEntrante` int(11) NOT NULL,
  `dateProvenance` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
  MODIFY `idClient` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `emissionco2`
--
ALTER TABLE `emissionco2`
  MODIFY `idEmission` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `livraisonentrante`
--
ALTER TABLE `livraisonentrante`
  MODIFY `idLivraisonEntrante` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `livraisonsortante`
--
ALTER TABLE `livraisonsortante`
  MODIFY `idLivraisonS` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `livreur`
--
ALTER TABLE `livreur`
  MODIFY `idLivreur` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `partenaire`
--
ALTER TABLE `partenaire`
  MODIFY `idPartenaire` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `tournee`
--
ALTER TABLE `tournee`
  MODIFY `idTournee` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `typevehicule`
--
ALTER TABLE `typevehicule`
  MODIFY `idTypeVehicule` int(11) NOT NULL AUTO_INCREMENT;
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
