import pygame, socket
#classic game of pong
port = 1500 #default port binding
def setup( ):
    mode = input( "[S]ingleplayer/[M]ultiplayer: " )
    if mode == 's' or mode == 'S':
        print( "Starting Singleplayer Game..." )
        return 0
    elif mode == 'm' or mode == 'M':
        print( "Starting Multiplayer Game..." )
        side = input( "[S]erver/[C]lient: ")
        global s 
        s = socket.socket( ) #create socket object
        #setup as server
        if side == 's' or side == 'S':
            host = socket.gethostname( )
            print( "Your IP is {}".format( host ) )
            s.bind( ( host, port ) )
            s.listen( )
            print( "Waiting for client." )
            global c
            c, addr = s.accept( ) #accept incoming connection
            print( "Connected to {}".format( addr ) )
            return 1
        #setup as client
        elif side == 'c' or side == 'C':
            host = input( "Enter server IP: " )
            s.connect( ( host, port ) ) #connect to server
            return 2
        else:
            setup() #back to top
    else:
        setup() #back to top
mode = setup( ) #setup singleplayer/multiplayer

#some variables
WHITE = ( 255, 255, 255 )
BLACK = ( 0, 0, 0 )
width, height = 1280, 720 #screen dimensions
ballsize = 20 #ball size
displacement = 10 #standard unit of movement
paddle, halfPaddle = ( 15, 70 ), 35 #paddle dimensions

#pygame boilerplate
pygame.init( ) #start pygame
pygame.mixer.init( ) #sound module
win = pygame.display.set_mode( ( width, height ) ) #create drawing surface
if mode == 0: pygame.display.set_caption( "Pong" )
if mode == 1: pygame.display.set_caption( "Pong: Client" )
if mode == 2: pygame.display.set_caption( "Pong: Server" )
clock = pygame.time.Clock( ) #pygame clock
font = pygame.font.Font( 'IBM.ttf', 20 ) #font for rendering
blip = pygame.mixer.Sound( 'blip.wav' ) #paddle sound

#class for player
class Player:
    score = 0
    def __init__( self, x ):
        self.rect = pygame.Rect( ( x, ( height // 2 ) - halfPaddle ), paddle )
        self.moving = 0; #1 = up, -1 = down
    def move( self ):
        if self.moving == 1:
            if self.rect.top > 0:
                self.rect.move_ip( 0, -displacement )
        if self.moving == -1:
            if self.rect.bottom < height:
                self.rect.move_ip( 0, displacement )

#class for ball
class Ball:
    def __init__( self ):
        self.rect = pygame.Rect( ( width // 2, height // 2 ), ( ballsize, ballsize ) )
        self.velocity = [ displacement, 0 ]
    def collisions( self ): #ball velocity must remain at 1 - need trigonometry
        if self.rect.colliderect( p1.rect ): #check collision with p1
            self.velocity[ 1 ] += displacement * ( self.rect.centery - p1.rect.centery ) / halfPaddle
            self.velocity[ 0 ] *= -1
            blip.play( )
        if self.rect.colliderect( p2.rect ): #check collision with p2
            self.velocity[ 1 ] += displacement * ( self.rect.centery - p2.rect.centery ) / halfPaddle
            self.velocity[ 0 ] *= -1
            blip.play( )
        if self.rect.top < 0 or self.rect.bottom > height: #check collision with boundary
            self.velocity[ 1 ] *= -1 #reflect ball vertically
    def score( self ):
        if self.rect.left < 0: #scores for p2
            p2.score += 1
            reset_field( )
        if self.rect.right > width: #scores for p1
            p1.score += 1
            reset_field( )
    def move( self ): #move the ball using given velocity
        self.rect.move_ip( int( self.velocity[ 0 ] ), int( self.velocity[ 1 ] ) )

#game objects
p1, p2 = Player( 10 ), Player( width - 10 - paddle[ 0 ] ) #create player objects
b = Ball( ) #create ball object

#drawing function
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
        win.blit( txt_score2, ( width - 130, 10 ) )

#reset function
def reset_field( ):
    b.__init__( )
    p1.__init__( 10 )
    p2.__init__( width - 10 - paddle[ 0 ] )

#game code function
def update( ):
    #singleplayer
    if mode == 0:
        p1.move( )
        if b.rect.centery < p2.rect.centery:
            p2.rect.move_ip( 0, -displacement )
        if b.rect.centery > p2.rect.centery:
            p2.rect.move_ip( 0, displacement )
    #client
    elif mode == 1:
        p2.move( )
        c.send( str( p2.moving ).encode( ) )
        p1.moving = int( c.recv( 1024 ) ) #retrieve opponent data
        if p1.moving == 1:
            p1.rect.move_ip( 0, -displacement )
        elif p1.moving == -1:
            p1.rect.move_ip( 0, displacement )
    #server
    elif mode == 2:
        p1.move( )
        s.send( str( p1.moving ).encode( ) )
        p2.moving = int( s.recv( 1024 ) ) #retrieve opponent data
        if p2.moving == 1:
            p2.rect.move_ip( 0, -displacement )
        elif p2.moving == -1:
            p2.rect.move_ip( 0, displacement )
    b.collisions( )
    b.score( ) #ball related functions
    b.move( )

#main loop
def main( ):
    running = 1 #initially running
    while running:
        clock.tick( 60 ) #60fps
        #key handling
        for event in pygame.event.get( ):
            if event.type == pygame.QUIT:
                running = 0
            #handle keydown
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = 0
                if event.key == pygame.K_o:
                    p2.moving = 1
                if event.key == pygame.K_l:
                    p2.moving = -1
                if event.key == pygame.K_w:
                    p1.moving = 1
                if event.key == pygame.K_s:
                    p1.moving = -1
            #handle keyup
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_o:
                    p2.moving = 0
                if event.key == pygame.K_l:
                    p2.moving = 0
                if event.key == pygame.K_w:
                    p1.moving = 0
                if event.key == pygame.K_s:
                    p1.moving = 0
        #check game scores
        if p1.score > 9 or p2.score > 9:
            running = 0
        update( ) #update the game state
        draw( ) #draw next frame in memory
        pygame.display.flip( ) #push everything to display
main( )

if mode != 0:
    s.close( ) #close the client connection
    print( "Closed connection." )
pygame.quit( ) #quit pygame