
import pygame
import random
import math
from pygame.locals import *
from pygame.transform import scale
from pygame.image import load
import csv
import cv2
import mediapipe as mp
import numpy as np
import os, sys

if getattr(sys, 'frozen', False):
    mp_root = os.path.join(sys._MEIPASS, "mediapipe")
    os.environ["MEDIAPIPE_ROOT"] = mp_root
else:
    mp_root = mp.__path__[0]
    os.environ["MEDIAPIPE_ROOT"] = mp_root


pontos_calibracao = np.zeros((4, 2), dtype=np.int32)
contador = 0
calibrado = False

class Jogo:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.run = True
        self.estado = 0  # 0 = tela inicial, 1 = jogando, 2 = acertou, 3 = acabou o tempo, 4 = mostrar cor certa
        self.largura, self.altura = 800, 600
        self.tamanho = 800, 600
        self.superficie = pygame.display.set_mode(self.tamanho)
        pygame.display.set_caption('Estoure a bola!')
        self.musica_pause = False

        self.largura_telacontrole = 640
        self.altura_telacontrole = 480

        # Variáveis de calibração
        self.pontos_calibracao = np.zeros((4, 2), dtype=np.int32)
        self.contador = 0
        self.calibrado = False
        self.csv_file = 'calibracao.csv'

        # MediaPipe
        self.mp_pose = mp.solutions.pose

        self.cor_botao = 'purple'
        self.cor_botao_ok = 'purple'
        self.fonte = pygame.font.SysFont(None, 55)

        self.branco = (255, 255, 255)
        self.azul = (50, 100, 255)
        self.verde = (50, 255, 100)
        self.vermelho = (255, 80, 80)

        # Pontuação por cor
        self.pontuacoes_cor = {
            "AZUL": 3,
            "VERDE": 2,
            "VERMELHO": 1
        }


    
    def salvar_calibracao(self, pontos):
        with open(self.csv_file, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['P1x', 'P1y', 'P2x', 'P2y', 'P3x', 'P3y', 'P4x', 'P4y'])
            dados = []
            for p in pontos:
                dados.extend(p)
            writer.writerow(dados)
        print('Calibração salva.')

    def carregar_calibracao(self):
        try:
            with open(self.csv_file, 'r') as f:
                reader = csv.reader(f, delimiter=';')
                next(reader)  # pula cabeçalho
                linha = next(reader)
                pontos = np.array(linha, dtype=np.int32).reshape((4, 2))
                print('Calibração carregada:', pontos)
                return pontos
        except:
            return None

    def mouse_callback(self, event, x, y, flags, param):
        global contador, pontos_calibracao, calibrado
        if event == cv2.EVENT_LBUTTONDOWN and contador < 4:
            pontos_calibracao[contador] = [x, y]
            print(f'Ponto {contador+1} registrado: {x}, {y}')
            contador += 1
            if contador == 4:
                self.salvar_calibracao(pontos_calibracao)
                calibrado = True


    def calibracao(self):
        global calibrado, contador, pontos_calibracao

        cap = cv2.VideoCapture(0)
        cv2.namedWindow('Calibração')
        cv2.setMouseCallback('Calibração', self.mouse_callback)

        while not calibrado:
            ret, frame = cap.read()
            if not ret:
                print("Erro na captura de vídeo")
                break

            for i in range(contador):
                cv2.circle(frame, tuple(pontos_calibracao[i]), 7, (255, 0, 0), -1)

            if contador == 4:
                cv2.line(frame, tuple(pontos_calibracao[0]), tuple(pontos_calibracao[1]), (0, 255, 0), 2)
                cv2.line(frame, tuple(pontos_calibracao[1]), tuple(pontos_calibracao[3]), (0, 255, 0), 2)
                cv2.line(frame, tuple(pontos_calibracao[3]), tuple(pontos_calibracao[2]), (0, 255, 0), 2)
                cv2.line(frame, tuple(pontos_calibracao[2]), tuple(pontos_calibracao[0]), (0, 255, 0), 2)

            cv2.putText(frame, 'Clique 4 pontos para calibrar', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
            cv2.putText(frame, 'Pressione R para resetar ou Q para sair', (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

            cv2.imshow('Calibração', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('r'):
                pontos_calibracao = np.zeros((4, 2), dtype=np.int32)
                contador = 0
                calibrado = False
                print('Calibração resetada')
            elif key == ord('q'):
                break

        cap.release()
        cv2.destroyWindow('Calibração')
    
    def desenhar_botao(self, tela, x, y, largura, altura, mouse_pos, cor_botao, cor_botao_ok, texto):
        rect = pygame.Rect(x, y, largura, altura)
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(tela, cor_botao_ok, rect)
        else:
            pygame.draw.rect(tela, cor_botao, rect)
        texto_render = self.fonte.render(texto, True, 'white')
        texto_rect = texto_render.get_rect(center=rect.center)
        tela.blit(texto_render, texto_rect)
        return rect

    def rodar(self):
        while self.run:

            if self.estado == 0:
                self.superficie.fill((255, 255, 255)) #tela inicial
                mouse_pos = pygame.mouse.get_pos()
                
                fonte_titulo = pygame.font.Font(None, 100)  # tamanho da fonte do título
                texto_titulo = fonte_titulo.render("Estoure a Bola!", True, (0, 0, 0))
                largura_texto = texto_titulo.get_width()
                x_titulo = (self.superficie.get_width() - largura_texto) // 2  # centraliza horizontalmente
                self.superficie.blit(texto_titulo, (x_titulo, 150))

                # Desenha botões
                botao_calibrar = self.desenhar_botao(self.superficie, 300, 400, 200, 60, mouse_pos, self.cor_botao, self.cor_botao_ok, "Calibrar")
                botao_jogar = self.desenhar_botao(self.superficie, 300, 300, 200, 60, mouse_pos, self.cor_botao, self.cor_botao_ok, "Jogar")
                pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == QUIT:
                    self.run = False

                if evento.type == pygame.KEYDOWN:
                    if evento.key == K_q:
                        self.run = False

                    elif self.estado == 0:
                        if evento.key == K_c:
                            print("Entrando em modo Calibrar")
                            self.superficie.fill((255, 255, 255)) #tela inicial
                            #self.fundo = pygame.transform.scale(
                            #pygame.image.load('imagens/fundo_calibrar.png').convert_alpha(),  # Carrega a imagem
                            #self.tamanho  # Redimensiona para (largura, altura)
                            #)
                            #self.superficie.blit(self.fundo, (0, 0))  # Desenha na posição (0, 0)
                            pygame.display.flip()
                            self.calibracao()
                            self.estado = 0
                            self.rodar()
                              # volta para o menu após calibrar
                        elif evento.key == K_j:
                            # Verifica se existe calibração antes de jogar
                            global pontos_calibracao, calibrado
                            pontos = self.carregar_calibracao()
                            if pontos is not None:
                                pontos_calibracao = pontos
                                calibrado = True
                
                                self.estado = 1
                                self.menu_modo()
                            else:
                                print("Nenhuma calibração encontrada. Por favor, calibre antes de jogar.")

                    
                    if evento.key == K_r:
                        self.estado = 1
                        self.menu_modo()
                    elif evento.key == K_v:
                        self.estado = 0
                        self.rodar()

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.estado == 1:
                        if self.estado == 3:
                            if self.botao_rejogar.collidepoint(evento.pos):
                                self.resetar_jogo()
                            elif self.botao_voltar.collidepoint(evento.pos):
                                self.resetar_jogo()

                    elif self.estado == 0:
                        if botao_calibrar.collidepoint(evento.pos):
                            print("Entrando em modo Calibrar")
                            self.superficie.fill((255, 255, 255)) #tela inicial
                            #self.fundo = scale(load('imagens/fundo_calibrar.png'), self.tamanho, self.superficie)
                            #self.fundo = pygame.transform.scale(
                            #pygame.image.load('imagens/fundo_calibrar.png').convert_alpha(),  # Carrega a imagem
                            #self.tamanho  # Redimensiona para (largura, altura)
                            #)
                            #self.superficie.blit(self.fundo, (0, 0))  # Desenha na posição (0, 0)
                            pygame.display.flip()
                            self.calibracao()
                            self.estado = 0
                            self.rodar()
                              # volta para o menu após calibrar
                        elif botao_jogar.collidepoint(evento.pos):
                            # Verifica se existe calibração antes de jogar
                            #global pontos_calibracao, calibrado
                            pontos = self.carregar_calibracao()
                            if pontos is not None:
                                pontos_calibracao = pontos
                                calibrado = True
                                #print("Calibração carregada, iniciando jogo.")
                                self.estado = 1
                                self.menu_modo()
                            else:
                                print("Nenhuma calibração encontrada. Por favor, calibre antes de jogar.")
                        

        pygame.quit()
        exit()
    def menu_modo(self):
        while True:
            self.superficie.fill((255, 255, 255))
            titulo = self.fonte.render("Escolha um modo:", True, (0, 0, 0))
            self.superficie.blit(titulo, (280, 200))

            modos = [
                "1 - Modo Vidas",
                "2 - Modo Infinito",
                "3 - Modo Constante"
            ]
            for i, texto in enumerate(modos):
                t = self.fonte.render(texto, True, (0, 0, 0))
                self.superficie.blit(t, (150, 260 + i * 40))

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_1:
                        self.main_jogo(vidas_iniciais=10, infinito=False, constante=False)
                    elif evento.key == pygame.K_2:
                        self.main_jogo(vidas_iniciais=None, infinito=True, constante=False)
                    elif evento.key == pygame.K_3:
                        self.main_jogo(vidas_iniciais=10, infinito=False, constante=True)
    
    

    def game_over(self, pontos):
        """Tela de fim de jogo"""
        while True:
            self.superficie.fill('white')
            msg1 = self.fonte.render("Fim de jogo!", True, 'black')
            msg2 = self.fonte.render(f"Pontuação final: {pontos}", True, 'black')
            msg3 = self.fonte.render("Aperte ENTER para voltar ao menu", True, 'black')
            self.superficie.blit(msg1, (310, 220))
            self.superficie.blit(msg2, (250, 270))
            self.superficie.blit(msg3, (200, 320))
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                if evento.type == pygame.KEYDOWN:
                    self.estado = 0
                    self.rodar()
    
    def main_jogo(self, vidas_iniciais=None, infinito=False, constante=False):
        #tempo_inicio = pygame.time.get_ticks()
        cap = cv2.VideoCapture(0)
        clock = pygame.time.Clock()
        running = True

        self.bolas = []
        ultimo_spawn = 0
        intervalo_minimo = 2000  # segundos (nível inicial)
        nivel = 1
        pontos =0
        tempo_proximo_nivel = pygame.time.get_ticks() + 10000 # sobe de nível a cada 10s
        vidas = vidas_iniciais if vidas_iniciais else 0

        pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        pos_circulo1 = [self.largura//2, self.altura//2]
        pos_circulo2 = [self.largura//2, self.altura//2]

        while running:
            ret, frame = cap.read()
            tempo_atual = pygame.time.get_ticks()
            if not ret:
                print("Erro ao capturar vídeo.")
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)

            pts1 = np.float32(pontos_calibracao)
            pts2 = np.float32([[0, 0], [self.largura_telacontrole, 0],
                       [0, self.altura_telacontrole], [self.largura_telacontrole, self.altura_telacontrole]])
            matrix = cv2.getPerspectiveTransform(pts1, pts2)

            # Transformar frame para perspectiva calibrada
            warped = cv2.warpPerspective(frame, matrix, (self.largura_telacontrole, self.altura_telacontrole))

            # Mostrar câmera (opcional)
            cv2.imshow('Controle de Pes', warped)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            elif self.estado == 1 and results.pose_landmarks:
                h, w, _ = frame.shape
                landmarks = results.pose_landmarks.landmark

                right_foot = landmarks[self.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]
                left_foot = landmarks[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]

                right_foot_coords = (int(right_foot.x * w), int(right_foot.y * h))
                left_foot_coords = (int(left_foot.x * w), int(left_foot.y * h))

                pe_direito_x = right_foot_coords[0]
                pe_direito_y = right_foot_coords[1]
                pe_esquerdo_x = left_foot_coords[0]
                pe_esquerdo_y = left_foot_coords[1]

                #meio_pe_x = int((right_foot_coords[0] + left_foot_coords[0]) / 2)
                #meio_pe_y = int((right_foot_coords[1] + left_foot_coords[1]) / 2)

                #p = np.array([[[meio_pe_x, meio_pe_y]]], dtype=np.float32)
                #p_trans = cv2.perspectiveTransform(p, matrix)[0][0]

                pd = np.array([[[pe_direito_x, pe_direito_y]]], dtype=np.float32)
                pd_trans = cv2.perspectiveTransform(pd, matrix)[0][0]

                pe = np.array([[[pe_esquerdo_x, pe_esquerdo_y]]], dtype=np.float32)
                pe_trans = cv2.perspectiveTransform(pe, matrix)[0][0]
                # Mapeia para a tela do jogo (ajustando escala)
                pos_circulo1[0] = int((pd_trans[0] / self.largura_telacontrole) * self.largura)
                pos_circulo1[1] = int((pd_trans[1] / self.altura_telacontrole) * self.altura)

                pos_circulo2[0] = int((pe_trans[0] / self.largura_telacontrole) * self.largura)
                pos_circulo2[1] = int((pe_trans[1] / self.altura_telacontrole) * self.altura)

                #pygame.draw.circle(self.superficie, 'white', pos_circulo1, 7)
                #pygame.draw.circle(self.superficie, 'black', pos_circulo1, 5)

                #pygame.draw.circle(self.superficie, 'white', pos_circulo2, 7)
                #pygame.draw.circle(self.superficie, 'black', pos_circulo2, 5)
                pygame.display.flip()
                #pygame.display.update()

                if not constante and not infinito and tempo_atual > tempo_proximo_nivel:
                    nivel += 1
                    intervalo_minimo = max(600, intervalo_minimo - 200)
                    tempo_proximo_nivel += 15000

                if tempo_atual - ultimo_spawn > intervalo_minimo + random.randint(0, 1000):  
                    nova_bola = {
                        "x": random.randint(50, self.largura - 50),
                        "y": random.randint(50, self.altura - 50),
                        "criada_em": tempo_atual
                        }
                    self.bolas.append(nova_bola)
                    ultimo_spawn = tempo_atual
                # Atualiza a tela
                self.superficie.fill('white')

                # Desenha as bolas e remove as que já passaram de 5 segundos
                novas_bolas = []
                
                
                for bola in self.bolas:
                    idade = tempo_atual - bola["criada_em"]  # em ms
                    if idade < 3000:
                        # Muda de cor a cada segundo (1000 ms)
                        fase = (idade // 1000) % 3  # 0, 1, 2 → azul, verde, vermelho
                        if fase == 0:
                            cor = self.azul
                            nome_cor = "AZUL"
                        elif fase == 1:
                            cor = self.verde
                            nome_cor = "VERDE"
                        else:
                            cor = self.vermelho
                            nome_cor = "VERMELHO"
                                    

                        bola["cor"] = cor
                        bola["cor_nome"] = nome_cor

                        pygame.draw.circle(self.superficie, cor, (bola["x"], bola["y"]), 70)
                        novas_bolas.append(bola)
                    
                    else:
                    # Bola estourou
                        if vidas_iniciais:
                            vidas -= 1
                            if vidas <= 0:
                                running = False
                                break

                # Atualiza a lista de bolas (mantém só as ativas)
                self.bolas = novas_bolas

                if infinito:
                    texto = self.fonte.render(f"Pontos: {pontos}   (Infinito)", True, 'black')
                else:
                    texto = self.fonte.render(f"Pontos: {pontos}   Vidas: {vidas}   Nível: {nivel}", True, 'black')
                self.superficie.blit(texto, (20, 20))
                

                for bola in self.bolas[:]:
                    dist1 = math.dist((pos_circulo1[0], pos_circulo1[1]), (bola["x"], bola["y"]))
                    dist2 = math.dist((pos_circulo2[0], pos_circulo2[1]), (bola["x"], bola["y"]))
                    if dist1 < 70 or dist2 < 70:
                        self.bolas.remove(bola)
                        pontos += self.pontuacoes_cor[bola["cor_nome"]]
                        print(f"pontos:{pontos}")
                        break


                pygame.display.flip()
                clock.tick(60)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    
                    elif event.type == pygame.KEYDOWN:
                        if event.key == K_r:
                            self.menu_modo()
                            self.tempo_inicio = pygame.time.get_ticks()
                        elif event.key == K_v:
                            self.estado = 0
                            self.rodar()

            pygame.display.update()
            clock.tick(30)

        if vidas_iniciais and vidas <= 0:
            self.game_over(pontos)

        cap.release()
        cv2.destroyAllWindows()
        pygame.quit()
        exit()

# Executar o jogo
if __name__ == "__main__":
    jogo = Jogo()
    while True:
        modo = jogo.rodar()
        if modo is None:
            break
        jogo.modo(modo)