import sys
import pygame

tempo = pygame.time.Clock()

# Iniciar jogo:
def game_init(w, h):
    pygame.init()
    tamanho = w, h
    tela = pygame.display.set_mode(tamanho)
    pygame.display.set_caption("Cowboy's Revenge")
    return tela

tela = game_init(740, 415)

# Jogador
posicao_x, posicao_y = 150, 280
posicao_y_inicial = posicao_y  # Posição inicial para verificar se o jogador pode pular

Parado = pygame.transform.scale(pygame.image.load('Imagens/SpriteParado.png'), (100, 120))
pulando = pygame.transform.scale(pygame.image.load('Imagens/SpritePulando.png'), (100, 110))
imagem_fundo = pygame.image.load('Imagens/fundo2.jpg')

Parado.set_colorkey((255, 0, 255))
pulando.set_colorkey((255, 0, 255))

jogador_rect = Parado.get_rect(center=(posicao_x, posicao_y))

# Dinâmica de pulo:
saltando = False
gravidade_y = 1
salto = 15
velocidade_y = salto

# Cacto
posicao_x_cacto, posicao_y_cacto = 800, 300
cacto = pygame.transform.scale(pygame.image.load('Imagens/Cacto3.png'), (50, 70))
cacto_rect = cacto.get_rect(center=(posicao_x_cacto, posicao_y_cacto))
cacto_correndo = True

# Sprites de corrida
Sprite1 = pygame.transform.scale(pygame.image.load('Imagens/Sprite1.png'), (120, 120))
Sprite2 = pygame.transform.scale(pygame.image.load('Imagens/Sprite2.png'), (120, 120))
Sprite3 = pygame.transform.scale(pygame.image.load('Imagens/Sprite3.png'), (120, 120))
Sprite4 = pygame.transform.scale(pygame.image.load('Imagens/Sprite4.png'), (120, 120))
Sprite5 = pygame.transform.scale(pygame.image.load('Imagens/Sprite5.png'), (120, 120))
sprites = [Sprite1, Sprite2, Sprite3, Sprite4, Sprite5]

# Animação
indice_sprite = 0
tempo_entre_frames = 0.04  # Intervalo entre frames
tempo_passado = 0
animacao_ativa = False

FPS = 60
estado = "menu"
font = pygame.font.Font(None, 32)

text_color = (0, 200, 200)
text_color2 = (0, 0, 0)

letreiro = pygame.transform.scale(pygame.image.load('Imagens/Letreiro.png'), (180, 100))
x_let = 370
y_let = 70
letreiro_rect = letreiro.get_rect(center=(x_let,y_let))
subindo = False

audio = pygame.mixer.Sound("audio.wav")
audio.set_volume(0.4)

# Pontuação
pontos = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys_pressed = pygame.key.get_pressed()

    tela.blit(imagem_fundo, (0, 0))  # Desenhar o fundo em todos os estados
    tela.blit(letreiro, letreiro_rect)
    audio.play()

    if estado == "menu":
        text_começo = font.render("Pressione espaço para começar!", True, text_color2)
        text_começo_rect = text_começo.get_rect()
        text_começo_rect.center = (tela.get_width() // 2, tela.get_height() // 2)
        tela.blit(text_começo, text_começo_rect)
        tela.blit(Parado, jogador_rect)  # Desenhar o personagem parado no menu
        tela.blit(letreiro, letreiro_rect)
        letreiro_rect = letreiro.get_rect(center=(x_let,y_let))

        if keys_pressed[pygame.K_SPACE]:
            saltando = True
            animacao_ativa = True  # Ativa a animação após o primeiro pulo
            estado = "jogando"


    elif estado == "jogando":
        # Verificar se o jogador está no chão para permitir um novo pulo
        y_let -= 10
        tela.blit(letreiro, letreiro_rect)
        letreiro_rect = letreiro.get_rect(center=(x_let,y_let))
        if not saltando and posicao_y >= posicao_y_inicial and keys_pressed[pygame.K_SPACE]:
            saltando = True
            velocidade_y = salto  # Reinicia a velocidade de pulo
        
        # Atualizar animação
        if animacao_ativa:
            tempo_passado += tempo.tick() / 100  # Tempo em segundos
            if tempo_passado >= tempo_entre_frames:
                tempo_passado -= tempo_entre_frames
                indice_sprite = (indice_sprite + 1) % len(sprites)  # Troca de sprite
    
        # Sistema de pontos
        pontos +=1
        text_pontos = font.render("Seus pontos são:" + str(pontos), True, text_color2)
        text_pontos_rect = text_pontos.get_rect()
        text_pontos_rect.center = (150,50)
        tela.blit(text_pontos, text_pontos_rect)

        # Desenhar o personagem
        if saltando:
            posicao_y -= velocidade_y
            velocidade_y -= gravidade_y
            if posicao_y >= posicao_y_inicial:
                posicao_y = posicao_y_inicial  # Garante que o jogador volte à posição inicial
                saltando = False
                velocidade_y = salto
            jogador_rect = pulando.get_rect(center=(posicao_x, posicao_y))
            tela.blit(pulando, jogador_rect)
        else:
            jogador_rect = sprites[indice_sprite].get_rect(center=(posicao_x, posicao_y))
            tela.blit(sprites[indice_sprite], jogador_rect)

        # Atualizar posição do cacto
        posicao_x_cacto -= 10
        if posicao_x_cacto <= -20:
            posicao_x_cacto = 800
        cacto_rect = cacto.get_rect(center=(posicao_x_cacto, posicao_y_cacto))
        tela.blit(cacto, cacto_rect)

        # Verificar colisão
        if jogador_rect.colliderect(cacto_rect):
            estado = "Fim de jogo"

    elif estado == "Fim de jogo":
        if keys_pressed[pygame.K_q]:
            pygame.quit()
            sys.exit()
        if keys_pressed[pygame.K_r]:
            estado = "menu"
            posicao_x_cacto = 800
            y_let = 50
            pontos = 0
        pygame.draw.rect(tela, (0, 0, 0), (0, 0, 800, 800))
        text_fim = font.render("Fim de jogo!" + " Você fez: " + str(pontos) + " pontos!", True, text_color)
        text_fim_rect = text_fim.get_rect()
        text_fim_rect.center = (tela.get_width() // 2, tela.get_height() // 2)
        tela.blit(text_fim, text_fim_rect)
    pygame.display.flip()
    tempo.tick(FPS)
