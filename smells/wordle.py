# import your modules
import random
import pygame
import words
pygame.init()

# create screen, fonts, colors, game variables

screen = pygame.display.set_mode([500, 700])
pygame.display.set_caption('Wordle Game')

move = 0
matrix = [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "]]


clock = pygame.time.Clock()
game_font = pygame.font.Font('freesansbold.ttf', 56)
random_word = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
game_status = False           #whether game is over or not
alphabet = 0


Black = (0, 0, 0)
lightGreen = (0, 255, 0)
red = (255,0,0)
yellow = (255, 255, 0)
grey = (128, 128, 128)
white = (255, 255, 255)
activeRows = True

# create box for playing game
def write():
    global matrix
    global move
    for j in range(0, 5):
        for i in range(0, 6):
            pygame.draw.rect(screen, white, [j * 100 + 12, i * 100 + 12, 75, 75], 3, 5)
            guessed_word = game_font.render(matrix[i][j], True, grey)
            screen.blit(guessed_word, (j * 100 + 30, i * 100 + 25))
    pygame.draw.rect(screen, lightGreen, [5, move * 100 + 5, 490, 90], 3, 5)


# write code for checking words
def compare_word():
    global matrix
    global move
    global random_word
    for j in range(0, 5):
        for i in range(0, 6):
            if random_word[j] == matrix[i][j] and move > i:
                pygame.draw.rect(screen, lightGreen, [j * 100 + 12, i * 100 + 12, 75, 75], 0, 5)
            elif matrix[i][j] in random_word and move > i:
                pygame.draw.rect(screen, yellow, [j * 100 + 12, i * 100 + 12, 75, 75], 0, 5)


# Code for main game 
Inactive = False
while not Inactive:
    clock.tick(60)
    screen.fill(Black)
    compare_word()
    write()
    
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:                  #if player chooses to quit game
            Inactive = True

        # adding player controls for letter input, backspacing, checking guesses and restarting

        if event.type == pygame.TEXTINPUT and activeRows and not game_status:
                inputAlphabet = event.__getattribute__('text')           #if player enters letter
                if inputAlphabet != " ":
                    inputAlphabet = inputAlphabet.lower()
                    matrix[move][alphabet] = inputAlphabet
                    alphabet += 1
                                    
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE and alphabet > 0:   #if player uses backspace
                matrix[move][alphabet - 1] = ' ' 
                alphabet -= 1 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and  not game_status:          
                move += 1
                alphabet = 0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_status:
                move = 0
                alphabet = 0 
                game_status = False                                                   #ending the game
                random_word = words.WORDS[random.randint(0, len(words.WORDS) - 1)]    # choosing a random word from given list of words

                matrix = [[" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "]]

        # control move activeRows based on letters
        if alphabet == 5:
            activeRows = False
        if alphabet < 5:
            activeRows = True

        # check if guess is correct, add game over conditions

        for i in range(0, 6):
            written_word = matrix[i][0] + matrix[i][1] + matrix[i][2] + matrix[i][3] + matrix[i][4]
            if written_word == random_word and i <= move:
                game_status = True
                                           
        if game_status and move < 6:                 # winning condition is moves used are less than 6
            winmsg = game_font.render('You Won', True, lightGreen)
            screen.blit(winmsg, (40, 610))
 
        elif move == 6:                                # if all the 6 moves are used up, then player loses
            game_status = True
            losemsg = game_font.render('You Lose', True, red)
            screen.blit(losemsg, (40, 610))
      


    pygame.display.flip()
pygame.quit()