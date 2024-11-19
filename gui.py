
import pygame

pygame.init()
main_font = pygame.font.SysFont("cambira", 25)

class Button():
  def __init__(self, xPos, yPos, textInput, width=0 , height=60):
    self.xPos = xPos
    self.yPos = yPos
    # Sets the width to be based on the length of the text if not specified
    if width == 0:
      width = 10 * len(textInput) + 20
    self.width = width
    self.height = height
    # Creates a rectangle for the background of the button
    self.rect = pygame.Rect(self.xPos, self.yPos, self.width, self.height) 
    self.rect.center = (self.xPos, self.yPos)
    # Creates a rectangle for the text contained in the button
    self.textInput = textInput
    self.text = main_font.render(self.textInput, True, "white")
    self.textRect = self.text.get_rect(center=(self.xPos, self.yPos))
    # Used to check if mouse is clicked once
    self.canClick = True
  
  def update(self, screen):
    # Draw the button when it is updated
    pygame.draw.rect(screen, "dark gray", self.rect, 0, 5)
    screen.blit(self.text, self.textRect)

  def check_hover(self):
    # Check when the position of the mouse is above the button
    mousePos = pygame.mouse.get_pos()
    if self.rect.collidepoint(mousePos):
      return True
    else:
      return False
    
  def check_click(self):
    # Check when the the button is clicked
    leftClick = pygame.mouse.get_pressed()[0]
    if self.check_hover():
      if leftClick:
        if self.canClick: # Needed to prevent holding the mouse button repeatedly activating function
          self.canClick = False
          return True
        else:
          return False
      else:
        self.canClick = True
