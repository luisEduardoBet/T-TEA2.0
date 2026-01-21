import pygame
import random

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, vel, largura_tela, altura_chao):
        super().__init__()

     
        tipos_de_obstaculos = [
            'assets/Imagens/PeA-juntos.png',
            'assets/Imagens/agonia.png',
            'assets/Imagens/panico.png',
            'assets/Imagens/Sprite-coluna-inteira.png',
            'assets/Imagens/Sprite-coluna-quebrada.png',
            'assets/Imagens/colunas-juntas.png',
            'assets/Imagens/Sprite-vaso.png',
            'assets/Imagens/hades1.png',
            'assets/Imagens/fogo1.gif',
            'assets/Imagens/fogão.png'
        ]

        imagem_escolhida = random.choice(tipos_de_obstaculos)
        if (imagem_escolhida == 'assets/Imagens/PeA-juntos.png') or (imagem_escolhida =='assets/Imagens/agonia.png') or (imagem_escolhida == 'assets/Imagens/panico.png'):
            scale_factor = random.uniform(1.5, 2.2) 
        elif imagem_escolhida == 'assets/Imagens/Sprite-coluna-quebrada.png':
            scale_factor = random.uniform(2, 2.7)
        else:
            scale_factor = random.uniform(2, 2.5) 

        original_image = pygame.image.load(imagem_escolhida).convert_alpha() 
        
        new_width = int(original_image.get_width() * scale_factor)
        new_height = int(original_image.get_height() * scale_factor)
        self.image = pygame.transform.scale(original_image, (new_width, new_height))

        alturas_possiveis = [altura_chao, altura_chao - 85, altura_chao - 90, altura_chao - 100]
        altura_escolhida = random.choice(alturas_possiveis)

        if imagem_escolhida == 'assets/Imagens/hades1.png' or imagem_escolhida == 'assets/Imagens/fogo1.png' or imagem_escolhida == 'assets/Imagens/fogão.png':
            self.rect = self.image.get_rect(bottomleft=(largura_tela + random.randint(200, 300), altura_escolhida))
        else:
            self.rect = self.image.get_rect(bottomleft=(largura_tela + random.randint(200, 300), altura_chao))

        self.mask = pygame.mask.from_surface(self.image)
        
        self.vel = vel

    def update(self):
        self.rect.x -= self.vel

        if self.rect.right < 0:
            self.kill()
