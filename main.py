import pygame
import math
import random
from threading import Timer



backgroundColour = (0, 0, 0)
run = True
res = pygame.Vector2(816,459) #16:9
surface = pygame.display.set_mode(res)
clock = pygame.time.Clock()
deltaTime = clock.tick(60)/1000





# Constants
foodAmount = 0
consumerAmount = 3
speedVariance = 10
senseVariance = 10
sizeVariance = 5
CREATE_FOOD = pygame.USEREVENT + 1

# Variables
i = 0

class Entity:
  def __init__(self):
    self.pos = randomVector()

  def draw(self):
    pass

  def update(self):
    pass

class Consumer(Entity):
  def __init__(self,pos,speed,senseRange,size):
    super().__init__()
    self.pos = pos
    self.path = randomVector()
    self.energy = 100
    
    self.speed = speed + random.randint(-10,10)
    self.senseRange = senseRange + random.randint(-8,8)
    self.eatRange = 20
    self.size = size + random.randint(-8,8)



    print("speed: ",self.speed,"sense: ",self.senseRange,"size: ",self.size)

  def draw(self):
    pygame.draw.circle(surface, (255, 255, 255), self.pos, self.size / 10)

  def update(self):
    self.updateVel()
    self.updatePosition()
    self.updateEating()
    self.updateEnergy()

  def updateVel(self):
    smallest = math.inf
    preyList = self.makePreyList()
    for food in foods:
      smallest = self.pathFinding(food,smallest)
    for prey in preyList:
      smallest = self.pathFinding(prey,smallest)


    if self.pos.distance_to(self.path) < 20:
      self.path = randomVector()
    self.vel = pygame.Vector2((self.path.x - self.pos.x, self.path.y - self.pos.y)).normalize()*self.speed*deltaTime

  
  def updateEating(self):

    for food in foods:
      if self.pos.distance_to(food.pos) < 20:
        foods.remove(food)
        self.newConsumer()
        
    preyList = self.makePreyList()
    for prey in preyList:
      distance = self.pos.distance_to(prey.pos)
      if distance < self.size + self.eatRange:
        consumers.remove(prey)
        self.newConsumer()
        print("CANNIBALISM")

  def makePreyList(self): #Adds the creatures that are small enough to the list to be eaten
    preyList = []
    for consumer in consumers:
      if self.size > 1.25 * consumer.size:
        preyList.append(consumer)
    return preyList
      
  def newConsumer(self):
    self.energy+=50
    if random.randint(1,2) == 1:
      consumers.append(Consumer(self.pos,self.speed,self.senseRange,self.size))
  
  def pathFinding(self,food,smallest):
    distance = self.pos.distance_to(food.pos)
    if distance < smallest:
      smallest = distance
    if distance < self.senseRange and distance == smallest:
      self.path = food.pos
    return smallest

  def updatePosition(self):
    self.pos = self.pos + self.vel


  def updateEnergy(self):
    self.energy -= 0.25
    if self.energy <= 0:
      consumers.remove(self)

  

class Food(Entity):
  def __init__(self):
    super().__init__()

  def draw(self):
    pygame.draw.circle(surface, (255, 255, 0), self.pos, 10)

def randomVector():
  return pygame.Vector2(random.randint(50, int(res.x) - 50), random.randint(50, int(res.y - 50)))

foods = [Food() for x in range(foodAmount)]
consumers = [Consumer(randomVector(),150,60,70) for x in range(consumerAmount)]

pygame.time.set_timer(CREATE_FOOD, 2500 - i)

while run:
  surface.fill(backgroundColour)

  for event in pygame.event.get():
    # Close window
    if event.type == pygame.QUIT:
      run = False

    elif event.type == CREATE_FOOD:
      foods.append(Food())
      i += 10
      pygame.time.set_timer(CREATE_FOOD, 1000 + i)

  entities = foods + consumers

  for entity in entities:
    entity.draw()
    entity.update()

  pygame.display.update()
  clock.tick(60)


  