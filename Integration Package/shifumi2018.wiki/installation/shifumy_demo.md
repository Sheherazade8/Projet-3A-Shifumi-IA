Le package `shifumy_player` doit être installé. 

Installez `shifumy_demo` à partir de la branche `master`.

Voir [ici](https://gitlab.lis-lab.fr/qarma/shifumi2018/wikis/installation/composants-principaux) pour installer un package `shifumy_*`.

Après installation du package `shifumy_demo`, il est nécessaire de mettre à jour Django.

Depuis une console (manage.py présent dans le répertoire shifumi2018/shifumy_demo/shifumy_demo/Django/):

```
python manage.py makemigrations
python manage.py migrate
```

# Lancement du serveur
Depuis une console (manage.py présent dans le répertoire shifumi2018/shifumy_demo/shifumy_demo/Django/):

```
python manage.py runserver
```
Puis aller à l'adresse: http://127.0.0.1:8000/