La branche `valentin` contient le code le plus à jour.

Un module `shifumy_player` contenant plusieurs joueurs artificiels a été crée. Les joueurs artificiels diffèrent par leur façon de détecter une stratégie chez l'humain, e.g. par les algorithmes d'apprentissage qu'ils utilisent. Vous trouverez l'ensemble des classes correpondantes aux joueurs artificiels implémentés à l'adresse sous l'arborescence `./shifumy_player/shifumy_player/players`

Deux interfaces de jeux ont été créees:
- Une interface WEB dans la module `shifumy_demo` et la branche `master` qui ne supporte pas la reconnaissance de geste;
- Une interface OpenCV (la plus récente) dans le module `shifumy_demo_cv` qui supporte la reconnaissance de geste grâce au module `shifumy_reco`.

Un module de reconnaissance de geste a été écrit et il comprend:
- L'extraction de features (suppression du fond vert, crop, etc.)
- La détection du geste

Une partie se déroule de la façon suivante:
1.  définir son coup à jouer en fonction de ce qu'il s'est passé auparavant, dans l'objectif de gagner;
2.  reconnaître le geste de l'humain (avec des erreurs parfois);
3.  calculer qui a gagné ce round, retourner à 1.
