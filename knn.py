import copy

def normalisation_distance(distances):
    for i in range(len(distances)):
        distances[i][0] /= distances[len(distances) - 1][0]
    return distances



def distance(fleurTest, dataTrainRow):
    distance = 0.
    for i in range(len(fleurTest)):
        distance += abs(fleurTest[i] - dataTrainRow[i])
    return distance


def get_voisin(fleurTest, k):
    distances = []
    for i in range(len(dataTrain)):
        distances.append([distance(fleurTest, dataTrain[i]), i])
    distances.sort(key=lambda x: x[0])
    distances=distances[:k]
    distances = normalisation_distance(distances)
    for i in range(len(distances)):
        distances[i][0] = 1 - distances[i][0]
    return distances


def get_class(distances):
    fleursVoisines = []
    for i in distances:
        fleursVoisines.append(dataTrain[i[1]][4])
    classes = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0}

    for i in range(len(fleursVoisines)):
        classes[fleursVoisines[i]] += distances[i][0]
    result = {k: v for k, v in sorted(classes.items(), key=lambda item: item[1])}
    return list(result.keys())[-1]


def prediction(fleur, k):
    fleur.append(get_class(get_voisin(fleur, k)))
    return fleur


# on crée les données d'entrainement
dataTrain = []
with open("data.csv") as myfile:
    for line in myfile:
        dataTrain.append(line.rstrip().split(';'))  # on supprime les /n et chaque valeur devient une case de la liste
myfile.close()  # on ferme le fichier

for i in range(len(dataTrain)):  # on convertit toutes les valeurs possibles en float
    for j in range(len(dataTrain[i])):
        try:
            dataTrain[i][j] = float(dataTrain[i][j])
        except ValueError:  # si c'est pas possible ca les laisse en string
            pass
moreData=[]
with open("preTest.csv") as myfile: #on prend les données du fichier de pre test comme données d'entrainement supplémentaires
    for line in myfile:
        moreData.append(line.rstrip().split(';'))  # on supprime les /n et chaque valeur devient une case de la liste
myfile.close()  # on ferme le fichier
#dataTrain.pop(len(dataTrain) - 1)  # la derniere case est vide on la supprime

for i in range(len(moreData)):  # on convertit toutes les valeurs possibles en float
    for j in range(len(moreData[i])):
        try:
            moreData[i][j] = float(moreData[i][j])
        except ValueError:  # si c'est pas possible ca les laisse en string
            pass
#for i in moreData: #on ajoute les données du pre test aux données d'entrainement
    #dataTrain.append(i)
dataTest = []  # données a tester

with open("preTest.csv") as myfile: #on récupère les données à tester
    for line in myfile:
        dataTest.append(line.rstrip().split(';'))  # on supprime les /n et chaque valeur devient une case de la liste
myfile.close()  # on ferme le fichier

for i in range(len(dataTest)):  # on convertit toutes les valeurs possibles en float
    for j in range(len(dataTest[i])):
        try:
            dataTest[i][j] = float(dataTest[i][j])
        except ValueError:  # si c'est pas possible ca les laisse en string
            pass


resultat = copy.deepcopy(dataTest)
for i in dataTest:
    i.pop(4)    #on enlève le label des données à tester
counter = 0
matriceConf = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

for i in dataTest:
    prediction(i, k=8)
    h=ord(resultat[counter][4])-65   #on fait la matrice de confusion
    j=ord(i[4])-65
    matriceConf[h][j] += 1
    counter += 1

    #print(dataTest)
    #print(resultat)
with open("LIAO_LEVY.txt", "w") as txt_file:    #on crée et remplit le fichier de réponses
    for line in dataTest:
        txt_file.write(line[4] + "\n")
txt_file.close()
precision=0      #on affiche la précision des predictions de notre algorithme
for i in range(len(matriceConf)):
    for j in range(len(matriceConf[i])):
        if i!=j:
            precision+=matriceConf[i][j]
print(1-(precision/2078))
