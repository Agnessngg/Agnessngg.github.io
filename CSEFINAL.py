import pygame #imported the real pygame because IDLE is just a coding platform 
import sys
import random #-> makes the program able to access the bulit in function -> random 

#width and height of screen
WIDTH = 700
HEIGHT = 700

#random generate checkpoint

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font("pixel-game.regular.otf", 20)

#images:
CHARACTERIMG = pygame.image.load("character.png").convert_alpha()
CHARACTERIMG = pygame.transform.scale(CHARACTERIMG, (452*0.07, 564*0.07))#<- scaling the images 

WELCOMEIMG = pygame.image.load("menu_background.png").convert_alpha()#<- using the alpha thing to make it complie faster

STARTIMG = pygame.image.load("StartButton.png").convert_alpha()
STARTIMG = pygame.transform.scale(STARTIMG, (1053*0.15, 315*0.15))

BACKGROUNDIMG = pygame.image.load("grass_maze2.png").convert_alpha() 
BACKGROUNDMASK = pygame.image.load("new_mask.png").convert_alpha()

CHECKPOINTIMG1 = pygame.image.load("checkpoint1.png").convert_alpha()
CHECKPOINTIMG1 = pygame.transform.scale(CHECKPOINTIMG1, (340*0.1, 394*0.1))

CHECKPOINTIMG2 = pygame.image.load("checkpoint2.png").convert_alpha()
CHECKPOINTIMG2 = pygame.transform.scale(CHECKPOINTIMG2, (340*0.1, 394*0.1))

CHECKPOINTIMG3 = pygame.image.load("checkpoint3.png").convert_alpha()
CHECKPOINTIMG3 = pygame.transform.scale(CHECKPOINTIMG3, (340*0.1, 394*0.1))

CHECKPOINTIMG4 = pygame.image.load("checkpoint4.png").convert_alpha()
CHECKPOINTIMG4 = pygame.transform.scale(CHECKPOINTIMG4, (340*0.1, 394*0.1))

CHECKPOINTIMG5 = pygame.image.load("checkpoint5.png").convert_alpha()
CHECKPOINTIMG5 = pygame.transform.scale(CHECKPOINTIMG5, (340*0.1, 394*0.1))

WIN = pygame.image.load("Win1.png").convert_alpha()
WIN = pygame.transform.scale(WIN, (735*0.7, 416*0.7))

GameOver = pygame.image.load("GameOver.png").convert_alpha()
GameOver = pygame.transform.scale(GameOver, (735*0.7, 416*0.7))

QUESTIONWINDOW = pygame.image.load("question_window.png").convert_alpha()
QUESTIONWINDOW_object = QUESTIONWINDOW.get_rect()
QUESTIONWINDOW_object.x = 50
QUESTIONWINDOW_object.y = 180

EXITBUTTON = pygame.image.load('exit_button.png')
EXITBUTTON = pygame.transform.scale(EXITBUTTON, (403*0.25, 198*0.25))
EXITBUTTON_object = EXITBUTTON.get_rect()
EXITBUTTON_object.x = 305
EXITBUTTON_object.y = 410


RESTARTBUTTON = pygame.image.load('restart_button.png')
RESTARTBUTTON = pygame.transform.scale(RESTARTBUTTON, (1326*0.1, 416*0.1))
RESTARTBUTTON_object = RESTARTBUTTON.get_rect()
# RESTARTBUTTON_object.x = 305
# RESTARTBUTTON_object.y = 410



#objects
background_object = BACKGROUNDIMG.get_rect()
character_object = CHARACTERIMG.get_rect()
startButton_object = STARTIMG.get_rect()

checkpoint1_object = CHECKPOINTIMG1.get_rect()
checkpoint2_object = CHECKPOINTIMG2.get_rect()
checkpoint3_object = CHECKPOINTIMG3.get_rect()
checkpoint4_object = CHECKPOINTIMG4.get_rect()
checkpoint5_object = CHECKPOINTIMG5.get_rect()


startButton_object.x = 260
startButton_object.y = 380

checkpoints_random_coordinates = [       #RANDOM COORDINATES FOR CHECKPOINTS
    (301, 542),
    (360, 595),
    (360, 420),
    (425, 365),
    (600, 365),
    (188, 595),
    (600, 595),
    (600, 535),
    (480, 535),
    (480, 365),
    (540, 365),
]

#questions: Made it into arrays -> separted it into 3 different categories -> makes it easier to code feedback?
questions_sequencing = []

questions_logic = []

questions_riddles = []

#masks -> remove the background (the white part)
background_mask = pygame.mask.from_surface(BACKGROUNDMASK)
character_mask = pygame.mask.from_surface(CHARACTERIMG)

#variables
random_question = ""
input_text = ""
type_here = "Type your answer in the box"
correct_answer = ""

total_score = 0 # calculating the total score, before it was score1, score2, score3
wrong1 = 0 # to count wrong answers for the question type 1 (for the feedback)
wrong2 = 0 # to count wrong answers for the question type 2 (for the feedback)
wrong3 = 0 # to count wrong answers for the question type 3 (for the feedback)
feedback_text = ['You need to improve in these questions type: '] # will save feedback text in the variable

running = False # start of the game. Initially we don't run the game, because we are in the menu, so it's False. When we start --> changes to True

def display_exit_restart(): # TO display exit and restart buttons at the end of the game
    global running
    mouse_x, mouse_y = pygame.mouse.get_pos() # to get position of mouse (we will check if we click on the buttons using the position)

    screen.blit(EXITBUTTON, (305, 410)) # to display exit button
    if EXITBUTTON_object.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]: # checking if we click on the exit button
        exit() # exits from the program (game)

    screen.blit(RESTARTBUTTON, (5, 5)) # to display restart button
    if RESTARTBUTTON_object.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]: # checking if we click on the restart button
        running = False
        start() # restarts the game

def display_feedback():  # Function to display the feedback. We will display it only if player loses the game
    global QUESTIONWINDOW, QUESTIONWINDOW_object
    if wrong1 > 0 and "sequencing" not in feedback_text:
        feedback_text.append("sequencing")
    if wrong2 > 0 and "logic" not in feedback_text:
        feedback_text.append("logic")
    if wrong3 > 0 and "riddles" not in feedback_text:
        feedback_text.append("riddles")
    text_line1 = font.render(feedback_text[0], True,
                             'black')  # TO DISPLAY THE FIRST LINE OF TEXT ON THE FEEDBACK WINDOW
    text_line2 = font.render(', '.join(feedback_text[1:]), True, 'black')  # TO DISPLAY THE CATEGORIES TO IMPROVE
    screen.blit(text_line1, (200, 350))
    text_window = text_line2.get_rect(centerx=QUESTIONWINDOW_object.centerx,
                                         centery=387)  # Use this window to display the text at the center of the question window
    screen.blit(text_line2, text_window)



def question():#most challenging part
    global correct_answer, QUESTIONWINDOW, QUESTIONWINDOW_object #-> made it so that it can be accessed outside of the method (instead of local)
    question_lines = random_question[0: -1]#the -1 does not include the last element
    correct_answer = random_question[-1] #the last element
    screen.blit(QUESTIONWINDOW, (50, 200))
    height = 300
    
    

    #wraps the text
    for line in question_lines:
        question_text = font.render(line, True, "Black")
        text_window = question_text.get_rect(centerx = QUESTIONWINDOW_object.centerx, centery = height) #Use this window to display the text at the center of the question window 
        screen.blit(question_text, text_window)
        height += 20

    display_text = font.render(input_text, True, "Black")
    display_type = font.render(type_here, True, "Black")
    screen.blit(display_type, (160, 365))
    screen.blit(display_text, (200, 400))
    
    #screen.blit(question_text, (80, 280))

    
def generate_question():
    global random_question #makes it not local
    random_question = random.choice(questions_sequencing + questions_logic + questions_riddles) #get's first index from the arrays which is the question
        

checkpoint_objects = [checkpoint1_object, checkpoint2_object, checkpoint3_object, checkpoint4_object, checkpoint5_object]

#Start function 
def start():
    global input_text, total_score, wrong1, wrong2, wrong3, feedback_text, running, questions_logic, questions_riddles, questions_sequencing

    questions_sequencing = [("What comes next in the sequence? 2, 4, 8, 16, 32, ___", "64"),
                            ("Fill in the blank: Monday, Wednesday, Friday, ___,", "Sunday"),
                            ("What letter comes next? A, C, F, J, ___", "O")]

    questions_logic = [
        ("If all Blorks are Snurps, and all Snurps are Frimps,", "are all Blorks also Frimps? Answer Yes or No.",
         "Yes"),
        ("A is the father of B.", " But B is not the son of A.", "How is this possible? (one word answer)", "Daughter"),
        ("A monkey, a squirrel, and a bird are racing to the",
         "top of a tall coconut tree. Which animal will get the banana first?", "None")]

    questions_riddles = [
        ("I speak without a mouth and hear without ears.", "I have no body, but I come alive with the wind. What am I?",
         "Echo"),
        ("The more you take, the more you leave behind.", "What am I?", "Footsteps"),
        ("I have cities but no houses. I have mountains but no trees.", "I have water but no fish. What am I?",
         "A Map")]

    total_score = 0  # to set total score as 0 when we restart the game
    start_time = pygame.time.get_ticks()//1000 #-> // math operator -> division -> rounds it
    
    X = 30
    Y = 595
    running = True
    start_text = font.render("START", True, "Red")
    finish_text = font.render("FINISH", True, "Green")
    timer_text = font.render("TIMER", True, "Black")
    finish_object = finish_text.get_rect() # to check in the character on the finish point
    finish_object.x = 645
    finish_object.y = 365
    fps = 60 #-> Frames per second
    clock = pygame.time.Clock()

    display_question = False
    first_collision = 0

    complete_1 = False
    complete_2 = False
    complete_3 = False
    complete_4 = False
    complete_5 = False
    
    score_text = font.render(f"SCORE: {total_score}", True, "Black")#-> the f means it can combine variables and string

    game_over = False
    TIMER = 300 # CHANGE IT TO SET DIFFERENT TIMER VALUE



    #RANDOM GENERATION OF POSITION OF CHECKPOINTS
    list_of_taken_pos = []
    for check_obj in [checkpoint1_object, checkpoint2_object, checkpoint3_object, checkpoint4_object, checkpoint5_object]:
        random_coord = random.choice(checkpoints_random_coordinates)
        while random_coord in list_of_taken_pos: # while generated position is already taken for another checkpoint, generate a new one
            random_coord = random.choice(checkpoints_random_coordinates)
        list_of_taken_pos.append(random_coord)

        check_obj.x = random_coord[0]
        check_obj.y = random_coord[1]


    
    while running:
        #timer
        if game_over == False: 
            current_time = pygame.time.get_ticks()//1000
            time_difference = current_time - start_time
            timer_text = font.render(f"TIMER: {TIMER - time_difference + 1}", True, "Black") #-> 300 - time difference will reverse it because we have to remove the amount of seconds that have passed from total time
     
            
        #variables for collision
        displacementX = 0
        displacementY = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[0: -1] #-> slice
                    
                elif event.key == pygame.K_RETURN:
                    if character_object.colliderect(checkpoint5_object) and complete_5 == False: #makes sure the player can answer before it's game over 
                        complete_5 = True
                    first_collision = 0

                    if input_text.lower() == correct_answer.lower():
                        print("Correct")
                        total_score += 1
                        score_text = font.render(f"SCORE: {total_score}", True, "Black")

                    else:
                        if random_question in questions_sequencing:
                            wrong1 += 1 #-> separately counts wrong answers for each of the type of questions, so we can display feedback at the end
                        if random_question in questions_logic:
                            wrong2 += 1
                        if random_question in questions_riddles:
                            wrong3 += 1
                        print("Incorrect")
                        #do if question is wrong, then minue one point . -> if 0 -> -1??
                            
                    display_question = False
                    input_text = "" #before it was placed before  checking the right answer -> but if after because we need to empty the input field AFTER we have checked the answer -> so it's not incorrect

                    for i in [questions_sequencing, questions_logic, questions_riddles]:  # removes the completed question, so it will not be generated again
                        if random_question in i:
                            i.remove(random_question)

                else:
                    if first_collision == 2: #retricts typing if not at checkpoint 
                        input_text += event.unicode #adds type char


                    
        if game_over == False and first_collision != 2: #only will happen if it's false; 2 means answering question 
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: #if it's left then it does left... so on 
                 displacementX -= 0.9 #-> changed from 'X' to 'displacementX' (the value we move the character for each frame)
            if keys[pygame.K_RIGHT]:
                 displacementX += 0.9
            if keys[pygame.K_UP]:
                 displacementY -= 0.9
            if keys[pygame.K_DOWN]:
                 displacementY += 0.9

        if not background_mask.overlap(character_mask, (X + displacementX, Y)): #checks if the player moves the character 0.1, will it collide with the maze lines
            if 0 <= X + displacementX <= 700 - character_object.width: #if NOT overlap -> then it will move, character_object.width -> width of object|| X + displacement should be in between 0 an 700|| and then minus the width to create a limit 
                X += displacementX

        if not background_mask.overlap(character_mask, (X, Y + displacementY)):
            if 0 <= Y + displacementY <= 700 - character_object.height:
                Y += displacementY

        character_object.x = X #made characters as an object to create a box like thing
        character_object.y = Y

        #all my screen blits to display the images 
        screen.blit(BACKGROUNDIMG, (0,0)) #show character
        screen.blit(BACKGROUNDMASK, (0,0))
        screen.blit(start_text, (65, 605))
        screen.blit(finish_text, (645, 365))
        screen.blit(score_text, (450, 20))
        screen.blit(timer_text, (550, 20))
        screen.blit(CHECKPOINTIMG1, (checkpoint1_object.x, checkpoint1_object.y))
        screen.blit(CHECKPOINTIMG2, (checkpoint2_object.x, checkpoint2_object.y))
        screen.blit(CHECKPOINTIMG3, (checkpoint3_object.x, checkpoint3_object.y))
        screen.blit(CHECKPOINTIMG4, (checkpoint4_object.x, checkpoint4_object.y))
        screen.blit(CHECKPOINTIMG5, (checkpoint5_object.x, checkpoint5_object.y))
        screen.blit(CHARACTERIMG, (X, Y))



            #how to loop this 
        if first_collision == 0:
            if character_object.colliderect(checkpoint1_object)and complete_1 == False:
                complete_1 = True
                display_question = True
                if first_collision == 0 :
                    first_collision = 1

            if character_object.colliderect(checkpoint2_object) and complete_2 == False:
                complete_2 = True
                display_question = True
                if first_collision == 0 :
                    first_collision = 1
                    
            if character_object.colliderect(checkpoint3_object) and complete_3 == False :
                complete_3 = True
                display_question = True
                if first_collision == 0 :
                    first_collision = 1
                    
            if character_object.colliderect(checkpoint4_object) and complete_4 == False:
                complete_4 = True
                display_question = True
                if first_collision == 0 :
                    first_collision = 1
                    
            if character_object.colliderect(checkpoint5_object) and complete_5 == False:
                display_question = True
                if first_collision == 0 :
                    first_collision = 1
                

        if first_collision == 1:
            generate_question()
            first_collision = 2

        if display_question == True:
            question()

        if TIMER - time_difference < 0: #-> 10 - time_differnce so it will go down instead of going up
            screen.blit(GameOver, (100, 200))
            game_over = True
            display_feedback()
            display_exit_restart()

        if TIMER - time_difference >= 0 and all([complete_1, complete_2, complete_3, complete_4, complete_5]) and character_object.colliderect(finish_object):#-> if the countdown value is greater than 0 then still have time|| 'all' function -> checks that all of the values are true (tasks complete)
            game_over = True #makes sure the character can't move 
            if total_score == 5:
                screen.blit(WIN, (100,200))
                display_exit_restart()

            else:
                screen.blit(GameOver, (100, 200))
                display_feedback()
                display_exit_restart()


        clock.tick(fps) #-> it updates image 60 times per second
        pygame.display.flip() #updates the frames


def menu():
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        mouse_position = pygame.mouse.get_pos() #gets the mouse position 
        if startButton_object.collidepoint(mouse_position[0], mouse_position[1]) and pygame.mouse.get_pressed()[0]:#if start button collides the mouse position 0 (X), 1(Y)|| also returns the array 
            start() #calls the start function 
            
            
        screen.blit(WELCOMEIMG, (0,0))
        screen.blit(STARTIMG, (260,380))


        pygame.display.flip() 



menu()
pygame.quit()
