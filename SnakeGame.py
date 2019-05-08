from processing import * 

import random 


# foods go in here...
food_list = []

# tails list 
tails = []

# setup the game screen 
gs = [448, 448]


# in this check collision, we check against the rectangle (a) against rectangle (b)
def check_col(a, b):

  if a.x < b.x + b.w and a.x + a.w > b.x and a.y < b.y + b.h and a.h + a.y > b.y:
      
    
    return True
  return False  

class Tail:
  
  def __init__(self):
    
    if len(tails) == 0:
      
      #  set the target to be the head itself
      self.target = head

      self.dir = head.dir
      
      if head.dir == 3:
        
        self.x = head.x
        self.y = head.y - 16
      
      elif head.dir == 2:
        self.x = head.x + 16
        self.y = head.y 
        
      elif head.dir == 1:
        self.x = head.x 
        self.y = head.y + 16
        
      elif head.dir == 0:
        self.x = head.x - 16
        self.y = head.y
      
      
      self.index = 0
    
    else:

      self.index = len(tails)
      
      # we should follow the tail ahead of us..
      self.target = tails[self.index - 1]
      
      self.dir = tails[self.index - 1].dir
      
      self.x = tails[self.index - 1].x
      self.y = tails[self.index - 1].y
      
    # THE Tail speed should be the same as the head speed
    self.speed = head.speed  
    # follow max and a follow cur
    self.follow_max = 8
    self.follow_cur = 0
      
    self.w = 16
    self.h = 16
    self.color = ( random.randint(0, 254), random.randint(0, 254), random.randint(0, 254))
    
    tails.append(self)
  

  
  # update of the tail 
  def update(self):
    
    # the first tail segment should always be behind the target..
    if self.target.dir == 3:
      self.x = self.target.x
      self.y = self.target.y - 16
    
    elif self.target.dir == 2:
      self.x = self.target.x + 16
      self.y = self.target.y 
      
    elif self.target.dir == 1:
      self.x = self.target.x 
      self.y = self.target.y + 16
      
    elif self.target.dir == 0:
      self.x = self.target.x - 16
      self.y = self.target.y
        
    if self.follow_cur < self.follow_max:
        
      self.move()
      
      # you only have to follow as far as you need to move 
      # to catch up to the next piece of the snake
      self.follow_cur += 1
     
    # else of the update of the tail 
    else:
      
      self.follow_cur = 0
      
      self.dir = self.target.dir

    
  
  def move(self):
    
    if self.dir == 0:
      
      self.x += self.speed 
    
    elif self.dir == 1:
      self.y -= self.speed 
    
    elif self.dir == 2:
      self.x -= self.speed 
    
    else:
      self.y += self.speed 
        
    
    # blip the tail... 
    if self.x < -10:
      self.x = 510
      
    if self.x > 512:
      self.x = 0
      
    if self.y < -10:
      self.y = 510
      
    if self.y > 512:
      self.y = 0    
        
    
  def draw(self):
    
    fill(*self.color)
    rect(self.x, self.y, self.w, self.h)

class Food:
  
  def __init__(self):
    
    self.x = random.randint(16, gs[0] - 32)
    self.y = random.randint(16, gs[1] - 32)
    
    self.w = 16
    self.h = 16
    
    self.color = ( random.randint(0, 254), random.randint(0, 254), random.randint(0, 254))
    
    food_list.append(self)
    
  def draw(self):
    
    fill( *self.color )
    rect( self.x, self.y, self.w, self.h )

class Head:
  
  def __init__( self ):
    
    self.x = random.randint(64, 328)
    self.y = random.randint(64, 328)
    
    self.w = 16
    self.h = 16
    
    self.dir = 0
    self.speed = 1
    self.score = 0
    self.color = ( 60, 250, 60)
    
    self.dead = False 
   
   
  def check_fail(self):
    
    for item in range(1, len(tails) ):
      
      if check_col(self, tails[item]):
        
        self.dead = True
        self.speed = 0
        self.color = (255, 0, 0)
      
    
    
  # in the head update...   
  def update(self):
    

    
    if check_col(self, food_list[0]):
      food_list.pop()
      
      Food()
      
      # make a tail 
      Tail()
      
      self.score += 1
    
    if self.dir == 0:
      
      self.x += self.speed 
    
    elif self.dir == 1:
      self.y -= self.speed 
    
    elif self.dir == 2:
      self.x -= self.speed 
    
    else:
      self.y += self.speed 
      
    # blip the player... 
    if self.x < -10:
      self.x = 510
      
    if self.x > 512:
      self.x = 0
      
    if self.y < -10:
      self.y = 510
      
    if self.y > 512:
      self.y = 0    
    
    
    if len(tails) > 1:
      
      self.check_fail()
    
    
  def draw(self):
    
    if self.dead:
      
      # draw the score
      textSize(100)
      fill(*food_list[0].color)
      text( "DEAD",  128, 128)
      
    # draw the score
    textSize(self.score)
    fill(*food_list[0].color)
    text( "SCORE: " + str(self.score),  64, 64)
    
    # draw the head
    fill(*self.color)
    rect(self.x, self.y, self.w, self.h)
    
    # prepare black color
    fill(0, 0, 0)
    if self.dir == 0:
      
      rect( self.x + self.w / 2 + 2, self.y + self.h / 4,     6, 2  )
      rect( self.x + self.w / 2 + 2, self.y + self.h / 4 + 6, 6, 2  )
      
    elif self.dir == 2:

      rect( self.x,  self.y + self.h / 4 ,    6, 2 )
      rect( self.x,  self.y + self.h / 4 + 6, 6, 2 )
      
    elif self.dir == 1:
      
      rect( self.x +  self.w / 4,      self.y,  2, 6)
      rect( self.x +  self.w / 4 + 6,  self.y,  2, 6)
      
    elif self.dir == 3:
      
      rect( self.x +  self.w / 4,      self.y + self.h / 2 + 2,  2, 6)
      rect( self.x +  self.w / 4 + 6,  self.y + self.h / 2 + 2,  2, 6)
      
# global setup area 
def setup():
  
  size( gs[0], gs[1])
  
  global head
  head = Head()
  # make a Food
  Food()
  
# global draw area 
def draw():
  
  background(100, 150, 255)
  
  # update and draw the head... 
  head.update()
  head.draw()
  
  # draw the foods 
  for food in food_list:
    
    food.draw()
    
  for tail in tails:
    tail.update()
    tail.draw()
  
def keyPressed():
  
  if key == "d":
    head.dir = 0
  elif key == "a":
    head.dir = 2
    
  elif key == "w":
    head.dir = 1
  elif key == "s":
    head.dir = 3
    

  
  
draw 
run()
