# Documentation

## Sommaire
1. [Sujet du projet](#sujet-du-projet)
2. [Architecture du dépôt](#architecture-du-dépôt)
3. [Choix](#choix)
4. [Architecture Ingescape circle](#architecture-ingescape-circle)
5. [Fonctionnalités](#fonctionnalités)
6. [Ingescape](#ingescape)
7. [Tests](#tests)
8. [Limites](#limites)
9. [Évolution](#évolution)
10. [Bilan](#bilan)  

## Projet
### Composition du groupe
Arnaud F.  

### Sujet
DuelEngine est un projet réalisé dans le cadre du module IHM et se développant avec le logiciel Ingescape Circle. Cliquez ici pour plus d'informations sur [Ingescape Circle](https://ingescape.com/fr/circle/) et son environnement. Dans ce document ne seront pas expliqués le vocabulaire ou les éléments d'Ingescape Circle mais ils seront mentionnés à de multiples reprises.  
DuelEngine est un agent qui simplifie la création de jeux en duel (deux joueurs sur un ordinateur). Il gère les éléments suivants : score du duel, tour de jeu, historique de jeu, sélection de jeu, jouer un coup, création simplifiée d’éléments graphiques (amovibles ou non). Évidemment DuelEngine ne peut fonctionner seul, il a besoin de 2 agents au minimum : Whiteboard et MouseSensor.  
Whiteboard est l'agent fourni pour ce projet et dont il convient d'utliser un maximum de fonctionnalités.  
MouseSensor est un agent qu'il a fallu créer, son utilité est, comme son nom l'indique, donner les informations relatives à la souris de l'utilisateur à savoir : sa position en x, en y et l'action clic gauche.  
Pour le bien du projet, deux agents représentant des jeux ont été créés afin d'utiliser DuelEngine : ClickIt et Morpion.  
ClickIt est un jeu très simple où il faut cliquer dans la cible.  
Morpion est le jeu classique du morpion sans aucune règle additionnelle.  

## Architecture du dépôt
### Dépôts
Dans ce dépôt de projet, vous pourrez retrouver les dossiers et fichiers suivants :
- **DuelEngine** : Dossier contenant les fichiers des agents principaux (DuelEngine et MouseSensor) mais aussi le fichier igsplatform du projet.
- **Games** : Dossier contenant les fichiers des agents étant des jeux.
- **Launcher** : Dossier contenant les scripts permettant de lancer les agents du projet.
- **VandV** : Dossier contenant les scripts relatifs aux tests du programme DuelEngine
- **Whiteboard** : Dossier contenant les fichiers de l'agent Whiteboard fourni pour ce projet
- *Documentation.md*: Ce document
- *README.md* : Document détaillant la procédure d'installation et d'exécution du programme DuelEngine
### DuelEngine
Dans ce dossier, vous pourrez retrouver les fichiers suivants :
- *DuelEngine.igsplatform* : Fichier igsplatform contenant la structure du projet pour Ingescape Circle
- *DuelEngine.py* : Script python contenant le code de l'agent DuelEngine
- *MouseSensor.py* : Script python contenant le code de l'agent MouseSensor
### Games
Dans ce dossier, vous pourrez retrouver les dossiers et fichiers suivants :
- **Images** : Dossier contenant les images nécessaires pour les jeux
- *ClickIt.py* : Script python contenant le code de l'agent ClickIt
- *GAME_TEMPLATE.py* : Template d'un script python contenant le code minimal pour créer l'agent d'un jeu utilisant DuelEngine. Les parties à modifier sont indiquées pour faciliter le développement.
- *Morpion.py* : Script python contenant le code de l'agent Morpion
#### Images
Dans ce dossier, vous pourrez retrouver les fichiers suivants :
- *ClickIt_board.png* : L'image du plateau du jeu ClickIt (600x600)
- *ClickIt_game_image.png* : L'image représentant le jeu ClickIt (300x300)
- *Morpion_board.png* : L'image du plateau du jeu Morpion (600x600)
- *Morpion_game_image.png* : L'image représentant le jeu Morpion (300x300)
### Launcher
Dans ce dossier, vous pourrez retrouver les fichiers suivants :
- *launch_clickit.ps1* : Script PowerShell permettant l'exécution de l'agent ClickIt
- *launch_duelengine.ps1* : Script PowerShell permettant l'exécution de l'agent DuelEngine
- *launch_morpion.ps1* : Script PowerShell permettant l'exécution de l'agent Morpion
- *launch_mousesensor.ps1* : Script PowerShell permettant l'exécution de l'agent MouseSensor
- *launch_whiteboard.ps1* : Script PowerShell permettant l'exécution de l'agent Whiteboard
### VandV
Dans ce dossier, vous pourrez retrouver les fichiers suivants :
- *verif_script.txt* : Fichier contenant les tests à effectuer pour vérifier le programme DuelEngine
### Whiteboard
Dans ce dossier, vous pourrez retrouver de nombreux fichiers dont *Whiteboard.exe* utilisé pour lancer l'agent Whiteboard.

## Choix
Plusieurs choix techniques ont été fait pour le développement de ce projet, les détails de ces choix seront développés dans les parties adaptées, néanmoins, en voici la liste :
- Le développement du projet a été entièrement fait en python avec, principalement, la librairie ingescape pour des raisons de simplicités de développement et de préférences personnelles.
- L'agent Whiteboard étant non modifiable et pas totalement adapté au besoin de ce projet, il a été décidé que DuelEngine interagirait avec un unique Whiteboard à la fois, considérant donc qu'un seul Whiteboard ne peut se connecter et qu'une déconnexion de l'agent Whiteboard signifie qu'aucun autre Whiteboard n'est présent.
- Le développement a été priorisé par rapport à l'esthétique. En effet, l'aspect esthétique est très simpliste, que ce soit dans les jeux ou en général. En revanche, il est facilement améliorable et ce sera un aspect abordé dans une autre partie de cette documentation.

## Architecture Ingescape Circle
![Image architecture Ingescape Circle](/Images/Ingescape_Circle_architecture.png)

## Fonctionnalités
Cette partie traite d'éléments conceptuel pouvant être retrouvé à plusieurs endroits dans le code. Il ne convient pas de décrire le code mais bien de présenter les concepts. Le code est commenté, partitionné mais il reste dense et complexe aux premiers abords, là est le principal objectif de cette partie, présenter les fonctionnalités apportées par DuelEngine pour simplifier la compréhension du code.
### Notions principales
#### Whiteboard et board
Utilisant les informations de la souris, il a été important dans ce projet de vérifier si un clic a lieu sur le Whiteboard et le cas échéant où a-t-il été fait. Pour ce faire, nous identifions deux informations principales : est-ce que le clic est dans le Whiteboard, est-ce que le clic est dans le plateau.  
Pour savoir si un clic a eu lieu dans le Whiteboard, la librairie pygetwindow nous permet de récupérer les informations de position et de taille du Whiteboard. Le Whiteboard possède un tchat sur le côté droit et une zone de titre sur le côté haut, ces deux zones ne sont pas considérées comme étant dans le Whiteboard puisqu'elles ne peuvent présenter aucune interaction. Ainsi, nous pouvons savoir si un clic a eu lieu dans le Whiteboard ou non, si tel est le cas, nous transformons alors les coordonées de la souris sur l'écran en coordonnées du Whiteboard pour une utilisation ultérieure simplifiée.  
Abordons maintenant la notion de plateau ou de "board", en effet, cette notion est centrale dans DuelEngine. Le plateau va représenter une zone imaginaire qui va simplifier les interactions entre DuelEngine et les jeux. Le plateau est donc divisé en cases identifiées par leur numéro de colonne et de ligne, chaque jeu doit fournir les dimensions de son plateau à DuelEngine. Chaque plateau est centré par rapport au centre du Whiteboard (de sa partie interactive). Ces informations sont composées de : nombre de colonnes, nombre de lignes, largeur d'une case, hauteur d'une case. Grâce à cette zone, DuelEngine pour indiquer un coup joué va indiquer la case cliquée du plateau (colonne 0 et ligne 0 correspond a un clic dans le Whiteboard mais en dehors du plateau de jeu).
#### Informations courantes
Il y a 3 types d'informations courantes qui sont mis à jour régulièrement :
- Les informations du Whiteboard : Les coordonnées et la taille du Whiteboard
- L'état courant de DuelEngine : Le titre à afficher, la couleur du fond (ou du joueur courant) et le jeu courant
- Les informations du plateau : Les coordonnées du point en haut à gauche et celui en bas à droite du plateau
### Internes
#### Éléments immobiles
L'agent Whiteboard permet plusieurs interactions de base :
- Déplacer les éléments  présents en maintenant le clic gauche enfoncé
- Supprimer les éléments présents
- Nettoyer le Whiteboard
  
Ces actions ne sont pas référencées, par conséquent, il est impossible de savoir si elles ont eu lieu uniquement via l'agent Whiteboard. Dans en premier temps, pour des jeux, il a été déterminé intéressant de rendre les éléments "non amovibles". Effectivement, chaque éléments pouvant être le plateau de jeux, les jetons ou encore les boutons interactifs. Ces éléments n'ont pas vocation à être bougé et doivent donc être non amovibles, pour cela, chaque élément créé va être enregistré par DuelEngine et un thread est chargé de repositionner chaque élément à sa place initiale. Pour enregistrer une création, nous avons besoin de l'identifiant de l'élément créé, ainsi, à chaque création d'un élément le Whiteboard va appeler un service de DuelEngine indiquant la création. DuelEngine reçoit à ce moment là un identifiant, or, ce dernier a besoin d'associer un identifiant à une position, dans un fonctionnement asynchrone, on ne peut pas garantir que le dernier élément créé correspond à cet identifiant si l'on en créé plusieurs d'affilés. DuelEngine va donc appeler un service du Whiteboard renvoyant chaque élément contenu et DuelEngine va enregistrer ce dont il ne connaît pas l'existesnce.  
Pour les actions de suppression, il était plus difficile de "contrer" les effets de ces dernières. Malheureusement, le replacement s'effectuant via un thread, il n'est pas possible de récupérer un appel retour de service indiquant la non possibilité d'effectuer le déplacement (car l'élément a été supprimé) dans l'agent DuelEngine. Cela aurait été l'indication idéale pour rajouter l'élément dont nous avons retenu toutes les informations. Néanmoins, le nettoyage du Whiteboard effaçant aussi le titre et le tchat, il a été décidé de laisser les actions de suppression effectuer leur effet de base et il relève de la responsabilité de l'utilisateur de ne pas les effectuer si il souhaite une utilisation normale de DuelEngine.
#### Sélection de jeux
DuelEngine permet la sélection de jeux, en effet, des jeux enregistrés par DuelEngine sont prêt à être joué et sont affichés sur l'écran de sélection des jeux. La sélection d'un jeu est considérée comme un "jeu spécial". En effet, le fonctionnement développé d'interaction avec un plateau est suffisamment perfomant et flexible pour pouvoir être appliqué au fonctionnement interne de DuelEngine. Ainsi, la sélection de jeu est considéré comme un "jeu spécial", on ne choisit pas d'y jouer, il n'est pas sélectionnable et ne présente pas non plus de tour de jeu ou de score mais il présente un plateau. Une case du plateau est un jeu sélectionnable, car, l'action sélectionner un jeu va afficher autant de jeux disponibles que possible. Tout jeu affiché est cliquable et redirige sur le jeu en question.
#### Couleur des joueurs
Tout comme la sélection de jeu, le menu des couleurs des joueurs est un "jeu spécial" dans lequel le plateau est rempli de titres "Couleur du joueur X" et d'un pannel de cases colorées en dessous. Cliquer sur une couleur sélectionne cette couleur pour le joueur X.
#### Changement de tour
Lorsqu'un jeu indique le changement de tour, DuelEngine affiche un message dans le tchat indiquant le changement de joueur et change la couleur de fond pour correspondre à celle du joueur courant.
#### Jouer un coup
DuelEngine envoie les informations nécessaires à un jeu pour calculer les conséquences du coup joué, ces informations sont composées de 3 éléments : la colonne et la ligne de la case cliquée (ou 0 et 0 si hors du plateau) ainsi qu'une impulsion pour indiquer quand le coup est joué.
#### Victoire d'un joueur / Égalité
Un jeu peut indiquer la victoire d'un joueur ou d'une égalité, DuelEngine va alors afficher un message et un titre équivalent à la situation rencontrée et mettre à jour ou non le score de la partie. Il passe également sur l'écran de fin de partie.
#### Fin de partie / Rejouer un jeu
À la fin d'une partie, les joueurs peuvent rejouer au jeu ou bien sélectionner un autre jeu. Si les joueurs décident de continuer le jeu, alors le score de la partie est conservé tant que les joueurs resteront sur le même jeu.
#### Score de la partie
DuelEngine retient le score de la partie, une partie étant considérée comme infinie tant que le jeu joué est toujours le même, sinon, il est remis à 0.
### Services
#### Register / Unregister
Un jeu peut s'enregistrer comme jeu jouable auprès de l'agent DuelEngine. Ce service permet d'avoir des jeux non connus à l'avance puisque l'appel au service demande de fournir les informations suivantes : 
- Le nom du jeu
- Les règles du jeu
- L'image du jeu
- L'image du plateau
- La longueur d'une case
- La hauteur d'une case
- Le nombre de colonnes du plateau
- Le nombre de lignes du plateau
Un jeu peut également se désinscrire de la liste des jeux jouables avec un autre service.
#### Ajout d'une forme
Un jeu peut ajouter une forme à n'importe quel endroit dans le Whiteboard.
#### Ajout d'une forme / texte / image dans le plateau
Le but est de faciliter aux jeux les actions résultant d'un coup joué, car, souvent dans les jeux, une action résulte en un affichage graphique d'un élément comme un pion. DuelEngine offre ici la possibilité d'ajouter simplement un élément en indiquant dans quel case du plateau l'ajouter. Il est également possible de fournir, au lieu d'une couleur, les chaînes de caractères "PLAYER1COLOR" ou "PLAYER2COLOR" pour que l'élément ajouté prennent la couleur du joueur mentionné.

## Ingescape
### Agents
Plusieurs agents ont été créé dans ce projet dans le but de proposer une interaction globale intéressante.
### Inputs, Outputs, Callbacks & Services
Assez classiquement, toutes les fonctionnalités basiques tels que les inputs, outputs, input_callback et services ont pu être mis en place à plusieurs endroits dans le projet.
### Services callback
Un peu plus original, dans DuelEngine, j'ai pu exploiter la fonctionnalité de callback de service à savoir l'appel d'un service émettant le résultat d'un précédent appel entre DuelEngine et Whiteboard.
### Évenements d'agents
Les événements d'agents ont été utiles pour deux aspects :
- L'arrivée du Whiteboard : avec AGENT_KNOWS_US, permet d'envoyer les informations sur l'état courant au Whiteboard. Cela permet donc de lancer les agents sans ordre précis, mais aussi, de renvoyer les informations si le Whiteboard a été fermé puis réouvert.
- La déconnexion d'un agent jeu : avec AGENT_EXITED, permet de supprimer un jeu qui a été fermé brutalement, sans effectuer de désinscription. Cela permet donc de quitter le jeu avec un message d'erreur ou bien d'actualiser la sélection pour ne pas proposer un jeu qui n'est plus accessible. 
### Altération du mapping
#### Ajout
Comme mentionné plus haut, les jeux ajoutés ne sont pas forcément connus de DuelEngine. Pour renforcer cet aspect et le rendre plus robuste, l'enregistrement d'un jeu, que ce soit du côté de DuelEngine ou bien du jeu, comprend également un ajout des liens entre input et output nécessaires. Effectivement, les jeux doivent présenter des inputs et outputs définis (par exemple dans le fichier *GAME_TEMPLATE.py*), il est par conséquent assez facile de généraliser l'ajout des liens dans le mapping.
#### Suppression
Selon la même logique que l'ajout de liens nécessaires pour le fonctionnement des jeux, il a été tenté d'enlever ce mapping au moment de la désinscription du jeu. Malheureusement, j'ai essayé toutes les fonctions suivantes mais aucune n'a fonctionné :
- igs.clear_mappings
- igs.clear_mappings_with_agent
- igs.clear_mappings_for_input 
- igs.mapping_remove_with_id
- igs.mapping_remove_with_name

## Tests
### TBD

## Limites
### Design graphique
La partie graphique est en tout point assez simpliste, l'un des principales raisons est la non possibilité de redimensionner des images ajoutées via url. Par conséquent, certains affichages nécessitent une grande taille du Whiteboard pour ne pas être superposés. Également, certains éléments d'interactions sont des formes ou des textes plutôt que des images pour cette raison.
### Reprise d'une partie en cours
Malgré la sauvegarde de l'état courant et l'envoi automatique à la connexion d'un Whiteboard, il n'est pas possible de restaurer une partie interrompue par la fermeture du Whiteboard. En effet, l'ajout de certains éléments graphiques sur le plateau étant le résultat d'actions effectués par les joueurs, le fait que l'on ne retienne pas les actions ou ne re-créons pas les éléments non-amovibles ne nous permet pas de restaurer une partie en cours.
### L'agent Whiteboard
L'agent Whiteboard ne pouvant être modifié, nous ne pouvons pas instaurer un appel de ce dernier vers DuelEngine pour indiquer sa présence. Cela aurait pu permettre de cibler l'agent via son identifiant et pas via son nom et de lui envoyer toutes les informations courantes et même créer les formes du plateau courant (et par la même occasion se servir de ce mécanisme pour reprendre une partie en cours). C'est pour cette raison que l'on ne considère qu'un unique Whiteboard. On pourrait également imaginer une amélioration avec un redimensionnement des images ajoutés via url.

## Évolution
### Plusieurs Whiteboard
Nous pourrions facilement imaginer plusieurs Whiteboard pouvant afficher la même chose. Comme décrit ci-dessus il serait possible de sauvegarder les éléments affichés et les créer sur les Whiteboard arrivant en cours de jeu. Cela requiert toujours une évolution du Whiteboard qui consisterait à informer DuelEngine de son arrivée. Évidemment, un seul de tout ces Whiteboard serait déterminé comme principal et serait la référence des interactions avec l'utilisateur.
### Amélioration du design
Plusieurs éléments d'interactions comme les boutons ou encore les textes pourraient être transformés en image. Cela permettrait de designer plus profondement ces éléments d'interaction pour les rendre plus attrayant et visuellement agréable.
### Recalibrage
Un bouton permettant de recalibrer l'affichage par rapport au Whiteboard pourrait être créé. En effet, si l'on redimensionne le Whiteboard l'affichage étant basé sur des coordonnées fixes, rien ne bouge. Un bouton permanent sur tous les écrans pourraient permettre de ré-afficher l'entièreté des éléments selon les nouvelles dimensions du Whiteboard. Cette partie nécessite également de mémoriser tous les éléments graphiques présents à ce moment-là dans le cas d'un appui pendant une partie d'un jeu.

## Bilan
Ce projet fut pour moi très intéressant mais surtout amusant. Je vous remercie d'avoir accepté le fait que mon projet puisse se dérouler en solo. J'ai pu pousser l'expérience aussi loin que je le souhaitais avec Ingescape Circle et je suis très satisfait car mes attentes ont été comblées. J'espère avoir reflété dans mon travail et dans mon utilisation d'Ingescape l'intérêt et l'admiration que j'éprouve envers cet outil.