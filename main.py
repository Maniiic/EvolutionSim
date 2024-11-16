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


foodAmount = 0
consumerAmount = 3
i=0


class Entity:
  def __init__(self):
    self.pos = pygame.Vector2(random.randint(50, int(res.x) - 50), random.randint(50, int(res.y - 50)))
    

  def updatePos(self):
    self.pos = self.pos + self.vel


class Consumer(Entity):

  def __init__(self,pos,speed,senseRange,size):
    super().__init__()
    self.pos = pos
    self.path = pygame.Vector2(random.randint(50, int(res.x) - 50), random.randint(50, int(res.y - 50)))
    self.energy = 100
    
    self.speed = speed + random.randint(-10,10)
    self.senseRange = senseRange + random.randint(-8,8)
    self.size = size + random.randint(-8,8)

    print("speed: ",self.speed,"sense: ",self.senseRange,"size: ",self.size)

  def updateVel(self):
    smallest = math.inf
    preyList = consumer.makePreyList()
    for food in foods:
      smallest = consumer.pathFinding(food,smallest)
    for prey in preyList:
      smallest = consumer.pathFinding(prey,smallest)


    if ((self.pos.x + 20 > self.path.x) and (self.pos.x - 20 < self.path.x)) and ((self.pos.y + 20 > self.path.y) and (self.pos.y - 20 < self.path.y)):
      self.path = pygame.Vector2(random.randint(50, int(res.x) - 50), random.randint(50, int(res.y - 50)))
    self.vel = pygame.Vector2((self.path.x - self.pos.x, self.path.y - self.pos.y)).normalize()*self.speed*deltaTime

  
  def updateEating(self):

    for food in foods:
      if (self.pos.x + 20 > food.pos.x) and (self.pos.x - 20 < food.pos.x) and (self.pos.y + 20 > food.pos.y) and (self.pos.y - 20 < food.pos.y):
        foods.remove(food)
        consumer.newConsumer()
        
    preyList = consumer.makePreyList()      
    for prey in preyList:   
      if (self.pos.x + 20 > prey.pos.x) and (self.pos.x - 20 < prey.pos.x) and (self.pos.y + 20 > prey.pos.y) and (self.pos.y - 20 < prey.pos.y):
        consumers.remove(prey)
        consumer.newConsumer()
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
    distance = ((self.pos.x - food.pos.x)**2 + (self.pos.y - food.pos.y)**2)**(1/2)
    if distance < smallest:
      smallest = distance
    if distance < self.senseRange and distance == smallest:
      self.path = food.pos
    return smallest


  def updateEnergy(self):
    self.energy -= 0.25
    if self.energy <= 0:
      consumers.remove(self)

  

class Food(Entity):
  def __init__(self):
    super().__init__()

def newFood():
  global i
  if run == False:
    return
  t = Timer(0.25+i, recursionFood) #Can't call itself due to recursion limit
  i+=0.01
  t.start()
  foods.append(Food())

def recursionFood():
  newFood()


foods = [Food() for x in range(foodAmount)]
consumers = [Consumer(pygame.Vector2(random.randint(50, int(res.x) - 50), random.randint(50, int(res.y - 50))),150,60,70) for x in range(consumerAmount)]


newFood()

while run:

  surface.fill(backgroundColour)

  for exit in pygame.event.get():
    if exit.type == pygame.QUIT:
      run = False

  for consumer in consumers:
    #Update All
    consumer.updateVel()
    consumer.updatePos()
    consumer.updateEating()
    consumer.updateEnergy()
    

    pygame.draw.circle(surface, (255,255,255), consumer.pos, consumer.size/10)

  for food in foods:
    pygame.draw.circle(surface, (255,255,0), food.pos, 10)

  pygame.display.update()
  clock.tick(60)
pygame.quit()


      
  