from math import floor
from random import shuffle
from pandas import read_excel, NA
import argparse
import time


QUADRIMESTRES = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]


def sanitize(clients_total):
    # enlever les colonnes inutiles qui vont compliqué le collage des données sur la liste sharepoint
    if "Type d'élément" in clients_total.columns:
        clients_total = clients_total.drop(columns=["Type d'élément"])
    if "Chemin d'accès" in clients_total.columns:
        clients_total = clients_total.drop(columns=["Chemin d'accès"])
    return clients_total


def create_output_file(clients_total, method: str, args):
    clients_total_sanitized = sanitize(clients_total)

    file_name = f"Clients_echantillons_{method}_{time.strftime("%Y-%m-%d")}.xlsx"

    if args.output:
        clients_total_sanitized.to_excel(args.output, index=False)
    else:
        clients_total_sanitized.to_excel(file_name, index=False)
    
    print("Fichier excel créé avec succès au chemin: ", args.output if args.output else file_name)


def update(clients_total, args):
    clients_total_size = clients_total.shape[0]

    # récuperer les clients qui n'ont pas d'échantillon
    clients_not_in_echantillon = clients_total[clients_total['Echantillon'].isna() == True]

    for client in clients_not_in_echantillon.index:
        # recuperer le mois de création du client
        mois = clients_total.loc[client, "Créé"].month
        
        # trouver le quadrimestre correspondant
        for quadrimestre in QUADRIMESTRES:
            if mois in quadrimestre:
                # ajouter l'échantillon correspondant
                clients_total.loc[client, "Echantillon"] = QUADRIMESTRES.index(quadrimestre) + 1
                break

    assert clients_total[clients_total['Echantillon'].isna() == True].shape[0] == 0, "Certaines entrées ne\
          sont affectées à aucun échantillons"
    assert clients_total.shape[0] == clients_total_size, "Le résultats des échantillons ne contient pas autant d'entrées\
          que au début du programme"
    
    print(clients_total.groupby("Echantillon").size())

    # créer un nouveau fichier excel en sortie
    create_output_file(clients_total, "update", args)


def initialisation(clients_total, args):
    clients_total_size = clients_total.shape[0]

    clients_total["Echantillon"] = NA

    # regrouper les clients par population differente après la fusion
    clients_by_population = clients_total.groupby(["Direction DTO ou Innov",
                                                   "PERIMETRE  DTO - DirInnov",
                                                   "Profil Client"])

    total_client = 0
        
    # print la table par population
    for _, clients in clients_by_population:

        size_population_total = clients.shape[0]

        size_25 = floor(size_population_total * 0.25)

        # taille de la population restante
        _ = size_population_total - (size_25 * 4)

        # séparer la population en 4 échantillons de 25%
        for i in range(1, 5):
            clients_not_in_echantillon = clients[clients['Echantillon'].isna() == True]

            # prendre les 25% de la population
            head_25 = clients_not_in_echantillon.head(size_25)

            # remplir la colonne echantillon
            clients.loc[head_25.index, "Echantillon"] = i

        # ajouter au reste des clients un échantillon unique
        clients_not_in_echantillon_reste = clients[clients['Echantillon'].isna() == True]

        echantillon = [1, 2, 3, 4]
        shuffle(echantillon)

        # ajouter le reste des clients a un échantillon
        for client in clients_not_in_echantillon_reste.index:
            clients.loc[client, "Echantillon"] = echantillon.pop(0)

        # ajouter le nombre de clients a la population totale
        total_client += clients.shape[0]

        # associer le échantillons a la population total
        clients_total.loc[clients.index, "Echantillon"] = clients["Echantillon"]

    assert clients_total[clients_total['Echantillon'].isna() == True].shape[0] == 0, "Certaines entrées ne\
          sont affectées à aucun échantillons"
    assert total_client == clients_total_size, "Le résultats des échantillons ne contient pas autant d'entrées\
          que au début du programme"

    print(clients_total.groupby("Echantillon").size())

    # créer un nouveau fichier excel en sortie
    create_output_file(clients_total, "initialisation", args)


def main(args):
    # lire le fichier excel
    clients_total = read_excel(args.path)

    # ajout d'une colonne pour ensuite insérer une valeur entre 1 et 4 pour chaque client
    if "Echantillon" not in clients_total.columns:
        clients_total["Echantillon"] = NA

    if args.update:
        update(clients_total, args)
    else:
        initialisation(clients_total, args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Echantillonage des clients")
    parser.add_argument(
        "-p",
        "--path",
        help="Chemin du fichier excel",
        type=str, 
        required=True
    )
    parser.add_argument(
        "-u",
        "--update",
        help="Indique si le fichier excel doit être mis à jour",
        action="store_true",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Chemin du fichier de sortie",
        type=str,
        required=False
    )

    args = parser.parse_args()

    main(args)