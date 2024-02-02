# DuelEngine

## Documentation
Pour toute information relative au projet, à son développement, à l'organisation du dépôt ou à son contenu, veuillez-vous référer au fichier *Documentation.md* présent dans ce même répertoire.  
Dans ce fichier ne sera détaillé que la mise en place et l'exécution du programme.

## Installation nécessaire non détaillée
- Windows (recommandé (des scripts PowerShell sont mis à disposition pour l'exécution des agents))
- Python
- Ingescape Circle

## Installation nécessaire
Les packages python suivant sont nécessaires pour l'exécution du programme DuelEngine : ingescape, pynput, pygetwindow  
Vous pouvez les installer avec les commandes suivantes :
- ingescape : pip install ingescape
- pynput : pip install pynput
- pygetwindow : pip install PyGetWindow

## Exécution (Windows)
Des fichiers pour une exécution sous Windows sont déjà présents dans le répertoire **Launcher**.  
En effet, 5 scripts PowerShell sont présents et suivant la nommenclature *launch_agentname.ps1* :
- L'agent DuelEngine : le programme principal
- L'agent Whiteboard : l'agent fourni pour ce projet
- L'agent MouseSensor : l'agent chargé de transmettre les actions de la souris
- L'agent ClickIt : un premier jeu exemple
- L'agent Morpion : un deuxième jeu exemple  
  
Voir la suite dans [Exécution du programme](#exécution-du-programme)

## Exécution (Ubuntu, MacOS, ...)
Aucun script n'est présent pour un système d'exploitation autre que Windows. Par conséquent, il relève de votre responsabilité d'exécuter les programmes suivants :
- Pour l'agent DuelEngine (le programme principal) : "./DuelEngine/DuelEngine.py"
- Pour l'agent Whiteboard (l'agent fourni pour ce projet) : "./Whiteboard/Whiteboard.exe" avec les options suivantes "--device "Loopback Pseudo-Interface 1"" et "--port 5670"
- Pour l'agent MouseSensor (l'agent chargé de transmettre les actions de la souris) : "./DuelEngine/MouseSensor.py"
- Pour l'agent ClickIt (un premier jeu exemple) : "./Games/ClickIt.py"
- Pour l'agent Morpion (un deuxième jeu exemple) : "./Games/Morpion.py"
  
Voir la suite dans [Exécution du programme](#exécution-du-programme)

## Exécution du programme
Les agents peuvent être exécutés dans n'importe quel ordre, en revanche :
- Vous devez lancer le logiciel Ingescape Circle avec la configuration donnée dans le fichier igsplatform dans le dossier **DuelEngine**. Veuillez-vous connecter sur le port "5670" de l'interface "Loopback Pseudo-Interface 1".
- Le programme a besoin de capter la souris, MouseSensor est indispensable
- Toute communication passe par DuelEngine, la présence de ce dernier est essentielle pour que les jeux puissent fonctionner
- Il est fortement conseillé de mettre le Whiteboard en plein écran et de lancer DuelEngine après. En effet, DuelEngine affiche des images en utilisant le service d'affichage d'image via url de l'agent Whiteboard, malheureusement, Whiteboard ne permet pas de les redimensionner. Par conséquent, l'affichage peut se superposer si le dimensionnement de la fenêtre du Whiteboard est trop petit. 
