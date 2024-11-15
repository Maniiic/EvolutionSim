

from asyncio.windows_events import NULL
from threading import Timer
from tkinter import N
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

CREATE_FOOD = pygame.USEREVENT + 1

#Constants
foodAmount = 5
creatureAmount = 3

#Variables
i=0




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
    self.senseRange = 70
    self.colour = (255,255,255)
    self.node = randomVector()


  def update(self):
    
    self.createPreyList()
    self.updateClosestTargetInRange(foods+self.preyList)
    self.updatePath()
    self.updateEating(foods)
    self.updateEating(self.preyList)
    self.updateVelocity()
    self.updatePosition()

  def createPreyList(self):
    self.preyList = []
    for creature in creatures:
      if self.size > 1.25 * creature.size:
        self.preyList.append(creature)

  def updateClosestTargetInRange(self, possibleTargetsList):
    closestTarget = NULL
    smallest = math.inf
    for target in possibleTargetsList:
      distance = self.pos.distance_to(target.pos)
      if distance < smallest:
        smallest = distance
        if distance <= self.senseRange:
          closestTarget = target
    self.closestTargetInRange = closestTarget

  def updateEating(self, targetList):
    try:
      if self.pos.distance_to(self.closestTargetInRange.pos) <= self.size:
        targetList.remove(self.closestTargetInRange)
    except:
      return

  def updatePath(self):
    target = self.closestTargetInRange
    if self.pos.distance_to(self.node) <= self.size:
      self.node = randomVector()
    if target != NULL:
      self.path = target.pos
    else:
      self.path = self.node

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

pygame.time.set_timer(CREATE_FOOD,2500-i)
while run:
  surface.fill(backgroundColour)

  for event in pygame.event.get():
    #Close window
    if event.type == pygame.QUIT:
      run = False

    elif event.type == CREATE_FOOD:
      foods.append(Food())
      i+=10
      pygame.time.set_timer(CREATE_FOOD,1000+i)
  
  for creature in creatures:
    creature.draw()
    creature.update()
    
   

  for food in foods:
    food.draw()

  pygame.display.update()
  clock.tick(60)
