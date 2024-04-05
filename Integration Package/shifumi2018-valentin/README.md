Lien vers le [wiki](https://gitlab.lis-lab.fr/qarma/shifumi2018/wikis/accueil) pour savoir comment l'installer  , et tout autre information concernant le projet.

# Description du Projet
Le jeu shifumy communément appelé le jeu(papier,feuille,ciseau) .
L’objectif et le mécanisme de jeu est simple, il faut affronter un ou plusieurs adversaires en utilisant l’une des trois armes: la pierre, la feuille ou la paire de ciseaux.

Le top départ est signaliser en général par 1/2/3 ou bien shi/fu/mi (phonétiquement [chi-fou-mi]), les adversaires dévoilent simultanément leur arme symbolisée par la forme de leur main.

- La pierre gagne face aux ciseaux. Elle les broie.
- Les ciseaux l’emportent face à la feuille qu’ils coupent.
- La feuille bat la pierre en l’enveloppant

Ayons découvert que l’être humain ne sait pas joue aleatoire mais qu’il plutôt influence par le sentiment d’avoir gagné ou d’avoir perdu.
nous avons essayer avec de faire sortir les strategie plus ou moins commune de l'être humain afin de créer un agent capable de predire le mouvement precedent de l'utilisateur avec une certaine certitude.
[voir article](https://www.pierrefeuilleciseaux.fr/pierre-feuille-ciseaux-les-regles-classiques/)


# Architecture du projet

![architecture de projet](https://image.ibb.co/doPJ3o/diagrame_package_Projet.png)

shufimi est la racine du projet dedans nous avons les dossier suivants:

- ressources  contient tout les fichier considere comme des données , ou les fichier utiliser par les agent 
- shifumy_demo  est un module qui contient tout les dossier de la platform , dans nôtre cas nous avons utilisé le framework django 
- shifumy_player est un module qui regroupe contient tout les code des agents artificiels

# Liens
Resources : https://sync.lif.univ-mrs.fr/index.php/s/QReyXYLQLV0oJnA (mdp: 
shifu)
