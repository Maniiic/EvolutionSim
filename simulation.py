
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
margin = 50

# Constants
white = (255, 255, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)

foodAmount = 0
consumerAmount = 10
consumerStartSpeed = 150
consumerStartRange = 60
consumerStartSize = 7
speedVariance = 10
senseVariance = 10
sizeVariance = 1
reproductionChance = 2 # 1 / reproductionChance

# Pygame event
CREATE_FOOD = pygame.USEREVENT + 1


class Entity:
  def __init__(self, col, size):
    self.pos = random_vector()
    self.col = col
    self.size = size

  def draw(self):
    pygame.draw.circle(surface, self.col, self.pos, self.size)


class Consumer(Entity):
  def __init__(self,pos,speed,senseRange,size):
    super().__init__((255, 255, 255), size + random.randint(-sizeVariance,sizeVariance)) # Attributes shared by classes
    self.pos = pos
    self.path = random_vector()
    self.energy = 100
    
    # Initial traits
    self.speed = speed + random.randint(-speedVariance, speedVariance)
    self.senseRange = senseRange + random.randint(-senseVariance, senseVariance)

    print("speed: ",self.speed,"sense: ",self.senseRange,"size: ",self.size)

  def update(self):
    self.update_vel()
    self.update_position()
    self.update_eating()
    self.update_energy()

  def update_vel(self):
    smallest = math.inf
    preyList = self.make_prey_list()
    # Check for closest food/prey
    for food in foods:
      smallest = self.path_finding(food,smallest)
    for prey in preyList:
      smallest = self.path_finding(prey,smallest)

    # Check if creature has reached its destination
    if self.pos.distance_to(self.path) <= self.size:
      self.path = random_vector()
    
    # Calculate velocity
    self.vel = pygame.Vector2(self.path - self.pos).normalize()*self.speed*deltaTime

  def update_eating(self):
    # Check if food or prey can be eaten
    for food in foods:
      if self.pos.distance_to(food.pos) <= self.size:
        foods.remove(food)
        self.new_consumer()
        
    preyList = self.make_prey_list()
    for prey in preyList:
      if self.pos.distance_to(prey.pos) <= self.size:
        consumers.remove(prey)
        self.new_consumer()
        print("CANNIBALISM")

  def make_prey_list(self): 
    # Adds the creatures that are small enough to the list to be eaten
    preyList = []
    for consumer in consumers:
      if self.size > 1.25 * consumer.size:
        preyList.append(consumer)
    return preyList
      
  def new_consumer(self):
    # Creates a new creature
    self.energy += 50
    if random.randint(1,reproductionChance) == 1:
      consumers.append(Consumer(self.pos, self.speed, self.senseRange, self.size))
  
  def path_finding(self, target, smallest):
    # Sets the path to the closest target
    distance = self.pos.distance_to(target.pos)
    if distance < smallest:
      smallest = distance
    if distance <= self.senseRange and distance == smallest:
      self.path = target.pos
    return smallest

  def update_position(self):
    # Changes the position based on the current velocity
    self.pos = self.pos + self.vel

  def update_energy(self):
    # Decrease energy over time
    self.energy -= 0.25
    # Kills creature
    if self.energy <= 0:
      consumers.remove(self)


class Food(Entity):
  def __init__(self):
    super().__init__((255, 255, 0), 10)


def random_vector():
  # Generates a random vector position within the window
  return pygame.Vector2(random.randint(margin, res.x - margin), random.randint(margin, res.y - margin))


# Creates the inital list for creatures and food
foods = [Food() for _ in range(foodAmount)]
consumers = [Consumer(random_vector(), consumerStartSpeed, consumerStartRange, consumerStartSize) for _ in range(consumerAmount)]

def main():
  foodReduction = 0

  # Starts the food generation
  pygame.time.set_timer(CREATE_FOOD, 2500 - foodReduction)

  pygame.display.set_caption("Simulation")
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
      if type(entity) == Consumer:
        entity.update()

    pygame.display.update()
    clock.tick(60)