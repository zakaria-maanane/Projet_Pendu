
"""Jeu du pendu , 

Structure : 

-Lire les fichiers txt où se trouve les mots (charger_mots)

-Choisir au hasard les mots a jouer puis les cacher pour etre révélé lettre par lettre par le jouer (choisir_mots , jouer_partie,  mot_cache)

-coeur du programme : Attribution d


"""


import pygame
import random
import os


# ==========(Bonus)Fichiers locaux : Chargement des mots et des scores==========
MOTS_FICHIER = "mots.txt"
SCORES_FICHIER = "scores.txt"



# Charger les mots depuis le fichier ou utiliser une liste par défaut
def charger_mots():
    
    # Mots de secours 
    mots_par_defaut = ["python", "programmation", "ordinateur", "developpement", "jeu", "pendu", "algorithme"]
    if not os.path.exists(MOTS_FICHIER):
        with open(MOTS_FICHIER, "w") as f:
            f.write("\n".join(mots_par_defaut) + "\n")


    with open(MOTS_FICHIER, "r") as f:
        mots = f.read().splitlines()

    # Si le fichier est vide, utiliser les mots par défaut
    if not mots:
        mots = mots_par_defaut

    return mots


# CHOIX MOT ALEATOIRE

def choisir_mot():
    mots = charger_mots()
    return random.choice(mots)
#=======================================================================

#===============================  BOUCLE PRINCIPALE  ==============================

def jouer_partie():
    mot = choisir_mot()
    lettres_trouvees = set()
    lettres_tentees = set()
    essais_restants = 6
    score = 0
    clock = pygame.time.Clock()

#Cachez le mot choisit au hasard 
    def mot_cache():
        return " ".join([lettre if lettre in lettres_trouvees else "_" for lettre in mot])

#Boucle principale
    while True:
        screen.fill(WHITE)#fond blanc
        
        # Dessiner le pendu au centre de l'écran
        dessiner_pendu(essais_restants)

        # Afficher les informations textuelles en bas
        afficher_texte("PENDU", WIDTH // 2 - 50, 50)
        afficher_texte(f"Mot: {mot_cache()}", 50, HEIGHT - 200)
        afficher_texte(f"Essais restants: {essais_restants}", 50, HEIGHT - 150)
        afficher_texte(f"Lettres tentées: {', '.join(sorted(lettres_tentees))}", 50, HEIGHT - 100)

        pygame.display.flip()
        
        #Boucle de Jeu 
        for event in pygame.event.get(): # si situiation = au mot 
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN: # KEYDOWN detecte la touche 
                lettre = event.unicode.lower() #event. detecte et réagis 

                if lettre.isalpha() and lettre not in lettres_tentees: 
                #.isalpha verifie que c'est une lettre ; # on verifie que la lettre n'a pas deja était tentée
                    lettres_tentees.add(lettre) #.add ajoute la lettre tentée 

                    if lettre in mot:
                        lettres_trouvees.add(lettre)
                        score += 10  # Augmente le score pour chaque lettre correcte
                    else:
                        essais_restants -= 1

        #La Perte
        if essais_restants <= 0:
            enregistrer_score(score)
            afficher_texte("Perdu!", WIDTH // 2 - 100, HEIGHT // 2, RED)
            pygame.display.flip()
            pygame.time.delay(2000)
        
        # (Jambe droite affichée lorsque le joueur a perdu)
            base_x, base_y = WIDTH // 2, HEIGHT // 2 + 100
            couleur = BLACK
            epaisseur = 5
            pygame.draw.line(screen, couleur, (base_x + 50, base_y - 50), (base_x + 70, base_y - 20), epaisseur)  
           
            return
        
        #La Gagne
        if all(lettre in lettres_trouvees for lettre in mot):
            score += 50  # Bonus pour avoir gagné
            enregistrer_score(score)
            afficher_texte("Gagné!", WIDTH // 2 - 100, HEIGHT // 2, RED)
            pygame.display.flip()
            pygame.time.delay(2000)

            return
    

        clock.tick(30)

      
#==================================================================================





#==================== (Bonus) Ajouter un mot ======================================
def ajouter_mot(mot):
    with open(MOTS_FICHIER, "a") as f:
        f.write(f"{mot}\n")
        

def ajouter_mot_interface():
    clock = pygame.time.Clock()
    mot = ""

    while True:
        screen.fill(WHITE)
        afficher_texte("Ajouter un mot", WIDTH // 2 - 150, 50)
        afficher_texte("Tapez le mot et appuyez sur Entrée:", 50, 150)
        afficher_texte(mot, 50, 250)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ajouter_mot(mot)
                    return
                elif event.key == pygame.K_BACKSPACE:
                    mot = mot[:-1]
                else:
                    mot += event.unicode


        clock.tick(30)

#==================================================================================





#==================== (Bonus) Voir les mots enregistrées ===========================
def voir_mots():
    clock = pygame.time.Clock()
    mots = charger_mots()
    while True:
        screen.fill(WHITE)
        afficher_texte("Liste des mots:", 50, 50)
        for i, mot in enumerate(mots):
            afficher_texte(mot, 50, 100 + i * 40)
        afficher_texte("Appuyez sur Echap pour revenir au menu", 50, HEIGHT - 50, RED)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        clock.tick(30)

        
def effacer_mots():
    with open(MOTS_FICHIER, "w") as f:
        f.write("")  # Réinitialise le fichier en l'effaçant

#==================================================================================






#======================(Bonus) Gestion des scores =================================
def enregistrer_score(score):
    with open(SCORES_FICHIER, "a") as f:
        f.write(f"{score}\n")

def voir_scores():
    if not os.path.exists(SCORES_FICHIER):
        return []
    with open(SCORES_FICHIER, "r") as f:
        return [int(score) for score in f.read().splitlines()]

def afficher_scores():
    clock = pygame.time.Clock()
    scores = voir_scores()
    while True:
        screen.fill(WHITE)
        afficher_texte("Scores:", 50, 50)
        for i, score in enumerate(scores):
            afficher_texte(f"Partie {i + 1}: {score} points", 50, 100 + i * 40)
        afficher_texte("Appuyez sur Echap pour revenir au menu", 50, HEIGHT - 50, RED)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        clock.tick(30)

#==================================================================================

#=============== Effacer Score =========================
def effacer_scores():
    with open(SCORES_FICHIER, "w") as f:
        f.write("")  # Réinitialise le fichier en l'effaçant

def effacer_scores_interface():
    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)
        afficher_texte("Effacer tous les scores", WIDTH // 2 - 150, 50, RED)
        afficher_texte("Êtes-vous sûr de vouloir effacer tous les scores ?", 50, 150)
        afficher_texte("O - Oui / Echap - Non", 50, 250)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:  # Touche 'O' pour confirmer
                    effacer_scores()
                    afficher_texte("Scores effacés!", WIDTH // 2 - 100, HEIGHT // 2, RED)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    return
                elif event.key == pygame.K_ESCAPE:  # Touche 'Echap' pour annuler
                    return

        clock.tick(30)
#=========================================================


#====================== Menu principal ============================================
def menu_principal():
    clock = pygame.time.Clock() # pygame.time.Clock sert a 
    while True:
        screen.fill(WHITE) #.fill sert a 
        afficher_texte("JEU DU PENDU", WIDTH // 2 - 100, 80) #WIDTH // 2 - 150 sert a centrer le texte
        afficher_texte("1. Jouer", WIDTH // 2 - 60, 200)
        afficher_texte("2. Ajouter un mot", WIDTH // 2 - 120, 300)
        afficher_texte("3. Voir les mots", WIDTH // 2 - 110, 400)
        afficher_texte("4. Effacer la liste des mots", WIDTH // 2 - 176, 500)
        afficher_texte("5. Voir les scores", WIDTH // 2 - 120, 600)
        afficher_texte("6.Effacer les scores", WIDTH // 2 - 140, 700) 
        afficher_texte("7. Quitter", WIDTH // 2 - 60, 800)
        
        pygame.display.flip() #pygame 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: 
                    jouer_partie()
                elif event.key == pygame.K_2:
                    ajouter_mot_interface()
                elif event.key == pygame.K_3:
                    voir_mots()
                elif event.key == pygame.K_4:
                    effacer_mots()
                elif event.key == pygame.K_5:
                    afficher_scores()
                elif event.key == pygame.K_6:
                    effacer_scores_interface()
                elif event.key == pygame.K_7:
                    pygame.quit()
                    return

        clock.tick(30)

#==================================================================================














# =======  Initialiser l'Ecran avec Pygame  =========
pygame.init()

# Dimensions fenêtre et couleurs et ecritures
WIDTH, HEIGHT = 1000, 900  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT = pygame.font.Font(None, 40) #se qui va etre écrit 

#=========
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #écrant va apparaitre sur fenetre
pygame.display.set_caption("Jeu du Pendu")
#=====================================================


#=========  Grande fonction afficher_texte qui permet a chaque "fenetres" d'afficher sa particularité =============
def afficher_texte(texte, x, y, couleur=BLACK):
    texte_render = FONT.render(texte, True, couleur) 
    screen.blit(texte_render, (x, y))   # liée a la ligne 290 , screen = pygame.display.set_mode
#===================================================================================================================
"""Ici toutes nos afficher_texte  """


def dessiner_pendu(essais_restants):
    base_x, base_y = WIDTH // 2, HEIGHT // 2 + 100
    couleur = BLACK
    epaisseur = 5

    # Dessiner la structure de base (toujours visible)
    pygame.draw.line(screen, couleur, (base_x - 100, base_y), (base_x + 100, base_y), epaisseur)  # Base
    pygame.draw.line(screen, couleur, (base_x - 50, base_y), (base_x - 50, base_y - 200), epaisseur)  # Pilier vertical
    pygame.draw.line(screen, couleur, (base_x - 50, base_y - 200), (base_x + 50, base_y - 200), epaisseur)  # Barre horizontale
    pygame.draw.line(screen, couleur, (base_x + 50, base_y - 200), (base_x + 50, base_y - 150), epaisseur)  # Corde

    # Dessiner les éléments selon les essais restants
    if essais_restants <= 5:  # Tête
        pygame.draw.circle(screen, couleur, (base_x + 50, base_y - 130), 20, epaisseur)
    if essais_restants <= 4:  # Corps
        pygame.draw.line(screen, couleur, (base_x + 50, base_y - 110), (base_x + 50, base_y - 50), epaisseur)
    if essais_restants <= 3:  # Bras gauche
        pygame.draw.line(screen, couleur, (base_x + 50, base_y - 100), (base_x + 30, base_y - 70), epaisseur)
    if essais_restants <= 2:  # Bras droit
        pygame.draw.line(screen, couleur, (base_x + 50, base_y - 100), (base_x + 70, base_y - 70), epaisseur)
    if essais_restants <= 1:  # Jambe gauche
        pygame.draw.line(screen, couleur, (base_x + 50, base_y - 50), (base_x + 30, base_y - 20), epaisseur)
    if essais_restants <= 0:  # Jambe droite
        pygame.draw.line(screen, couleur, (base_x + 50, base_y - 50), (base_x + 70, base_y - 20), epaisseur)






if __name__ == "__main__":
    menu_principal()
