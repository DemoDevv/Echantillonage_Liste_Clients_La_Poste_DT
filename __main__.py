from math import ceil
from pandas import read_excel, NA

excel_file = "Echantillonage_Aleatoire_Liste_Clients_La_Poste_DT_25%/Clients.xlsx"
FUSION_LEN = 10


def merge_small_population(clients_total, population):
    # Filtrer les populations qui ont moins de 8 clients
    small_groups = population.groupby("Code DT").filter(lambda x: len(x) < FUSION_LEN)

    # transformer la liste en string avec un tiret entre chaque code DT
    merged_name_code_DT = "-".join(small_groups["Code DT"].unique())
    
    # Fusionner les petits groupes avec le reste du groupe
    clients_total.loc[small_groups.index, "Code DT"] = merged_name_code_DT


def main():
    clients_total = read_excel(excel_file)

    # remplacer les bonnes valeurs NA par _NA pour que pandas les prenne en compte
    clients_total.fillna("_NA", inplace=True)

    # enlever les rows ou "Direction DTO ou Innov" est vide
    clients_total = clients_total[clients_total["Direction DTO ou Innov"] != "_NA"]

    clients_total_size = clients_total.shape[0]

    # ajout d'une colonne pour ensuite insérer une valeur entre 1 et 4 pour chaque client
    clients_total["echantillon"] = NA

    # regrouper les clients par population differente
    clients_by_population = clients_total.groupby(["Direction DTO ou Innov", "PERIMETRE  DTO - DirInnov"])

    # fusionner les populations qui ont moins de 8 clients
    for _, population in clients_by_population:
        merge_small_population(clients_total, population)

    # regrouper les clients par population differente après la fusion
    clients_by_population = clients_total.groupby(["Direction DTO ou Innov", "PERIMETRE  DTO - DirInnov", "Code DT"])

    total_client = 0

    # boucle pour construire chaque echantillon
    for i in range(1, 5):
        
        # print la table par population
        for _, clients in clients_by_population:

            size_population_total = clients.shape[0]

            # prendre 25% de la population qui ne sont pas dans un echantillon et le ceil pour avoir un nombre entier
            population_not_in_echantillon = clients[clients["echantillon"].isna()]

            size_population = population_not_in_echantillon.shape[0]

            if size_population == 0:
                continue
                
            size_25 = ceil(size_population_total * 0.25)

            # prendre les 25% de la population
            head_25 = population_not_in_echantillon.head(size_25)

            # remplir la colonne echantillon
            clients_total.loc[head_25.index, "echantillon"] = i

            # ajouter le nombre de clients a la population totale
            total_client += head_25.shape[0]

    assert clients_total[clients_total['echantillon'].isna() == True].shape[0] == 0, "Certaines entrées ne sont affectées à aucun échantillons"
    assert total_client == clients_total_size, "Le résultats des échantillons ne contient pas autant d'entrées que au début du programme"

    print(clients_total.groupby("echantillon").size())

    # créer un nouveau fichier excel en sortie
    clients_total.to_excel("Echantillonage_Aleatoire_Liste_Clients_La_Poste_DT_25%/Clients_echantillons.xlsx", index=False)


if __name__ == "__main__":
    main()