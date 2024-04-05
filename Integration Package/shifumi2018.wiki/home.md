* [Données (Version web)](https://gitlab.lis-lab.fr/qarma/shifumi2018/wikis/données)
* [Les joueurs IA](ias)
* [La logistique](logistique)

# Installation

Le projet Shifum-AI se décompose en trois parties que sont:
- La démo
- La reconnaissance de geste
- L'intelligence de jeu

Ces trois parties sont plus ou moins indépendantes et nécessitent une installation séparée.

La version principale du projet est celle qui supporte OpenCV (branche `Valentin`). Si vous souhaitez essayer la version sans reconnaissance de geste, visitez la branche `master` et faites l'installation en version web. Cette dernière n'est pas garantie de fonctionner.

- [Principale (Version OpenCV)](https://gitlab.lis-lab.fr/qarma/shifumi2018/wikis/installation/composants-principaux)
- [Dépréciée (Version WEB)](https://gitlab.lis-lab.fr/qarma/shifumi2018/wikis/installation/shifumy_demo)


# Description du projet
- [Objectifs initiaux](https://gitlab.lis-lab.fr/qarma/shifumi2018/wikis/Projet/Objectifs)
- [Etat courant](https://gitlab.lis-lab.fr/qarma/shifumi2018/wikis/Projet/etat-courant)
- [A faire](https://gitlab.lis-lab.fr/qarma/shifumi2018/wikis/Projet/A-faire)


# CR des réunions
* [Réunion du 24 mai 2018](Réunions/cr_2018-05-24)
* [Réunion du 8 juin 2018](Réunions/cr_2018-06-08)
* [Réunion du 15 juin 2018](Réunions/cr_2018-06-15)
* [Réunion du 29 juin 2018](Réunions/cr_2018-06-29)
* [Réunion du 17 juillet 2018](Réunions/cr_2018-07-17)
* [Réunion du 20 juillet 2018](Réunions/cr_2018-07-20)
* [Réunion du 25 juillet 2018](Réunions/cr_2018-07-25)

# Descriptifs des présentations
* [Nuit des chercheurs 2018]
* [Fête de la science 2018](https://gitlab.lis-lab.fr/qarma/shifumi2018/wikis/Evenements/Fete-de-la-Science-2018)

# Questions et actions fréquentes des participants

## Questions

1.  "Il triche !" 
Non, montrer la séquence d'événements, puisque l'ordi IA indique le coup que va jouer l'IA avant même que l'humain ne joue: l'IA décide très vite sa solution, et elle n'est prise en compte qu'une fois que l'humain a joué son coup.
2.  "Pourquoi n'y a-t-il pas le puits ?"
Ce n'est pas nécessaire pour ce que nous voulons vous démontrer (rappel). Mais surtout, ajouter le puits crée un déséquilibre (le puits gagne sur 2 autres/3 -- caillou et ciseaux --, ciseaux et caillou ne gagnent que sur un autre/3 (resp. papier et ciseaux), et papier gagne sur 2 autres/3 -- caillou et puits). Ce déséquilibre modifie le hasard, est même si cela n'a pas de conséquences immédiates, il est évident que cela pousse l'humain à privilégier le jeu de puits ou papier, quid de la machine ?  
3.  "Quelles sont les différences entre les joueurs artificiels ?"
4.  "Pourquoi y'a des joueurs artificiels plus forts que d'autres ?"
5.  "Comment faire pour les battre tous les trois ?" 
6.  "Avec ma stratégie, j'ai battu OlivIA facilement, mais j'ai lamentablement perdu contre KillIAs. Pourquoi ?"
7.  "Donc, si j'ai bien compris, plus je joue de round, moins j'ai de chances de gagner contre la machine ?"
8.  "Pourquoi vous ne nous montrez pas un joueur artificiel qui jouerait contre un autre ? Qui gagnerait ?"
A faire
9.  "Et moi, je peux créer mon joueur artificiel ? Je voudrais qu'il joue toujours Caillou et voir si comme ça je peux battre OlivIA"
10.  "C'est l'IA qui ne sait pas voir la différence entre papier et ciseaux ? Elle est trop bête pour une intelligence !"
Rappeler le dispositif en deux parties
11.  "Ma grand-mère sait jouer à ce jeu, mais elle est handicapée mentale: elle peut quand même battre AI-Capone ? Ca lui ferait plaisir !"
12.
 
## Actions

1.  Quand le public a accès au coup que va jouer l'IA, il a tendance à souffler une solution au joueur, soit pour le faire gagner, soit pour le faire perdre: cela biaise le jeu de données en construction, donc limiter l'accès au coup futur seulement dans les 2 premières minutes, puis l'enlever, pour récupérer qques données sans ce biais.
2.  Faire un geste qui ne fait pas partie du jeu (pouce levé, doigt d'honneur, etc.): en profiter pour rappeler les deux phases du programme.
3.  Tentative de jeu très rapide (donc qui tend au hasard), et ça marche ! Mais parfois ça bugue (temps de reconnaissance du geste, nécessité de retirer la main pas toujours respectée, etc.)
4.  

# Bugs ou difficultés constatés

1.  Non reconnaissance de la webcam sur mac: dans le programme de reconnaissance des gestes, y'a un VideoCapture quelque part: changer le paramètre 0 -- webcam par défaut, souvent celle du laptop -- par 1 -- la deuxième reconnue par l'ordi.
2.  Internet n'est pas requis: on relie les deux ordis par un cable ethernet, l'un des deux aura défini une adresse IP virtuelle, l'autre s'y greffe et ça roule ma poule
3.  Du bruit dans la captation video: retendre le tissu vert, jouer avec les lumières alentours quand aucune lumière blanche n'est dispo: la moindre ombre peut être fatale.
4.  Nécessité de redémarrer l'ordi IA à chaque fin de round: j'ai oublié la solution que Marina et Luc ont mise en oeuvre avec succès. 

[Nettoyage](cleaning)