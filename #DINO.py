  
import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange, choice

pygame.init()
pygame.mixer.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'imagens')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

LARGURA = 600
ALTURA = 600
    
BRANCO = (255,255,255)
PRETO = (0,0,0)
AMARELO = (255,255,0)
AZUL = (0,0,255)
VERMELHO = (255,0,0)

tela = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption('PET ARCADE')

fundo = pygame.image.load(os.path.join(diretorio_imagens, 'fundo.png'))

banner = pygame.image.load(os.path.join(diretorio_imagens, 'banner.png'))
banner = pygame.transform.scale(banner, (600,120))

sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'dinoSpritesheet.png')).convert_alpha()
sprite_sheet2 = pygame.image.load(os.path.join(diretorio_imagens, 'obstaculos.png')).convert_alpha()

pygame.mixer.music.set_volume(0.02)
musica=pygame.mixer.music.load(os.path.join(diretorio_sons, 'musica.wav'))
pygame.mixer.music.play(-1)

som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'death_sound.wav'))
som_colisao.set_volume(0.1)

som_pontuacao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'score_sound.wav'))
som_pontuacao.set_volume(0.05)

colidiu = False

escolha_obstaculo = choice([0, 1])

pontos = 0
record = 0

xfundo = 0
velocidade_jogo = 10
velocidade_tela = velocidade_jogo-5

def exibe_mensagem(msg, tamanho, cor):
    fonte = pygame.font.Font('ka1.ttf', tamanho)
    mensagem = f'{msg}' 
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado

def reiniciar_jogo():
    global pontos, velocidade_jogo, colidiu, escolha_obstaculo, velocidade_tela, xfundo
    pontos = 0
    velocidade_jogo = 10
    colidiu = False
    dino.rect.y = ALTURA - 64 - 96//2
    dino.pulo = False
    dino_voador.rect.x = LARGURA
    cacto.rect.x = LARGURA
    escolha_obstaculo = choice([0, 1])
    xfundo=0
    velocidade_jogo=10
    velocidade_tela=velocidade_jogo-5

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'jump_sound.wav'))
        self.som_pulo.set_volume(0.05)
        self.imagens_dinossauro = []
        for i in range(3):
            img = sprite_sheet.subsurface((i * 32,0), (32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.imagens_dinossauro.append(img)
        
        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_inicial = ALTURA - 64 - 96//2
        self.rect.topleft = (100, self.pos_y_inicial) #368   416(centro y)
        self.pulo = False

    def pular(self):
        self.pulo = True
        self.som_pulo.play()

    def update(self):

        if self.pulo == True:
            if self.rect.y <= self.pos_y_inicial - 150:
                self.pulo = False
            self.rect.y -= 15

        else:
            if self.rect.y >= self.pos_y_inicial:
                self.rect.y = self.pos_y_inicial
            else:
                self.rect.y += 15
        
 
        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_dinossauro[int(self.index_lista)]


class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet2.subsurface((0*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect.center = (LARGURA,  ALTURA - 64)
        self.rect.x = LARGURA

    def update(self):
        
        if self.escolha == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade_jogo
      
        if velocidade_jogo<16:
            self.image = sprite_sheet2.subsurface((0*32, 0), (32,32))
            self.image = pygame.transform.scale(self.image, (32*2, 32*2))       
        
        if velocidade_jogo==16:
            self.image = sprite_sheet2.subsurface((1*32, 0), (32,32))
            self.image = pygame.transform.scale(self.image, (32*2, 32*2))
       
        if velocidade_jogo==19:
            self.image = sprite_sheet2.subsurface((2*32, 0), (32,32))
            self.image = pygame.transform.scale(self.image, (32*2, 32*2))
       
        if velocidade_jogo==22:
            self.image = sprite_sheet2.subsurface((3*32, 0), (32,32))
            self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        
        if velocidade_jogo==25:
            self.image = sprite_sheet2.subsurface((4*32, 0), (32,32))
            self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        
        if velocidade_jogo==28:      
            self.image = sprite_sheet2.subsurface((5*32, 0), (32,32))
                 

class DinoVoador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_dinossauro = []
        for i in range(3,5):
            img = sprite_sheet.subsurface((i*32, 0), (32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.imagens_dinossauro.append(img)

        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA, 420)
        self.rect.x = LARGURA
    
    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade_jogo

            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.imagens_dinossauro[int(self.index_lista)]

todas_as_sprites = pygame.sprite.Group()
dino = Dino()
todas_as_sprites.add(dino)

cacto = Cacto()
todas_as_sprites.add(cacto)

dino_voador = DinoVoador()
todas_as_sprites.add(dino_voador)

grupo_obstaculos = pygame.sprite.Group()
grupo_obstaculos.add(cacto)
grupo_obstaculos.add(dino_voador)

relogio = pygame.time.Clock()
while True:
    relogio.tick(30)
    tela.fill(PRETO)
    tela.blit(banner,(0,0))
    xfundo-=velocidade_tela
    tela.blit(fundo,(xfundo,120))
    tela.blit(fundo,(xfundo+14000,120))
    tela.blit(fundo,(xfundo+2*14000,120))
    tela.blit(fundo,(xfundo+3*14000,120))
    tela.blit(fundo,(xfundo+4*14000,120))
    tela.blit(fundo,(xfundo+5*14000,120))
    tela.blit(fundo,(xfundo+6*14000,120))
    tela.blit(fundo,(xfundo+7*14000,120))
    tela.blit(fundo,(xfundo+8*14000,120))
    tela.blit(fundo,(xfundo+9*14000,120))
    tela.blit(fundo,(xfundo+10*14000,120))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE and colidiu == False:
                if dino.rect.y != dino.pos_y_inicial:
                    pass
                else:
                    dino.pular()

            if event.key == K_r and colidiu == True:
                reiniciar_jogo()

    colisoes = pygame.sprite.spritecollide(dino, grupo_obstaculos, False, pygame.sprite.collide_mask)

    todas_as_sprites.draw(tela)

    if cacto.rect.topright[0] <= 0 or dino_voador.rect.topright[0] <= 0:
        escolha_obstaculo = choice([0, 1])
        cacto.rect.x = LARGURA
        dino_voador.rect.x = LARGURA
        cacto.escolha = escolha_obstaculo
        dino_voador.escolha = escolha_obstaculo

    if colisoes and colidiu == False:
        som_colisao.play()
        colidiu = True

    if colidiu == True:
        if pontos % 100 == 0:
            pontos += 1
        game_over = exibe_mensagem('GAME OVER', 40, (255,255,0))
        tela.blit(game_over, (LARGURA//2 -40, ALTURA//2))
        restart = exibe_mensagem('Pressione r para reiniciar', 19, (AMARELO))
        tela.blit(restart, (LARGURA//2 -80, (ALTURA//2) + 60))
        velocidade_jogo=0
        velocidade_tela=0
        i=0

    else:
        pontos += 1
        if pontos>record:
            record=pontos
        todas_as_sprites.update()
        texto_pontos = exibe_mensagem(pontos, 25, (AZUL))
        texto_record = exibe_mensagem(record,25,(VERMELHO))

    if pontos % 100 == 0:
        som_pontuacao.play()
        if velocidade_jogo >= 28:
            velocidade_jogo += 0
        else:
            velocidade_jogo += 1
            velocidade_tela = velocidade_jogo-5
        
    tela.blit(texto_pontos, (415, 17))
    tela.blit(texto_record, (487, 72))
    barreira=pygame.draw.rect(tela, PRETO, (0,120,600,4))

    pygame.display.flip()