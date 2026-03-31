import pygame
import numpy as np
import pygame.surfarray as surfarray
from math import sqrt
 
# crée une palette de couleurs
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


# dimensions
WIDTH = 20  # largeur d'une case en pixels
NBcases = 20

# plan original 10x10 (utilisé pour créer automatiquement une version 20x20)
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

# Générer plan 20x20 en doublant chaque cellule du plan 10x10
plan = []
for row in plan10:
    doubled = ''.join([c*2 for c in row])
    plan.append(doubled)
    plan.append(doubled)

# injecter quelques pièges 'T' (emplacements choisis pour être sur des chemins)
plan_chars = [list(r) for r in plan]
trap_positions = [(3,2),(10,5),(16,12),(7,14),(12,9)]  # (x,y)
for (tx,ty) in trap_positions:
    if 0 <= ty < len(plan_chars) and 0 <= tx < len(plan_chars[0]):
        plan_chars[ty][tx] = 'T'

# retransformer en liste de chaînes
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
         c = ligne[x]  # on recupere la lettre
         TBL[x,y] = palette[c]  #on stocke le code couleur RVB
    
   # conversion du tableau de RVB en sprite pygame
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

treasure = [ '   YYYYYY    ',
            '   YYYYYY    ',
            '   YYYYYY    ',
            '   YYYYYY    ',
            '   YYYYYY    ',
            '   YYYYYY    ',
            '   YYYYYY    ',
            '   YYYYYY    ',
            '   YYYYYY    ',
            '   YYYYYY    ',
            '   YYYYYY    ',
            '   YYYYYY    ' ]


player_sprite = ToSprite(pers1)
player_x = 50
player_y = 50

# create treasure sprite once (avoid recreating every frame)
treasure_sprite = ToSprite(treasure)

###################################################################################
 
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [400, 400]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("LABYRINTHE")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    event = pygame.event.Event(pygame.USEREVENT)    # Remise à zero de la variable event
    
    for event in pygame.event.get():  # User did something
        
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
            
    KeysPressed = pygame.key.get_pressed()

    treasure_x = 300
    treasure_y = 150
    
    if KeysPressed[pygame.K_UP]:
        up_pixel_color = screen.get_at((player_x + player_sprite.get_width()//2, player_y-1))
        if up_pixel_color[0] == 0 and up_pixel_color[1] == 0 and up_pixel_color[2] == 0 : 
            player_y -= 1

    if KeysPressed[pygame.K_DOWN]:
        down_pixel_color = screen.get_at((player_x + player_sprite.get_width()//2, player_y + player_sprite.get_height()))
        if down_pixel_color[0] == 0 and down_pixel_color[1] == 0 and down_pixel_color[2] == 0 :
            player_y += 1
        
    if KeysPressed[pygame.K_LEFT]:
        left_pixel_color = screen.get_at((player_x-1, player_y + player_sprite.get_height()//2))
        if left_pixel_color[0] == 0 and left_pixel_color[1] == 0 and left_pixel_color[2] == 0 :
            player_x -= 1
        
    if KeysPressed[pygame.K_RIGHT]:
        right_pixel_color = screen.get_at((player_x + player_sprite.get_width(), player_y + player_sprite.get_height()//2)) # pour mi-hauteur du sprite
        if right_pixel_color[0] == 0 and right_pixel_color[1] == 0 and right_pixel_color[2] == 0 : 
            player_x += 1

    # Après déplacement, vérifier si le joueur est sur un piège
    # on calcule la case sur laquelle se trouve le centre du sprite
    cx = player_x + player_sprite.get_width() // 2
    cy = player_y + player_sprite.get_height() // 2
    tile_x = int(cx // WIDTH)
    tile_y = int(cy // WIDTH)
    if 0 <= tile_x < NBcases and 0 <= tile_y < NBcases:
        if plan[tile_y][tile_x] == 'T':
            print('TRAP! repositionnement au départ')
            player_x = 50
            player_y = 50

    # Draw background
    for ix in range(NBcases):
        for iy in range(NBcases):
            xpix = WIDTH * ix
            ypix = WIDTH * iy
            couleur = LABY[ix,iy]
            pygame.draw.rect(screen,couleur,[xpix,ypix,WIDTH,WIDTH])

    # draw treasure (use precreated sprite)
    screen.blit(treasure_sprite, (treasure_x, treasure_y))
    
    # draw player
    if int(pygame.time.get_ticks()/500) % 2 == 0 :
        player_sprite = ToSprite(pers1)
    else:
        player_sprite = ToSprite(pers2)
    
    screen.blit(player_sprite,(player_x,player_y))

    # debug: sprite width (désactivé pour éviter le flood de la console)

    # Check win using rectangle edge distance
    player_rect = player_sprite.get_rect(topleft=(player_x, player_y))
    treasure_rect = treasure_sprite.get_rect(topleft=(treasure_x, treasure_y))

    # compute distance between rect edges (0 if overlapping)
    dx = 0
    if player_rect.right < treasure_rect.left:
        dx = treasure_rect.left - player_rect.right
    elif treasure_rect.right < player_rect.left:
        dx = player_rect.left - treasure_rect.right

    dy = 0
    if player_rect.bottom < treasure_rect.top:
        dy = treasure_rect.top - player_rect.bottom
    elif treasure_rect.bottom < player_rect.top:
        dy = player_rect.top - treasure_rect.bottom

    distance_between_edges = sqrt(dx*dx + dy*dy)

    # threshold in pixels between sprite edges
    THRESHOLD_PIXELS = 5
    if distance_between_edges < THRESHOLD_PIXELS:
        print("WIN")
        my_font = pygame.font.SysFont('Arial', 30)
        text_surface = my_font.render('WIN', True, (255, 255, 255))
        screen.blit(text_surface, (200, 150))
        
    # 30 fps
    clock.tick(30)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 

pygame.quit()