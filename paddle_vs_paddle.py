import turtle as t
import random 
import pygame
import math
import random as rand
import os





class Paddle():

    ### Constant 
    global WIDTH, HEIGHT, PUCK_SIZE,PADDLE_SIZE, OBSTACLE_SIZE, SPEED_CLOCK, WHITE, RED, BLUE, BLACK,BACKGROUND_color
    global GOAL_x0, GOAL_x1, GOAL_y0, GOAL_y1

    # metric un time 
    WIDTH = 500
    HEIGHT = 700
    PUCK_SIZE = 20 # Diameter Puck
    PADDLE_SIZE = 100 # Paddle length 
    OBSTACLE_SIZE = 80 # Obstacle length
    SPEED_CLOCK = 15
    GOAL_x0, GOAL_x1, GOAL_y0, GOAL_y1 = 4*WIDTH/10, 6*WIDTH/10 , 0, HEIGHT/20

    # rgb colors
    WHITE = (255, 255, 255)
    RED = (200,55,55)
    BLUE = (122, 115, 81)
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

        # self.win = t.Screen()
        # self.win.title('Paddle')
        # self.win.bgcolor('black')
        # self.win.setup(width=600, height=600)
        # self.win.tracer(0)

        pygame.init()


        #gamelogo = pygame.image.load(os.path.join(auxDirectory, 'AHlogo.png'))
        gamelogo = pygame.image.load(os.path.join('AHlogo.png'))
        pygame.display.set_icon(gamelogo)

        pygame.display.set_caption('AirHockey AI')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.smallfont = pygame.font.SysFont("comicsans", 25)
        self.roundfont = pygame.font.SysFont("comicsans", 45)  
        

        self.clock = pygame.time.Clock()

        


        #self.reset()



        


        # Paddle

        #self.paddle = t.Turtle()
        #self.paddle.speed(10)
        #self.paddle.shape('circle')
        #self.paddle.shapesize(stretch_wid=1, stretch_len=5)
        #self.paddle.color('white')
        #self.paddle.penup()
        #self.paddle.goto(0, -275)

        self.paddlex = WIDTH/2
        self.paddley = int(9*HEIGHT/10)
        self.paddledx = 33


        # Moving obstacle

        self.obstaclx = WIDTH/2
        self.obstacly = int(3*HEIGHT/10)
        self.obstacldx = 5
        self.obstacldy = 5


    



        # Ball

        #self.ball = t.Turtle()
        #self.ball.speed(10)
        #self.ball.shape('circle')
        #self.ball.color('red')
        #self.ball.penup()
        #self.ball.goto(0, 100)
        #self.ball.dx = 3
        #self.ball.dy = -3
        #self.ball.dx = 5
        #self.ball.dy = -5

        self.puckx = random.randint(int(WIDTH/3),int(2*WIDTH/3))
        self.pucky = random.randint(int(HEIGHT/8),int(HEIGHT/2))
        self.puckangle = rand.uniform(math.pi/3, 2*math.pi/3)
        self.puckdx = 25
        self.puckdy = 25

        # Score


        # self.score = t.Turtle()
        # self.score.speed(10)
        # self.score.color('white')
        # #self.score.penup()
        # self.score.hideturtle()
        # self.score.goto(0, 250)
        # self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))



        # -------------------- Keyboard control ----------------------

        # self.win.listen()
        # self.win.onkey(self.paddle_right, 'Right')
        # self.win.onkey(self.paddle_left, 'Left')







    # Paddle movement

    def paddle_right(self):
        if self.paddlex < WIDTH-PADDLE_SIZE/2:
            self.paddlex +=  self.paddledx

    def paddle_left(self):
        if self.paddlex > PADDLE_SIZE/2 :
            self.paddlex -=  self.paddledx

    def run_frame(self):

        #self.win.update()

        # Ball moving

        #self.ball.setx(self.ball.xcor() + self.ball.dx)
        #self.ball.sety(self.ball.ycor() + self.ball.dy)

        #self.puckx +=  self.puckdx ##change with dx*angle
        #self.pucky = self.pucky + self.puckdy
        self.puckx +=  int(math.cos(self.puckangle)*self.puckdx)
        self.pucky += int(math.sin(self.puckangle)*self.puckdy)

        # Obstacle moving
        move =  rand.randint(1,2)
        if move == 1:
            self.obstaclx += rand.randint(-1,1)*self.obstacldx
            self.obstacly += rand.randint(-1,1)*self.obstacldy

        if self.obstacly > HEIGHT/2:
            self.obstacly = HEIGHT/2



        # Ball and Wall collision

        # if self.ball.xcor() > 290:
        #     self.ball.setx(290)
        #     self.ball.dx *= -1

        # if self.ball.xcor() < -290:
        #     self.ball.setx(-290)
        #     self.ball.dx *= -1

        # if self.ball.ycor() > 290:
        #     self.ball.sety(290)
        #     self.ball.dy *= -1
        if self.puckx > WIDTH - PUCK_SIZE:
            self.puckx = WIDTH - PUCK_SIZE
            self.puckdx *= -1

        if self.puckx < PUCK_SIZE :
            self.puckx = 0 + PUCK_SIZE
            self.puckdx *= -1

        if self.pucky < 0 + PUCK_SIZE :
            self.pucky = PUCK_SIZE
            #self.puckdy *= -1
            self.puckangle *= -1


        

        # Ball Ground contact

        if self.pucky > self.paddley:
            # self.ball.goto(0, 100)
            # self.miss += 1
            # self.score.clear()
            # self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))
            # self.reward -= 3
            # self.done = True

            #self.puck.x = 0
            self.miss += 1
            #self.score.clear()
            #self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))
            self.reward -= 1
            
            self.done = True
            self.hit = 0
            self.goal = 0
            self.reset()

        # Ball Paddle collision

        # if abs(self.ball.ycor() + 250) < 10 and abs(self.paddle.xcor() - self.ball.xcor()) < 55:
        #     self.ball.dy *= -1
        #     self.hit += 1
        #     self.score.clear()
        #     self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))
        #     self.reward += 3
        if  (self.paddley - self.pucky - self.puckdy/2) <= PUCK_SIZE/2 and abs(self.paddlex - self.puckx - self.puckdx/2) <= PADDLE_SIZE/2:
            #self.puckdy *= -1
            self.pucky -= PUCK_SIZE
            self.puckangle = -(self.puckangle/abs(self.puckangle))*(math.pi/2 + math.pi*abs(self.puckx-self.paddlex)/(3*PADDLE_SIZE/2))
            #print("puck.angle = ",self.puckangle)
            #self.puckangle =  3*abs((math.pi*(self.puckx-self.paddlex)/(PUCK_SIZE/2))/2)/4 - math.pi/2 #pi/2 => verticale, 0 horizontale
            #self.puckdx *= math.sin((0.9*math.pi*(self.puckx+self.paddlex)/(PADDLE_SIZE/2)))
            self.hit += 1
            self.total_hit += 1
            #self.score.clear()
            #self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))
            self.reward += 0

        ## Goal - Ball in the target
        if (self.puckx + PUCK_SIZE/2 >= GOAL_x0 and self.puckx + PUCK_SIZE/2 <= GOAL_x1 and self.pucky - PUCK_SIZE/2 < GOAL_y1 and self.pucky - PUCK_SIZE/2 > GOAL_y0):
            #self.puckdy *= -1
            self.puckangle *= -1
            self.pucky += PUCK_SIZE/2
            self.goal += 1
            self.reward += 1
            self.total_goal += 1
            #print("GOOOAAALLLL")
            self.reset()

        # Ball Paddle collision
        # if (self.puckx + PUCK_SIZE/2 >= GOAL_x0 and self.puckx + PUCK_SIZE/2 <= GOAL_x1 and self.pucky - PUCK_SIZE/2 < GOAL_y1 and self.pucky - PUCK_SIZE/2 > GOAL_y0):
        #     #self.puckdy *= -1
        #     self.puckangle *= -1
        #     self.pucky += PUCK_SIZE/2
        #     self.goal += 1
        #     self.reward += 1
        #     self.total_goal += 1
        #     #print("GOOOAAALLLL")
        #     self.reset()


    #Print screen
    def update_screen(self):
        # Render Logic
        self.screen.fill(BACKGROUND_color)
        # center circle
        pygame.draw.circle(self.screen,WHITE, (WIDTH / 2, HEIGHT / 2), 70, 5)
        # borders
        pygame.draw.rect(self.screen, WHITE, (0, 0, WIDTH, HEIGHT), 5)
        # Goal
        pygame.draw.rect(self.screen, BLUE, (GOAL_x0, GOAL_y0,GOAL_x1-GOAL_x0, GOAL_y1), 0)
        text = pygame.font.Font('arial.ttf', 20).render(" GOAL ", True, RED)
        self.screen.blit(text, [int(WIDTH/2) - 35, int(GOAL_y1/2)-10])
        # Divider
        pygame.draw.rect(self.screen, WHITE, (0,HEIGHT / 2, WIDTH, 3))

        # Puck
        pygame.draw.circle(self.screen, RED, (self.puckx, self.pucky), PUCK_SIZE/2, 0,True,True,True,True)

        # Paddle
        pygame.draw.rect(self.screen, BLUE, pygame.Rect(self.paddlex-int(PADDLE_SIZE/2), self.paddley , PADDLE_SIZE, int(PADDLE_SIZE/5)))
        pygame.draw.ellipse(self.screen, BLUE, pygame.Rect(self.paddlex-int(PADDLE_SIZE/2), self.paddley - int(PADDLE_SIZE/5)  , PADDLE_SIZE, int(PADDLE_SIZE/2)))
        text = pygame.font.Font('arial.ttf', 20).render(" AI ", True, BLACK)
        self.screen.blit(text, [self.paddlex-15, self.paddley-15])

        # Obstacle
        pygame.draw.rect(self.screen, BLUE, pygame.Rect(self.obstaclx-int(OBSTACLE_SIZE/2), self.obstacly , OBSTACLE_SIZE, int(OBSTACLE_SIZE/5)))


        # Score
        text = pygame.font.Font('arial.ttf', 20).render(" Miss : " + str(self.miss), True, BLACK)
        self.screen.blit(text, [10, 10])
        text = pygame.font.Font('arial.ttf', 20).render( " total hit : " + str(self.total_hit), True, BLACK)
        self.screen.blit(text, [10, 35])
        text = pygame.font.Font('arial.ttf', 20).render("hit : " + str(self.hit), True, BLACK)
        self.screen.blit(text, [10, 60])
        text = pygame.font.Font('arial.ttf', 20).render("Goal : " + str(self.goal), True, BLACK)
        self.screen.blit(text, [WIDTH - 80, 10])
        text = pygame.font.Font('arial.ttf', 20).render("total Goal : " + str(self.total_goal), True, BLACK)
        self.screen.blit(text, [WIDTH - 120, 35])
        pygame.display.flip()

    # def render_field(self, background_color):
    #     # Render Logic
    #     self.screen.fill(background_color)
    #     # center circle
    #     pygame.draw.circle(self.screen, WHITE, (WIDTH / 2, HEIGHT / 2), 70, 5)
    #     # borders
    #     pygame.draw.rect(self.screen, WHITE, (0, 0, WIDTH, HEIGHT), 5)
    #     # D-box
    #     pygame.draw.rect(self.screen, WHITE, (0, HEIGHT / 2 - 150, 150, 300), 5)
    #     pygame.draw.rect(self.screen, WHITE, (width - 150, HEIGHT / 2 - 150, 150, 300), 5)
    #     # goals
    #     pygame.draw.rect(self.screen, const.BLACK, (0, const.GOAL_Y1, 5, const.GOAL_WIDTH))
    #     pygame.draw.rect(self.screen, const.BLACK, (width - 5, const.GOAL_Y1, 5, const.GOAL_WIDTH))
    #     # Divider
    #     pygame.draw.rect(self.screen, const.WHITE, (width / 2, 0, 3, height))

    #     pygame.draw.rect(self.screen, (200,150,50), (const.WIDTH/8, 0, const.WIDTH/5, const.HEIGHT-10), 0)   
    #     #disp_text(self.screen, "sensor area", (width / 4.5, const.HEIGHT/2), smallfont, (0,0,0))


    #     # PAUSE
    #     screen.blit(pause_image, (width / 2 - 32, height - 70))



    # ------------------------ AI control ------------------------

    # 0 move left
    # 1 do nothing
    # 2 move right

    def reset(self):
        self.puckx = random.randint(int(WIDTH/3),int(2*WIDTH/3))
        self.pucky = random.randint(int(HEIGHT/5),int(HEIGHT/2))
        self.puckangle = rand.uniform(math.pi/3, 2*math.pi/3)
        self.puckdx = 25
        self.puckdy = 25

        self.paddlex = int(WIDTH/2)
        self.paddley = int(9*HEIGHT/10)

        # x_init = random.randint(0,200)
        # y_init = random.randint(0,200)
        # self.paddle.goto(0, -275)
        # self.ball.goto(x_init, y_init)
        # return [self.paddle.xcor()*0.01, self.ball.xcor()*0.01, self.ball.ycor()*0.01, self.ball.dx, self.ball.dy]
    
        return [self.paddlex/WIDTH, self.puckx/WIDTH, self.pucky/HEIGHT, 0.5*(math.cos(self.puckangle)*self.puckdx)/self.puckdx+0.5, 0.5*(math.sin(self.puckangle)*self.puckdy)/self.puckdy+0.5]

    def step(self, action):

        self.reward = 0
        self.done = 0
        #self.hit = 0

        if action == 0:
            self.paddle_left()
            self.reward -= 0 # 0.1

        if action == 2:
            self.paddle_right()
            self.reward -= 0 # 0.1

        self.run_frame()  

        #state = [self.paddle.xcor()*0.01, self.ball.xcor()*0.01, self.ball.ycor()*0.01, self.ball.dx, self.ball.dy]

        state =  [self.paddlex/WIDTH, self.puckx/WIDTH, self.pucky/HEIGHT, 0.5*(math.cos(self.puckangle)*self.puckdx)/self.puckdx+0.5, 0.5*(math.sin(self.puckangle)*self.puckdy)/self.puckdy+0.5]

        # 5. update ui and clock
        #self.render_field()
        #if self.total_hit//5 == 0:
        self.update_screen()
        self.clock.tick(SPEED_CLOCK)

        # 6. return game over and score

        return self.reward, state, self.done,self.hit,self.goal,self.total_hit