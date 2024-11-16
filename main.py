import pygame
#import simulation



# Variables for pygame window
res = 816,459 #16:9
surface = pygame.display.set_mode(res)
clock = pygame.time.Clock()
deltaTime = clock.tick(60)/1000
run = True
backgroundColour = (0, 0, 0)




while run:
  surface.fill(backgroundColour)

  for event in pygame.event.get():
    #Close window
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()
  clock.tick(60)