import time

plateau = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
"""renvoie la première ligne qui sera disponnible en fonction de la colonne choisie"""
def ligneDispo(colonne, plateau):
    for i in range(len(plateau), 0, -1):
        if plateau[i - 1][colonne] == 0:
            return i - 1

"""indique s'il reste une place dans la colonne choisie"""
def colonneValide(colonne, plateau):
    return plateau[0][colonne] == 0

"""enregistre toutes les colonnes disponnibles dans un tableau"""
def colonneDispo(plateau):
    colonnes = []
    for i in range(len(plateau[0])):
        if colonneValide(i, plateau):
            colonnes.append(i)
    return colonnes

"""vérifie si quelqu'un a gagné"""
def gagne(plateau, tour):
    for i in range(len(plateau)):
        for j in range(len(plateau[i]) - 3):
            if plateau[i][j] == tour and plateau[i][j] == plateau[i][j + 1] and plateau[i][j + 1] == plateau[i][
                j + 2] and \
                    plateau[i][j + 2] == plateau[i][j + 3]:
                return True
    for i in range(len(plateau) - 3):
        for j in range(len(plateau[i])):
            if plateau[i][j] == tour and plateau[i][j] == plateau[i + 1][j] and plateau[i + 1][j] == plateau[i + 2][
                j] and \
                    plateau[i + 2][j] == plateau[i + 3][j]:
                return True
    for i in range(len(plateau) - 3):
        for j in range(len(plateau[i]) - 3):
            if plateau[i][j] == tour and plateau[i][j] == plateau[i + 1][j + 1] and plateau[i + 1][j + 1] == \
                    plateau[i + 2][j + 2] and plateau[i + 2][j + 2] == plateau[i + 3][j + 3]:
                return True
    for i in range(3, len(plateau)):
        for j in range(len(plateau[i]) - 3):
            if plateau[i][j] == tour and plateau[i][j] == plateau[i - 1][j + 1] and plateau[i - 1][j + 1] == \
                    plateau[i - 2][j + 2] and plateau[i - 3][j + 3] == plateau[i - 2][j + 2]:
                return True
    else:
        return False

"""place une pièce dans la colonne indiquée"""
def placerPiece(tour, plateau, colonne):
    if type(ligneDispo(colonne, plateau))==int:
        plateau[ligneDispo(colonne, plateau)][colonne] = tour
    return plateau
import matplotlib.pyplot as plt
"""affiche le plateau"""
def dessinerPlateau(plateau):
    for i in plateau:
        print(i)
    plt.scatter(plateau)

    plt.show()
"""permet de faire tourner une matrice à 45° afin de simplifier le calcul de l'heuristique"""
def rotate45(plateau, horloge):
    resultat = []
    if horloge:
        for i in range(len(plateau)):
            resultat.append([0] * (len(plateau) + len(plateau[0]) - 1))
            for j in range(len(plateau[i])):
                resultat[i][int(i + j)] = plateau[i][j]
    if not horloge:
        for i in range(len(plateau)):
            resultat.append([0] * (len(plateau) + len(plateau[0]) - 1))
            for j in range(len(plateau[i])):
                resultat[i][int(i + j)] = plateau[i][len(plateau[i]) - 1 - j]
    return resultat

"""calcule l'heuristique de tout le plateau"""
def getUtility(plateau):
    compteur = utility(plateau) #calcule la valeur de chaque ligne
    a = utility(list(map(list, zip(*plateau)))) #calcule la valeur de chaque colonne en utilisant la transposée du plateau
    d = utility(list(map(list, zip(*rotate45(plateau[3:14], True))))) #calcule la valeur des diagonales en tournant la matrice de 45°
    f = utility(list(map(list, zip(*rotate45(plateau[3:14], False))))) #calcule la valeur des diagonales en tournant la matrice de -45°
    compteur += a + d + f
    return compteur



"""calcule la valeur d'un tableau """
def utility(plateau):
    grandCompteur = 0
    i = 0
    j = 0
    while i < len(plateau):
        while j < len(plateau[i]):
            compteur = 0
            if j < len(plateau[i]) and plateau[i][j] == pieces.pieceJOUEUR:
                while len(plateau[i]) > j >= 0 and plateau[i][j] == pieces.pieceJOUEUR:
                    compteur += 1

                    j += 1
                compteur = 10 * compteur ** compteur
                grandCompteur += compteur
            compteur = 0
            if j < len(plateau[i]) and plateau[i][j] == pieces.pieceIA:
                while len(plateau[i]) > j >= 0 and plateau[i][j] == pieces.pieceIA:
                    compteur += 1
                    j += 1
                compteur = 10 * compteur ** compteur
                grandCompteur -= compteur
            j += 1
        j = 0
        i += 1
    return grandCompteur

"""fonction minimax implémentant l'élagage alpha beta"""
def minimax(plateau, alpha, beta, maximise, depth):
    colonnes = colonneDispo(plateau)
    colonne = colonnes[0]
    terminal = pieces.compteurPieceIA == 0 or pieces.compteurPieceJoueur == 0 or gagne(plateau, 1) or gagne(plateau, 2)
    if terminal or depth == 0:
        if terminal:
            if gagne(plateau, pieces.pieceJOUEUR):
                return None, float('inf')
            if gagne(plateau, pieces.pieceIA):
                return None, -float('inf')
            else:
                return None, 0
        else:
            return None, getUtility(plateau)
    if maximise:
        valeur = -float('inf')

        for i in colonnes:
            plateauCopie = list(map(list, plateau))
            plateauCopie = placerPiece(pieces.pieceJOUEUR, plateauCopie, i)
            valeur2 = minimax(plateauCopie, alpha, beta, False, depth - 1)[1]
            if valeur2 > valeur:
                colonne = i
                valeur = valeur2
            alpha = max(alpha, valeur)
            if alpha >= beta:
                break
        return colonne, valeur
    else:
        valeur = float('inf')

        for i in colonnes:
            plateauCopie = list(map(list, plateau))
            plateauCopie = placerPiece(pieces.pieceIA, plateauCopie, i)
            valeur2 = minimax(plateauCopie, alpha, beta, True, depth - 1)[1]
            if valeur2 < valeur:
                colonne = i
                valeur = valeur2
            beta = min(beta, valeur)
            if alpha >= beta:
                break
        return colonne, valeur

"""classe permettant d'acceder aux informations des pieces plus rapidement"""
class Pieces:
    def __init__(self):
        self.pieceIA = 2
        self.pieceJOUEUR = 1
        self.compteurPieceJoueur = 21
        self.compteurPieceIA = 21


tour = 0
pieces = Pieces()
while pieces.compteurPieceIA + pieces.compteurPieceJoueur <= 42 and not gagne(plateau,
                                                                              pieces.pieceJOUEUR) and not gagne(
        plateau, pieces.pieceIA):
    starttime = time.time()
    piece = pieces.pieceJOUEUR
    if tour == 0:
        col=minimax(plateau, -float('inf'), float('inf'), False, 5)[0]
        placerPiece(pieces.pieceIA, plateau, col)
        print('fini en ', time.time() - starttime)
        print("L'ia a joué en ",col+1)
        pieces.compteurPieceIA -= 1

    else:
        colonne = int(input())-1
        placerPiece(pieces.pieceJOUEUR, plateau, colonne)
        pieces.compteurPieceJoueur -= 1

    dessinerPlateau(plateau)

    tour = (tour + 1) % 2
