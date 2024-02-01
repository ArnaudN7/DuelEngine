# Documentation

## Sommaire
1. [Sujet du projet](#sujet-du-projet)
2. [Architecture du dépôt](#architecture-du-dépôt)
3. [Choix](#choix)
4. [Architecture Ingescape circle](#architecture-ingescape-circle)
5. [Originale](#originale)
6. [Finale](#finale)
7. [Fonctionnalités](#fonctionnalités)
8. [Ingescape](#ingescape)
9. [Tests](#tests)
10. [Limites](#limites)
11. [Évolution](#évolution)
12. [Bilan](#bilan)  

## Projet
### Composition du groupe
Arnaud F.  

### Sujet
DuelEngine est un agent qui simplifie la création de jeux en duel (deux joueurs sur un ordinateur). Il gère les éléments suivants : score du duel, tour de jeu, historique de jeu, sélection de jeu, jouer un coup, création simplifiée d’éléments graphiques (amovibles ou non). Évidemment DuelEngine ne peut fonctionner seul, il a besoin de 2 agents au minimum : Whiteboard et MouseSensor.  
Whiteboard est l'agent fourni pour ce projet et dont il convient d'utliser un maximum de fonctionnalités.  
MouseSensor est un agent qu'il a fallu créer, son utilité est, comme son nom l'indique, donner les informations relatives à la souris de l'utilisateur à savoir : sa position en x, en y et l'action clic gauche.  
Pour le bien du projet, deux agents représentant des jeux ont été créés afin d'utiliser DuelEngine : ClickIt et Morpion.  
ClickIt est un jeu très simple où il faut cliquer dans la cible.  
Morpion est le jeu classique du morpion sans aucune règle additionnelle.  

## Architecture du dépôt

## Choix

## Architecture Ingescape circle

### Originale

### Finale

## Fonctionnalités

## Ingescape
### Altération du mapping
#### Ajout
OK
#### Suppression
Tout essayé mais aucune n'a marché :
- igs.clear_mappings
- igs.clear_mappings_with_agent
- igs.clear_mappings_for_input 
- igs.mapping_remove_with_id
- igs.mapping_remove_with_name

## Tests

## Limites
### Design graphique
Limité par les images
### Reprise d'une partie en cours
### L'agent Whiteboard
- Un seul Whiteboard
- Affichage des images

## Évolution
### Plusieurs Whiteboard
Un seul interactif, d'autres affichage
### Amélioration du design
### Recalibrage

## Bilan