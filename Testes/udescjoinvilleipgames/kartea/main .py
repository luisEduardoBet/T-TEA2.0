from teste import Target 
import pygame as pg 



pg.init()
screen = pg.display.set_mode((800,600), flags= pg.SCALED)



run = True 


alvo = Target()

while run: 

    for event in pg.event.get():
        if ( event.type == pg.QUIT ):
            run = False

    alvo.draw(screen)
    pg.display.flip()
    
