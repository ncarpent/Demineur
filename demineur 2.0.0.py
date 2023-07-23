"""
Créé le Di 12/03/2023 à 22h17
Auteur : Natanaël
"""

"""
A faire :

grille solution :
    ¤ générer une grille vide
    ¤ générer les emplacements des bombes (différents de la case de départ choisie)
    ¤ générer les bombes dans la grille (à partir d'une grille et d'une liste de coordonnées)
    ¤ calculer le nombre de bombe(s) adjacente(s) à une case
    ¤ générer les chiffres d'indications
    ¤ générer la grille solution
    
grille de jeu :
    ¤ générer une grille vierge (copie de la solution)
    
jeu :
    ¤ récupérer les coordonnées
    ¤ demander une action
    ¤ modifier la grille
    ¤ initialisation du jeu
    ¤ afficher la grille
    ¤ menu de jeu
    
fin de jeu :
    ¤ arrêt du jeu en cas de défaite
    ¤ arrêt du jeu en cas de victoire
    ¤ victoire
    ¤ échec
    
améliorations :
    ¤ afficher les coordonnées avec la grille
    ¤ impossibilité de tomber sur un chiffre au début
    ¤ éclaircir plusieurs cases en 0 (ouvrir aussi les cases marquées, mais pas par une bombe)
    ¤ réindexation : taille de la grille : 9x9 au lieu de 10x10.
    ¤ réindexation : indices démarrant à 1 lors des interactions i/o avec l'utilisateur (traitement interne inchangé)
        ¤ affichage
        ¤ entrées de commande
        (affichage du 10 pose problème (deux caractères au lieu d'un), donc je garde l'indiçage démarrant à zéro pour l'instant.)
    ¤ noter le nombre de bombes restantes
    ¤ affiner les conditions de fin
    ¤ annulation des marquages (codes d'action supplémentaires, ce sera sûrement plus simple...)
        ¤ drapeaux
        ¤ points d'interrogation
    ¤ impossibilité de marquer une case ouverte et d'ouvrir une case marquée d'un drapeau.
    ¤ laisser la première action libre
    ¤ affichage final
    
    ¤ ==> faire des versions /!\
    ¤ ==> documenter les fonctions /!\
    
    ¤ anticipations des entrées erronées
    ¤ créer des variables générales regroupant les caractères utilisés, les tailles de grille, ...
    ¤ renommer propremment les variables
    ¤ réorganiser les fonctions
    _ anticiper les exceptions (?)
    _ utiliser des classes (Case, Array)
    _ utiliser des fonctions 'placer drapeau', 'masquer case'...
    _ définir le nombre de caractères par case



-> éclaircir les cases au-delà des cases marquées par des bombes (à priori non)
|-> lors de l'ouverture d'une case vide, certaines cases sont ouvertes automatiquement sous certaines conditions :
    - une case non-marquée peut être ouverte
    - une case marquée d'un "?" peut être ouverte
    - une case marquée d'un "!" ne peut pas être ouverte
    - les cases adjacentes à la case vide s'ouvrent si possible (processus récursif)
    - nb: les cases au-delà d'une case marquée d'un "!" ne peuvent pas être ouvertes directement
    - nb: les cases en diagonales sont adjacentes et peuvent donc être ouverte, potentiellement
    - nb: une case chiffre ne peut pas déclencher cet effet, même pour ouvrir une case qui se serait ouverte naturellement (si elle n'avait pas été bloquée par une case "!"





! compter le nombre de cases ouvertes (pour la victoire)... (variable globale)
/!\ fin de jeu prématurée, à voir ... edit : non à priori je me suis juste planté en jouant x)
/!\ affichage : une case passe de 1 à 12 au tour suivant / edit c'est un tiret et les espaces entre 2 cases qui sont supprimmés (lors du placement d'une bombe) / edit2 : erreur rectifiée au tour suivant
! test_fin à revoir
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
_ Une case fermée contient '#' ou une marque ('!'/'X' ou '?').
_ L'affichage d'une grille (fournie en argument) s'effectue dans la console.
_ Un tour de jeu consiste en la réalisation d'une action (ouverture de case ou ajout / suppression de marque).
_ Les interractions avec l'utilisateur sont bouclées tant qu'elles n'ont pas un format adéquat.
_ Une partie consiste en une répétition de tours de jeu tant qu'elle n'est pas terminée.
_ La fin de partie consiste en l'affichage de la grille de jeu puis d'un mesage de Victoire ou de Défaite selon les cas.
_ Les paramètres comme taille de grille ou nombre de bombes se changent facilement avec les variables au début.

¤ Liste des sections (fonctions et constantes) :

# Définition des constantes :
# Génération de la grille solution :
    _ generation_grille
    _ cases_adj
    _ emplacement_bombe
    _ placement_bombe
    _ test_bomb
    _ nb_bombes_adj
    _ placement_chiffre
    _ generation_grille_decouverte
# Affichage d'une grille :
    _ affichage_tirets
    _ affichage_ligne
    _ affichage_nb_bombe
    _ affichage
# Modélisation d'un tour de jeu :
    _ demander_coord
    _ demander_action
    _ action
    _ zero_extension
    _ tour
# Modélisation d'une partie complète :
    _ tour_init
    _ action_init
    _ initialisation
    _ jeu
# Gestion de la fin du jeu :
    _ test_fin
    _ maj_bombes
    _ defaite
    _ victoire
# Statistiques :
    _ calcul_nb_marques_bombe

¤ Mises à jours :

+ structures de case et grille

¤ Démineur version  ()

démarrer la partie avec la commande : jeu()
"""



## Structures



class Case :
    
    """
    Cette clase définit la structure d'une case d'une grille de démineur.
    
    Méthodes :
        * Edition de l'objet :
            __init__()
            __repr__()
        * Comparaison de l'objet :
            __eq__()
        * Autre : (méthodes ou champs ???)
            est_ouverte()
            est_fermee()
            ouvrir()
            valeur()
            coord()
            contient_marque()
            marque()
            placer_marque()
            retirer_marque()
            est_init()
            test_bombe()
            placer_bombe()
            
    idées :
    _ méthode "changer_val" qui lève une exception si une var loc/glob (les deux sont possible ?) "init" vaut false et change la val sinon.
    """
    
    ## Edition d'une Case
    
    def __init__ (self, ligne, colonne) :
        """
        Constructeur de la classe Case. val doit tjs être une str (?!)
        """
        self.ligne = ligne
        self.colonne = colonne
        self.val = None
        self.ouverte = False
        self.marq = None
    
    
    
    def __repr__ (self) :
        """
        Affiche une case selon qu'elle est ouverte ou marquée.
        """
        if self.est_ouverte() :
            if self.valeur() == None :
                return "None"
            return self.valeur()
        else :
            if self.contient_marque() :
                return self.marque()
            else :
                return symb_cache
    
    
    
    ## Comparaison d'une Case
    
    
    
    def __eq__ (self, obj) :
        """
        Teste l'égalité de deux cases.
        Permet notamment la recherche dans une liste.
        """
        return type(obj) == Case and self.ligne == obj.ligne and self.colonne == obj.colonne
    
    
    
    ## Autres méthodes
    
    
    
    def est_ouverte (self) :
        """
        Teste si le contenu de la case est visible (si la case est ouverte).
        """
        return self.ouverte
    
    
    
    def est_fermee (self) :
        """
        Teste si la case est bien fermée.
        """
        return not self.ouverte
    
    
    
    def ouvrir (self) :
        """
        Ouvre la case.
        """
        self.ouverte = True
    
    
    
    def valeur (self) :
        """
        Renvoie la valeur de la case.
        """
        return self.val
    
    
    
    def coordonnees (self) :
        """
        Renvoie la valeur des coordonnées de la case.
        """
        return self.ligne, self.colonne
    
    
    
    def contient_marque (self) :
        """
        Teste si la case possède une marque.
        """
        return self.marq != None
    
    
    
    def marque (self) :
        """
        Renvoie la marque qui est sur la case.
        """
        return self.marq
    
    
    
    def placer_marque (self, mark) :
        """
        Place une marque (fournie en argument) sur la case.
        """
        if mark != symb_detect and mark != symb_supp :
            raise ValueError("Une marque ne peut être qu'une marque de suspicion (\"" + symb_supp + "\") ou une marque de détection (\"" + symb_detect + "\").")
        self.marq = mark
    
    
    
    def retirer_marque (self) :
        """
        Retire une marque éventuelle de la case (ne fais rien si la case n'est pas marquée).
        """
        self.marq = None
    
    
    
    def est_init (self) :
        """
        Teste si la case est initialisée (possède une valeur).
        """
        return self.valeur() != None
    
    
    
    def test_bombe (self) :
        """
        Teste si la case contient une bombe.
        """
        return self.val == symb_bmb
    
    
    
    def placer_bombe (self) :
        """
        Place une bombe dans la case.
        """
        self.val = symb_bmb





class Grille :
    
    """
    Cette classe définit la structure d'une grille de démineur.
    
    Méthodes :
        ¤ Edition de l'objet :
            __init__()
            __repr__()
                | repr_ligne()
                | repr_tirets()
        ¤ Méthodes de conteneur :
            __getitem__()           : renvoie la case (ou sa valeur ?)
                | verification_double_indice()
            __setitem__()           : modifie la valeur !
                | verification_valeur()
            __delitem__ ?
            __contains__ ?
            __len__()
        ¤ Autres :
            cases_adjacentes()
            placer_bombes()         -- ok -- arg optionnel ?
            nombre_bombes_adjacentes()
            placer_chiffres()
            zero_extension --ou pas pour l'instant???
            initialisation          -- tmp ok
            test_defaite()
            test_victoire()         -- ok (condition à préciser ? - inclus la clause "n'est pas une défaite"
            maj_bombes              -- non, au pire ouvrir suffit pour l'instant
            calcul_nb_marq_bombs    -- à voir plus tard
        ¤ Débugage :
            ouvrir                  -- ok (case / ligne / colonne / grille)
                | ouvrir_ligne
                | ouvrir_colonne
    """
    
    ## Edition d'une Grille
    
    def __init__ (self) :
        """
        Constructeur de la classe Grille.
        """
        self.grille = [[Case(i, j) for j in range(nb_col)] for i in range(nb_lig)]
    
    
    
    def repr_ligne (self, i) :
        """
        Affichage d'une ligne d'une grille.
        """
        ret = "| "
        for j in range(nb_col) :
            ret += str(self[i, j]) + " | "
        return ret
    
    
    
    def repr_tirets (self) :
        """
        Affiche une ligne de tirets.
        """
        ret = "-"
        for j in range(nb_col) :
            ret += "----"
        return ret
    
    
    
    def __repr__ (self) :
        """
        Affiche une grille.
        """
        ret = ""
        for i in range(nb_lig) :
            ret += self.repr_tirets() + "\n"
            ret += self.repr_ligne(i) + "\n"
        ret += self.repr_tirets()
        return ret
    
    
    
    ## Méthodes de conteneur
    
    
    
    def verification_double_indice (self, inds) :
        """
        Teste la validité de l'indice double et lève les éventuelles exceptions nécessaires.
        Renvoie les coordonnées sous forme de couple.
        """
        if not (type(inds) == tuple and len(inds) == 2) :
            raise IndexError ("La lecture élémentaire d'une grille nécessite un double indice.")
        if not (type(inds[0]) == int and inds[0] in range(nb_lig)) :
            raise IndexError (str(inds[0]) + " n'est pas un entier entre 0 et " + str(nb_lig) + ".")
        if not (type(inds[1]) == int and inds[1] in range(nb_col)) :
            raise IndexError (str(inds[1]) + " n'est pas un entier entre 0 et " + str(nb_col) + ".")
        return (inds[0], inds[1])
    
    
    
    def verification_valeur (self, val) :
        """
        Teste la validité de la valeur à placer dans une case et lève les éventuelles exceptions.
        Renvoie la valeur sous forme de chaîne de caractères (str).
        """
        return str(val)
    
    
    
    def __getitem__ (self, inds) :
        """
        Renvoie la case d'indices i, j de la grille (avec la syntaxe self[i, j]).
        """
        (i, j) = self.verification_double_indice(inds)
        return self.grille[i][j]
    
    
    
    def __setitem__ (self, inds, val) :
        """
        Met à jour la valeur de la case d'indices i, j avec val (avec la syntaxe self[i][j] = val).
        Cette fonction a donc pour vocation de n'être utilisée que lors de l'initialisation de la grille.
        """
        (i, j) = self.verification_double_indice(inds)
        self.grille[i][j].val = self.verification_valeur(val)
    
    
    
    def __len__ (self) :
        """
        Renvoie le nombre de cases de la grille (nb_lig * nb_col).
        """
        return nb_lig * nb_col
    
    
    
    ## Autres méthodes
    
    
    
    def cases_adjacentes (self, i, j) :
        """
        Renvoie la liste des cases adjacentes à celle dont les coordonnées sont fournies en argument.
        """
        cases = []
        if i+1 < nb_lig :
            cases.append(self[i+1, j])
            if j+1 < nb_col :
                cases.append(self[i+1, j+1])
            if j-1 >= 0 :
                cases.append(self[i+1, j-1])
        if i-1 >= 0 :
            cases.append(self[i-1, j])
            if j+1 < nb_col :
                cases.append(self[i-1, j+1])
            if j-1 >= 0 :
                cases.append(self[i-1, j-1])
        if j+1 < nb_col :
            cases.append(self[i, j+1])
        if j-1 >= 0 :
            cases.append(self[i, j-1])
        return cases
    
    
    
    def placer_bombes (self, i, j) :
        """
        Place des bombes au hasard dans un certain nombre de cases.
        Le nombre de cases recevant une bombe est déterminé par la variable globale "nb_bmb".
        """
        cases_dispo = []
        adj = self.cases_adjacentes(i, j)
        for l in range(nb_lig) :
            for c in range(nb_col) :
                if self[l, c] != self[i, j] and self[l, c] not in adj :
                    cases_dispo.append(self[l, c])
        cases_bombes =  sample(cases_dispo, nb_bmb)
        for c in cases_bombes :
            c.placer_bombe()
    
    
    
    def nombre_bombes_adjacentes (self, i, j) :
        """
        Calcule le nombre de bombes présentent dans les cases adjacentes à celle dont on fournis les coordonnées.
        """
        nb = 0
        adj = self.cases_adjacentes(i, j)
        for c in adj :
            if c.test_bombe() :
                nb += 1
        return nb
    
    
    
    def placer_chiffres (self) :
        """
        Place les chiffres dans la grille.
        Chaque chiffre représente le nombre de bombes dans les cases adjacentes.
        """
        for i in range(nb_lig) :
            for j in range(nb_col) :
                if self[i, j].valeur() == None :
                    self[i, j] = self.nombre_bombes_adjacentes(i, j)
    
    
    
    def initialisation (self, i=None, j=None) :
        """
        Initialise une grille (place les bombes et les chiffres).
        version temporaire.
        1ere case choisie aléatoirement !
        """
        if i == None :
            i=randint(0,8)
        if j == None :
            j=randint(0,8)
        print(i, j)
        self.placer_bombes(i, j)
        self.placer_chiffres()
    
    
    
    def test_defaite (self) :
        """
        Teste si la grille représente une défaite.
        """
        for i in range(nb_lig) :
            for j in range(nb_col) :
                if self[i, j].test_bombe() and self[i, j].est_ouverte() :
                    return True
        return False
    
    
    
    def test_victoire (self) :
        """
        Teste si la grille représente une victoire.
        """
        for i in range(nb_lig) :
            for j in range(nb_col) :
                if self[i, j].test_bombe() and self[i, j].est_ouverte() :
                    return False
                elif not self[i, j].test_bombe() and self[i, j].est_fermee() :
                    return False
        return True
    
    
    
    ## Débugage
    
    
    
    def ouvrir_ligne (self, l) :
        """
        Ouvre toutes les cases de la grille sur la ligne fournie.
        """
        for j in range(nb_col) :
            self[l, j].ouvrir()
    
    
    
    def ouvrir_colonne (self, c) :
        """
        Ouvre toutes les cases de la grille sur la colonne fournie.
        """
        for i in range(nb_lig) :
            self[i, c].ouvrir()
    
    
    
    def ouvrir (self, l=None, c=None) :
        """
        Ouvre toutes les cases de la grille.
        """
        if l == None and  c == None :
            for i in range(nb_lig) :
                for j in range(nb_col) :
                    self[i, j].ouvrir()
        elif l == None :
            self.ouvrir_colonne(c)
        elif c == None :
            self.ouvrir_ligne(l)
        else :
            self[l, c].ouvrir()



## Définition des constantes

"""
Cette section définit des constantes utilisées dans tout le programme. Cela permet de centraliser la définition de certains symboles, messages
et paramètres. Cela permet aussi de pouvoir les modifier facilement selon les besoins.
"""
# paramètres :
nb_lig = 9 # maj ok
nb_col = 9 # maj ok
nb_bmb = 10 # maj ok

# symboles :
symb_cache = '#' # maj ok
symb_detect = 'X' # maj ok # !
symb_supp = '?' # maj ok

symb_bmb = 'B' #  maj ok

# messages :
msg_def = "Game Over : vous avez fait exploser une bombe !" # maj ok
msg_vic = "Bravo : vous avez terminé cette grille." # maj ok

# i, l : lignes, j, c : colonnes



def jeu () :
    """
    Lance une partie de Démineur.
    """
    g = Grille()
    print(g)
    c0, c1 = demander_coord()
    g.initialisation(c0, c1)
    g.ouvrir(c0, c1)
    while not (g.test_victoire() or g.test_defaite()) :
        print(g)
        c0, c1 = demander_coord()
        g.ouvrir(c0, c1)
    print(g) #remplace le return
    if g.test_victoire() :
        print("victoire")
    if g.test_defaite() :
        print("Défaite")
    # return g debuggage



def demander_coord () :
    """
    Demande les coordonnées de la case à ouvrir et les renvoie sous forme de couple d'int.
    """
    print("Coordonnées de la case à ouvrir ?")
    l = input("ligne : ")
    c = input("colonne : ")
    return (int(l), int(c))



def demander_action () :
    """
    Demande le code de l'action et le renvoie sous forme d'int.
    """
    print("Codes action : {ouvrir : 0 / marquer : marque / retirer : 1}")
    act = input("action : ")
    return act



## génération de la grille solution

"""
Cette section permet de générer une grille solution. C'est une grille de jeu dont toutes les cases sont ouvertes.
On peut fournir les coordonnées d'une case qui ne contiendra pas de bombe et qui ne verra aucune bombe dans son voisinage, lors de la création.
"""
"""
def generation_grille (symb = None) :
    
    Génère une grille de taille nb_lig x nb_col, remplie par le symbole fournit en paramètre (None par défaut).
    
    Paramètres : symb : symbole de remplissage de la grille.
    Valeur de retour : grille remplie.
    
    return [[symb for j in range(nb_col)] for i in range(nb_lig)]
"""

"""
def cases_adj (l, c) :
    
    Calcule les coordonnées des cases adjacentes à la case fournie en paramètre.
    
    Arguments : l : un numéro de ligne / c : un numéro de colonne.
    Valeur de retour : liste des coordonnées des cases adjacentes.
    
    cases = []
    if l+1 < nb_lig :
        cases.append((l+1, c))
        if c+1 < nb_col :
            cases.append((l+1, c+1))
        if c-1 >= 0 :
            cases.append((l+1, c-1))
    if l-1 >= 0 :
        cases.append((l-1, c))
        if c+1 < nb_col :
            cases.append((l-1, c+1))
        if c-1 >= 0 :
            cases.append((l-1, c-1))
    if c+1 < nb_col :
        cases.append((l, c+1))
    if c-1 >= 0 :
        cases.append((l, c-1))
    return cases
"""

"""
def emplacement_bombe (l = None, c = None) :
    
    Tire au hasard dix cases sur la grille. Les cases sont repérées par leurs coordonnées.
    Les cases tirées représentent des emplacements de bombes.
    On peut optionnellement fournir en paramètre les coordonnées d'une case qui ne contiendra aucune bombe et qui n'aura aucune bombe dans son voisinage.
    
    Arguments : l : numéro de ligne (optionnel) / c : numéro de colonne (optionnel).
    Valeur de retour : liste des dix coordonnées tirées au hasard.
    
    if not(type(l) == int and type(c) == int and l >= 0 and l < nb_lig and c >= 0 and c < nb_col) :
        raise IndexError("Coordonnée de la case à ouvrir erronnées.")
    indices = [(i, j) for i in range(nb_lig) for j in range(nb_col)]
    voisins = cases_adj(l, c)
    indices.remove((l, c))
    for coord in voisins :
        indices.remove(coord)
    indices_bombes = sample(indices, nb_bmb)
    return indices_bombes
"""

"""
def placement_bombe (grille, liste) :
    
    Place des bombes dans la grille aux coordonnées fournies par la liste.
    
    Arguments : grille : une grille / liste : une liste de coordonnées.
    Valeur de retour : aucune.
    
    for coord in liste :
        grille[coord[0]][coord[1]] = symb_bmb
"""

"""
def test_bomb (grille, l, c) :
    
    Teste si une bombe est présente dans la case de la grille aux coordonnées fournies.
    
    Arguments : grille : une grille / l : un numéro de ligne / c : un numéro de colonne.
    Valeur de retour : renvoie 1 si la case (l, c) de grille contient une bombe, 0 sinon.
    
    if grille[l][c] == symb_bmb :
        return 1
    else :
        return 0
"""

"""
def nb_bombes_adj (grille, l, c) :
    
    Calcule le nombre de bombes présentes dans les cases adjacentes à la case fournie en paramètre.
    Une case adjacente est une case qui a un côté ou un coin en commun.
    
    Arguments : grille : une grille / l : un numéro de ligne / c : un numéro de colonne.
    Valeur de retour : nombre de bombes dans les cases adjacentes.
    
    cpt = 0
    voisins = cases_adj(l, c)
    for coord in voisins :
        cpt += test_bomb(grille, coord[0], coord[1])
    return cpt
"""

"""
def placement_chiffre (grille) :
    
    Place dans chaque case de la grille fournie le nombre de bombes présentes dans les cases adjacentes.
    Ne fais rien si une bombe est déjà placée dans la case.
    
    Arguments : grille : une grille (on attend que les bombes soient déjà placées dans cette grille).
    Valeur de retour : aucune.
    
    for i in range(nb_lig) :
        for j in range(nb_col) :
            if grille[i][j] == None :
                grille[i][j] = str(nb_bombes_adj(grille, i, j))
"""

"""
def generation_grille_decouverte (l = None, c = None) :
    
    Génère une grille solution complète (remplie avec 10 bombes et le nombre de bombes adjacentes dans les cases qui restent).
    La grille générée ne possède pas de bombe aux coordonnées (optionnelles) fournies, ni dans les cases adjacentes.
    
    Arguments : l : numéro de ligne (optionnel) / c : numéro de colonne (optionnel).
    Valeur de retour : la grille solution remplie.
    
    grille = generation_grille()
    indices_bombes = emplacement_bombe(l, c)
    placement_bombe(grille, indices_bombes)
    placement_chiffre(grille)
    return grille
"""




## affichage

"""
Cette section permet d'afficher une grille en mode console.
"""
"""
def affichage_tirets () :
    
    Affiche une ligne de tirets dans la console.
    
    Arguments : aucun.
    Valeur de retour : aucune.
    
    for j in range(nb_col) :
        print('----', end='')
    print('-')
"""

"""
def affichage_ligne (grille, i) :
    
    Affiche une ligne d'une grille dans la console.
    
    Arguments : grille : la grille dont on veut afficher une ligne / i : le numéro de la ligne à afficher.
    Valeur de retour : aucune.
    
    print('|', end=' ')
    for j in range(nb_col) :
        print(str(grille[i][j]), end=' | ')
    print()
"""

"""
def affichage_nb_bombe (grille) :
    
    Affiche un message précisant le nombre de marques "bombe" placées dans la grille.
    
    Arguments : grille : une grille de jeu.
    Valeur de retour : aucune.
    
    print("Nombre de bombes détectées : ", calcul_nb_marques_bombe(grille), "/", nb_bmb, ".")
"""

"""
def affichage (grille) :
    
    Affiche une grille de jeu dans la console.
    La grille de jeu est munie de coordonnées sur la ligne du haut et la colonne de gauche.
    Affiche à la suite le nombre de bombes placées / à trouver.
    
    Arguments : grille : la grille à afficher.
    Valeur de retour : aucune.
    
    print('  |', end=' ')
    for j in range(nb_col) :
        print(j+1, end=' | ')
    print()
    print('-', end='-')
    affichage_tirets()
    for i in range(nb_lig) :
        print(i+1, end=' ')
        affichage_ligne(grille, i)
        print('-', end='-')
        affichage_tirets()
    affichage_nb_bombe(grille)
    print()
"""


## tour de jeu

"""
Cette section permet de gérer un tour de jeu.
Un tour de jeu consiste à cibler une case, choisir une action et effectuer cette action.
"""
"""
def demander_coord () :
    
    Demande les coordonnées d'une case à l'utilisateur (tant qu'il n'a pas fournit des coordonnées correctes).
    
    Arguments : aucun.
    Valeur de retour : couple de coordonnées (dans le type int).
    
    print("Coordonnées de la case ;")
    (l, c) = ('', '')
    while not (l.isdigit() and int(l) >= 1 and int(l) <= nb_lig) :
        l = input("ligne : ")
    while not (c.isdigit() and int(c) >= 1 and int(c) <= nb_col) :
        c = input("colonne : ")
    return (int(l) - 1, int(c) - 1)
"""

"""
def demander_action () :
    
    Demande une action à effectuer à l'utilisateur (tant que le format fournit n'est pas adéquat).
    
    Arguments : aucun.
    Valeur de retour : numéro de l'action à effectuer (type int).
    
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
"""

"""
def action (grille, solution, l, c, act) :
    
    Effectue une action (fournie sous forme de numéro) sur une case donnée.
    En cas d'ouverture d'une case qui contient '0', les cases adjacentes sont automatiquement ouvertes (et ainsi de suite, si elles contiennent '0').
    
    Arguments : grille : une grille de jeu / solution : la grille solution associée / l : un numéro de ligne / c : un numéro de colonne / act : un numéro d'action.
    Valeur de retour : False si l'action consiste en l'ouverture d'une case munie d'une bombe, True sinon.
    
    if act == 0 and grille[l][c] != symb_detect :
        grille[l][c] = solution[l][c]
        if solution[l][c] == symb_bmb :
            return False
        elif grille[l][c] == '0' :
            zero_extension(grille, solution, l, c)     #/!\ boucle infinie
    elif act == 1 and not grille[l][c].isdigit() :
        grille[l][c] = symb_detect
    elif act == 2 and not grille[l][c].isdigit() :
        grille[l][c] = symb_supp
    elif act == 3 and grille[l][c] == symb_detect :
        grille[l][c] = symb_cache
    elif act == 4 and grille[l][c] == symb_supp :
        grille[l][c] = symb_cache
    return True
"""
# tour(g,s)
"""
def zero_extension (grille, solution, li, col) :
    
    Ouvre les cases adjacentes à la case fournie en argument, qui ne sont pas marquées par une bombe ou déjà ouvertes.
    
    Arguments : grille : une grille de jeu / solution : la grille solution associée / li : un numéro de ligne / col : un numéro de colonne.
    Valeur de retour : aucune.
    
    cases = cases_adj(li, col)
    for c in cases :
        if grille[c[0]][c[1]] == symb_cache or grille[c[0]][c[1]] == symb_supp:
            action(grille, solution, c[0], c[1], 0)
"""

"""
def tour (grille, solution) :
    
    Effectue un "tour de jeu", ce qui correspond à :
    _ afficher la grille de jeu ;
    _ demander des coordonnées pour cibler une case précise ;
    _ demander une action à effectuer dans cette case sous forme de numéro ;
    _ effectuer cette action.
    
    Arguments : grille : une grille de jeu / solution : la grille solution associée.
    Valeur de retour : False si une bombe a été découverte durant l'action, True sinon.
    
    affichage(grille)
    (l, c) = demander_coord()
    act = demander_action()
    resultat = action(grille, solution, l, c, act)
    return resultat
"""


## menu de jeu

"""
Cette section gère le coeur du jeu. Elle utilise toutes les autres sections pour générer une partie de jeu complète.
"""
"""
def tour_init(grille) :
    
    Effectue le premier tour de jeu.
    Le premier tour du jeu consiste à afficher la grille, cibler une case et une action, et effectuer la première action du jeu (en fonction de l'action demandée).
    
    Arguments : grille : une grille de jeu.
    Valeur de retour : coordonnées de la case en cas de demande d'ouverture (sur une case ouvrable), None sinon.
    
    affichage(grille)
    (l, c) = demander_coord()
    act = demander_action()
    resultat = action_init(grille, l, c, act)
    return resultat
"""

"""
def action_init (grille, l, c, act) :
    
    Effectue la première action du jeu.
    Si c'est une ouverture de case (et que la case est ouvrable), retransmet les coordonnées de la case cible. Sinon (l'action demandée est un ajout / suppression de marque ou la case contient une marque "bombe"), effectue cette action si possible.
    
    Arguments : grille : une grille de jeu (vierge car la grille solution associée n'a pas encore été générée) / l : un numéro de ligne / c : un numéro de colonne / act : un numéro d'action à effectuer.
    Valeur de retour : coordonnées de la case en cas de demande d'ouverture (sur une case ouvrable), None sinon.
    
    if act == 0 and grille[l][c] != symb_detect :
        return (l, c)
    elif act == 1 :
        grille[l][c] = symb_detect
    elif act == 2 :
        grille[l][c] = symb_supp
    elif act == 3 and grille[l][c] == symb_detect :
        grille[l][c] = symb_cache
    elif act == 4 and grille[l][c] == symb_supp :
        grille[l][c] = symb_cache
    return None
"""

"""
def initialisation () :
    
    Génère la grille de jeu et effectue le premier tour de jeu (potentiellement en boucle) jusqu'à obtenir les coordonnées de la première case à ouvrir (aucune bombe ne sera placé sur cette case ni dans les cases adjacentes).
    Génère la grille solution (en fonction de cette case) et ouvre la première case de la grille de jeu.
    Il est possible de marquer des cases avant l'ouverture de la première case.
    
    Arguments : aucun.
    Valeur de retour : couple grille de jeu et grille solution associée.
    
    grille = generation_grille(symb_cache)
    coord_init = None
    while coord_init == None :
        coord_init = tour_init(grille)
    l = coord_init[0]
    c = coord_init[1]
    solution = generation_grille_decouverte(l, c)
    affichage(solution) # nécessaire au débugage
    action(grille, solution, l, c, 0)
    return grille, solution
"""

"""
def jeu () :
    
    Menu principal du jeu.
    Modélise une partie de jeu :
    _ Initialise la grille de jeu et la grille solution associée.
    _ effectue des "tours de jeu" tant que la partie n'est pas terminée. La boucle prend fin en cas de défaite ou de victoire.
    _ Affiche la grille de jeu en fin de partie.
    _ Redirige vers une défaite ou une victoire en fonction de la sortie de boucle.
    
    Arguments : aucun.
    Valeur de retour : aucune. 
    
    (grille, solution) = initialisation()
    continuer = True
    while continuer and not test_fin(grille, solution):
        continuer = tour(grille, solution)
    affichage(grille)
    if not continuer :
        defaite(grille, solution)
    else :
        victoire()
"""


## Fin de jeu

"""
Cette section gère l'arrêt de la partie et la fin du jeu.
"""


"""
def test_fin (grille, solution) :
    
    Teste si la grille de jeu est complète (victoire). Remplace la fonction "test_fin" car est plus précise que cette dernière.
    La grille est complète si toutes les cases comportant une bombe sont fermées et toutes les autres sont ouvertes.
    
    Arguments : grille : une grille de jeu / solution : la grille solution associée
    Valeur de retour : True si la grille est complète, False sinon.
    
    for i in range(nb_lig) :
        for j in range(nb_col) :
            if not grille[i][j].isdigit() and solution[i][j] != symb_bmb :
                return False
    return True
"""

"""
def maj_bombes (grille, solution) :
    
    Ouvre toutes les cases qui contiennent une bombe pour les mettre en évidence.
    
    Arguments : grille : une grille de jeu / solution : la grille solution associée.
    Valeur de retour : aucune.
    
    for i in range(nb_lig) :
        for j in range(nb_col) :
            if solution[i][j] == symb_bmb and grille[i][j] != symb_detect :
                grille[i][j] = solution[i][j]
"""

"""
def defaite (grille, solution) :
    
    Affiche la grille (avec toutes les bombes mises en valeur) et un message de défaite.
    Améliore et remplace la fonction "defaite".
    
    Arguments : grille : une grille de jeu / solution : la grille solution associée.
    Valeur de retour : aucune.
    
    print(msg_def)
    maj_bombes(grille, solution)
    affichage(grille)
"""

"""
def victoire () :
    
    Affiche le message de victoire.
    
    Arguments : aucun.
    Valeur de retour : aucune.
    
    print(msg_vic)
"""


## Statistiques

"""
Cette section permet d'obtenir des statistiques et des données supplémentaires sur une partie.
"""
"""
def calcul_nb_marques_bombe (grille) :
    
    Calcule le nombre de marques "bombe" qui ont été placées sur la grille.
    
    Arguments : grille : une grille de jeu.
    Valeur de retour : nombre de marques "bombe" présentes sur la grille.
    
    nb = 0
    for i in range(nb_lig) :
        for j in range(nb_col) :
            if grille[i][j] == symb_detect :
                nb +=1
    return nb
"""
