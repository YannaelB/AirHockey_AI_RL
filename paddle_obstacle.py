import turtle as t
import random 
import pygame
import math
import random as rand
import os
import time
import sys


 

class Paddle():

    ### Constant 
    global WIDTH, HEIGHT, PUCK_SIZE,PADDLE_SIZE, OBSTACLE_SIZE, SPEED_CLOCK, WHITE, RED, BROWN, BLACK,BACKGROUND_color
    global GOAL_x0, GOAL_x1, GOAL_y0, GOAL_y1

    # metric and time 
    WIDTH = 500
    HEIGHT = 650
    PUCK_SIZE = 20 #Diameter Puck
    PADDLE_SIZE = 100 # Paddle length 
    OBSTACLE_SIZE = 100 # Obstacle length
    SPEED_CLOCK = 15
    GOAL_x0, GOAL_x1, GOAL_y0, GOAL_y1 = 3*WIDTH/10, 7*WIDTH/10 , 0, HEIGHT/40

    # rgb colors
    WHITE = (255, 255, 255)
    RED = (200,55,55)
    BROWN = (122, 115, 81)
    BLACK = (0,0,0)
    BACKGROUND_color = (252, 235, 151)

    def __init__(self):

        # Init 

        self.done = False
        self.reward = 0
        self.goal = 0
        self.total_goal = 0
        self.hit = 0
        self.total_hit, self.miss = 0, 0


        

        # Setup Background

        pygame.init()

        #gamelogo = pygame.image.load(os.path.join(auxDirectory, 'AHlogo.png'))
        gamelogo = pygame.image.load(os.path.join('Yakologo.png'))
        pygame.display.set_icon(gamelogo)

        pygame.display.set_caption('AirHockey AI')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.smallfont = pygame.font.SysFont("comicsans", 25)
        self.roundfont = pygame.font.SysFont("comicsans", 45)  
        

        self.clock = pygame.time.Clock()

    
        # Paddle
        self.paddlex = WIDTH/2
        self.paddley = 9*HEIGHT/10
        self.paddledx = 33

    
        # Ball
        self.puckx = random.randint(int(WIDTH/3),int(2*WIDTH/3))
        self.pucky = random.randint(int(HEIGHT/8),int(HEIGHT/2))
        self.puckangle = rand.uniform(math.pi/3, 2*math.pi/3)
        self.puckdx = 25
        self.puckdy = 25

        # Moving obstacle

        self.obstaclx = WIDTH/2
        self.obstacly = int(3*HEIGHT/10)
        self.obstacldx = 15
        self.obstacldy = 15





    # Paddle movement
    def paddle_right(self):
        if self.paddlex < WIDTH-PADDLE_SIZE/2:
            self.paddlex +=  self.paddledx

    def paddle_left(self):
        if self.paddlex > PADDLE_SIZE/2 :
            self.paddlex -=  self.paddledx

    # Iteration of the game
    def run_frame(self):

        #Make the puck move at each iteration depending on his direction
        self.puckx +=  int(math.cos(self.puckangle)*self.puckdx)
        self.pucky += int(math.sin(self.puckangle)*self.puckdy)


        # Obstacle moving
        move =  rand.randint(1,2)
        if move == 1:
            self.obstaclx += rand.randint(-1,1)*self.obstacldx
            self.obstacly += rand.randint(-1,1)*self.obstacldy

        
        


        # Puck and Wall collision
        if self.puckx > WIDTH - PUCK_SIZE:
            self.puckx = WIDTH - PUCK_SIZE
            self.puckdx *= -1

        if self.puckx < PUCK_SIZE :
            self.puckx = 0 + PUCK_SIZE
            self.puckdx *= -1

        # Puck and Obstacle collision
        if ((self.puckx-self.obstaclx)**2 + (self.pucky-self.obstacly)**2)**0.5 < OBSTACLE_SIZE/2 + PUCK_SIZE/2:
            n = random.randint(0,9)
            self.puckangle = ((-1)**n)*rand.uniform(math.pi/3, 2*math.pi/3) #to throw back randomly the puck
        

        # Obstacle and wall collision

        if self.obstacly < HEIGHT/3:
            self.obstacly = HEIGHT/3

        if self.obstacly > HEIGHT/2:
            self.obstacly = HEIGHT/2

        if self.obstaclx < WIDTH/3 + OBSTACLE_SIZE/2:
            self.obstaclx = WIDTH/3 + OBSTACLE_SIZE/2

        if self.obstaclx > 2*WIDTH/3 - OBSTACLE_SIZE/2:
            self.obstaclx = 2*WIDTH/3 - OBSTACLE_SIZE/2
                

        ## Puck goal 1
        if (self.puckx + PUCK_SIZE/2 >= GOAL_x0 and self.puckx - PUCK_SIZE/2 <= GOAL_x1 and self.pucky < GOAL_y1 + PUCK_SIZE):
            self.puckangle *= -1
            #self.pucky += PUCK_SIZE/2
            self.goal += 1
            self.reward += 1
            self.total_goal += 1
            #print("GOOOAAALLLL")
            text = pygame.font.Font('arial.ttf', 40).render("GOAL !", True, BLACK)
            self.screen.blit(text, [WIDTH/2-65, HEIGHT/2-15])
            pygame.display.flip()
            time.sleep(0.3)
            self.reset()

        if self.pucky < 0 + PUCK_SIZE :
            self.pucky = PUCK_SIZE
            self.puckangle *= -1
            self.reward -= 0.3

        # Puck Goal 2 (AI)

        if self.pucky + PUCK_SIZE > HEIGHT and self.puckx > GOAL_x0 and self.puckx < GOAL_x1:
            self.miss += 1
            self.reward -= 1
            self.done = True
            self.hit = 0
            self.goal = 0
            self.reset()

        if self.pucky + PUCK_SIZE >  HEIGHT :
            self.pucky -= PUCK_SIZE
            self.puckangle *= -1
            #self.reward -= 0.1

        # Puck Paddle collision

        if  (self.paddley - self.pucky - self.puckdy/2) <= PUCK_SIZE/2 and abs(self.paddlex - self.puckx - self.puckdx/2) <= PADDLE_SIZE/2:
            self.pucky -= PUCK_SIZE
            #to make the puck direction after collision depending on where it arrives on the paddle. It allows the paddle to attack accordinf to his position
            self.puckangle = -(self.puckangle/abs(self.puckangle))*(math.pi/2 + math.pi*abs(self.puckx-self.paddlex)/(3*PADDLE_SIZE/2)) #angle between Pi/2 and 5*Pi/6
            self.hit += 1
            self.total_hit += 1
            self.reward += 0 #no reward cause we want him to attack no defend his goal, so only negative reward if he can't

        if self.hit >= 100:
            print("reached 100 hit => reset")
            self.hit = 0
            self.done = True
        

    #Print screen
    def update_screen(self):
        # Render Logic
        self.screen.fill(BACKGROUND_color)
        # center circle
        pygame.draw.circle(self.screen,WHITE, (WIDTH / 2, HEIGHT / 2), 70, 5)
        # borders
        pygame.draw.rect(self.screen, WHITE, (0, 0, WIDTH, HEIGHT), 6)
        # Goal 1
        pygame.draw.rect(self.screen, (250, 233, 149), (GOAL_x0, GOAL_y0,GOAL_x1-GOAL_x0, GOAL_y1), 0)
        #text = pygame.font.Font('arial.ttf', 20).render(" GOAL 1 ", True, WHITE)
        #self.screen.blit(text, [int(WIDTH/2) - 35, int(GOAL_y1/2)-10])
        # Goal 2
        pygame.draw.rect(self.screen, (250, 233, 149), (GOAL_x0, HEIGHT - GOAL_y1,GOAL_x1-GOAL_x0, HEIGHT ), 0)
        # Divider
        pygame.draw.rect(self.screen, WHITE, (0,HEIGHT / 2, WIDTH, 6))
        # Puck
        pygame.draw.circle(self.screen, RED, (self.puckx, self.pucky), PUCK_SIZE/2, 0,True,True,True,True)
        # Paddle
        pygame.draw.rect(self.screen, BROWN, pygame.Rect(self.paddlex-int(PADDLE_SIZE/2), self.paddley , PADDLE_SIZE, int(PADDLE_SIZE/5)))
        pygame.draw.ellipse(self.screen, BROWN, pygame.Rect(self.paddlex-int(PADDLE_SIZE/2), self.paddley - int(PADDLE_SIZE/5)  , PADDLE_SIZE, int(PADDLE_SIZE/2)))
        text = pygame.font.Font('arial.ttf', 20).render(" AI ", True, BLACK)
        self.screen.blit(text, [self.paddlex-15, self.paddley-15])

        # Obstacle
        pygame.draw.circle(self.screen, BROWN, (self.obstaclx, self.obstacly), OBSTACLE_SIZE/2, 0,True,True,True,True)

        # Score evolution information
        text = pygame.font.Font('arial.ttf', 20).render(" Miss : " + str(self.miss), True, BLACK)
        self.screen.blit(text, [10, 10])
        text = pygame.font.Font('arial.ttf', 20).render( " total hit : " + str(self.total_hit), True, BLACK)
        self.screen.blit(text, [10, 35])
        text = pygame.font.Font('arial.ttf', 20).render("hit : " + str(self.hit), True, BLACK)
        self.screen.blit(text, [10, 60])
        text = pygame.font.Font('arial.ttf', 20).render("Goal : " + str(self.goal), True, BLACK)
        self.screen.blit(text, [WIDTH - 80, 10])
        text = pygame.font.Font('arial.ttf', 20).render("total Goal : " + str(self.total_goal), True, BLACK)
        self.screen.blit(text, [WIDTH - 140, 35])
        pygame.display.flip()
    
        



    # ------------------------ AI control ------------------------

    # 0 move left
    # 1 do nothing
    # 2 move right

    def reset(self):
        self.puckx = random.randint(int(WIDTH/3),int(2*WIDTH/3))
        self.pucky = int(HEIGHT/2)
        #self.pucky = random.randint(int(HEIGHT/5),int(HEIGHT/2))
        self.puckangle = rand.uniform(math.pi/3, 2*math.pi/3)
        self.puckdx = 25
        self.puckdy = 25

        self.paddlex = int(WIDTH/2)
        self.paddley = int(9*HEIGHT/10)

        self.obstacly = int(1*HEIGHT/3)
        self.obstaclx = int(WIDTH/2)
    
        # we send normalize data (between 0 and 1, even for puck_direction)
        return [self.paddlex/WIDTH, self.puckx/WIDTH, self.pucky/HEIGHT, 0.5*(math.cos(self.puckangle)*self.puckdx)/self.puckdx+0.5, 0.5*(math.sin(self.puckangle)*self.puckdy)/self.puckdy+0.5,self.obstaclx/WIDTH, self.obstacly/HEIGHT]

    def step(self, action):

        self.reward = 0
        self.done = 0

        if action == 0:
            self.paddle_left()
            self.reward -= 0 # You can penalize the paddle for moving, useful according to cases

        if action == 2:
            self.paddle_right()
            self.reward -= 0 

        self.run_frame()  

        
            

        # Markov state of the environment, essential for the agent
        state =  [self.paddlex/WIDTH, self.puckx/WIDTH, self.pucky/HEIGHT, 0.5*(math.cos(self.puckangle)*self.puckdx)/self.puckdx+0.5, 0.5*(math.sin(self.puckangle)*self.puckdy)/self.puckdy+0.5,self.obstaclx/WIDTH, self.obstacly/HEIGHT]

        # update ui and clock
        #if self.total_hit//5 == 0: this function is useful for training, to not refresh the screen while training (or sometimes for checking thanks to //5), only for playing
        self.update_screen()
        self.clock.tick(SPEED_CLOCK)

        # return game over and score
        return self.reward, state, self.done,self.hit,self.goal,self.total_hit