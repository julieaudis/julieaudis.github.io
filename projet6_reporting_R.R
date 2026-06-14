# Définition du répertoire de travail où se trouvent les fichiers
setwd("/Volumes/EMTEC C410/SAE reporting data visualisation/Les fichiers-20260518")

# Chargement de la librairie ggplot2 pour les graphiques
library(ggplot2)

# Chargement du fichier parcoursup 2025
parcoursup_2025 <- read.csv2("fr-esr-parcoursup_2025.csv")

# Chargement du fichier parcoursup 2024
parcoursup_2024 <- read.csv2("fr-esr-parcoursup_2024.csv")

# Chargement du fichier des effectifs en terminale
terminale <- read.csv2("fr-en-effectifs-specialites-doublettes-terminale-generale.csv")

# Sélection des lignes dont la filière commence par BUT dans le fichier 2025
but2025 <- parcoursup_2025[substr(parcoursup_2025$Filière.de.formation,1, 3) == "BUT",]

# Sélection des lignes dont la filière commence par BUT dans le fichier 2024
but2024 <- parcoursup_2024[substr(parcoursup_2024$Filière.de.formation,1, 3) == "BUT",]

# Création de la colonne Domaine pour but2025 : attribution du domaine selon le nom de la filière
but2025$Domaine <- ifelse(
  # Si la filière contient informatique, réseaux ou multimédia
  grepl("informatique|réseaux|multimédia", 
        but2025$Filière.de.formation,
        ignore.case = TRUE),
  # Alors le domaine est Informatique
  "Informatique",
  
  ifelse(
    # Si la filière contient carrières sociales ou social
    grepl("carrières sociales|social", 
          but2025$Filière.de.formation,
          ignore.case = TRUE),
    # Alors le domaine est Social
    "Social",
    
    ifelse(
      # Si la filière contient gestion, commerce ou techniques de commercialisation
      grepl("gestion|commerce|techniques de commercialisation",
            but2025$Filière.de.formation,
            ignore.case = TRUE),
      # Alors le domaine est Commerce / Gestion
      "Commerce / Gestion",
      
      ifelse(
        # Si la filière contient génie, mesures physiques, chimie ou biologie
        grepl("génie|mesures physiques|chimie|biologie",
              but2025$Filière.de.formation,
              ignore.case = TRUE),
        # Alors le domaine est Sciences / Industrie
        "Sciences / Industrie",
        
        # Sinon le domaine est Autres
        "Autres"
      )
    )
  )
)

# Création de la colonne Domaine pour but2024 : même logique que pour but2025
but2024$Domaine <- ifelse(
  # Si la filière contient informatique, réseaux ou multimédia
  grepl("informatique|réseaux|multimédia", 
        but2024$Filière.de.formation,
        ignore.case = TRUE),
  # Alors le domaine est Informatique
  "Informatique",
  
  ifelse(
    # Si la filière contient carrières sociales ou social
    grepl("carrières sociales|social", 
          but2024$Filière.de.formation,
          ignore.case = TRUE),
    # Alors le domaine est Social
    "Social",
    
    ifelse(
      # Si la filière contient gestion, commerce ou techniques de commercialisation
      grepl("gestion|commerce|techniques de commercialisation",
            but2024$Filière.de.formation,
            ignore.case = TRUE),
      # Alors le domaine est Commerce / Gestion
      "Commerce / Gestion",
      
      ifelse(
        # Si la filière contient génie, mesures physiques, chimie ou biologie
        grepl("génie|mesures physiques|chimie|biologie",
              but2024$Filière.de.formation,
              ignore.case = TRUE),
        # Alors le domaine est Sciences / Industrie
        "Sciences / Industrie",
        
        # Sinon le domaine est Autres
        "Autres"
      )
    )
  )
)

# ── Graphique 1 : variable qualitative ──────────────────────────────────────

# Comptage et tri croissant du nombre de formations par domaine
tab <- sort(table(but2025$Domaine))

# Définition des marges : bas, gauche, haut, droite
par(mar = c(5, 12, 5, 5))

# Diagramme en barres horizontal du nombre de formations par domaine
barplot(tab,
        horiz     = TRUE,      # barres horizontales
        las       = 1,         # labels perpendiculaires à l'axe
        col       = "plum",    # couleur des barres
        border    = "black",   # couleur de la bordure des barres
        xlim      = c(0, 300), # limite maximale de l'axe x
        main      = "Nombre de formations BUT présentes par domaine ", # titre
        xlab      = "Nombre de formations", # label axe x
        cex.main  = 1,         # taille du titre
        cex.names = 0.9)       # taille des noms des barres

# ── Graphique 2 : variable quantitative ─────────────────────────────────────

# Conversion du taux d'accès en numérique pour éviter l'erreur de calcul
but2025$Taux.d.accès <- as.numeric(but2025$Taux.d.accès)

# Définition des marges avec marge droite agrandie pour afficher les labels
par(mar = c(5, 5, 5, 7))

# Boîte à moustaches de la distribution du taux d'accès
boxplot(but2025$Taux.d.accès,
        col    = "plum",       # couleur de la boîte
        border = "black",      # couleur de la bordure
        ylim   = c(0, 100),    # limite de l'axe y entre 0 et 100
        xlim   = c(0.5, 1.8),  # limite de l'axe x pour centrer la boîte
        main   = "Distribution du taux d'accès\ndans les formations BUT (2025)", # titre
        ylab   = "Taux d'accès (%)", # label axe y
        xlab   = "BUT 2025")         # label axe x

# Calcul du premier quartile
q1  <- quantile(but2025$Taux.d.accès, 0.25, na.rm = TRUE)

# Calcul de la médiane
med <- median(but2025$Taux.d.accès, na.rm = TRUE)

# Calcul du troisième quartile
q3  <- quantile(but2025$Taux.d.accès, 0.75, na.rm = TRUE)

# Ligne pointillée horizontale au niveau de Q1
abline(h = q1,  lty = 2, col = "plum")

# Ligne pointillée horizontale au niveau de la médiane
abline(h = med, lty = 2, col = "black")

# Ligne pointillée horizontale au niveau de Q3
abline(h = q3,  lty = 2, col = "plum")

# Label Q1 affiché dans la marge droite
mtext(paste("Q1 =", q1, "%"),       side = 4, at = q1,  las = 1, col = "plum",  cex = 0.9)

# Label médiane affiché dans la marge droite
mtext(paste("Médiane =", med, "%"), side = 4, at = med, las = 1, col = "black", cex = 0.9)

# Label Q3 affiché dans la marge droite
mtext(paste("Q3 =", q3, "%"),       side = 4, at = q3,  las = 1, col = "plum",  cex = 0.9)

# ── Graphique 3 : variable qualitative × variable quantitative ───────────────
# Conversion de la variable "Taux.d.accès" en données numériques
# pour pouvoir effectuer des calculs statistiques
but2025$Taux.d.accès <- as.numeric(but2025$Taux.d.accès)

# Calcul de la moyenne du taux d'accès pour chaque domaine de BUT
# tapply applique ici la fonction mean selon les catégories de Domaine
moy_taux <- tapply(but2025$Taux.d.accès,
                   but2025$Domaine,
                   mean,
                   na.rm = TRUE) # ignore les valeurs manquantes

# Tri des moyennes dans l'ordre croissant
moy_taux <- sort(moy_taux)

# Définition des marges du graphique :
# bas, gauche, haut, droite
par(mar = c(5, 12, 5, 5))

# Création d'un diagramme en barres horizontal
bp <- barplot(moy_taux,
              
              horiz = TRUE, # barres horizontales
              
              las = 1, # orientation horizontale des labels
              
              col = "plum", # couleur des barres
              
              border = "black", # couleur des bordures
              
              xlim = c(0, 100), # limites de l'axe des x
              
              xlab = "Taux d'accès moyen (%)", # label de l'axe x
              
              main = "Taux d'accès moyen par domaine BUT", # titre
              
              cex.names = 0.9) # taille des noms des domaines

# Ajout des valeurs numériques au bout des barres
text(x = moy_taux + 6, # position légèrement à droite des barres
     
     y = bp, # position verticale des textes
     
     labels = round(moy_taux,1), # affichage arrondi à 1 décimale
     
     cex = 0.8) # taille du texte

# ── Graphique 4 : deux variables qualitatives ────────────────────────────────

# Comptage du nombre de formations BUT par domaine en 2024
tab2024 <- table(but2024$Domaine)

# Comptage du nombre de formations BUT par domaine en 2025
tab2025 <- table(but2025$Domaine)

# Création d'une matrice regroupant 2024 et 2025
tab_compare <- rbind(tab2024, tab2025)

# Définition des marges :
# bas, gauche, haut, droite
par(mar = c(7, 12, 5, 2))

# Création du diagramme en barres groupées
barplot(tab_compare,
        
        beside = TRUE, # barres côte à côte
        
        horiz = TRUE, # barres horizontales
        
        las = 1, # labels horizontaux
        
        col = c("plum", "violet"), # couleurs des années
        
        border = "black", # bordure des barres
        
        xlab = "Nombre de formations", # label axe x
        
        
        main = "Comparaison des domaines BUT\nentre 2024 et 2025" # titre
)

# Ajout de la légende
legend(
  x = 200, y = 15,
  
  legend = c("2024", "2025"), # années
  
  fill = c("plum", "violet"), # couleurs associées
  
  bty = "n", # suppression du cadre
  
  cex = 0.9 # taille du texte
)

# ── Graphique 5 : deux variables quantitatives ───────────────────────────────
# Normalisation du nom de la colonne académie dans le fichier terminale (majuscules + suppression espaces)
terminale$Academie_norm  <- toupper(trimws(terminale$Académie))

# Conversion de l'effectif total en numérique pour pouvoir faire des calculs
terminale$Effectif.total <- as.numeric(terminale$Effectif.total)

# Normalisation du nom de la colonne académie dans le fichier parcoursup (majuscules + suppression espaces)
but2025$Academie_norm    <- toupper(trimws(but2025$Académie.de.l.établissement))

# Calcul de la somme des effectifs en terminale générale par académie
eff_acad  <- aggregate(Effectif.total ~ Academie_norm, data = terminale, FUN = sum,  na.rm = TRUE)

# Calcul du taux d'accès moyen en BUT par académie
taux_acad <- aggregate(Taux.d.accès   ~ Academie_norm, data = but2025,   FUN = mean, na.rm = TRUE)

# Fusion des deux tableaux sur la colonne académie
merged <- merge(eff_acad, taux_acad, by = "Academie_norm")

# Définition des marges du graphique : bas, gauche, haut, droite
par(mar = c(5, 5, 5, 2))

# Création du nuage de points : chaque point = une académie
plot(merged$Effectif.total, merged$Taux.d.accès,
     col  = "plum",   # couleur des points
     pch  = 19,       # forme des points : cercle plein
     xlab = "Effectif total en terminale générale",  # label axe x
     ylab = "Taux d'accès moyen en BUT (%)",         # label axe y
     main = "Effectif en terminale vs taux d'accès BUT\npar académie (2025)") # titre

# Ajout du nom de chaque académie au-dessus de son point
text(merged$Effectif.total, merged$Taux.d.accès,
     labels = merged$Academie_norm, # nom de l'académie
     cex    = 0.6,  # taille du texte
     pos    = 3)    # position au-dessus du point
# ── Graphique 6 : 3 variables (ggplot2) ─────────────────────────────────────

# Agrégation des effectifs d'admis par domaine
donneess <- aggregate(cbind(Effectif.des.admis.néo.bacheliers.généraux,
                            Effectif.des.admis.néo.bacheliers.technologiques,
                            Effectif.des.admis.néo.bacheliers.professionnels) ~ Domaine,
                      data = but2025, # données source
                      FUN  = sum)     # fonction d'agrégation : somme

# Initialisation du graphique avec le domaine en axe x
ggplot(donneess, aes(x = Domaine)) +
  # Barres des admis bac général en lavande
  geom_col(aes(y = Effectif.des.admis.néo.bacheliers.généraux,       fill = "General")) +
  # Barres des admis bac technologique en violet
  geom_col(aes(y = Effectif.des.admis.néo.bacheliers.technologiques,  fill = "Techno"))  +
  # Barres des admis bac professionnel en violet foncé
  geom_col(aes(y = Effectif.des.admis.néo.bacheliers.professionnels,  fill = "Pro"))     +
  # Définition manuelle des couleurs pour chaque type de bac
  scale_fill_manual(values = c("General" = "lavender",  # lavande pour bac général
                               "Techno"  = "violet",    # violet pour bac techno
                               "Pro"     = "purple")) + # violet foncé pour bac pro
  # Titres des axes et du graphique
  labs(title = "Admis par domaine BUT et type de bac (2025)", # titre
       x     = "Domaine",       # label axe x
       y     = "Nombre d'admis", # label axe y
       fill  = "Type de bac") + # titre de la légende
  # Thème épuré sans fond gris
  theme_minimal()

# ── Graphique 7 : données géographiques ─────────────────────────────────────

# Comptage et tri croissant du nombre de formations BUT par région
count_region <- sort(table(but2025$Région.de.l.établissement))


# Définition des marges avec grande marge gauche pour les noms de régions
par(mar = c(5, 14, 5, 4))

# Diagramme en barres horizontal du nombre de formations par région
bp <- barplot(count_region,
              horiz     = TRUE,    # barres horizontales
              las       = 1,       # labels horizontaux
              col       = "plum",  # couleur des barres
              border    = "black", # bordure noire
              xlab      = "Nombre de formations BUT", # label axe x
              main      = "Nombre de formations BUT par région", # titre
              cex.names = 0.8)    # taille des noms des régions
            

# Affichage des valeurs numériques à droite de chaque barre
text(x      = count_region + 10, # position légèrement à droite de la barre
     y      = bp,                # position verticale alignée sur la barre
     labels = count_region,      # valeur affichée
     cex    = 0.8,               # taille du texte
     font   = 1)                 # style normal

