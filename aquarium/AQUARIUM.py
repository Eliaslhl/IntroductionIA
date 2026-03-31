import pygame
import os, inspect
from pygame.transform import scale

# recherche du répertoire de travail
# inspect.getsourcefile() peut retourner None (p.ex. dans certains environnements interactifs),
# donc on gère ce cas et on utilise __file__ ou le répertoire courant en secours.
source = inspect.getsourcefile(lambda: 0)
if source is None:
   try:
      source = __file__
   except NameError:
      # pas de __file__ (interpréteur interactif), fallback sur le répertoire courant
      source = os.getcwd()
scriptPATH = os.path.abspath(source)
scriptDIR = os.path.dirname(scriptPATH)
assets = os.path.join(scriptDIR, "data")


# Setup
pygame.init()

# Define some colors
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
RED   = [255, 0, 0]
BLUE  = [0 , 0 , 255]

police = pygame.font.SysFont("arial", 15)
 
 
print(scriptDIR)
 
 
# Set the width and height of the screen [width,height]
screeenWidth = 400
screenHeight = 400
screen = pygame.display.set_mode((screeenWidth,screenHeight))
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Hide the mouse cursor
pygame.mouse.set_visible(True) 
 
fond = pygame.image.load(os.path.join(assets, "fond.bmp"))
poisson = pygame.image.load(os.path.join(assets, "fish1.bmp"))
 
 

poisson1_x  = 100
poisson1_y  = 200
poisson1_vx = -2
 
 
# -------- Main Program Loop -----------
while not done:
   event = pygame.event.Event(pygame.USEREVENT)    # Remise à zero de la variable event
   
   # récupère la liste des touches claviers appuyeées sous la forme liste bool
   pygame.event.pump()
   
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         done = True
      
   
    # LOGIQUE
 
   poisson1_x += poisson1_vx
   if ( poisson1_x < 50 ):
      poisson1_x = 50
      poisson1_vx = -poisson1_vx

 
    # DESSIN
    
   # affiche la zone de rendu au dessus de fenetre de jeu
   screen.blit(fond,(0,0))
   
   #tt = pygame.rect(poisson1_x,poisson1_y,10,10)
   
   screen.blit(poisson, (poisson1_x,poisson1_y))
   
  
    # Go ahead and update the screen with what we've drawn.
   pygame.display.flip()
 
    # Limit frames per second
   clock.tick(30)
 
# Close the window and quit.
pygame.quit()