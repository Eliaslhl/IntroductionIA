import pygame
import numpy as np
import pygame.surfarray as surfarray
from math import sqrt
import random

# palette de couleurs
palette = {} # initialise un dictionnaire
palette['B'] =  [  0,   0, 255]   # BLUE
palette[' '] =  [  0,   0,   0]   # BLACK
palette['W'] =  [255, 255, 255]   # WHITE
palette['G'] =  [  0, 255,   0]   # GREEN
palette['R'] =  [255,   0,   0]   # RED
palette['Y'] =  [255, 255,   0]   # YELLOW
palette['C'] =  [  0, 225, 255]   # CYAN

# couleur pour les pièges
palette['T'] =  [160,  32, 240]   # TRAP (purple)
palette['K'] =  [255, 215,   0]   # KEY (gold)
palette['D'] =  [139,  69,  19]   # DOOR (brown)


# dimensions
WIDTH = 20  # largeur d'une case en pixels
NBcases = 20

# plan original 10x10
plan10 = [ 'BBBBBBBBBB', 
           'B        B',
           'B BB BBBBB',
           'B B  B   B',
           'B BB BB  B',
           'B B   BB B',
           'B  B  B  B',
           'BB BB BB B',
           'B   B    B',
           'BBBBBBBBBB' ]

# plan 20x20
plan = []
for row in plan10:
    doubled = ''.join([c*2 for c in row])
    plan.append(doubled)
    plan.append(doubled)

# Fonction pour trouver toutes les cases libres
def get_free_cells(plan):
    free_cells = []
    for y in range(len(plan)):
        for x in range(len(plan[0])):
            if plan[y][x] == ' ':
                free_cells.append((x, y))
    return free_cells

# Fonction pour sélectionner N cases aléatoires parmi les cases libres
def select_random_free_cells(plan, num_cells):
    free_cells = get_free_cells(plan)
    if len(free_cells) < num_cells:
        print(f"Avertissement: seulement {len(free_cells)} cases libres disponibles, demande de {num_cells}")
        return free_cells
    return random.sample(free_cells, num_cells)

# pièges aléatoirement sur le plan
plan_chars = [list(r) for r in plan]
num_traps = 10
trap_positions = select_random_free_cells(plan, num_traps)
for (tx, ty) in trap_positions:
    if 0 <= ty < len(plan_chars) and 0 <= tx < len(plan_chars[0]):
        if plan_chars[ty][tx] != 'B':
            plan_chars[ty][tx] = 'T'

plan = [''.join(r) for r in plan_chars]

# vérification du plan
if ( len(plan) != NBcases ): print("erreur, nombre de lignes dans le plan")
for ligne in plan:
    if ( len(ligne) != NBcases ): print("erreur, ligne pas à la bonne dimension")

# remplissage du tableau du labyrinthe
LABY  = np.zeros((NBcases,NBcases,3))
for y in range(NBcases):
    ligne = plan[y]
    for x in range(NBcases):
        c = ligne[x]
        LABY[x,y] = palette.get(c, palette[' '])
        
###################################################################################

def ToSprite(ascii):
   _larg = len(max(ascii, key=len)) # on prend la ligne la plus grande
   _haut = len(ascii)
   TBL = np.zeros((_larg,_haut,3)) # tableau 3 dimensions

   for y in range(_haut):
      ligne = ascii[y]
      for x in range(len(ligne)):
         c = ligne[x]
         TBL[x,y] = palette[c]  # couleur RVB
    
   # conversion du tableau de RVB en sprite
   sprite = surfarray.make_surface(TBL)
   return sprite


pers1= [ '   RRR    ', 
         '  RRWWR   ',
         '   RRR    ',
         '   YY     ',
         '   YYY     ',
         '   YY YG   ',
         '   GG      ',
         '   CC      ',
         '   CC      ',
         '  C  C     ',
         '  C  C    ' ]
         
pers2 = [ '   RRR    ', 
         '  RRWWR   ',
         '   RRR    ',
         '   YY     ',
         '   YYY     ',
         '   YY YG   ',
         '   GG      ',
         '   CC      ',
         '   CC      ',
         '   CC     ',
         '   CC    ' ]

pers3 = [ '   RRR    ', 
          '  RRWWR   ',
          '   RRR    ',
          '   YY     ',
          '   YYY     ',
          '   YY YG   ',
          '   GG      ',
          '   CC      ',
          '  C CC     ',
          '  C  C     ',
          '   CC    ' ]

pers4 = [ '   RRR    ', 
          '  RRWWR   ',
          '   RRR    ',
          '   YY     ',
          '   YYY     ',
          '   YY YG   ',
          '   GG      ',
          '   CC      ',
          '  CC C     ',
          '   C  C    ',
          '   CC    ' ]

pers5 = [ '   RRR    ', 
          '  RRWWR   ',
          '   RRR    ',
          '   YY     ',
          '   YYY     ',
          '   YY YG   ',
          '   GG      ',
          '   CC      ',
          '   C CC    ',
          '   C  C    ',
          '   CC    ' ]

pers6 = [ '   RRR    ', 
          '  RRWWR   ',
          '   RRR    ',
          '   YY     ',
          '   YYY     ',
          '   YY YG   ',
          '   GG      ',
          '   CC      ',
          '   CC C    ',
          '   C  C    ',
          '   CC    ' ]

treasure = [ '      K      ',
             '     KYK     ',
             '    KYYYK    ',
             '   KYYYYK    ',
             '   KYYYYK    ',
             '    KYYYK    ',
             '     KYK     ',
             '      K      ' ]

key = [ '  KKKK       ',
        '  KGGK       ',
        '  KGGK       ',
        '  KKKK       ',
        '     KKKKKK  ',
        '     KGGGGK  ',
        '     KGGGGK  ',
        '     KKKKKK  ' ]

door = [ '   DDDDDD    ',
         '   DWWWWD    ',
         '   DWWWWD    ',
         '   DWWWWD    ',
         '   DWWWWD    ',
         '   DWWWWD    ',
         '   DWWWWD    ',
         '   DDDDDD    ' ]

chest = [ '   RRRRRR    ',
          '   RYYYR R   ',
          '   RYYYRR    ',
          '   RRRRRR    ',
          '  RRRRRRRR   ',
          '  RYYYYYYYR  ',
          '  RYYYYYYYR  ',
          '  RRRRRRRR   ' ]


player_sprite = ToSprite(pers1)
player_x = 50
player_y = 50

# Création des sprites une fois
treasure_sprite = ToSprite(treasure)
key_sprite = ToSprite(key)
door_sprite = ToSprite(door)
chest_sprite = ToSprite(chest)

# Palette de couleur pour le coffre
palette['Chest'] = [255, 0, 0]  # Red pour le coffre

###################################################################################

pygame.init()

# taille de la fenêtre
WINDOW_SIZE = [400, 400]
screen = pygame.display.set_mode(WINDOW_SIZE)

# titre de la fenêtre
pygame.display.set_caption("LABYRINTHE")

done = False

# Gestion de la fréquence de rafraîchissement
clock = pygame.time.Clock()

# Système de score et trésors multiples
score = 0
TREASURE_VALUE = 100  # Points par trésor

# Sélection de 6 cases aléatoires distinctes : 5 treasures, 1 key
positions = select_random_free_cells(plan, 6)

treasures = []
for i in range(5):
    x, y = positions[i]
    pixel_x = x * WIDTH + WIDTH // 2
    pixel_y = y * WIDTH + WIDTH // 2
    treasures.append({'x': pixel_x, 'y': pixel_y, 'active': True})

TREASURE_THRESHOLD = 10  # Distance en pixels pour ramasser un trésor

# Système de clé et de porte - positionnement aléatoire
has_key = False  # Inventaire key
key_x, key_y = positions[5]
key_x = key_x * WIDTH + WIDTH // 2
key_y = key_y * WIDTH + WIDTH // 2
KEY_THRESHOLD = 10  # Distance pour ramasser la clé

# Trouve une case libre dans le coin inférieur droit du labyrinthe
door_candidates = [(x, y) for x, y in get_free_cells(plan) if x >= 15 and y >= 15]
if door_candidates:
    door_x, door_y = random.choice(door_candidates)
else:
    # Fallback si pas de case disponible
    door_x, door_y = 17, 17
door_x = door_x * WIDTH + WIDTH // 2
door_y = door_y * WIDTH + WIDTH // 2

# Cooldown pour les pièges (en ms)
last_trap_time = 0
TRAP_COOLDOWN = 1000  # 1 seconde de cooldown

print("=== GAUNTLET - Démarrage du jeu ===")
print(f"Nombre de pièges placés: {num_traps}")
print(f"Positions des trésors (5 au total):")
for i, treasure in enumerate(treasures):
    print(f"  Trésor {i+1}: pixel ({treasure['x']}, {treasure['y']})")
print(f"Position de la clé: pixel ({key_x}, {key_y})")
print(f"Position de la porte: pixel ({door_x}, {door_y})")
print(f"Position du joueur: pixel ({player_x}, {player_y})")
print("=" * 40)

# -------- Boucle principale du jeu -----------
while not done:
    event = pygame.event.Event(pygame.USEREVENT)  # Réinitialisation de la variable event
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            done = True 
            
    KeysPressed = pygame.key.get_pressed()
    
    if KeysPressed[pygame.K_UP]:
        # collision avec la case au-dessus
        proposed_y = player_y - 2 
        center_x = player_x + player_sprite.get_width() // 2
        top_y = proposed_y
        for test_x in [player_x + 2, player_x + player_sprite.get_width() // 2, player_x + player_sprite.get_width() - 2]:
            tile_x = int(test_x // WIDTH)
            tile_y = int(top_y // WIDTH)
            if not (0 <= tile_x < NBcases and 0 <= tile_y < NBcases and plan[tile_y][tile_x] != 'B'):
                break
        else:
            player_y = proposed_y

    if KeysPressed[pygame.K_DOWN]:
        # collision avec la case en-dessous
        proposed_y = player_y + 2
        bottom_y = proposed_y + player_sprite.get_height()
        for test_x in [player_x + 2, player_x + player_sprite.get_width() // 2, player_x + player_sprite.get_width() - 2]:
            tile_x = int(test_x // WIDTH)
            tile_y = int(bottom_y // WIDTH)
            if not (0 <= tile_x < NBcases and 0 <= tile_y < NBcases and plan[tile_y][tile_x] != 'B'):
                break
        else:
            player_y = proposed_y
        
    if KeysPressed[pygame.K_LEFT]:
        # collision avec la case à gauche
        proposed_x = player_x - 2  # Augmentation de l'offset
        left_x = proposed_x
        # Test 3 points : haut, centre, bas du côté gauche
        for test_y in [player_y + 2, player_y + player_sprite.get_height() // 2, player_y + player_sprite.get_height() - 2]:
            tile_x = int(left_x // WIDTH)
            tile_y = int(test_y // WIDTH)
            if not (0 <= tile_x < NBcases and 0 <= tile_y < NBcases and plan[tile_y][tile_x] != 'B'):
                break
        else:
            player_x = proposed_x
        
    if KeysPressed[pygame.K_RIGHT]:
        # collision avec la case à droite
        proposed_x = player_x + 2  # Augmentation de l'offset
        right_x = proposed_x + player_sprite.get_width()
        # Test 3 points : haut, centre, bas du côté droit
        for test_y in [player_y + 2, player_y + player_sprite.get_height() // 2, player_y + player_sprite.get_height() - 2]:
            tile_x = int(right_x // WIDTH)
            tile_y = int(test_y // WIDTH)
            if not (0 <= tile_x < NBcases and 0 <= tile_y < NBcases and plan[tile_y][tile_x] != 'B'):
                break
        else:
            player_x = proposed_x

    # Vérification si le joueur est sur un piège
    # on calcule la case sur laquelle se trouve le centre du sprite
    cx = player_x + player_sprite.get_width() // 2
    cy = player_y + player_sprite.get_height() // 2
    tile_x = int(cx // WIDTH)
    tile_y = int(cy // WIDTH)
    if 0 <= tile_x < NBcases and 0 <= tile_y < NBcases:
        if plan[tile_y][tile_x] == 'T':
            # Vérification du cooldown pour éviter la téléportation répétée
            current_time = pygame.time.get_ticks()
            if current_time - last_trap_time > TRAP_COOLDOWN:
                print('TRAP! repositionnement au départ')
                player_x = 50
                player_y = 50
                last_trap_time = current_time

    # Vérifie si le joueur ramasse des trésors
    player_center_x = player_x + player_sprite.get_width() // 2
    player_center_y = player_y + player_sprite.get_height() // 2
    
    for treasure in treasures:
        if treasure['active']:
            distance_to_treasure = sqrt((player_center_x - treasure['x'])**2 + (player_center_y - treasure['y'])**2)
            if distance_to_treasure < TREASURE_THRESHOLD:
                treasure['active'] = False
                score += TREASURE_VALUE
                print(f'Trésor ramassé! Score: {score}')

    # Vérifie si le joueur ramasse la clé
    if not has_key:
        distance_to_key = sqrt((player_center_x - key_x)**2 + (player_center_y - key_y)**2)
        if distance_to_key < KEY_THRESHOLD:
            has_key = True
            print('Clé ramassée! Elle apparaît dans l\'inventaire.')

    # Affichage du fond (labyrinthe)
    for ix in range(NBcases):
        for iy in range(NBcases):
            xpix = WIDTH * ix
            ypix = WIDTH * iy
            couleur = LABY[ix,iy]
            pygame.draw.rect(screen,couleur,[xpix,ypix,WIDTH,WIDTH])

    # Affichage des coffres au trésor
    for treasure in treasures:
        if treasure['active']:
            screen.blit(chest_sprite, (treasure['x'] - chest_sprite.get_width() // 2, treasure['y'] - chest_sprite.get_height() // 2))

    # Affichage de la clé
    if not has_key:
        screen.blit(key_sprite, (key_x - key_sprite.get_width() // 2, key_y - key_sprite.get_height() // 2))
    
    # Affichage de la porte
    screen.blit(door_sprite, (door_x - door_sprite.get_width() // 2, door_y - door_sprite.get_height() // 2))
    
    # Affichage du score en haut à gauche
    score_font = pygame.font.SysFont('Arial', 24)
    score_text = score_font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    # Affichage de l'inventaire à côté du score
    if has_key:
        small_key = pygame.transform.scale(key_sprite, (16, 16)) # Sprite plus petit pour l'inventaire
        screen.blit(small_key, (150, 15))
    
    # Affichage du personnage avec animation de marche fluide (6 frames)
    animation_frame = int(pygame.time.get_ticks() / 100) % 6
    if animation_frame == 0:
        player_sprite = ToSprite(pers1)
    elif animation_frame == 1:
        player_sprite = ToSprite(pers2)
    elif animation_frame == 2:
        player_sprite = ToSprite(pers3)
    elif animation_frame == 3:
        player_sprite = ToSprite(pers4)
    elif animation_frame == 4:
        player_sprite = ToSprite(pers5)
    else:
        player_sprite = ToSprite(pers6)
    
    screen.blit(player_sprite,(player_x,player_y))

    # Check win
    player_rect = player_sprite.get_rect(topleft=(player_x, player_y))
    door_rect = door_sprite.get_rect(center=(door_x, door_y))

    # calcule la distance entre les bords du rectangle
    dx = 0
    if player_rect.right < door_rect.left:
        dx = door_rect.left - player_rect.right
    elif door_rect.right < player_rect.left:
        dx = player_rect.left - door_rect.right

    dy = 0
    if player_rect.bottom < door_rect.top:
        dy = door_rect.top - player_rect.bottom
    elif door_rect.bottom < player_rect.top:
        dy = player_rect.top - door_rect.bottom

    distance_to_door = sqrt(dx*dx + dy*dy)

    THRESHOLD_DOOR = 15
    
    # Victoire seulement si clé ramassée ET à proximité de la porte
    if has_key and distance_to_door < THRESHOLD_DOOR:
        print("VICTOIRE! Vous avez trouvé la clé et atteint la sortie!")
        my_font = pygame.font.SysFont('Arial', 30)
        text_surface = my_font.render('VICTOIRE!', True, (0, 255, 0))
        screen.blit(text_surface, (120, 180))
        
    clock.tick(30)

    # Mise à jour de l'affichage
    pygame.display.flip()
 

pygame.quit()