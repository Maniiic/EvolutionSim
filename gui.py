
from turtle import position
import pygame
import sys


pygame.init()
main_font = pygame.font.SysFont("cambira", 25)

class Button():
  def __init__(self, xPos, yPos, width, height, textInput):
    self.xPos = xPos
    self.yPos = yPos
    self.width = width
    self.height = height
    self.rect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)
    self.rect.center = (self.xPos, self.yPos)
    self.textInput = textInput
    self.text = main_font.render(self.textInput, True, "white")
    self.textRect = self.text.get_rect(center=(self.xPos, self.yPos))
    self.canClick = True

  def update(self, screen):
    pygame.draw.rect(screen, "dark gray", self.rect, 0, 5)
    screen.blit(self.text, self.textRect)

  def check_hover(self):
    mousePos = pygame.mouse.get_pos()
    if self.rect.collidepoint(mousePos):
      return True
    else:
      return False
    
  def check_click(self):
    leftClick = pygame.mouse.get_pressed()[0]
    if self.check_hover():
      if leftClick:
        if self.canClick:
          self.canClick = False
          return True
        else:
          return False
      else:
        self.canClick = True
