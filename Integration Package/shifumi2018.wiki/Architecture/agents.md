# Classe Round

Cette classe contient deux attributs:
- `agent` correspondant au geste de l'agent à ce round
- `opponent` correspondant au geste du joueur à ce round

Nous avons défini des variables globales *ROCK, PAPER, SCISSORS* dans `shifumi2018/shifumy_player/shifumy_player/base.py` permettant d'avoir des valeurs communes pour chaque geste (actuellement 0, 1, 2 respectivement)



# API RpsAgent

L'API (interface de programmation applicative) est la classe *RpsAgent*, tous les agents devront hériter de ses méthodes qui sont les suivantes:

- `reset_game` vide l'attribut `game` de l'agent correspondant à l'historique de la partie en cours.
- `record` ajoute le round donné en argument à l'historique `game`.
- `predict` renvoie le geste que va jouer l'agent au prochaine round.
- `load` est une méthode statique qui renvoie une instance chargée (opérationnelle) de l'agent.

# Créer son propre agent

Prenons l'exemple d'un agent artificiel qui fait une prédiction de façon aléatoire.

Pour commencer vous allez créer un fichier python contenant la classe *Nom_Classe(RpsAgent)*: pour notre exemple nous allons utiliser:
*RandomPlayer(RpsAgent)*
RandomPlayer hérite des méthodes de RpsAgent cependant il est nécessaire de modifier au moins les méthodes `load` et `predict` pour que l'agent soit fonctionnel.

Voici le code correspondant à RandomPlayer:
```
class RandomPlayer(RpsAgent):
    def __init__(self):
        RpsAgent.__init__(self)

    def predict(self):
        gestures = [ROCK, PAPER, SCISSORS]
        return gestures[randint(0, 2)]

    def load(filename=None):
        assert filename is None
        return RandomPlayer()
```

# Ajouter un nouvel Agent dans l'application

Pour pouvoir intégrer un nouvel agent, celui-ci doit être une classe python héritant de la classe RpsAgent (voir plus haut).

Une fois le code de l'agent ajouter dans `shifumy_player/shifumy_player/players` et les éventuels fichiers
nécessaires à sa fonction load ajouter dans `resources/data/models/`, il faut modifier le fichier
`shifumy_demo/shifumy_demo/GlobalDefinition.py` en ajoutant la ligne de code permettant d'importer la classe de l'agent
et en ajoutant dans le dictionnaire `dict_all_agent` le nom de l'agent en clef et sa classe en valeur.

Voici la ligne de code qu'il faut ajouter pour RandomPlayer dans `GlobalDefinition.py`:

```
from shifumy_player.players.random_player import RandomPlayer
```
Et voici à quoi ressemble la variable `dict_all_agent` s'il n'y a que l'agent qui hérite de RandomPlayer:

```
dict_all_agent = {"Agent Aléatoire" : RandomPlayer }
```