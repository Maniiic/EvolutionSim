
import pygame
import sys

import gui
import simulation

# Variables for pygame window
res = pygame.Vector2(816,459) #16:9
surface = pygame.display.set_mode(res)
clock = pygame.time.Clock()
deltaTime = clock.tick(60)/1000
run = True
backgroundColour = (0, 0, 0)

# Buttons
startButton = gui.Button(res.x/2, res.y/4, "Start Simulation")
quitButton = gui.Button(res.x/2, res.y/2, "Quit")

buttons = [startButton, quitButton]


def main_menu():
  pygame.display.set_caption("Main Menu")

  while True:

    surface.fill(backgroundColour)

    for button in buttons:
      button.update(surface)

    # Functions for each button
    if startButton.check_click():
      simulation.main()
    
    if quitButton.check_click():
      pygame.quit()
      sys.exit()


    for event in pygame.event.get():
      # Close window
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    pygame.display.update()
    clock.tick(60)

