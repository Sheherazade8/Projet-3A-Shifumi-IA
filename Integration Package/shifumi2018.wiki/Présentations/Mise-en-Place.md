Ce document considère que les deux ordinateurs utilisés sont:
- Ordinateur de Luc: Dell XPS 13
- Ordinateur de Valentin: Macbook Pro

Les écrans utilisés sont:
- Ecran de Marina: iiyama gros
- Ecran de Valentin: iiyama petit

# Plan de montage

![IMG_20181114_114618](uploads/a319fc55a0b0700cb8e599fb8950c599/IMG_20181114_114618.jpg)

Architecture "client-serveur":
- Client: ordinateur chargé de la reconnaissance de geste (Ordinateur de Luc)
- Serveur: ordinateur principal, chargé de l'interface utilisateur et des intelligences artificielles (Ordinateur de Valentin).

L'accès à Internet n'est pas nécessaire, nous créons un réseau local grâce au cable Ethernet.

# Branchement réseau

Etapes:
- Brancher les deux ordinateurs entre eux avec le cable Ethernet (ou utiliser le WIFI, à vos risques et périls);
- Noter l'adresse IP de l'ordinateur "serveur" (grâce à la commande `ip a` ou `ifconfig` ou en se rendant dans Préférences Système>Réseaux);
- Noter cette adresse dans la variable `DEFAULT_HOST` en haut du fichier situé à `shifumy_reco/shifumy_reco/gesture_recognition_client.py` sur l'ordinateur "client";
- Sur l'ordinateur de Luc (client), cliquer sur l'icône ![icone](uploads/6d69eb5d80afbe9d9cbb32ecbef72188/icone.png) en haut à droite de l'écran et cliquer sur `Connecter` à droite du réseau appelé `Shifumi`

## Problèmes possibles

### Conflit d'adresse IP entre les ordinateurs: 

Changer manuellement l'adresse IP l'ordinateur de Luc (client):
- Cliquez sur l'icone ![icone](uploads/6d69eb5d80afbe9d9cbb32ecbef72188/icone.png) en haut à droite;
- Cliquez sur l'icone ![icone2](uploads/bf80e8b304f6c1d242e7e84c6a94718a/icone2.png);
- Allez ensuite sur Shifumi>IPv4 ;
- Double cliquez sur l'adresse Ip;
- Changez le dernier chiffre de cette adresse et enregistrez.

# Branchement des écrans

Chaque ordinateur doit être branché à un écran supplémentaire:

- Ordinateur Luc (client) relié à l'écran de Marina (le plus gros) via le cable HDMI (et un petit dongle usb-C)
- Ordinateur Valentin (serveur) relié à l'écran de Valentin (le plus petit) via le cable DVI (et un petit dongle special mac)

Paramètres des moniteurs sur les ordinateurs (devrait être déjà fait par défaut)

- Ordinateur Luc (client): Affichage dupliqué
- Ordinateur Valentin (serveur): Affichage étendu. Idéalement, l'écran de l'ordinateur est "virtuellement au dessus" de l'écran externe (dans les options de disposition des moniteurs, mais ce n'est pas non plus très important).

## Problèmes possibles

### Problème de résolution de l'affichage sur l'écran de Marina:

- Aller dans la configuration du système (menu déroulant en haut à gauche);
- Aller dans Matériel>Affichage et Ecran>Affichages;
- Choisir la bonne résolution, et la noter;
- Aller dans le fichier `shifumy_reco/shifumy_reco/image_processing.py` sur l'ordinateur de Luc et mettre la résolution notée précedemment dans la variable `DEFAULT_SCREEN_SIZE`, en haut du fichier (format (h x w)).

### Problème de résolution de l'affichage sur l'ordinateur serveur:

- Identifier les résolutions des deux écrans (main: écran du joueur; back: écran du public) et les noter;
- Aller dans le fichier `shifumy_demo_cv/shifumy_demo_cv/main.py` sur l'ordinateur de Valentin et mettre les résolutions notées précédemment dans les paramètres par défaut de la fonction `main_loop`, ligne 297.

# Lancement des programmes

Il faut d'abord lancer l'ordinateur serveur avant l'ordinateur client.
Il faut d'abord quitter l'ordinateur client avant l'ordinateur serveur. (IMPORTANT sinon c'est lourd)

## Ordinateur serveur:
- Ouvrir Pycharm (faire glisser le curseur de la souris sur la gauche de l'écran pour voir l'icone)
- Lancer le fichier `shifumy_demo_cv/shifumy_demo_cv/main.py`

### Problèmes possibles

#### Erreur de connection

- Attendre un peu, quelques essais;
- Vérifier que toutes les instances du programme ont bien été quittées;
- Vérifier qu'aucun programme n'est attaché au port 50000;
- Relancer.

#### Erreur module introuvable

- Vérifier dans la configuration de pycharm que c'est bien l'environnement `py35` qui est utilisé.

## Ordinateur client:

- Ouvrir Pycharm (Menu déroulant en haut à gauche)
- Lancer le fichier `shifumy_reco/shifumy_reco/gesture_recognition_client.py`

### Problèmes possibles

#### Erreur de connection

- Verifier que vous avez bien mis la bonne adresse IP en haut du fichier `shifumy_reco/shifumy_reco/gesture_recognition_client.py` (celle de l'autre ordinateur)

#### Erreur module introuvable

- Vérifier dans la configuration de pycharm que c'est bien l'environnement `shifuenv` qui est utilisé.

#### Artefacts sur la mosaique de la reconnaissance de geste ou l'image pré-processée n'est pas claire

- Essayer de positioner une lampe qui va bien éclairer le fond vert. Eviter les ombres ou les gradients de lumière;
- Executer le script `ve/check_image_stats.py`;
- Evacuer de devant la caméra pour qu'il n'y ai que le fond vert;
- Arrêter l'execution quand les chiffres ont l'air stable;
- Chaque ligne est une représentation en percentile des pixels de l'image (représentation hls: hue, luminosity, saturation);
- Identifier les valeurs de hue très majoritaires, eg, les valeurs comprises entre le deuxième percentile et l'avant dernier percentile;
- L'interval entre ces deux valeurs est l'interval de base. Les pixels qui ont des valeurs dans cet interval sont supprimés;
- Rajouter quelques unités (dépend de la stabilité des valeurs pendant le test, il vaut mieux voir grand) pour augmenter la taille de l'interval (le rendre moins sensible aux perturbations);
- Modifier les arguments `hls_lb` (lowerbound) et `hls_up` (upperbound) dans le constructeur de la classe ColoredBackgroundImageFeatureExtractor du fichier `shifumy_reco/shifumy_reco/image_processing.py` ligne 216 et 217;
- Lancer le script `shifumy_reco/shifumy_reco/image_processing.py` pour vérifier que ça fonctionne bien... et faire des ajustements tant que ça ne fonctionne pas.