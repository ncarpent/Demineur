"""
Créé le Ma 29/06/2021 à 19h07
Auteur : Natanaël
demineur 1.2.py
"""


from random import *

"""
¤ Présentation du jeu :

_ Une grille de 9 x 9 cases est fournie (numérotées de 1 à 9).
_ Une case peut être "ouverte" (on voit ce qu'elle contient), ou "fermée" (on ne voit rien).
    Au début de la partie, toutes les cases sont fermées.
_ Chaque case peut contenir (choix exclusif et par ordre de priorité) : _ une bombe (il y en a 10 en tout dans la grille) ;
                                                                        _ un chiffre indiquant le nombre de bombes dans les cases adjacentes ;
                                                                        _ rien du tout (le chiffre 0 dans ce cas).
    NB: deux cases sont adjacentes si elles sont en contact (elles peuvent avoir un côté ou un coin en commun).
        Une case qui n'est pas au bord de la grille a donc 8 cases adjacentes.
_ Il est possible d'ouvrir une case (pour voir ce qu'elle contient), mais pas de la refermer.
_ La première case à être ouverte lance la partie et ne contient pas de bombe (et ses cases adjacentes non plus).
_ Avant que la partie ne soit lancée, il est possible de marquer n'importe quelle case.
_ Si une case contenant 0 est ouverte, toutes ses cases adjacentes s'ouvrent automatiquement (cette règle peut se réitérer automatiquement).
_ Une case peut être marquée pour mémoriser une indication.
    Il existe deux types de marques :   _ "!" : permet de signaler une bombe sur la case ("marque bombe");
                                        _ "?" : permet d'exprimer un doute sur la présence d'une bombe sur la case ("marque doute").
_ Une marque peut-être retirée d'une case marquée.
_ La partie se termine soit par une défaite, soit par une victoire.
    La partie est gagnée lorsque toutes les cases ne contenant pas de bombe sont ouvertes (et les autres fermées).
    La partie est perdue dès qu'une case contenant une bombe a été ouverte.

¤ Implémentation :

_ Une grille est un tableau 2D (liste de listes).
_ Les lignes sont numérotées classiquement en interne de 0 à 8, mais de 1 à 9 lors des interractions avec l'utilisateur.
_ Une grille solution est générée aléatoirement à partir de coordonnées d'une case qui ne peut pas accueillir de bombes dans son voisinage.
_ La grille de jeu est générée comme une copie fermée de la grille solution, qui se dévoile progressivement (la grille solution contient donc toutes les valeurs de la grille de jeu).
_ Une case ouverte contient une valeur (un chiffre de 0 à 9 ou 'B').
_ Une case fermée contient '#' ou une marque ('!' ou '?').
_ L'affichage d'une grille (fournie en argument) s'effectue dans la console.
_ Un tour de jeu consiste en la réalisation d'une action (ouverture de case ou ajout / suppression de marque).
_ Les interractions avec l'utilisateur sont bouclées tant qu'elles n'ont pas un format adéquat.
_ Une partie consiste en une répétition de tours de jeu tant qu'elle n'est pas terminée.
_ La fin de partie consiste en l'affichage de la grille de jeu puis d'un mesage de Victoire ou de Défaite selon les cas.

¤ Liste des fonctions :


# Génération de la grille solution :
    _ generation_grille_vide
    _ emplacement_bombe
    _ placement_bombe
    _ test_bomb
    _ nb_bombes_adj
    _ placement_chiffre
    _ generation_grille_decouverte
# Génération de la grille de jeu :
    _ generation_grille_jeu
# Affichage d'une grille :
    _ affichage_tirets
    _ affichage_ligne
    _ affichage
# Modélisation d'un tour de jeu :
    _ demander_coord
    _ demander_action
    _ action
    _ tour
# Modélisation d'une partie complète :
    _ initialisation
    _ jeu
# Gestion de la fin du jeu :
    _ test_fin
    _ defaite
    _ victoire
# Améliorations :
    _ cases_adj
    _ zero_extension
    _ emplacement_bombe_ameliore
    _ calcul_nb_bombe
    _ affichage_nb_bombe
    _ test_fin_ameliore
    _ tour_init
    _ action_init
    _ maj_bombes
    _ defaite_amelioree

¤ Mises à jours :

_ Anticipation des entrées erronnées (boucle tant que l'entrée n'est pas sous un format attendu)

¤ Démineur version 1.2 (Anticipation des entrées)

Démarrer la partie avec la commande : jeu()
"""


## génération de la grille solution

"""
Cette section permet de générer une grille solution. C'est une grille de jeu dont toutes les cases sont ouvertes.
On peut fournir les coordonnées d'une case qui ne contiendra pas de bombe et qui ne verra aucune bombe dans son voisinage, lors de la création.
"""

def generation_grille_vide () :
    """
    Génère une grille vide de taille 9x9.
    
    Arguments : aucun.
    Valeur de retour : grille de taille 9x9 remplie de None.
    """
    return [[None for j in range(9)] for i in range(9)]



def emplacement_bombe (k = None, l = None) :
    """
    Tire au hasard dix cases sur la grille. Les cases sont repérées par leurs coordonnées.
    Les cases tirées représentent des emplacements de bombes.
    On peut optionnellement fournir en paramètre les coordonnées d'une case qui ne contiendra aucune bombe et qui n'aura aucune bombe dans son voisinage.
    
    Arguments : k : numéro de ligne (optionnel) / l : numéro de colonne (optionnel).
    Valeur de retour : liste des dix coordonnées tirées au hasard.
    """
    ind_tot = [(i, j) for i in range(9) for j in range(9)]
    if type(k) == int and type(l) == int :
        ind_tot.remove((k, l))
        emplacement_bombe_ameliore(k, l, ind_tot)
    ind_bomb = sample(ind_tot, 10)
    return ind_bomb



def placement_bombe (G, l) :
    """
    Place des bombes dans la grille aux coordonnées fournies.
    
    Arguments : G : une grille / l : une liste de coordonnées.
    Valeur de retour : aucune.
    """
    for coord in l :
        G[coord[0]][coord[1]] = "B"



def test_bomb (G, i, j) :
    """
    Teste si une bombe est présente dans la case de la grille aux coordonnées fournies.
    
    Arguments : G : une grille / i : un numéro de ligne / j : un numéro de colonne.
    Valeur de retour : renvoie 1 si la case (i, j) de G contient une bombe, 0 sinon.
    """
    if G[i][j] == "B" :
        return 1
    else :
        return 0



def nb_bombes_adj (G, i, j) :
    """
    Calcule le nombre de bombes présentes dans les cases adjacentes à la case fournie en paramètre.
    Une case adjacente est une case qui a un côté ou un coin en commun.
    
    Arguments : G : une grille / i : un numéro de ligne / j : un numéro de colonne.
    Valeur de retour : nombre de bombes dans les cases adjacentes.
    """
    cpt = 0
    if i+1 < 9 :
        cpt += test_bomb(G, i+1, j)
    if i-1 >= 0 :
        cpt += test_bomb(G, i-1, j)
    if j+1 < 9 :
        cpt += test_bomb(G, i, j+1)
    if j-1 >= 0 :
        cpt += test_bomb(G, i, j-1)
    if i+1 < 9 and j+1 < 9 :
        cpt += test_bomb(G, i+1, j+1)
    if i+1 < 9 and j-1 >= 0 :
        cpt += test_bomb(G, i+1, j-1)
    if i-1 >= 0 and j+1 < 9 :
        cpt += test_bomb(G, i-1, j+1)
    if i-1 >= 0 and j-1 >= 0 :
        cpt += test_bomb(G, i-1, j-1)
    return cpt



def placement_chiffre (G) :
    """
    Place dans chaque case de la grille fournie le nombre de bombes présentes dans les cases adjacentes.
    Ne fais rien si une bombe est déjà placée dans la case.
    
    Arguments : G : une grille (on attend que les bombes soient déjà placées dans cette grille).
    Valeur de retour : aucune.
    """
    for i in range(9) :
        for j in range(9) :
            if G[i][j] == None :
                G[i][j] = str(nb_bombes_adj(G, i, j))



def generation_grille_decouverte (i = None, j = None) :
    """
    Génère une grille solution complète (remplie avec 10 bombes et le nombre de bombes adjacentes dans les cases qui restent).
    La grille générée ne possède pas de bombe aux coordonnées fournies, ni dans les cases adjacentes.
    
    Arguments : i : numéro de ligne (optionnel) / j : numéro de colonne (optionnel).
    Valeur de retour : la grille solution remplie.
    """
    grille = generation_grille_vide()
    ind_bomb = emplacement_bombe(i, j)
    placement_bombe(grille, ind_bomb)
    placement_chiffre(grille)
    return grille



## génération de la grille de jeu

"""
Cette section permet de générer une grille de jeu. C'est une grille dont toutes les cases sont fermées.
Cette grille sera associée à une grille solution et se comportera en jeu comme si elle avait les mêmes valeurs que celle-ci.
"""

def generation_grille_jeu () :
    """
    Génère une grille dont toutes les cases sont fermées.
    
    Arguments : aucun.
    Valeur de retour : grille de taille 9x9 remplie de '#'.
    """
    return [['#' for j in range(9)] for i in range(9)]



## affichage

"""
Cette section permet d'afficher une grille en mode console.
"""

def affichage_tirets () :
    """
    Affiche une ligne de tirets dans la console.
    
    Arguments : aucun.
    Valeur de retour : aucune.
    """
    for j in range(9) :
        print('----', end='')
    print('-')



def affichage_ligne (grille, i) :
    """
    Affiche une ligne d'une grille dans la console.
    
    Arguments : grille : la grille dont on veut afficher une ligne / i : le numéro de la ligne à afficher.
    Valeur de retour : aucune.
    """
    print('|', end=' ')
    for j in range(9) :
        print(str(grille[i][j]), end=' | ')
    print()



def affichage (grille) :
    """
    Affiche une grille de jeu dans la console.
    La grille de jeu est munie de coordonnées sur la ligne du haut et la colonne de gauche.
    Affiche à la suite le nombre de bombes placées / à trouver.
    
    Arguments : G : la grille à afficher.
    Valeur de retour : aucune.
    """
    print('  |', end=' ')
    for j in range(9) :
        print(j+1, end=' | ')
    print()
    print('-', end='-')
    affichage_tirets()
    for i in range(9) :
        print(i+1, end=' ')
        affichage_ligne(grille, i)
        print('-', end='-')
        affichage_tirets()
    affichage_nb_bombe(grille)
    print()



## tour de jeu

"""
Cette section permet de gérer un tour de jeu.
Un tour de jeu consiste à cibler une case, choisir une action et effectuer cette action.
"""

def demander_coord () :
    """
    Demande les coordonnées d'une case à l'utilisateur (tant qu'il n'a pas fournit des coordonnées correctes).
    
    Arguments : aucun.
    Valeur de retour : couple de coordonnées (dans le type int).
    """
    print("Coordonnées de la case ;")
    (l, c) = ('', '')
    while not (l.isdigit() and int(l) >= 1 and int(l) <= 9) :
        l = input("ligne : ")
    while not (c.isdigit() and int(c) >= 1 and int(c) <= 9) :
        c = input("colonne : ")
    return (int(l) - 1, int(c) - 1)



def demander_action () :
    """
    Demande une action à effectuer à l'utilisateur (tant que le format fournit n'est pas adéquat).
    
    Arguments : aucun.
    Valeur de retour : numéro de l'action à effectuer (type int).
    """
    print("Choisir une action (entrer le code correspondant).")
    print("0 : ouvrir la case.")
    print("1 : placer un drapeau.")
    print("2 : placer un point d'interrogation.")
    print("3 : retirer un drapeau.")
    print("4 : retirer un point d'interrogation.")
    act = ''
    while not (act.isdigit() and int(act) >= 0 and int(act) <= 4) :
        act = input("action : ")
    return int(act)



def action (grille, sol, i, j, act) :
    """
    Effectue une action (fournie sous forme de numéro) sur une case donnée.
    En cas d'ouverture d'une case qui contient '0', les cases adjacentes sont automatiquement ouvertes (et ainsi de suite, si elles contiennent '0').
    
    Arguments : grille : une grille de jeu / sol : la grille solution associée / i : un numéro de ligne / j : un numéro de colonne / act : un numéro d'action.
    Valeur de retour : False si l'action consiste en l'ouverture d'une case munie d'une bombe, True sinon.
    """
    if act == 0 and grille[i][j] != '!' :
        grille[i][j] = sol[i][j]
        if sol[i][j] == "B" :
            return False
        elif grille[i][j] == '0' :
            zero_extension(grille, sol, i, j)
    elif act == 1 and not grille[i][j].isdigit() :
        grille[i][j] = '!'
    elif act == 2 and not grille[i][j].isdigit() :
        grille[i][j] = '?'
    elif act == 3 and grille[i][j] == '!' :
        grille[i][j] = '#'
    elif act == 4 and grille[i][j] == '?' :
        grille[i][j] = '#'
    return True



def tour (grille, sol) :
    """
    Effectue un "tour de jeu", ce qui correspond à :
    _ afficher la grille de jeu ;
    _ demander des coordonnées pour cibler une case précise ;
    _ demander une action à effectuer dans cette case sous forme de numéro ;
    _ effectuer cette action.
    
    Arguments : grille : une grille de jeu / sol : la grille solution associée.
    Valeur de retour : False si une bombe a été découverte durant l'action, True sinon.
    """
    affichage(grille)
    (i, j) = demander_coord()
    act = demander_action()
    result = action(grille, sol, i, j, act)
    return result



## menu de jeu

"""
Cette section gère le coeur du jeu. Elle utilise toutes les autres sections pour générer une partie de jeu complète.
"""

def initialisation () :
    """
    Génère la grille de jeu et effectue le premier tour de jeu (potentiellement en boucle) jusqu'à obtenir les coordonnées de la première case à ouvrir (aucune bombe ne sera placé sur cette case ni dans les cases adjacentes).
    Génère la grille solution (en fonction de cette case) et ouvre la première case de la grille de jeu.
    Il est possible de marquer des cases avant l'ouverture de la première case.
    
    Arguments : aucun.
    Valeur de retour : couple grille de jeu et grille solution associée.
    """
    grille = generation_grille_jeu()
    coord_init = None
    while coord_init == None :
        coord_init = tour_init(grille)
    i = coord_init[0]
    j = coord_init[1]
    sol = generation_grille_decouverte(i, j)
    # affichage(sol) nécessaire au débugage
    action(grille, sol, i, j, 0)
    return grille, sol



def jeu () :
    """
    Menu principal du jeu.
    Modélise une partie de jeu :
    _ Initialise la grille de jeu et la grille solution associée.
    _ effectue des "tours de jeu" tant que la partie n'est pas terminée. La boucle prend fin en cas de défaite ou de victoire.
    _ Affiche la grille de jeu en fin de partie.
    _ Redirige vers une défaite ou une victoire en fonction de la sortie de boucle.
    
    Arguments : aucun.
    Valeur de retour : aucune. 
    """
    (grille, sol) = initialisation()
    continuer = True
    while continuer and not test_fin_ameliore(grille, sol):
        continuer = tour(grille, sol)
    affichage(grille)
    if not continuer :
        defaite_amelioree(grille, sol)
    else :
        victoire()



## Fin de jeu

"""
Cette section gère l'arrêt de la partie et la fin du jeu.
"""

def test_fin (grille, sol) :
    """
    Teste si la grille de jeu est complète (victoire).
    La grille est complète si toutes les cases comportant une bombe sont marquées par "!" et toutes les autres sont ouvertes.
    Cette fonction est remplacée par "test_fin_ameliorer"
    
    Arguments : grille : une grille de jeu / sol : sa grille solution associée
    Valeur de retour : True si la grille est complète, False sinon.
    """
    for i in range(9) :
        for j in range(9) :
            if not(grille[i][j].isdigit()) and (grille[i][j] != '!' or sol[i][j] != 'B') :
                return False
    return True



def defaite () :
    """
    Affiche le message de défaite.
    Cette fonction est remplacée par "defaite_amelioree".
    
    Arguments : aucun.
    Valeur de retour : aucune.
    """
    print("Game Over : vous avez fait explosé une bombe !")



def victoire () :
    """
    Affiche le message de victoire.
    
    Arguments : aucun.
    Valeur de retour : aucune.
    """
    print("Bravo : vous avez terminé cette grille.")



## Améliorations

"""
Cette section gère des option supplémentaires qui ne sont pas absolument indispensables au fonctionnement.
"""

def cases_adj (i, j) :
    """
    Calcule les coordonnées des cases adjacentes à la case fournie en paramètre.
    
    Arguments : i : un numéro de ligne / j : un numéro de colonne.
    Valeur de retour : liste des coordonnées des cases adjacentes.
    """
    cases = []
    if i+1 < 9 :
        cases.append((i+1, j))
        if j+1 < 9 :
            cases.append((i+1, j+1))
        if j-1 >= 0 :
            cases.append((i+1, j-1))
    if i-1 >= 0 :
        cases.append((i-1, j))
        if j+1 < 9 :
            cases.append((i-1, j+1))
        if j-1 >= 0 :
            cases.append((i-1, j-1))
    if j+1 < 9 :
        cases.append((i, j+1))
    if j-1 >= 0 :
        cases.append((i, j-1))
    return cases



def zero_extension (grille, sol, i, j) :
    """
    Ouvre les cases adjacentes à la case fournie en argument, qui ne sont pas marquées par une bombe ou déjà ouvertes.
    
    Arguments : grille : une grille de jeu / sol : la grille solution associée / i : un numéro de ligne / j : un numéro de colonne.
    Valeur de retour : aucune.
    """
    cases = cases_adj(i, j)
    for c in cases :
        if grille[c[0]][c[1]] == '#' or grille[c[0]][c[1]] == '?':
            action(grille, sol, c[0], c[1], 0)



def emplacement_bombe_ameliore (i, j, liste) :
    """
    Retire d'une liste de coordonnées de cases les coordonnées des cases adjacentes à la case fournie en argument.
    
    Arguments : i : numéro de ligne / j : numéro de colonne / liste : liste de coordonnées des cases de la grille.
    Valeur de retour : aucune.
    """
    cases = cases_adj(i, j)
    for c in cases :
        liste.remove(c)



def calcul_nb_bombe (grille) :
    """
    Calcule le nombre de marques "bombe" qui ont été placées sur la grille.
    
    Arguments : grille : une grille de jeu.
    Valeur de retour : nombre de marques "bombe" présentes sur la grille.
    """
    nb = 0
    for i in range(9) :
        for j in range(9) :
            if grille[i][j] == '!' :
                nb +=1
    return nb



def affichage_nb_bombe (grille) :
    """
    Affiche un message précisant le nombre de marques "bombe" placées dans la grille.
    
    Arguments : grille : une grille de jeu.
    Valeur de retour : aucune.
    """
    print("Nombre de bombes détectées : ", calcul_nb_bombe(grille), "/ 10.")



def test_fin_ameliore (grille, sol) :
    """
    Teste si la grille de jeu est complète (victoire). Remplace la fonction "test_fin" car est plus précise que cette dernière.
    La grille est complète si toutes les cases comportant une bombe sont fermées et toutes les autres sont ouvertes.
    
    Arguments : grille : une grille de jeu / sol : la grille solution associée
    Valeur de retour : True si la grille est complète, False sinon.
    """
    for i in range(9) :
        for j in range(9) :
            if not grille[i][j].isdigit() and sol[i][j] != 'B' :
                return False
    return True



def tour_init(grille) :
    """
    Effectue le premier tour de jeu.
    Le premier tour du jeu consiste à afficher la grille, cibler une case et une action, et effectuer la première action du jeu (en fonction de l'action demandée).
    
    Arguments : grille : une grille de jeu.
    Valeur de retour : coordonnées de la case en cas de demande d'ouverture (sur une case ouvrable), None sinon.
    """
    affichage(grille)
    (i, j) = demander_coord()
    act = demander_action()
    result = action_init(grille, i, j, act)
    return result



def action_init (grille, i, j, act) :
    """
    Effectue la première action du jeu.
    Si c'est une ouverture de case (et que la case est ouvrable), retransmet les coordonnées de la case cible. Sinon (l'action demandée est un ajout / suppression de marque ou la case contient une marque "bombe"), effectue cette action si possible.
    
    Arguments : grille : une grille de jeu (vierge car la grille solution associée n'a pas encore été générée) / i : un numéro de ligne / j : un numéro de colonne / act : un numéro d'action à effectuer.
    Valeur de retour : coordonnées de la case en cas de demande d'ouverture (sur une case ouvrable), None sinon.
    """
    if act == 0 and grille[i][j] != '!' :
        return (i, j)
    elif act == 1 :
        grille[i][j] = '!'
    elif act == 2 :
        grille[i][j] = '?'
    elif act == 3 and grille[i][j] == '!' :
        grille[i][j] = '#'
    elif act == 4 and grille[i][j] == '?' :
        grille[i][j] = '#'
    return None



def maj_bombes (grille, sol) :
    """
    Ouvre toutes les cases qui contiennent une bombe pour les mettre en évidence.
    
    Arguments : grille : une grille de jeu / sol : la grille solution associée.
    Valeur de retour : aucune.
    """
    for i in range(9) :
        for j in range(9) :
            if sol[i][j] == 'B' :
                grille[i][j] = sol[i][j]



def defaite_amelioree (grille, sol) :
    """
    Affiche la grille (avec toutes les bombes mises en valeur) et un message de défaite.
    Améliore et remplace la fonction "defaite".
    
    Arguments : grille : une grille de jeu / sol : la grille solution associée.
    Valeur de retour : aucune.
    """
    print("Game Over : vous avez fait explosé une bombe !")
    maj_bombes(grille, sol)
    affichage(grille)
    


