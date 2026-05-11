import pygame
import numpy as np
import os, inspect
import pygame.surfarray as surfarray
 
#recherche du répertoire de travail
scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0)) # compatible interactive Python Shell
scriptDIR  = os.path.dirname(scriptPATH)
assets = os.path.join(scriptDIR,"data")
  
fond = pygame.image.load(os.path.join(assets, "map.png"))
planche_sprites = pygame.image.load(os.path.join(assets, "planche.png"))
planche_sprites.set_colorkey((0,0,0))

LARG = 30
def ChargeSerieSprites(id):
   sprite = []
   for i in range(18):
      spr = planche_sprites.subsurface((LARG * i, LARG * id, LARG,LARG))
      test = spr.get_at((10,10))
      if ( test != (255,0,0,255) ):
         sprite.append( spr )
   return sprite



###################################################################################

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [800, 400]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("LEMMINGS")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# liste des etats
EtatMarche = 'EtatMarche'
EtatChute  = 'EtatChute'
EtatStop   = 'EtatStop'
EtatDead   = 'EtatDead'
EtatCreuse = 'EtatCreuse'
EtatFloater = 'EtatFloater'

# Définition des icônes d'aptitudes (rectangles pour la détection de clic)
aptitudes = {
    'Creuser': pygame.Rect(191, 353, 40, 30),
    'Stopper': pygame.Rect(239, 357, 40, 30),
    'Floater': pygame.Rect(338, 375, 40, 30),
    'Bomber': pygame.Rect(288, 359, 40, 30)
}

# Aptitude sélectionnée
aptitude_selectionnee = None

# liste des lemmins en cours de jeu

lemmingsLIST = []
compteur_creation = 0

# -------- Main Program Loop -----------

marche = ChargeSerieSprites(0)
tombe  = ChargeSerieSprites(2)
mort   = ChargeSerieSprites(10)
stop   = ChargeSerieSprites(4)
creuse = ChargeSerieSprites(9)
parachute = ChargeSerieSprites(3)

# Chargement du sprite de sortie
sortie_sprite_original = pygame.image.load(os.path.join(assets, "sortie.png"))
# Redimensionner la sortie à 40x40 pixels
sortie_sprite = pygame.transform.scale(sortie_sprite_original, (40, 40))

# Position de la porte de sortie (ajustée pour être bien visible et accessible)
sortie_x = 680
sortie_y = 280

pygame.mouse.set_visible(1)

while not done:
    event = pygame.event.Event(pygame.USEREVENT)    # Remise à zero de la variable event

    time = int( pygame.time.get_ticks() / 100 )
    
    # draw background
    screen.blit(fond,(0,0))
    
    # creation des lemmings : 1 lemming toutes les 1,@  5 secondes
    if (  (compteur_creation < 15 ) and ( (time+compteur_creation) % 15 == 0) ):
      compteur_creation += 1
      new_lemming = {}
      new_lemming['x']  = 250
      new_lemming['y']  = 100
      new_lemming['vx'] = -1
      new_lemming['direction'] = -1  # -1 = gauche, +1 = droite
      new_lemming['flipped'] = False  # True = retourné
      new_lemming['etat'] = EtatChute  
      new_lemming['fallcount'] = 0
      new_lemming['Decal'] = np.random.randint(0, len(marche))
      new_lemming['deadcount'] = 0
      new_lemming['creuse_timer'] = 0  # Compteur pour le creusage (toutes les 2s)
      new_lemming['floater_active'] = False  # Le parachute est-il actif?
      lemmingsLIST.append(new_lemming)

    # gestion des évènements
    for event in pygame.event.get():  # User did something
        
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]
            
            # Détection du clic sur les icônes d'aptitudes
            clic_sur_icone = False
            for nom_aptitude, rect_aptitude in aptitudes.items():
                if rect_aptitude.collidepoint(x, y):
                    aptitude_selectionnee = nom_aptitude
                    clic_sur_icone = True
                    print(f"Aptitude sélectionnée: {nom_aptitude}")
                    break
            
            # Si clic en dehors des icônes
            if not clic_sur_icone:
                # Vérifier si on a cliqué sur un lemming
                lemming_clique = None
                for onelemming in lemmingsLIST:
                    # Hitbox du lemming (30x30 pixels)
                    if (onelemming['x'] <= x <= onelemming['x'] + 30 and 
                        onelemming['y'] <= y <= onelemming['y'] + 30):
                        lemming_clique = onelemming
                        break
                
                # Appliquer l'aptitude au lemming cliqué
                if lemming_clique:
                    if aptitude_selectionnee == 'Stopper':
                        # Blocker : ne fonctionne que sur les lemmings en marche
                        if lemming_clique['etat'] == EtatMarche:
                            lemming_clique['etat'] = EtatStop
                            print("Lemming bloqué!")
                    elif aptitude_selectionnee == 'Creuser':
                        # Creuser : ne fonctionne que sur les lemmings en marche
                        if lemming_clique['etat'] == EtatMarche:
                            lemming_clique['etat'] = EtatCreuse
                            print("Lemming creuse!")
                    elif aptitude_selectionnee == 'Floater':
                        # Floater : active le parachute pour ce lemming
                        lemming_clique['floater_active'] = True
                        print("Parachute activé!")
                else:
                    pygame.draw.line(screen, (255,255,255),(x-5,y),(x+5,y))
                    pygame.draw.line(screen, (255,255,255),(x,y-5),(x,y+5))
                    print("Click - Grid coordinates: ", x, y)
            
    # ETAPE 1 : gestion des transitions
    for onelemming in lemmingsLIST:
        if ( onelemming['etat'] == EtatChute ):
            # Vérifier 3 points en dessous du sprite pour détecter une collision
            points_check = [
                (onelemming['x'] + 10, onelemming['y'] + 30),
                (onelemming['x'] + 15, onelemming['y'] + 30),
                (onelemming['x'] + 20, onelemming['y'] + 30)
            ]
            
            collision_detected = False
            for x_check, y_check in points_check:
                if 0 <= x_check < WINDOW_SIZE[0] and 0 <= y_check < WINDOW_SIZE[1]:
                    couleur = screen.get_at((int(x_check), int(y_check)))
                    if couleur[:3] != (0, 0, 0):
                        collision_detected = True
                        break
            
            if collision_detected:
                # Si le lemming a le floater actif, il ne prend pas de dégâts
                if onelemming['floater_active']:
                    onelemming['etat'] = EtatMarche
                    onelemming['floater_active'] = False  # Désactiver le floater
                    print("Lemming atterri avec parachute!")
                # Si le lemming a chuté d'une hauteur mortelle
                elif onelemming['fallcount'] > 160:
                    onelemming['etat'] = EtatDead
                else:
                    onelemming['etat'] = EtatMarche
        
        # Transition vers Chute si le lemming marche et il y a du noir en dessous
        if ( onelemming['etat'] == EtatMarche ):
            # Vérifier 3 points en dessous du sprite
            points_check = [
                (onelemming['x'] + 10, onelemming['y'] + 30),
                (onelemming['x'] + 15, onelemming['y'] + 30),
                (onelemming['x'] + 20, onelemming['y'] + 30)
            ]
            
            no_support = True
            for x_check, y_check in points_check:
                if 0 <= x_check < WINDOW_SIZE[0] and 0 <= y_check < WINDOW_SIZE[1]:
                    couleur = screen.get_at((int(x_check), int(y_check)))
                    if couleur[:3] != (0, 0, 0):
                        no_support = False
                        break
            
            if no_support:
                onelemming['etat'] = EtatChute
                onelemming['fallcount'] = 0
            
            # Vérifier collision avec mur devant
            direction = onelemming['direction']
            # Points à vérifier devant le lemming
            wall_check_x = onelemming['x'] + (direction * 3)
            wall_check_points = [
                (wall_check_x, onelemming['y'] + 5),
                (wall_check_x, onelemming['y'] + 15),
                (wall_check_x, onelemming['y'] + 25)
            ]
            
            collision_mur = False
            for x_check, y_check in wall_check_points:
                if 0 <= x_check < WINDOW_SIZE[0] and 0 <= y_check < WINDOW_SIZE[1]:
                    couleur = screen.get_at((int(x_check), int(y_check)))
                    if couleur[:3] != (0, 0, 0):
                        collision_mur = True
                        break
            
            # Si collision avec mur, inverse la direction et le sprite
            if collision_mur:
                onelemming['direction'] *= -1
                onelemming['flipped'] = not onelemming['flipped']
            
            # Détection de collision avec un autre lemming STOP
            for other_lemming in lemmingsLIST:
                if other_lemming != onelemming and other_lemming['etat'] == EtatStop:
                    # Calcule la distance entre les lemmings
                    dx = other_lemming['x'] - onelemming['x']
                    dy = other_lemming['y'] - onelemming['y']
                    distance = (dx**2 + dy**2)**0.5
                    
                    # Si collision (distance < 30 pixels, taille du sprite)
                    if distance < 30:
                        # Change de direction
                        onelemming['direction'] *= -1
                        onelemming['flipped'] = not onelemming['flipped']
                        break
        
        # Transition de Creuse vers Marche quand le sol est dégagé
        if ( onelemming['etat'] == EtatCreuse ):
            # Vérifier 3 points en dessous du sprite
            points_check = [
                (onelemming['x'] + 10, onelemming['y'] + 30),
                (onelemming['x'] + 15, onelemming['y'] + 30),
                (onelemming['x'] + 20, onelemming['y'] + 30)
            ]
            
            no_support = True
            for x_check, y_check in points_check:
                if 0 <= x_check < WINDOW_SIZE[0] and 0 <= y_check < WINDOW_SIZE[1]:
                    couleur = screen.get_at((int(x_check), int(y_check)))
                    if couleur[:3] != (0, 0, 0):
                        no_support = False
                        break
            
            # Si le sol est dégagé, retourne à Marche
            if no_support:
                onelemming['etat'] = EtatMarche

    # ETAPE 2 : gestion des actions

    for onelemming in lemmingsLIST:
        if ( onelemming['etat'] == EtatChute ):
            # Si le floater est actif, le lemming descend lentement (1 pixel/frame)
            if onelemming['floater_active']:
                onelemming['y'] += 1
                onelemming['fallcount'] += 1
            else:
                onelemming['y'] += 3
                onelemming['fallcount'] += 3
        if ( onelemming['etat'] == EtatDead ):
            onelemming['deadcount'] += 1
            # Si l'animation est terminée, supprime le lemming
            if onelemming['deadcount'] > len(mort):
                lemmingsLIST.remove(onelemming)   
        if ( onelemming['etat'] == EtatMarche ):
            onelemming['x'] += onelemming['direction'] * 3
        if ( onelemming['etat'] == EtatCreuse ):
            # Creuser : creuse le terrain toutes les 2 secondes (20 ticks)
            onelemming['creuse_timer'] += 1
            if onelemming['creuse_timer'] >= 20:
                onelemming['creuse_timer'] = 0
                # Creuse 20 pixels en dessous du lemming
                for px in range(20):
                    fond.set_at((int(onelemming['x']) + px - 10, int(onelemming['y']) + 30), (0, 0, 0))
                # Descend le lemming après avoir creusé
                onelemming['y'] += 1
    
    # Détection de collision avec la porte de sortie
    lemmings_a_supprimer = []
    for onelemming in lemmingsLIST:
        # Centre du lemming
        lemming_center_x = onelemming['x'] + LARG / 2
        lemming_center_y = onelemming['y'] + LARG / 2
        
        # Centre de la porte de sortie
        sortie_center_x = sortie_x + sortie_sprite.get_width() / 2
        sortie_center_y = sortie_y + sortie_sprite.get_height() / 2
        
        # Distance entre les centres
        dx = lemming_center_x - sortie_center_x
        dy = lemming_center_y - sortie_center_y
        distance = (dx**2 + dy**2)**0.5
        
        # Si le lemming est proche du centre de la porte (distance < 25 pixels)
        if distance < 25:
            lemmings_a_supprimer.append(onelemming)
            print("Lemming sauvé!")
    
    # Supprimer les lemmings qui sont sortis
    for lemming in lemmings_a_supprimer:
        lemmingsLIST.remove(lemming)
    
    # ETAPE 3 : affichage des lemmings
    
    # Afficher la porte de sortie en arrière-plan
    screen.blit(sortie_sprite, (sortie_x, sortie_y))
    
    for onelemming in lemmingsLIST:
        xx = onelemming['x']
        yy = onelemming['y']
        state = onelemming['etat']      
        
        if ( state == EtatChute ):
            # Si le floater est actif, affiche le sprite du parachute
            if onelemming['floater_active']:
                if len(parachute) > 0:
                    sprite = parachute[time % len(parachute)]
                    if onelemming['flipped']:
                        sprite = pygame.transform.flip(sprite, True, False)
                    screen.blit(sprite,(xx,yy))
            else:
                screen.blit(tombe[time%len(tombe)],(xx,yy))
        if ( state == EtatMarche ):
            decal = onelemming['Decal']
            sprite_index = (time + decal) % len(marche)
            sprite = marche[sprite_index]
            # Retourne le sprite si flipped
            if onelemming['flipped']:
                sprite = pygame.transform.flip(sprite, True, False)
            screen.blit(sprite,(xx,yy))
        if ( state == EtatDead ):
            # animation Dead
            dead_frame = min(onelemming['deadcount'] - 1, len(mort) - 1)
            if dead_frame >= 0 and dead_frame < len(mort):
                screen.blit(mort[dead_frame],(xx,yy))
        if ( state == EtatStop ):
            # Affiche le sprite de blocage (première frame)
            if len(stop) > 0:
                sprite = stop[0]
                if onelemming['flipped']:
                    sprite = pygame.transform.flip(sprite, True, False)
                screen.blit(sprite,(xx,yy))
        if ( state == EtatCreuse ):
            # Affiche le sprite de creusage (animation)
            if len(creuse) > 0:
                sprite_index = time % len(creuse)
                sprite = creuse[sprite_index]
                if onelemming['flipped']:
                    sprite = pygame.transform.flip(sprite, True, False)
                screen.blit(sprite,(xx,yy))
    
    # ETAPE 4 : affichage des lampes d'aptitudes
    lamp_size = 8
    lamp_y_fixed = 335  # Hauteur fixe pour aligner toutes les lampes
    for nom_aptitude, rect_aptitude in aptitudes.items():
        # Position de la lampe : au-dessus de l'icône, à hauteur fixe
        lamp_x = rect_aptitude.centerx
        
        # Couleur : rouge/orange si sélectionnée, gris si inactive
        if aptitude_selectionnee == nom_aptitude:
            couleur_lampe = (255, 165, 0)  # Orange/jaune
        else:
            couleur_lampe = (100, 100, 100)  # Gris
        
        # Dessiner la lampe (cercle)
        pygame.draw.circle(screen, couleur_lampe, (lamp_x, lamp_y_fixed), lamp_size)
        pygame.draw.circle(screen, (200, 200, 200), (lamp_x, lamp_y_fixed), lamp_size, 1)  # Bordure

    clock.tick(20)
 
    pygame.display.flip()
 

pygame.quit()