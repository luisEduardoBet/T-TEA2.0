from geometry import * 
from config import *
from game import * 




screen = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption("RepeTEA")
    
game = Jogo(3,2,screen)

game.main_loop()

pygame.quit()


