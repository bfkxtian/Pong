import pygame, math
#(mostly) classic game of pong

#program constants
white=(255,255,255)
black=(0,0,0)
width,height=1280,720 #screen dimensions
ballsize=20 #size of ball
displacement=12 #standard unit of movement
paddle,halfPaddle=(15,70),35 #paddle dimensions

#pygame boilerplate
pygame.init() #intialise pygame
win=pygame.display.set_mode((width,height))
pygame.display.set_caption("Pong")
clock=pygame.time.Clock()
font=pygame.font.Font('IBM.ttf',20) #import font
blip=pygame.mixer.Sound('blip.wav') #import sound

#class for player
class Player:
    score=0
    def __init__(self,x):
        self.rect=pygame.Rect((x,(height//2)-halfPaddle),paddle)
        self.moving=0; #1 = up, -1 = down
    def move(self):
        if self.moving==1:
            if self.rect.top>0:
                self.rect.move_ip(0,-displacement) #move paddle vertically
        if self.moving==-1:
            if self.rect.bottom<height:
                self.rect.move_ip(0,displacement) #move paddle vertically

#class for ball
class Ball:
    def __init__(self):
        self.rect=pygame.Rect((width//2,height//2),(ballsize,ballsize))
        self.velocity=[displacement,0]
    def collisions(self): #determine and compute collisions
        if self.rect.colliderect(p1.rect): #check collision with p1
            self.velocity[1]+=(self.rect.centery-p1.rect.centery)/halfPaddle*displacement
            self.velocity[0]=math.sqrt((displacement*displacement)-(self.velocity[1]*self.velocity[1]))
            blip.play()
        if self.rect.colliderect(p2.rect): #check collision with p2
            self.velocity[1]+=(self.rect.centery-p2.rect.centery)/halfPaddle*displacement
            self.velocity[0]=-math.sqrt((displacement*displacement)-(self.velocity[1]*self.velocity[1]))
            blip.play()
        if self.rect.top<0 or self.rect.bottom>height: #check collision with boundary
            self.velocity[1]*=-1 #reflect ball vertically
    def score(self):
        if self.rect.left<0: #scores for p2
            p2.score+=1
            reset_field()
        if self.rect.right>width: #scores for p1
            p1.score+=1
            reset_field()
    def move(self): #move the ball using given velocity
        self.rect.move_ip(int(self.velocity[0]),int(self.velocity[1]))

#game objects
p1,p2=Player(10),Player(width-10-paddle[0]) #create player objects
b=Ball() #create ball object

#drawing function
def draw():
    win.fill(black) #blank screen
    pygame.draw.rect(win,white,p1.rect)
    pygame.draw.rect(win,white,p2.rect)
    pygame.draw.rect(win,white,b.rect)
    if p1.score<10: #to avoid drawing '10'
        txt_score1=font.render('P1 = {}'.format(p1.score),True,white)
        win.blit(txt_score1,(10,10))
    if p2.score<10:
        txt_score2=font.render('P2 = {}'.format(p2.score),True,white)
        win.blit(txt_score2,(width-130,10))

#reset function
def reset_field():
    b.__init__()
    p1.__init__(10)
    p2.__init__(width-10-paddle[0])

#game code function
def update():
    p1.move()
    if b.rect.centery<p2.rect.centery:
        p2.rect.move_ip(0,-displacement)
    if b.rect.centery>p2.rect.centery:
        p2.rect.move_ip(0,displacement)
    b.collisions()
    b.score()
    b.move() #move ball

def main():
    running=1
    while running:
        #key handling
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=0
            #handle keydown
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    running=0
                if event.key==pygame.K_o:
                    p2.moving=1
                if event.key==pygame.K_l:
                    p2.moving=-1
                if event.key==pygame.K_w:
                    p1.moving=1
                if event.key==pygame.K_s:
                    p1.moving=-1
            #handle keyup
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_o or pygame.K_l:
                    p2.moving=0
                if event.key==pygame.K_w or pygame.K_s:
                    p1.moving=0
        #check game scores
        if p1.score>9 or p2.score>9:
            running=0
        update() #update the game state
        draw() #draw next frame in memory
        pygame.display.flip() #push everything to display
        clock.tick(60) #60fps
main()
pygame.quit() #quit python and pygame
