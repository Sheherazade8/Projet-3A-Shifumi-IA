# Installation

## Créer et activer un environnement virtuel
Pour se projet nous avons utilisé `Pyhton3.5`, l'utilisation d'un environnement virtuel est conseillé.
Par exemple, avec `virtualenv` (si besoin, installer `virtualenv` avec `pip` ou `aptget`), depuis une console:

```
virtualenv --python=python3.5 shifuenv
source shifuenv/bin/activate
```

Pour désactiver l'environnement virtuel: `deactivate`

Avec `Anaconda3` ([site officiel](https://www.anaconda.com/download/#linux)), depuis une console:

```
conda create -n shifuenv python=3.5
source activate shifuenv
```

Pour désactiver l'environnement virtuel: `source deactivate`

# Installation des packages

Le projet est constitué de plusieurs packages python que sont:
- `shifumy_player`: "intelligences" de jeu
- `shifumy_demo_cv`: interface utilisateur et gestionnaire du programme
- `shifumy_reco`: reconnaissance de geste

Le fonctionnement du programme complet nécessite l'installation de tous les packages. Pour installer un de ces packages (noté `shifumy_package` dans l'exemple, à remplacer par les noms adéquats), tapez dans une console:

```
cd shifumi2018/shifumy_package/
pip install -e .
```

La commande `pip install -e .` permet d'installer une version éditable du paquet du répertoire courant, ainsi le package pourra être édité sans avoir à être réinstallé après chaque édition.

En tapant la commande `pip list`, les paquets installés apparaissent avec leur chemin d'accès.

# Téléchargement des données
Les jeux de données, les fichiers relatifs aux différents agents et la base de donnée sont présents [ici](https://drive.google.com/drive/folders/158l9e82MdSisJ9BTd83O2n1_H1X-S_7D?usp=sharing).

Télécharger et fusionner le répertoire `ressources/`.

# Installation du code `Prasad9` (Optionnel)
* Télécharger le projet Prasad9 sur le git:
  https://github.com/Prasad9/Classify-HandGesturePose
  (`Clone or download`, `Download zip`)
* Décompresser le projet dans le répertoire `shifumi2018/third_parties/`
* Télécharger les données [ici](https://lmb.informatik.uni-freiburg.de/projects/hand3d/ColorHandPose3D_data_v3.zip)
  et décompresser dans le dossier racine du projet Prasad9 (shifumi2018/third_parties/Classify-HandGesturePose-master/)
(Cela va créer 3 dossiers: "data", "results" et "weights")
* Installer les dépendances:
`pip install numpy scipy matplotlib tensorflow opencv-python`

# Problèmes d'installation connus
Si vous rencontrer des problèmes lors de l'installation d'`opencv`, notamment si vous avez des problèmes de compatibilités avec certaines librairies (ex: libgtk2.0-dev), nous vous conseillons l'utilisation d'`Anaconda3`. Par ailleurs, essayez plutôt d'installer opencv à l'avance.