
import pygame
import random
import math


#Variables for pygame window
res = pygame.Vector2(816,459) #16:9
surface = pygame.display.set_mode(res)
clock = pygame.time.Clock()
deltaTime = clock.tick(60)/1000
run = True
backgroundColour = (0, 0, 0)

#Constants
foodAmount = 5
creatureAmount = 3


#Food and creatures will inherit from entity class
class Entity:
  def __init__(self):
    #Spawn with a random position on the screen, 
    self.pos = pygame.Vector2(random.randint(50, int(res.x) - 50), random.randint(50, int(res.y - 50)))
    self.speed = 0
    self.size = 100
    
  
  def draw(self):
    pygame.draw.circle(surface,self.colour,self.pos,self.size/10)

class Creature(Entity):
  def __init__(self):
    super().__init__()
    self.speed = 150
    self.senseRange = 600
    self.colour = (255,255,255)
    self.path = pygame.Vector2(random.randint(50, int(res.x) - 50), random.randint(50, int(res.y - 50)))

  def pathFinding(self):
    smallest = math.inf
    for food in foods:
      distance = ((self.pos.x - food.pos.x)**2 + (self.pos.y-food.pos.y)**2)**1/2
      if distance < smallest:
        smallest = distance
        print(smallest)
        if distance <= self.senseRange:
          self.path = food.pos


  def updateVel(self):
    
    self.pathFinding()
    #Gives new path when it reaches destination
    if ((self.pos.x + 20 > self.path.x) and (self.pos.x - 20 < self.path.x)) and ((self.pos.y + 20 > self.path.y) and (self.pos.y - 20 < self.path.y)):
      self.path = pygame.Vector2(random.randint(50, int(res.x) - 50), random.randint(50, int(res.y - 50)))
    #Sets velocity in direction of path
    self.vel = pygame.Vector2((self.path.x - self.pos.x, self.path.y - self.pos.y)).normalize()*self.speed*deltaTime

  def updatePos(self):
    self.pos += self.vel


class Food(Entity):
  def __init__(self):
    super().__init__()
    self.colour = (255,255,0)
  

#Initial lists
foods = [Food() for x in range(foodAmount)]
creatures = [Creature() for x in range(creatureAmount)]


#Main Loop
while run:
  surface.fill(backgroundColour)

  #Close window
  for exit in pygame.event.get():
    if exit.type == pygame.QUIT:
      run = False
  
  for creature in creatures:
    creature.draw()
    creature.updateVel()
    creature.updatePos()
    
   

  for food in foods:
    food.draw()

  pygame.display.update()
  clock.tick(60)
FWEHUF