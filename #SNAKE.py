#SNAKE
import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

pygame.mixer.music.set_volume(0.05)
musica_de_fundo = pygame.mixer.music.load('musica1.wav')
pygame.mixer.music.play(-1)

barulho_colisao = pygame.mixer.Sound('coin.wav')
barulho_perdeu = pygame.mixer.Sound('fireball.wav')
largura = 600
altura = 600

x_cobra = int(largura/2) 
y_cobra = int(altura/2)

velocidade = 10
x_controle = velocidade
y_controle = 0

x_maca = randint(40, 520)
y_maca = randint(170, 520)

pontos = 0
record = 0
fonte = pygame.font.Font('ka1.ttf', 25, bold=True, italic=True)
fonte2 = pygame.font.SysFont('arial', 20, True, True)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo')
relogio = pygame.time.Clock()
lista_cobra = []
comprimento_inicial = 5
morreu = False

imagens=["lightning.png", "gears.png", "calculus2.png", "calculus.png", "atom.png", "magnet.png", "motherboard.png", "coding.png", "graduation.png", "logosite.png"]
i=0
imagem1=pygame.image.load("lightning.png")
imagem1= pygame.transform.scale(imagem1, (40, 40))
maça=pygame.image.load(imagens[i])
maça=pygame.transform.scale(maça, (40,40))

banner=pygame.image.load("banner.png")
banner=pygame.transform.scale(banner, (600,120))
grama=pygame.image.load("grama.png")
grama=pygame.transform.scale(grama, (600,480))

def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        #XeY = [x, y]
        #XeY[0] = x
        #XeY[1] = y

        pygame.draw.rect(tela, (247,132,17), (XeY[0], XeY[1], 20, 20))

def reiniciar_jogo():
    global pontos, comprimento_inicial, x_cobra, y_cobra, lista_cobra, lista_cabeca, x_maca, y_maca, morreu
    pontos = 0
    comprimento_inicial = 5
    x_cobra = int(largura/2) 
    y_cobra = int(altura/2)
    lista_cobra = []
    lista_cabeca = []
    x_maca = randint(50, 520)
    y_maca = randint(170, 520)
    morreu = False

while True:
    relogio.tick(30)
    tela.fill((0,0,0))

    tela.blit(banner, (0,0))
    
    borda1 = pygame.draw.rect(tela, (255, 0 , 0), (0,120,600,5))
    borda2 = pygame.draw.rect(tela, (255, 0 , 0), (595,120,5,480))
    borda3 = pygame.draw.rect(tela, (255, 0 , 0), (0,595,600,5))
    borda4 = pygame.draw.rect(tela, (255, 0 , 0), (0,120,5,475))
    
    tela.blit(grama, (0,120))

    
    mensagem = f'{pontos}'
    recorde = f'{record}'
    texto_formatado = fonte.render(mensagem, True, (0,0,255))
    texto2 = fonte.render(recorde,True, (0,0,255))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if x_controle == velocidade:
                    pass
                else:
                    x_controle = -velocidade
                    y_controle = 0
            if event.key == K_RIGHT:
                if x_controle == -velocidade:
                    pass
                else:
                    x_controle = velocidade
                    y_controle = 0
            if event.key == K_UP:
                if y_controle == velocidade:
                    pass
                else:
                    y_controle = -velocidade
                    x_controle = 0
            if event.key == K_DOWN:
                if y_controle == -velocidade:
                    pass
                else:
                    y_controle = velocidade
                    x_controle = 0

    x_cobra = x_cobra + x_controle
    y_cobra = y_cobra + y_controle
        
    cobra = pygame.draw.rect(tela, (247,132,17), (x_cobra-2.5,y_cobra-2.5,25,25))
    maca = pygame.draw.rect(tela, (0,0,0), (x_maca,y_maca,25,25))
    tela.blit(maça, (x_maca-7,y_maca-10))

    
    if cobra.colliderect(maca):
        x_maca = randint(50, 520)
        y_maca = randint(170, 520)
        pontos += 1
        barulho_colisao.play()
        i+=1
        comprimento_inicial+=1
        velocidade+=0.2
        maça=pygame.image.load(imagens[i])
        maça=pygame.transform.scale(maça, (40,40))
        retmaça=maça.get_rect()
        if i==9:
            i=-1
    
    if pontos>record:
        record=pontos
    
    lista_cabeca = []
    lista_cabeca.append(x_cobra)
    lista_cabeca.append(y_cobra)
    
    lista_cobra.append(lista_cabeca)

    if (lista_cobra.count(lista_cabeca) > 1) or cobra.colliderect(borda1) or cobra.colliderect(borda2) or cobra.colliderect(borda3) or cobra.colliderect(borda4):
        barulho_perdeu.play()
        mensagem = 'Game over! Pressione a tecla R para jogar novamente.'
        texto_formatado = fonte2.render(mensagem, True, (255,255,0))
        ret_texto = texto_formatado.get_rect() 
        i==0 
        
        morreu = True
        while morreu:
            tela.fill((0,0,0))
            velocidade=10

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:                       
                        reiniciar_jogo()
                        
                        
                      

            ret_texto.center = (largura//2, altura//2) 
            tela.blit(texto_formatado, ret_texto)
            pygame.display.update()

    
    if x_cobra > largura:
        x_cobra = 0
    if x_cobra < 0:
        x_cobra = largura
    if y_cobra < 0:
        y_cobra = altura
    if y_cobra > altura:
        y_cobra = 0

    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]

    aumenta_cobra(lista_cobra)

    tela.blit(texto_formatado, (470,17))
    tela.blit(texto2, (540,73))


    
    pygame.display.update()