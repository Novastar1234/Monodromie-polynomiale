# Monodromie polynomiale

## Presentation
Ce projet s'est fait à l'issu de mon travail de recherches mathématiques durant mon année de MP*, la synthèse théorique ainsi qu'une vidéo présentant bien le phénomène se trouve dans le fichier TIPE. 

main.py lance une application matplotlib permettant de visualiser le relèvement polynomial et l'apparition du phénomène de monodromie. Une démo de son fonctionnement se trouve ci-dessous.

Enfin la fonction Is_MonP_Sn: numpy Polynomial ->bool dans Poly_package.py résout numériquement la question 
avec rélèvement numérique + algorythme de schreier_sims
## Demonstration

[Watch the demonstration](fulldemo.mp4)
## Installation

```bash
git clone https://github.com/Novastar1234/Monodromie-polynomiale

cd Monodromie polynomiale

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Running

```bash
python main.py
```

## Project structure
Ocaml              ocaml files used for schreiers_sims

TIPE               rendu de mon TIPE. 

fulldemo.mp4.      demo of the visualization tool

main.py            matplotlib app.

Poly_package.py    crée les courbes et le texte à afficher

scheier_sims.py    fais le lien avec les fichiers ocaml pour l'implémentation de Schreier_sims



