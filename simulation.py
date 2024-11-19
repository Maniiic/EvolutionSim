
import sys
import pygame
import math
import random

# Variables for pygame window
backgroundColour = (0, 0, 0)
res = pygame.Vector2(816,459) # 16:9
surface = pygame.display.set_mode(res)
clock = pygame.time.Clock()
deltaTime = clock.tick(60)/1000

# Constants
foodAmount = 0
consumerAmount = 10
speedVariance = 10
senseVariance = 10
sizeVariance = 1
reproductionChance = 2 # 1 / reproductionChance

# Pygame event
CREATE_FOOD = pygame.USEREVENT + 1

# Variables
foodReduction = 0


class Entity:
  def __init__(self, col, size):
    self.pos = randomVector()
    self.col = col
    self.size = size

  def draw(self):
    pygame.draw.circle(surface, self.col, self.pos, self.size)

  def update(self):
    pass


class Consumer(Entity):
  def __init__(self,pos,speed,senseRange,size):
    super().__init__((255, 255, 255), size + random.randint(-sizeVariance,sizeVariance)) # Attributes shared by classes
    self.pos = pos
    self.path = randomVector()
    self.energy = 100
    
    # Initial traits
    self.speed = speed + random.randint(-speedVariance, speedVariance)
    self.senseRange = senseRange + random.randint(-senseVariance, senseVariance)

    print("speed: ",self.speed,"sense: ",self.senseRange,"size: ",self.size)

  def draw(self):
    # Draws the objects on the pygame screen
    pygame.draw.circle(surface, self.col, self.pos, self.size)

  def update(self):
    self.updateVel()
    self.updatePosition()
    self.updateEating()
    self.updateEnergy()

  def updateVel(self):
    smallest = math.inf
    preyList = self.makePreyList()
    # Check for closest food/prey
    for food in foods:
      smallest = self.pathFinding(food,smallest)
    for prey in preyList:
      smallest = self.pathFinding(prey,smallest)

    # Check if creature has reached its destination
    if self.pos.distance_to(self.path) <= self.size:
      self.path = randomVector()
    
    # Calculate velocity
    self.vel = pygame.Vector2(self.path - self.pos).normalize()*self.speed*deltaTime

  def updateEating(self):
    # Check if food or prey can be eaten
    for food in foods:
      if self.pos.distance_to(food.pos) <= self.size:
        foods.remove(food)
        self.newConsumer()
        
    preyList = self.makePreyList()
    for prey in preyList:
      if self.pos.distance_to(prey.pos) <= self.size:
        consumers.remove(prey)
        self.newConsumer()
        print("CANNIBALISM")

  def makePreyList(self): 
    # Adds the creatures that are small enough to the list to be eaten
    preyList = []
    for consumer in consumers:
      if self.size > 1.25 * consumer.size:
        preyList.append(consumer)
    return preyList
      
  def newConsumer(self):
    # Creates a new creature
    self.energy += 50
    if random.randint(1,reproductionChance) == 1:
      consumers.append(Consumer(self.pos, self.speed, self.senseRange, self.size))
  
  def pathFinding(self, target, smallest):
    # Sets the path to the closest target
    distance = self.pos.distance_to(target.pos)
    if distance < smallest:
      smallest = distance
    if distance <= self.senseRange and distance == smallest:
      self.path = target.pos
    return smallest

  def updatePosition(self):
    # Changes the position based on the current velocity
    self.pos = self.pos + self.vel

  def updateEnergy(self):
    # Decrease energy over time
    self.energy -= 0.25
    # Kills creature
    if self.energy <= 0:
      consumers.remove(self)


class Food(Entity):
  def __init__(self):
    super().__init__((255, 255, 0), 10)


def randomVector():
  # Generates a random vector
  return pygame.Vector2(random.randint(50, int(res.x) - 50), random.randint(50, int(res.y - 50)))

# Creates the inital list for creatures and food
foods = [Food() for x in range(foodAmount)]
consumers = [Consumer(randomVector(),150,60,7) for x in range(consumerAmount)]

# Starts the food generation
pygame.time.set_timer(CREATE_FOOD, 2500 - foodReduction)

def main():
  global foodReduction
  
  while True:
    surface.fill(backgroundColour)

    for event in pygame.event.get():
      # Closes the window
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      # Continues generating food every so often
      if event.type == CREATE_FOOD:
        foods.append(Food())
        foodReduction += 10
        pygame.time.set_timer(CREATE_FOOD, 1000 + foodReduction)

    # Combines the list of entities
    entities = foods + consumers

    # Draws each entity
    for entity in entities:
      entity.draw()
      entity.update()

    pygame.display.update()
    clock.tick(60)


