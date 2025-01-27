

# ==========IMPORT MODULES==========
import pygame
import random
import os
import json
import time

#======================Initialisation des paramètres de jeu=================================

#==================================================================================


pygame.mixer.init()


MOTS_FICHIER = "mots.txt"
fichier_son_defaite=pygame.mixer.Sound('sons/defaite.wav')
fichier_son_victoire=pygame.mixer.Sound('sons/victoire.wav')
fichier_son_corde=pygame.mixer.Sound('sons/corde.mp3')
# ==========(Bonus)Sons : Chargement des bruits d'ambiance==========
def son_defaite():
    pygame.mixer.Sound.play(fichier_son_defaite)

def son_victoire():
    pygame.mixer.Sound.play(fichier_son_victoire)

def son_corde():
    pygame.mixer.Sound.play(fichier_son_corde)



# ==========(Bonus)Fichiers locaux : Chargement des mots et des scores==========

# Charger les mots depuis le fichier ou utiliser une liste par défaut
def charger_mots():
    
    # Mots de secours 
    mots_par_defaut = ["python", "programmation", "ordinateur", "developpement", "jeu", "pendu", "algorithme","neurone","ingenieur","github","synchronisation","education","plateforme","lunettes","football","cheveux"]
    if not os.path.exists(MOTS_FICHIER):
        with open(MOTS_FICHIER, "w") as f:
            f.write("\n".join(mots_par_defaut) + "\n")


    with open(MOTS_FICHIER, "r") as f:
        mots = f.read().splitlines()

    # Si le fichier est vide, utiliser les mots par défaut
    if not mots or len(mots) < len(mots_par_defaut):
        mots = mots_par_defaut
        with open(MOTS_FICHIER, "w") as f:
            f.write("\n".join(mots_par_defaut) + "\n")
    return mots


# CHOIX MOT ALEATOIRE

def choisir_mot():
    mots = charger_mots()
    return random.choice(mots)
#=======================================================================
# =======  Initialiser l'Ecran avec Pygame  =========
pygame.init()

# Dimensions fenêtre et couleurs et ecritures
WIDTH, HEIGHT = 800, 800  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT = pygame.font.Font(None, 40) #ce qui va etre écrit 

#=========
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #écran va apparaitre sur fenetre
pygame.display.set_caption("Jeu du Pendu")
#=====================================================


#=========  Grande fonction afficher_texte qui permet a chaque "fenetres" d'afficher sa particularité =============
def afficher_texte(texte, x, y, couleur=BLACK):
    texte_render = FONT.render(texte, True, couleur) 
    screen.blit(texte_render, (x, y))   # liée a la ligne 290 , screen = pygame.display.set_mode
#===================================================================================================================


#=========Affichage du pendu=============

def dessiner_pendu(essais_restants):
    base_x, base_y = WIDTH // 2, HEIGHT // 2 + 100
    couleur = BLACK
    epaisseur = 5

    # Dessiner la structure de base du pendu
    if essais_restants <= 9:
        pygame.draw.line(screen, couleur, (base_x - 100, base_y), (base_x + 100, base_y), epaisseur)  # Base
    if essais_restants <= 8:    
        pygame.draw.line(screen, couleur, (base_x - 50, base_y), (base_x - 50, base_y - 200), epaisseur)  # Pilier vertical
    if essais_restants <= 7:      
        pygame.draw.line(screen, couleur, (base_x - 50, base_y - 200), (base_x + 50, base_y - 200), epaisseur)  # Barre horizontale
    if essais_restants <= 6: 
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

# =============================================================================================

        



#======================Menu Mots =================================
def menu_mots():
    clock = pygame.time.Clock()
    mots = charger_mots()
    mots_par_page = 10
    page_actuel = 0
    page_total = (len(mots) + mots_par_page - 1) // mots_par_page
    while True:
        index_debut = page_actuel * mots_par_page
        index_fin = index_debut + mots_par_page
        screen.fill(WHITE)
        afficher_texte("Mots:", WIDTH // 2 - 50, 50)
        for i, mot in enumerate(mots[index_debut:index_fin]):
            afficher_texte(mot, 50, 100 + i * 40)
        afficher_texte("Appuyez sur Echap pour revenir au menu", 50, HEIGHT - 50, RED)
        afficher_texte("Appuyez sur A pour ajouter un mot", 50, HEIGHT - 150, RED)
        afficher_texte("Appuyez sur E pour effacer les mots", 50, HEIGHT - 100, RED)
        afficher_texte(f"Page {page_actuel + 1}/{page_total}", WIDTH // 2 - 50, HEIGHT - 200)
        afficher_texte(f"Page suivante: S / Page précédente: P", WIDTH // 2 - 200, HEIGHT - 250, RED)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_e:
                    effacer_mots()
                    afficher_texte("Mots effacés!", WIDTH // 2 - 100, HEIGHT // 2, RED)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    return
                if event.key == pygame.K_a:
                    ajouter_mot_interface()
                    return
                if event.key == pygame.K_p:
                    if page_actuel > 0:
                        page_actuel -= 1
                if event.key == pygame.K_s:
                    if index_fin < len(mots):
                        page_actuel += 1

        clock.tick(30)
#==================================================================================

#==================== (Bonus) Ajouter un mot ======================================
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
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_RETURN:
                    ajouter_mot(mot)
                    return
                elif event.key == pygame.K_BACKSPACE:
                    mot = mot[:-1]
                else:
                    mot += event.unicode.lower()


        clock.tick(30)

def ajouter_mot(mot):
    with open(MOTS_FICHIER, "a") as f:
        f.write(f"{mot}\n")
        
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
#==================================================================================




#==================== (Bonus) Effacer tous les mots enregistrées ===========================
def effacer_mots():
    with open(MOTS_FICHIER, "w") as f:
        f.write("")  # Réinitialise le fichier en l'effaçant

#==================================================================================
    


SCORES_FICHIER = "scores.json"
#======================Menu Scores =================================
def menu_scores():
    clock = pygame.time.Clock()
    scores = voir_scores()
    page_actuel = 0
    joueurs_par_page = 2
    page_total = (len(scores) + joueurs_par_page - 1) // joueurs_par_page
    while True:
        screen.fill(WHITE)
        afficher_texte("Scores:", WIDTH // 2 - 50, 50)
        index_debut = page_actuel * joueurs_par_page
        index_fin = index_debut + joueurs_par_page
        axe_y = 100
        joueurs_liste = list(scores.items())[index_debut:index_fin]
        for joueur, difficulte_scores in joueurs_liste:
            afficher_texte(f"Joueur: {joueur}", 50, axe_y)
            axe_y += 40
            for difficulte, joueur_scores in difficulte_scores.items():
                afficher_texte(f"Difficulté: {difficulte}", 70, axe_y)
                axe_y += 40
                if joueur_scores:
                    afficher_texte(f"Meilleur score: {max(joueur_scores)} points", 90, axe_y)
                else:
                    afficher_texte("Aucun score", 90, axe_y)
                axe_y += 40
        afficher_texte(f"Page {page_actuel +1}/{page_total}", WIDTH // 2 +100, HEIGHT - 155, RED)
        afficher_texte("Page suivante: S / Page précédente: P", 50, HEIGHT - 120, RED)
        afficher_texte("Appuyez sur Echap pour revenir au menu", 50, HEIGHT - 50, RED)
        afficher_texte("Appuyez sur E pour effacer les scores et les joueurs", 50, HEIGHT - 85, RED)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_e:
                    effacer_scores_interface()
                    scores = voir_scores()  # Refresh the scores after deletion
                if event.key == pygame.K_p:
                    if page_actuel > 0:
                        page_actuel -= 1
                if event.key == pygame.K_s:
                    if index_fin < len(scores):
                        page_actuel += 1

        clock.tick(30)
#==================================================================================







#======================(Bonus) Gestion des scores =================================
def charger_scores():
    if not os.path.exists(SCORES_FICHIER):
        return {}
    try:
        with open(SCORES_FICHIER, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}
    
def enregistrer_score(joueur, score, difficulte): #enregistrer le score du joueur selon la difficulté
    scores = charger_scores()
    if joueur not in scores:
        scores[joueur] = {"facile": [], "moyen": [], "difficile": []}
    if not scores[joueur][difficulte] or score > max(scores[joueur][difficulte]):
        scores[joueur][difficulte] = [score]  # Replace with the new highest score
    with open(SCORES_FICHIER, "w") as f:
        json.dump(scores, f, indent=4)

def voir_scores():
    return charger_scores()

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
        afficher_texte("Êtes-vous sûr de vouloir effacer tous les scores", 50, 150)
        afficher_texte("et les joueurs ?",50,200)
        afficher_texte("O - Oui / Echap - Non", 50, 250)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:  # Touche 'O' pour con²firmer
                    effacer_scores()
                    afficher_texte("Scores et joueurs effacés!", WIDTH // 2 - 100, HEIGHT // 2, RED)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    return
                elif event.key == pygame.K_ESCAPE:  # Touche 'Echap' pour annuler
                    return

        clock.tick(30)
#=========================================================




#====================== Menu CHOIX DIFFICULTE ============================================

def menu_difficulte(ready,difficulte_actuelle):
    clock = pygame.time.Clock()
    while True:
        screen.fill(WHITE)
        afficher_texte("JEU DU PENDU", WIDTH // 2 - 150, 50) #WIDTH // 2 - 150 sert a centrer le texte
        afficher_texte("Choisissez la difficulté:", WIDTH // 2 - 200, 100)
        afficher_texte("1. Facile", WIDTH // 2 - 100, 200)
        afficher_texte("2. Moyen", WIDTH // 2 - 100, 300)
        afficher_texte("3. Difficile", WIDTH // 2 - 100, 400)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "facile"
                elif event.key == pygame.K_2:
                    return "moyen"
                elif event.key == pygame.K_3:
                    return "difficile"
                if ready==1:
                    if event.key == pygame.K_ESCAPE:
                        return difficulte_actuelle

        clock.tick(30)
#==================================================================================

#====================== Menu JOUEUR ============================================

def menu_joueur(ready, joueur_actuel):
    clock = pygame.time.Clock()
    while True:
        screen.fill(WHITE)
        afficher_texte("Choix du joueur", WIDTH // 2 - 150, 50)
        afficher_texte("1. Joueur existant", WIDTH // 2 - 150, 150)
        afficher_texte("2. Nouveau Joueur", WIDTH // 2 - 150, 250)
        afficher_texte("Appuyez sur Echap pour quitter", WIDTH // 2 - 200, 350)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return menu_joueurexistant()
                elif event.key == pygame.K_2:
                    return menu_joueur_nouveau()
                if ready == 1:
                    if event.key == pygame.K_ESCAPE:
                        return joueur_actuel
        clock.tick(30)


def ajouter_joueur(joueur):
    scores = charger_scores()
    if joueur not in scores:
        scores[joueur] = {"facile":[], "moyen":[], "difficile":[]}  # Ajoute un nouveau joueur avec des scores vides
    with open(SCORES_FICHIER, "w") as f:
        json.dump(scores, f, indent=4)


def menu_joueur_nouveau():
    clock = pygame.time.Clock()
    joueur = ''
    while True:
        screen.fill(WHITE)
        afficher_texte("Ajouter un nom de joueur", WIDTH // 2 - 150, 50)
        afficher_texte("Tapez le nom et appuyez sur Entrée:", 50, 150)
        afficher_texte(joueur, 50, 250)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if joueur:
                        ajouter_joueur(joueur)
                        return joueur
                elif event.key == pygame.K_BACKSPACE:
                    joueur = joueur[:-1]
                else:
                    lettre=event.unicode
                    if lettre.isalpha():
                        joueur +=lettre 
        clock.tick(30)


def menu_joueurexistant():
    clock = pygame.time.Clock()
    joueurs = list(voir_scores().keys())  # Get the list of player names
    if joueurs:
        while True:            
            screen.fill(WHITE)
            afficher_texte("Choix du Joueur", 50, 50)
            for i, joueur in enumerate(joueurs, 1):
                afficher_texte(f"Joueur {i}: {joueur}", 50, 100 + i * 50)
            afficher_texte("Appuyez sur Echap pour revenir au menu", 50, HEIGHT - 50, RED)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        index = event.key - pygame.K_1
                        if index < len(joueurs):
                            return joueurs[index]
                    if event.key == pygame.K_0 and len(joueurs) >= 10:
                        return joueurs[9]
            clock.tick(30)
    else:
        while True:
            screen.fill(WHITE)
            afficher_texte("Aucun joueur trouvé!", WIDTH // 2 - 150, HEIGHT // 2)
            afficher_texte("Redirection vers la création d'un nouveau joueur", 50, HEIGHT - 50, RED)
            pygame.display.flip()
            pygame.time.delay(2000)
            return menu_joueur_nouveau()

#==================================================================================

#====================== Menu principal ============================================
def menu_principal():
    difficulte=menu_difficulte(0,0)
    joueur=menu_joueur(0,0)
    clock = pygame.time.Clock() # pygame.time.Clock sert a 
    while True:
        screen.fill(WHITE) #.fill sert a 
        afficher_texte("JEU DU PENDU", WIDTH // 2 - 100, 80) #WIDTH // 2 - 150 sert a centrer le texte
        afficher_texte("1. Jouer", WIDTH // 2 - 80, 200)
        afficher_texte("2. Menu mots", WIDTH // 2 - 80, 300)
        afficher_texte("3. Menu scores", WIDTH // 2 - 80, 400)
        afficher_texte("4. Choix de difficulté", WIDTH // 2 - 80, 500)
        afficher_texte("5. Choix du joueur", WIDTH // 2 - 80, 600)
        afficher_texte("6. Quitter", WIDTH // 2 - 80, 700)
        
        pygame.display.flip() #pygame 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: 
                    jouer_partie(difficulte, joueur)
                elif event.key == pygame.K_2:
                    menu_mots()
                elif event.key == pygame.K_3:
                    menu_scores()
                elif event.key == pygame.K_4:
                    difficulte = menu_difficulte(1,difficulte)
                elif event.key == pygame.K_5:
                    joueur = menu_joueur(1,joueur)
                elif event.key == pygame.K_6:
                    pygame.quit()
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        clock.tick(30)

#==================================================================================

#===============================  BOUCLE PRINCIPALE  ==============================

def jouer_partie(difficulte, joueur):
    mot = choisir_mot()
    lettres_trouvees = set()
    lettres_tentees = set()
    if difficulte == 'facile':
        essais_restants = 10
        temps_restant = 60
    if difficulte == 'moyen':
        essais_restants = 6
        temps_restant = 30
    if difficulte == 'difficile':
        essais_restants = 3
        temps_restant = 10
    score = 0
    clock = pygame.time.Clock()
    constante_temps = time.time()
#Cachez le mot choisit au hasard 
    def mot_cache():
        return " ".join([lettre if lettre in lettres_trouvees else "_" for lettre in mot])

#Boucle principale
    while True:  
        ecart_temps = time.time()
        if ecart_temps > constante_temps + 1:
            constante_temps+=1
            temps_restant-=1
        screen.fill(WHITE)#fond blanc
        
        # Dessiner le pendu au centre de l'écran
        dessiner_pendu(essais_restants)

        # Afficher les informations textuelles en bas
        afficher_texte("PENDU", WIDTH // 2 - 50, 50)
        afficher_texte("Difficulté: " + difficulte, 50, HEIGHT - 250)
        afficher_texte(f"Joueur: {joueur}", 50, HEIGHT - 300)
        afficher_texte(f"Mot: {mot_cache()}", 50, HEIGHT - 200)
        afficher_texte(f"Essais restants: {essais_restants}", 50, HEIGHT - 150)
        afficher_texte(f"Lettres tentées: {', '.join(sorted(lettres_tentees))}", 50, HEIGHT - 100)       
        afficher_texte(f"{temps_restant}s",600,100)
        pygame.display.flip()
        
        #Boucle de Jeu 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return                
            if event.type == pygame.KEYDOWN: # KEYDOWN detecte la touche
                if event.key == pygame.K_ESCAPE: #si on appuie sur echap, quittes
                    return

                lettre = event.unicode.lower() #event. detecte et réagis 

                if lettre.isalpha() and lettre not in lettres_tentees: 
                #.isalpha verifie que c'est une lettre ; # on verifie que la lettre n'a pas deja était tentée
                    lettres_tentees.add(lettre) #.add ajoute la lettre tentée 

                    if lettre in mot:
                        lettres_trouvees.add(lettre)
                        score += 10  # Augmente le score pour chaque lettre correcte
                    else:
                        essais_restants -= 1
                        son_corde()

        if temps_restant==0:
            essais_restants=0
        #Défaite
        if essais_restants <= 0:
            enregistrer_score(joueur,score, difficulte)
            afficher_texte(f"{'Perdu! Le mot était:'}{mot}", WIDTH // 2 - 200, 200, RED)
            son_defaite()            
        # (Jambe droite affichée lorsque le joueur a perdu)
            base_x, base_y = WIDTH // 2, HEIGHT // 2 + 100
            couleur = BLACK
            epaisseur = 5
            pygame.draw.line(screen, couleur, (base_x + 50, base_y - 50), (base_x + 70, base_y - 20), epaisseur)
            pygame.display.flip()
            pygame.time.delay(2000)
            return
        
        #Victoire
        if all(lettre in lettres_trouvees for lettre in mot):
            score += 50 + temps_restant  # Bonus pour avoir gagné
            enregistrer_score(joueur,score, difficulte)
            afficher_texte(f"{'Gagné! Le mot était:'}{mot}", WIDTH // 2 - 200, 200, RED)
            son_victoire()
            pygame.display.flip()
            pygame.time.delay(2000)

            return
    

        clock.tick(30)

# =============================================================================================









if __name__ == "__main__":
    menu_principal()