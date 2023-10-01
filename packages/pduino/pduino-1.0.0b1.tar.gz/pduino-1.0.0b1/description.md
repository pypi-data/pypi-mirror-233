# Duinolabo

`Duinolabo` est un module à destination des enseignants de physique chimie et de biologie qui permet la réalisation sous _python_ de systèmes de mesures utilisant la carte _Arduino_.

Ce module est très efficace et **simplifie considérablement** la réalisation de _mesures temporelles_ ou _point par point_ à l'aide d'une carte _Arduino_.

`Duinolabo ` est constitué de deux bibliothèques :
- `pduino` qui fonctionne sous python
- `juduino` qui permet de créer très simplement des systèmes d'interfaces de mesures graphiques sous jupyter.

Sans remplacer un oscilloscope ou une interface de mesures, le système peut néanmoins effectuer des mesures temporelles de 100 ou 200 points jusqu'à une fréquence de 40kHz, ce qui est largement suffisant dans la plupart des cas du programmes de lycée.

Dans la mesure où toutes les activités sont basées sur le même modèle, (en particulier avec `juduino` sous Jupyter), les élèves, conformément au B.O. Français, se familiarisent rapidement avec l'environnement _python_ pour analyser leurs résultats.

Sont également fournis plusieurs exemples documentés, fonctionnels et testés avec des élèves, applicables au programme Français de sciences physiques dans les classes de lycée.


## Installation

- Si vous travaillez uniquement avec un IDE _phyton_ (edupython, thonny, spyder, ect...), dans la console de votre environnement python, tapez:
```
    pip install pduino
```
- Si vous travaillez avec Jupyter, dans la console de votre environnement Jupyter, tapez
```
    pip install pduino
```
puis 
```
    pip install juduino
```    

## Github

Documentation, exemples et sources sur github : https://github.com/bultec/duinolab