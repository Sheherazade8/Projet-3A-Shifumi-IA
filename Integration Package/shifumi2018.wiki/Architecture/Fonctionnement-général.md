Dans ce projet nous avons utilise le framework Django qui utilise le model MVT (Model View Template) cela nous a faciliter les tâche grandement .



# Diagramme de cas d'utilisation

![diagram_usecase](https://image.ibb.co/ftPJ3o/usecase.png)
****
Pour pouvoir joue une partie et voir le score de ta dernier partie vous devez saisir le pseudo et choisir un agent artificiel sont cela vous pouvez pas jouer.

Par contre vous pouvez allez directement sur la page destine a affichez tout les statique de tout les parties.  


# Diagrame de navigation

![diagram_navigation](https://image.ibb.co/mjPU9T/diagrame_navigation.png)

Après avoir démarrer le serveur vous serez rediriger vers la page d'accueil .
Avez donc le choix d'allez directement a la page Tableau de bord ou lance une nouvelle partie .




# Architecture 

![architecture](https://image.ibb.co/fiNSw8/diagrame_package_Demo.png)

Dans le repertoire shifumy_demo/shifumy_demo vous allez retrouver l'arborescence ci-dessus.


- Backoffice est une application django , celle-ci contient interface avec le souris cliquable  
    - migration c'est le dossier qui stocke tout les migrations de la base de données
    - template contient tout les page html vous pouvez par exemple retrouve dans dossier Pages le fichier index.html ce dernier contient le code html de la page d'accueil

-shifumiIA est dossier d'entre du projet ShifumiProjet il contient les fichiers suivants:
     - Le fichier * manage.py*  est le point d'entrée de commande de management du projet. Il permet de créer des applications  
        et d'autres actions
     - Le fichier *urls.py* est ue sorte de table de routage. Pour chaque URL définie on peut l'envoyer vers une fonction 
        choisie.
     - Enfin le fichier *settings.py* qui est comme son nom l'indique un fichier de configuration.
       C'est ici que vous pourrez indiquer quelle base de données utiliser ou quelles applications ajouter au projet, où se 
        situent les fichier statiques, etc.

- Static contient tout les fichier statique du projet
      - Le dossier css contient tout les fichier css , les fichier css de boostrap et le fichier style.css qui est contient 
         tout nos code de style personnaliser donc c'est dans ce fichier qu'il faut modifier si vous voulez personnalisez le 
          template de l'application  
       - Le dossier js contient tout les fichier javascript
       - Images regroupe tout les images utiliser par exemple vous retrouverez dedans l'image des main de l'agent artificiel et humain.



# Base de données


![db](https://image.ibb.co/c5M4b8/uml4.png)


- Nous avons qu'une seul table dans la base de données qui regroupe tout les champs.
Pour visualiser la base de données sql vous pouvez utilise *DB_Browser_sqlite* et voir la table backoffice.humansRobot qui contient tous les données des partie.

Les champs des cette table sont les suivants :

- game_id : contient tout identifiant des parties qui commence de 1 et s'incrémente de 1
- round_id : ce champ est initialiser a 1 pour chaque nouvelle partie et s'increment de 1 jusqu'à la fin de la partie
- opponent : mouvement choisir par l'utilisateur
- agent : mouvement choisir par agent artificiel
- Model_Used : agent utiliser 
- System : actuellement nous avons développe un sytème avec boutton représentent le choix de l'utilisateur mais si par exemple en 
veut utilise la reconnaissance des geste de la main   alors là nous aurons un autre Système
- Pseudo_Player : c'est le pseudo de l'utilisateur choisir
- Gain : nous avons ajouter ce champ pour souci de performance il contient le nombre victoire de cette partie 
  

# Enregistrement des fichiers csv

Lorsque vous avez joué un nombre suffisant de partie, vous pouvez depuis la page des scores (accessible depuis la page d'accueil du jeu) cliquer sur le bouton tout en bas à droite ![logo][https://image.freepik.com/icones-gratuites/extension-de-fichier-excel_318-40499.jpg].

Cela créera un fichier .csv dans le dossier `shifumi2018/resources/FromDb/`. Le nom des fichier .csv a pour format
`année_mois_jour_heure_minute_randomstring.csv`.

Les données sont formatées de la façon suivante:
Nom de l'agent, numéro de la partie, numéro du round, coup du joueur, coup de l'agent, pseudo du joueur.

Pour lire les données, vous pouvez utiliser le script `shifumi2018/resources/DB/db_csv_to_list.py` qui lit l'intégralité des fichiers .csv dans le dossier `DB` et les convertit en une liste de game, chaque game étant une liste de round (round est une classe présente dans `shifumi2018/shifumy_player/shifumy_player/base.py`).




