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
EtatClimber = 'EtatClimber'
EtatBasher = 'EtatBasher'

# Définition des icônes d'aptitudes (rectangles pour la détection de clic)
aptitudes = {
    'Stopper': pygame.Rect(190, 359, 40, 30),
    'Creuser': pygame.Rect(546, 376, 40, 30),
    'Floater': pygame.Rect(338, 375, 40, 30),
    'Climber': pygame.Rect(288, 359, 40, 30),
    'Basher': pygame.Rect(481, 357, 40, 30)
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
climber = ChargeSerieSprites(8)
basher = ChargeSerieSprites(6)

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
        new_lemming['climber_active'] = False  # Le grimpeur est-il actif?
        new_lemming['basher_timer'] = 0  # Compteur pour le basher
        new_lemming['basher_pending'] = False  # Basher sélectionné mais pas encore contre un mur
        new_lemming['basher_started'] = False  # Le basher a réellement commencé à creuser
        new_lemming['basher_exit_cooldown'] = 0  # Evite le rebond juste après un tunnel
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
                        if lemming_clique['etat'] == EtatMarche:
                            lemming_clique['etat'] = EtatStop
                            print("Lemming bloqué!")
                    elif aptitude_selectionnee == 'Creuser':
                        if lemming_clique['etat'] == EtatMarche:
                            lemming_clique['etat'] = EtatCreuse
                            print("Lemming creuse!")
                    elif aptitude_selectionnee == 'Floater':
                        lemming_clique['floater_active'] = True
                        print("Parachute activé!")
                    elif aptitude_selectionnee == 'Climber':
                        lemming_clique['climber_active'] = True
                        print("Grimpeur activé!")
                    elif aptitude_selectionnee == 'Basher':
                        if lemming_clique['etat'] == EtatMarche:
                            # On arme le basher: il démarrera seulement quand le lemming touche un mur
                            lemming_clique['basher_pending'] = True
                            lemming_clique['basher_started'] = False
                            lemming_clique['basher_timer'] = 0
                            print("Lemming bash!")
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
                    couleur = fond.get_at((int(x_check), int(y_check)))
                    if couleur[:3] != (0, 0, 0):
                        collision_mur = True
                        break
            
            # Si collision avec mur, inverse la direction et le sprite
            if collision_mur:
                # Vérifier si le lemming est dans un tunnel (noir sous les pieds)
                # Si c'est le cas, ignorer la collision mur
                in_tunnel = False
                tunnel_check_points = [
                    (int(onelemming['x']) + 10, int(onelemming['y']) + 30),
                    (int(onelemming['x']) + 15, int(onelemming['y']) + 30),
                    (int(onelemming['x']) + 20, int(onelemming['y']) + 30)
                ]
                for tx, ty in tunnel_check_points:
                    if 0 <= tx < WINDOW_SIZE[0] and 0 <= ty < WINDOW_SIZE[1]:
                        couleur = fond.get_at((tx, ty))
                        if couleur[:3] == (0, 0, 0):
                            in_tunnel = True
                            break
                
                # Si on est dans un tunnel, ignorer la collision mur (continuer tout droit)
                if in_tunnel:
                    pass  # Ignore la collision, on continue
                # Si on est en Basher, on ignore la collision (on creuse le mur!)
                elif onelemming['etat'] == EtatBasher:
                    pass  # Ignore la collision, on continue à creuser
                # Si le basher est "armé" et qu'on touche un mur en marchant, on démarre le basher
                elif onelemming.get('basher_pending', False):
                    onelemming['etat'] = EtatBasher
                    onelemming['basher_started'] = True
                    onelemming['basher_pending'] = False
                    onelemming['basher_timer'] = 0
                    onelemming['basher_exit_cooldown'] = 0
                elif onelemming['climber_active']:
                    # Si le climber est actif, le lemming grimpe au lieu de changer de direction
                    onelemming['etat'] = EtatClimber
                    print("Lemming grimpe le mur!")
                else:
                    # Si on vient juste de finir un basher, on évite un rebond instantané
                    # (sinon ça donne un aller-retour sur place)
                    if onelemming.get('basher_exit_cooldown', 0) > 0:
                        pass
                    else:
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
        
        # Transition de Climber vers Marche quand il n'y a plus de mur
        if ( onelemming['etat'] == EtatClimber ):
            # Vérifier si le mur continue AU-DESSUS ET sur le CÔTÉ du lemming
            direction = onelemming['direction']
            wall_check_x = onelemming['x'] + (direction * 3)
            # Points à vérifier au-dessus du lemming
            wall_check_points = [
                (wall_check_x, onelemming['y'] - 15),
                (wall_check_x, onelemming['y'] - 10),
                (wall_check_x, onelemming['y'] - 5)
            ]
            
            collision_mur_climb = False
            for x_check, y_check in wall_check_points:
                if 0 <= x_check < WINDOW_SIZE[0] and 0 <= y_check < WINDOW_SIZE[1]:
                    couleur = screen.get_at((int(x_check), int(y_check)))
                    if couleur[:3] != (0, 0, 0):
                        collision_mur_climb = True
                        break
            
            # Si pas de mur au-dessus, on regarde si on peut marcher devant (et on retourne à Marche)
            if not collision_mur_climb:
                # Vérifier s'il y a du sol devant pour marcher
                wall_check_points_devant = [
                    (wall_check_x, onelemming['y'] + 5),
                    (wall_check_x, onelemming['y'] + 15),
                    (wall_check_x, onelemming['y'] + 25)
                ]
                collision_sol_devant = False
                for x_check, y_check in wall_check_points_devant:
                    if 0 <= x_check < WINDOW_SIZE[0] and 0 <= y_check < WINDOW_SIZE[1]:
                        couleur = screen.get_at((int(x_check), int(y_check)))
                        if couleur[:3] != (0, 0, 0):
                            collision_sol_devant = True
                            break
                
                if collision_sol_devant:
                    onelemming['etat'] = EtatMarche
                    onelemming['climber_active'] = False
                else:
                    # Pas de sol devant = c'est un vide, on tombe
                    onelemming['etat'] = EtatChute
                    onelemming['fallcount'] = 0
                    onelemming['climber_active'] = False
        
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
        
        # (Basher) Note: la condition d'arrêt est gérée en ETAPE 2 (actions)
        # pour éviter d'annuler le basher dès la frame d'activation.

    # ETAPE 2 : gestion des actions

    for onelemming in lemmingsLIST:
        # Cooldown qui empêche le rebond sur mur juste après un basher
        if onelemming.get('basher_exit_cooldown', 0) > 0:
            onelemming['basher_exit_cooldown'] -= 1

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
            onelemming['Decal'] += 1
        if ( onelemming['etat'] == EtatClimber ):
            # Climber : grimpe le mur vers le haut
            onelemming['y'] -= 2  # Monte de 2 pixels par frame
            onelemming['Decal'] += 1  # Animation de grimpe
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
        if ( onelemming['etat'] == EtatBasher ):
            # Basher : creuse devant lui horizontalement dès la première frame
            # ET continue à avancer en même temps
            onelemming['basher_timer'] += 1
            onelemming['x'] += onelemming['direction'] * 3  # Avance
            
            if onelemming['basher_timer'] > 0:  # Creuse dès la première frame
                # Creuse 20 pixels devant le lemming (dans sa direction)
                direction = onelemming['direction']
                
                # AVANT de creuser, vérifie s'il y a du terrain à creuser devant
                check_x = int(onelemming['x']) + (direction * 20)
                has_terrain_ahead = False
                for dy in range(WINDOW_SIZE[1]):
                    if 0 <= check_x < WINDOW_SIZE[0] and 0 <= dy < WINDOW_SIZE[1]:
                        couleur = fond.get_at((check_x, dy))
                        if couleur[:3] != (0, 0, 0):
                            has_terrain_ahead = True
                            break
                
                # Ne creuse que s'il y a du terrain devant
                if has_terrain_ahead:
                    # Point de départ collé au mur (évite un "espace" avant le tunnel)
                    base_x = int(onelemming['x']) + (direction * -3)
                    # Tunnel au niveau des pieds du lemming
                    base_y = int(onelemming['y']) + 15
                    
                    # Creuse 20 pixels horizontalement devant lui à sa hauteur
                    for px in range(30):
                        x_pos = base_x + (direction * px)
                        # Tunnel plus grand, surtout vers le haut ET vers le bas
                        for py in range(30):
                            y_pos = base_y + py - 8
                            if 0 <= x_pos < WINDOW_SIZE[0] and 0 <= y_pos < WINDOW_SIZE[1]:
                                fond.set_at((x_pos, y_pos), (0, 0, 0))

            # Stop condition: s'il n'y a plus rien à creuser juste devant (déjà noir),
            # on revient à Marche. On attend quelques frames après activation
            # pour éviter un arrêt immédiat si le lemming était déjà dans un trou.
            # On ne stoppe que si on a réellement démarré le basher contre un mur
            if onelemming.get('basher_started', False) and onelemming['basher_timer'] > 5:
                direction = onelemming['direction']
                check_x = int(onelemming['x']) + (direction * 16)
                
                # Vérifie toute la colonne devant le lemming
                all_black = True
                for dy in range(WINDOW_SIZE[1]):
                    check_y = dy
                    if 0 <= check_x < WINDOW_SIZE[0] and 0 <= check_y < WINDOW_SIZE[1]:
                        couleur = fond.get_at((check_x, check_y))
                        if couleur[:3] != (0, 0, 0):
                            all_black = False
                            break
                
                if all_black:
                    onelemming['etat'] = EtatMarche
                    onelemming['basher_timer'] = 0
                    onelemming['basher_started'] = False
                    # Petit délai: évite le rebond sur le mur la frame où on sort du basher
                    onelemming['basher_exit_cooldown'] = 6

            # Garde-fou (évite basher infini)
            if onelemming['basher_timer'] > 250:
                onelemming['etat'] = EtatMarche
                onelemming['basher_timer'] = 0
            onelemming['Decal'] += 1  # Animation de bash
    
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
        if ( state == EtatClimber ):
            # Affiche le sprite de grimpage (animation)
            if len(climber) > 0:
                sprite_index = time % len(climber)
                sprite = climber[sprite_index]
                if onelemming['flipped']:
                    sprite = pygame.transform.flip(sprite, True, False)
                screen.blit(sprite,(xx,yy))
        if ( state == EtatBasher ):
            # Affiche le sprite de basher (animation)
            if len(basher) > 0:
                sprite_index = time % len(basher)
                sprite = basher[sprite_index]
                if onelemming['flipped']:
                    sprite = pygame.transform.flip(sprite, True, False)
                screen.blit(sprite,(xx,yy))
    
    # ETAPE 4 : affichage des lampes d'aptitudes
    lamp_size = 8
    lamp_y_fixed = 340  # Hauteur fixe pour aligner toutes les lampes
    
    # Positions X spécifiques pour chaque lampe
    lamp_positions = {
        'Stopper': 195 + 20,   
        'Creuser': 530 + 20,
        'Floater': 338 + 20,
        'Climber': 290 + 20,
        'Basher': 500 + 20
    }
    
    for nom_aptitude in aptitudes.keys():
        lamp_x = lamp_positions.get(nom_aptitude, aptitudes[nom_aptitude].centerx)
        
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