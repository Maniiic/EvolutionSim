

from asyncio.windows_events import NULL
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
foodAmount = 20
creatureAmount = 3




#Food and creatures will inherit from entity class
class Entity:
  def __init__(self):
    #Spawn with a random position on the screen, 
    self.pos = randomVector()
    self.speed = 0
    self.size = 10
    
  
  def draw(self):
    pygame.draw.circle(surface,self.colour,self.pos,self.size)


class Creature(Entity):
  def __init__(self):
    super().__init__()
    self.speed = 150
    self.senseRange = 600
    self.colour = (255,255,255)
    self.node = randomVector()

    


  def update(self):
    self.closestFoodInRange = self.getClosestFoodInRange()
    self.updatePath()
    self.updateEating()
    self.updateVelocity()
    self.updatePosition()

  def getClosestFoodInRange(self):
    closestFood = NULL
    smallest = math.inf
    for food in foods:
      distance = self.pos.distance_to(food.pos)
      if distance < smallest:
        smallest = distance
        if distance <= self.senseRange:
          closestFood = food
    return closestFood

  def updatePath(self, ):
    target = self.closestFoodInRange
    if self.pos.distance_to(self.node) <= self.size:
      self.node = randomVector()
    if target != NULL:
      self.path = target.pos
    else:
      self.path = self.node

  def updateEating(self):
    return


  def updateVelocity(self):
    self.vel = (self.path - self.pos).normalize()*self.speed*deltaTime

  def updatePosition(self):
    self.pos += self.vel



class Food(Entity):
  def __init__(self):
    super().__init__()
    self.colour = (255,255,0)
  



def randomVector():
  return pygame.Vector2(random.randint(50, int(res.x) - 50), random.randint(50, int(res.y - 50)))



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
    creature.update()
    
   

  for food in foods:
    food.draw()

  pygame.display.update()
  clock.tick(60)
