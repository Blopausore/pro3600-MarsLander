# Mars Lander

## Utilisation

Le fichier launcher lance la simulation.
Dedans vous pouvez modifier les maps employés. 

```bash
python3 src/launcher.py
```


Des commandes permettent ensuite de :
* flèche droite : Faire évoluer une population
* touche q : quitte la simulation

Si une trajectoire qui fonctionne a été trouvé, elle s'affichera toute seule et en vert.

## Environement 
### Surface
La surface est initialiser à l'aide d'une liste de point.
Elle transformera cette liste en une liste de segment.

#### Méthodes
* is_landing_area(segment: Segment) 
    * vérifie si la zone donné en argument est une zone d'atterissage.
* they_collide(trajectory: Segment) 
  * trajectory représente la trajectoire tracer entre deux frames
  * vérifie si la trajectoire à traverser la surface
* get_points 
  * retourne l'ensemble des points qui compose la surface de droites à gauche

#### Entity
Objet représentant une entité, il est caractériser par :
* position : x, y
* vitesse : h_speed, v_speed

#### Méthodes
* update(attributs)
  * met à jour avec les valeurs d'attributs 
* get_state -> [x, y, h_speed, v_speed]
* copy(other)
  * Copie les attributs de other dans self
  
### Lander
Objet représentant le lander, il est caractériser par :
* position : x, y
* vitesse : h_speed, v_speed
* fuel 
* rotate
* power

### Environment
La classe environment permet de générer la surface et le lander à l'aide de points et de conditions initiales.

#### Méthodes
* reset 
  * Remet au paramètre initiaux le lander
* exit_zone -> bool
  * Indique si le lander est bien dans le cadre de la carte
* next_dynamics_parameters(rotate, power) -> x, y, h_speed, v_speed
  * Retourne le prochain état selon l'action 
* step(action) -> bool
  * Joue une étape de l'environment 
  * Retourne vrai si la partie est finie


* landing_on_site -> bool 
  * Indique si la zone de collision est zone d'atterissage
* landing_angle -> bool
  * Indique si le lander atterit  bien droit
* landing_vertical_speed -> bool
  * Indique si la vitesse vertical d'atterrissage n'est pas trop élevé
* landing_horizontal_speed -> bool
  * Indique si la vitesse horizontal d'atterrissage n'est pas trop élevé
* Successful_landing -> bool
  * Indique si l'atterrisage est un succès

## Fonction de score
Pour employer des méthodes analytiques tel que l'algorithme génétique, il faudra déterminer une fonction de score. Cette fonction permettra de donner une note pour une trajectoire donnée et ses paramètres.

### Critères
Il existe plusieurs critères plus ou moins important allant de la distance entre la zone de crash et la zone d'atterissage, à la vitesse à l'atterissage ,...

#### Distance
Le plus important des critères est la distance qui sépare le point d'atterissage à la zone d'atterissage prescrite par l'énoncé.
Mais comment définire un bonne distance dans notre cas. Selon l'[article](https://www.codingame.com/blog/genetic-algorithm-mars-lander/) proposé comme source d'inspiration pour ce projet, la meilleur distance semble être la distance à la marche donc pas la distance absolue mais plutot la distance nécessaire pour aller de la zone de crash à la zone d'atterissage en suivant la surface de l'environnement.

#### Vitesse

Il existe des contraintes de vitesses à l'atterissage qu'il faut respecter et donc des nouveaux paramètres pour une fonction de score, cependant il est important de préciser que ce sont les vitesses à l'atterissage, ce paramètre pourra donc être par exemple pris en compte si et seulement si le vaisseau a atterit au bonne endroit.

#### Angle

Pareil que la vitesse

#### Autres

Lorsque j'écris ceci, je me demande si il ne serait pas interressant de créer un score en fonction de l'amélioration d'une trajectoire qui a pour source deux autres trajectoires. Cela me fait penser notamenent au régulateur PID, ce sera peut être le sujet d'une amélioration.


## Solution

La classe solution permet la création de solution informatique. Cette solution peut employer l'environement pour pouvoir s'entrainer.

### Créer sa solution

Afin d'ajouter sa solution il faut créer un dossier solution contenant au moins une classe qui hérite de AbstractSolution et d'un fichier config contenant les paramètres par défaut de la solution qui seront changeable dans l'interface graphique.


### Methodes

* get_parameters : Renvoi les paramètres de la solution que l'on souhaite afficher.
* use(environment) : Renvoi l'action a appliquer pour cette étape

### Interface graphique : TODO

Grace à get_parameters on a une idée des paramètres de la solution mais les changer à la main requiert du temps.
C'est pourquoi je vais stocker dans un fichier config pour chaque solution ces hyperparamètres qui pourraient alors être changé durant une simulation.

#### Config
Le fichier config contient la valeur par défaut des paramètres et peut être modifier dans le GUI.


## Interface graphique (GUI)

L'interface graphique permet d'observer les différentes solutions proposées.

## Fonctionnement

Son fonctionnement est étroitement lié à la solution créer car différents type d'observation peuvent être proposés. 
* Dynamique : avec un frame, affiche la trajectoire se dessiner au file du temps (sera fait plus tard)
* Statique unique : écrit la trajectoire proposé par la solution
* Statique multiple : écrit plusieurs trajectoire en même temps 
  
Statique multiple voit son utilité dans l'étude de solution heuristique dans lesquelles il y a une évolution de la stratégie au fur et à mesure des simulations.

## Architecture
  
On veut retrouver dans cette interface graphique différentes fonctionnalités :
* Affichage du jeu (évidemment)
* Accès à des commandes (Exemple : pilotage du vaisseau, évolution de la population, ou simplement l'accès au settings)
* Modification de paramètres dans les settings (Exemple : sensibilité pour la commande manuel ou bien la taille de la population dans le cas de GA)
  
### Paramètres attendus en fonctions des modes

### Statique
La solution produit une liste de trajectoire à chaque tour, ainsi on laisse à la solution le choix d'afficher le nombre de trajectoire. De plus par défaut pour passer au tracer de la/les prochaines trajectoires, par défaut, ce sera manuel mais on peut imaginer ajouter un fréquence d'affichage.




