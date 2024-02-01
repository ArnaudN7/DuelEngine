# DuelEngine

## Documentation
Pour toute information relative au développement du projet, à l'organisation du dépôt ou à son contenu, veuillez-vous référer au fichier ==Documentation.md== présent dans ce même répertoire.
Dans ce fichier ne sera détaillé que la mise en place et l'exécution du programme

## Installation recommandée
- Windows
- Python

## Installation nécessaire
Les packages python suivant sont nécessaires pour l'exécution de l'outil DuelEngine : ingescape, pynput, pygetwindow
Vous pouvez les installer avec les commandes suivantes :
- ingescape : pip install ingescape
- pynput : pip install pynput
- pygetwindow : pip install PyGetWindow

## Exécution (Windows)
Des fichiers pour une exécution sous Windows sont déjà présents dans le répertoire ==Launcher==.
En effet, 5 scripts PowerShell sont présents et suivant la nommenclature *launch_agentname.ps1* :
- L'agent DuelEngine : le programme principal
- L'agent Whiteboard : l'agent fourni pour ce projet
- L'agent MouseSensor : l'agent chargé de transmettre les actions de la souris
- L'agent ClickIt : un premier jeu exemple
- L'agent Morpion : un deuxième jeu exemple
Les agents peuvent être exécutés dans n'importe quel ordre, en revanche :
- Le programme a besoin de capter la souris, MouseSensor est indispensable
- Toute communication passe par DuelEngine, la présence de ce dernier est essentielle pour que les jeux puissent fonctionner
- Il est fortement conseillé de mettre le Whiteboard en plein écran et de lancer DuelEngine après. En effet, DuelEngine affiche des images en utilisant le service d'affichage d'image via url de l'agent Whiteboard, malheureusement, Whiteboard ne permet pas de les redimensionner. Par conséquent, l'affichage peut se superposer sur un dimensionnement de la fenêtre du Whiteboard trop petite. 
