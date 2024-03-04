# Echantillonage_Liste_Clients_La_Poste_DT

## Description

Le script permet de séparer une liste de client en 4 population.

## Installation

### Prérequis

Python 3.7.4  
Les modules et librairies nécéssaire au bon fonctionnement du script sont renseignés dans le fichier requirements.txt  

### Installation du script

(Optionnel) Créez un fichier d'environnement virtuel et activez-le:
```bash
python -m venv venv  
source venv/bin/activate  
cd venv
```  

Clonez le dépôt GitHub:  
```bash
git clone https://github.com/DemoDevv/Echantillonage_Liste_Clients_La_Poste_DT.git
```
Accédez au dossier du script:  
```bash
cd Echantillonage_Liste_Clients_La_Poste_DT
```
Installez les modules requis:  
```bash
pip install -r requirements.txt
```

## Utilisation

### Lancement du script

python [__main__.py ou Echantillonage_Liste_Clients_La_Poste_DT] [options]  
### Options

-h ou --help: Affiche l'aide du script.  
--path: Donner le chemin d'accès au fichier Excel qui contient tout les clients à échantillonnés  
--fusion: (optionnel) Permet de donner la limite de taille pour la fusion des petits groupes  
--output: (optionnel) Donner le chemin du fichier de sortie  
### Exemples d'utilisation

```bash
python Echantillonage_Liste_Clients_La_Poste_DT fichier_entrée.xlsx --fusion 8 --output C:/Documents
```
```bash
python Echantillonage_Liste_Clients_La_Poste_DT -h
```

## Auteurs

@DemoDevv  

## Contact

Pour toute question ou problème, veuillez contacter Mathieu LE BRAS à l'adresse mathieulebras@icloud.com.
