
import pygame
import sys

import gui

#Variables for pygame window
res = pygame.Vector2(816,459) #16:9
surface = pygame.display.set_mode(res)
clock = pygame.time.Clock()
deltaTime = clock.tick(60)/1000
run = True
backgroundColour = (0, 0, 0)

#Pygame events

button1 = gui.Button(100,75,100,50,"Button")

def main_menu():
  pygame.display.set_caption("Main Menu")

  while True:
    surface.fill(backgroundColour)
    
    button1.update(surface)
    if button1.check_click():
      print("Clicked")

    for event in pygame.event.get():
      #Close window
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    pygame.display.update()
    clock.tick(60)

