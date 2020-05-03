import pygame, math
#program parameters
tmp = input( "[S]ingleplayer/[M]ultiplayer: " )
if tmp == 'S':
    singleplayer = True
if tmp == 'M':
    singleplayer = False
winsize = ( 1280, 720 )
paddlesize = ( 15, 70 )
ballsize = ( 20, 20 )
displacement = 10
#some colors
WHITE = ( 255, 255, 255 )
BLACK = ( 0, 0, 0 )
#pygame boilerplate
pygame.init( ) #start pygame
pygame.mixer.init( ) #sound module
win = pygame.display.set_mode( winsize ) #create drawing surface
pygame.display.set_caption( "Pong" ) #set win define
clock = pygame.time.Clock( ) #python clock
font = pygame.font.Font( 'IBM.ttf', 20 ) #font for rendering
blip = pygame.mixer.Sound( 'blip.wav' )
#class for player
class Player:
    score = 0;
    def __init__( self, x ):
        self.rect = pygame.Rect( ( x, int( winsize[ 1 ] / 2 ) - int( paddlesize[ 1 ] / 2 ) + int( ballsize[ 1 ] / 2 ) ), paddlesize ) #centering paddles and ball is quite annoying
        self.moving = 0; #1 = up, -1 = down
    def move( self ):
        if self.moving == 1:
            if self.rect.top > 0:
                self.rect.move_ip( 0, -displacement )
        if self.moving == -1:
            if self.rect.bottom < winsize[ 1 ]:
                self.rect.move_ip( 0, displacement )
p1, p2 = Player( 10 ), Player( int( winsize[ 0 ] - 10 - paddlesize[ 0 ] ) ) #create player objects
#class for ball
class Ball:
    def __init__( self ):
        self.rect = pygame.Rect( ( int( winsize[ 0 ] / 2 ), int( winsize[ 1 ] / 2 ) ), ballsize )
        self.velocity = [ displacement, 0 ] #velocity array for ball
    def collisions( self ):
        if self.rect.colliderect( p1.rect ): #check collision with p1
            self.velocity[ 1 ] += displacement * ( self.rect.centery - p1.rect.centery ) / ( paddlesize[ 1 ] / 2 )
            self.velocity[ 0 ] *= -1
            blip.play( )
        if self.rect.colliderect( p2.rect ): #check collision with p2
            self.velocity[ 1 ] += displacement * ( self.rect.centery - p2.rect.centery ) / ( paddlesize[ 1 ] / 2 )
            self.velocity[ 0 ] *= -1
            blip.play( )
        if self.rect.top < 0 or self.rect.bottom > winsize[ 1 ]: #check collision with boundary
            self.velocity[ 1 ] *= -1 #reflect ball vertically
    def score( self ):
        if self.rect.left < 0: #scores for p2
            p2.score += 1
            reset_field( )
        if self.rect.right > winsize[ 0 ]: #scores for p1
            p1.score += 1
            reset_field( )
    def move( self ): #move the ball using given velocity
        self.rect.move_ip( int( self.velocity[ 0 ] ), int( self.velocity[ 1 ] ) )
b = Ball( ) #create ball object
#function to draw in pygame
def draw( ):
    win.fill( BLACK ) #blank screen
    pygame.draw.rect( win, WHITE, p1.rect )
    pygame.draw.rect( win, WHITE, p2.rect )
    pygame.draw.rect( win, WHITE, b.rect )
    if p1.score < 10: #to avoid drawing '10'
        txt_score1 = font.render( 'P1 = {}'.format( p1.score ), True, WHITE )
        win.blit( txt_score1, ( 10, 10 ) )
    if p2.score < 10:
        txt_score2 = font.render( 'P2 = {}'.format( p2.score ), True, WHITE )
        win.blit( txt_score2, ( winsize[ 0 ] - 130, 10 ) )
#reset field data when called
def reset_field( ):
    b.__init__( )
    p1.__init__( 10 )
    p2.__init__( int( winsize[ 0 ] - 10 - paddlesize[ 0 ] ) )
#update game data
def update( ):
    p1.move( ) #move player 1
    if singleplayer:
        if b.rect.centery < p2.rect.centery:
            p2.rect.move_ip( 0, -displacement )
        if b.rect.centery > p2.rect.centery:
            p2.rect.move_ip( 0, displacement )
    else:
        p2.move( ) #move player 2
    b.collisions( )
    b.score( ) #ball related functions
    b.move( )
#set game flag and enter main loop
running = True
while running:
    clock.tick( 60 ) #60fps
    if p1.score > 9 or p2.score > 9:
        running = False
    for event in pygame.event.get( ):
        if event.type == pygame.QUIT:
            running = False
        #handle keydown
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w:
                p1.moving = 1
            if event.key == pygame.K_s:
                p1.moving = -1
            if event.key == pygame.K_o:
                p2.moving = 1
            if event.key == pygame.K_l:
                p2.moving = -1
        #handle keyup
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                p1.moving = 0
            if event.key == pygame.K_s:
                p1.moving = 0
            if event.key == pygame.K_o:
                p2.moving = 0
            if event.key == pygame.K_l:
                p2.moving = 0
    update( ) #compute game data
    draw( ) #draw next frame
    pygame.display.flip( ) #push everything to display
pygame.quit( ) #quit pygame
