from pickle import FALSE, TRUE
from re import I
from tkinter.messagebox import NO
#from typing_extensions import Self
from sokoPuzzle import SokoPuzzle
from node import Node
from collections import deque
import itertools
from copy import deepcopy
import numpy as np
import pygame
from search import Search
import time



#--------------------------------create noeud ---------------------------------------------------------------

def create_initial_node(board=None):        
        
        height = len(board)
        width = len(board[0])
                
        # Separate walls, spaces and obstacles board from robot and boxes board
        robot_block = [['']*width for _ in range(height)]
        wall_space_obstacle = [['']*width for _ in range(height)]
        deadlock_matrice = [['']*width for _ in range(height)] #creer matrice deadlock initialemnt vide 
        
        for i, j in itertools.product(range(height), range(width)):
            if board[i][j] == 'R':
                robot_position = (i, j) 
                robot_block[i][j] = 'R'
                wall_space_obstacle[i][j] = ' '
            elif board[i][j] == 'B':
                robot_block[i][j] = 'B'
                wall_space_obstacle[i][j] = ' '
            elif board[i][j] == 'S' or board[i][j] == 'O' or board[i][j] == ' ':
                robot_block[i][j] = ' '   
                wall_space_obstacle[i][j] = board[i][j]         
            elif board[i][j] == '*':
                robot_block[i][j] = 'B'
                wall_space_obstacle[i][j] = 'S'
            else: # self.board[i][j] == '.'
                robot_position = (i, j) 
                robot_block[i][j] = 'R'
                wall_space_obstacle[i][j] = 'S'
            #creer les ddls coins
            if board[i][j] ==' ' or board[i][j] =='R':
                if ((board[i-1][j]=='O' and board[i][j-1]=='O')or(board[i-1][j]=='O' and board[i][j+1]=='O') or (board[i][j-1]=='O'and board[i+1][j]=='O')
                or (board[i][j+1]=='O' and board[i+1][j])=='O'): 
                   deadlock_matrice[i][j]='D'    
        
        #continuer la creation des deadlocks en ligne 
        print("old")
        print(deadlock_matrice)
        for i1 in range(height):
          list=deque()
          ligne_mur_haut=TRUE
          ligne_mur_bas=TRUE 
          storage=0
          for j1  in range(width):
             if (deadlock_matrice[i1][j1]=='D'):
                 list.append((i1,j1))
             #if (wall_space_obstacle[i1][j1]=='S'): 
               # storage=storage+1   
          
          #if storage==0:
          len_listt=len(list) 
          if len_listt>=2  :
          
             if (len(list) % 2) == 0:
                 len_list=len(list) 
             else:
                len_list=len(list)-1
         
        
             for s in range(len_list-1):
              if len(list)>=2:
                print("before pop")
                print(list) 
                x0,y0 = list.popleft()
                x1,y1 = list.popleft()
                print("after pop")
                print(list)  

                for x in range (y0,y1): 
                        
                        if wall_space_obstacle[i1-1][x]!='O' or wall_space_obstacle[i1][x]=='S':
                                print("this is"+str(wall_space_obstacle[i1-1][x]))
                                ligne_mur_haut=False
                               
                        if wall_space_obstacle[i1+1][x]!='O' or wall_space_obstacle[i1][x]=='S':
                                print("this is"+str(wall_space_obstacle[i1+1][x]))
                                ligne_mur_bas=False 
                                

                if (ligne_mur_bas!=False ):  
                 for x1 in range (y0,y1): 
                                if (wall_space_obstacle[i1][x1]==' ' or robot_block[i1][x1]=='R'):
                                         deadlock_matrice[i1][x1]='D'
                
                if (ligne_mur_haut!=False ):  
                 for x2 in range (y0,y1): 
                                if (wall_space_obstacle[i1][x2]==' ' or robot_block[i1][x2]=='R' ):
                                         deadlock_matrice[i1][x2]='D'  

        #deadlock matrice de coté des column 
        for j in range(width):
          listC=deque()
          ligne_mur_right=TRUE
          ligne_mur_left=TRUE 
          for i  in range(height):
             if (deadlock_matrice[i][j]=='D'):
                   listC.append((i,j))
                
          len_list1=len(listC)     
          if len_list1>=2  :
       
            if (len(listC) % 2) == 0:
              len_list=len(listC) 
            else:
               len_list=len(listC)-1
         
        
            for s in range(len_list-1):
              if len(listC)>=2:   
                print("before pop")
                print(list)  
                x0,y0 = listC.popleft()
                x1,y1 = listC.popleft()
                print("after pop")
                print(list) 

                for x in range (x0,x1): 
                        
                        if wall_space_obstacle[x][j-1]!='O' or wall_space_obstacle[x][j]=='S':
                                print("this is hh" +str(wall_space_obstacle[x][j-1]))
                                ligne_mur_right=False
                               
                        if wall_space_obstacle[x][j+1]!='O' or wall_space_obstacle[x][j]=='S':
                                ligne_mur_left=False 
                                

                if (ligne_mur_left!=False ):  
                 for yl in range (x0,x1): 
                                if (wall_space_obstacle[yl][j]==' ' or robot_block[yl][j]=='R' ):
                                         print("ggg")
                                         deadlock_matrice[yl][j]='D'
                
                if (ligne_mur_right!=False ):  
                 for yr in range (x0,x1): 
                                if (wall_space_obstacle[yr][j]==' ' or robot_block[yr][j]=='R' ):
                                         deadlock_matrice[yr][j]='D'                                    
    
       
                         


             
        Node.wall_space_obstacle = wall_space_obstacle  
        Node.deadlock_matrice = deadlock_matrice    
        Node.robot_block=robot_block  
        initial_node = Node(SokoPuzzle(robot_block, robot_position))
        print(deadlock_matrice)
        #print(robot_block)
        #print(wall_space_obstacle)
        return initial_node
                                    
""" ***************************************************** Main function **************************************************** """

board1 = [['O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'S', ' ', 'B', ' ', 'O'],
        ['O', ' ', 'O', 'R', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O']]

board2 = [['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
        ['O', ' ', ' ', 'O', 'O', 'O', ' ', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', 'O', '.', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', ' ', 'O', ' ', 'O'],
        ['O', ' ', ' ', 'B', ' ', ' ', 'O', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', ' ', 'O', ' ', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']]

board3 = [['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', ' ', ' ', ' ', 'O', ' ', ' ', 'O'],
        ['O', ' ', ' ', 'B', 'R', ' ', ' ', 'O'],
        ['O', ' ', ' ', ' ', 'O', 'B', ' ', 'O'],
        ['O', 'O', 'O', 'O', 'O', ' ', 'S', 'O'],
        ['O', 'O', 'O', 'O', 'O', ' ', 'S', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']]

board4 = [['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', ' ', ' ', 'O', 'O', 'O'],
        ['O', 'O', ' ', ' ', 'O', 'O', 'O'],
        ['O', 'O', ' ', '*', ' ', ' ', 'O'],
        ['O', 'O', 'B', 'O', 'B', ' ', 'O'],
        ['O', ' ', 'S', 'R', 'S', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', 'O', 'O'],
        ['O', 'O', 'O', ' ', ' ', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O']]

board5 = [['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'S', 'O', ' ', ' ', 'O', 'O'],
        ['O', ' ', ' ', ' ', ' ', 'B', ' ', 'O', 'O'],
        ['O', ' ', 'B', ' ', 'R', ' ', ' ', 'S', 'O'],
        ['O', 'O', 'O', ' ', 'O', ' ', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'B', 'O', ' ', 'O', 'O', 'O'],
        ['O', 'O', 'O', ' ', ' ', 'S', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']]

board6 = [['O', 'O', 'O', 'O', 'O', 'O', 'O'],
            ['O', 'S', ' ', 'O', ' ', 'R', 'O'],
            ['O', ' ', ' ', 'O', 'B', ' ', 'O'],
            ['O', 'S', ' ', ' ', 'B', ' ', 'O'],
            ['O', ' ', ' ', 'O', 'B', ' ', 'O'],
            ['O', 'S', ' ', 'O', ' ', ' ', 'O'],
            ['O', 'O', 'O', 'O', 'O', 'O', 'O']]

board7=[['O', 'O', 'O', 'O', 'O', 'O','O','O'],
        ['O', 'S', 'S', 'S', ' ', 'O','O','O'],
        ['O', ' ', 'S', ' ', 'B',' ', ' ','O'],
        ['O', ' ', ' ', 'B', 'B','B',' ', 'O'],
        ['O', 'O', 'O', 'O', ' ', ' ','R','O'],
        ['O', 'O', 'O', 'O', 'O', 'O','O','O']]

board8=[['O', 'O', 'O', 'O', 'O', 'O','O','O'],
        ['O', ' ', ' ', ' ', ' ', 'O','O','O'],
        ['O', ' ', ' ', ' ', 'B',' ', ' ','O'],
        ['O', 'S', 'S', 'S', '*','B','R', 'O'],
        ['O', ' ', ' ', ' ', 'B', ' ',' ','O'],
        ['O', ' ', ' ', ' ', 'O', 'O','O','O'],
        ['O', 'O', 'O', 'O', 'O', 'O','O','O']]

board9=[['O', 'O', 'O', 'O', 'O', 'O','O','O','O'],
        ['O', 'O', 'O', 'S', ' ', 'O','O','O','O'],
        ['O', 'O', 'O', ' ', ' ', 'O','O','O','O'],
        ['O', 'S', ' ', 'S', ' ', 'O','O','O','O'],
        ['O', ' ', 'B', ' ', 'B', 'B',' ',' ','O'],
        ['O', 'O', 'O', 'S', ' ', ' ','B','R','O'],
        ['O', 'O', 'O', ' ', ' ', 'O','O','O','O'],
        ['O', 'O', 'O', 'O', 'O', 'O','O','O','O']]

""" This function will create from a board (a level): a static board (wall_space_obstacle) and a dynamic board (robot_block) 
    The static board will be the same in the whole search process (we will use it just for comparison), 
    so it's better to declare it as a static variable in the class Node 
    This function will also create the initial node"""







#------------------------------------------------GAMING SCREEN  -----------------------------------------#

wall = pygame.image.load('images/stones.png')
BOX_SIZE = wall.get_width()

clock = pygame.time.Clock()
def drawBoard (screen,board):
    storagePoint = pygame.image.load('images/bomb.png')
    box = pygame.image.load('images/box.png')
    robot = pygame.image.load('images/mushroom.png')
    space = pygame.image.load('images/square.png')
    boxIN = pygame.image.load('images/boxIN.png')
    robIN = pygame.image.load('images/robotIN.png')
    ddl= pygame.image.load('images/blocked.png')
   
    images = {
        'O': wall,
        'S': storagePoint,
        'B': box,
        'R': robot,
        ' ': space,
        '*': boxIN,
        '.': robIN,
        'D': ddl
    }
    screen.fill("white")
    pygame.display.flip()
    for i in range(len(board)):
        for j in range(len(board[i])):
            #isDeadlock(i, j)
            
            screen.blit(images[board[i][j]], (j * BOX_SIZE, i * BOX_SIZE))
            pygame.display.flip()        
            
        
   
   
level = board3
board = level
pygame.font.init()


def screenSize():
    j = 0
    for i in range(len(board)):
        j = len(board[i]) if len(board[i]) > j else j

    return j * BOX_SIZE, len(board) * BOX_SIZE


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def message_display(text):
    h, w = screenSize()
    largeText = pygame.font.Font('Blackout.otf', 50)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (int(h/2),int(w/2))
    screen.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)



#---------------------------------------------------------main-------------------------------------#
initial_node = create_initial_node(board=level) 
goalNode, num_steps = Search.Addl(initial_node, heuristic=3)
    
if goalNode:
       print (f"Optimal Solution found after {num_steps} steps")
       solution = goalNode.getSolution()      
else:
      print ("Optimal solution not found") 



screen = pygame.display.set_mode(screenSize())
pygame.display.set_caption("Sokoban MIV - M1")
screen.fill((255, 255, 255))
done = False



while not done:
   

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            done = True
        
    for i in range (len(solution)):
        
        pygame.display.flip()
        drawBoard(screen,solution[i])
        
        time.sleep(0.5)
        pygame.display.flip()  
    pygame.display.flip() 
    message_display(f"{num_steps} itérations")
    pygame.display.flip()   
    clock.tick(40)
    done = True
    
    
   
   
    
