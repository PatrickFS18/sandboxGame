import pygame
import random
from character import Character
from tree import Tree
# Inicialização do Pygame e do mixer para os sons
pygame.init()
pygame.mixer.init()

# Definindo a largura e altura da tela
screen = pygame.display.set_mode((1200, 700))
clock = pygame.time.Clock()

# Carregar a imagem do fundo para o dia e noite
grass_day = pygame.image.load('assets/images/ambient/grass.jpg')
grass_day = pygame.transform.scale(grass_day, (1200, 700))
grass_night = pygame.image.load('assets/images/ambient/grass_night.jpg')
grass_night = pygame.transform.scale(grass_night, (1200, 700))

# Carregar os sons de ambiente
rain_sound = pygame.mixer.Sound('assets/sounds/rain.mp3')  # Som de chuva
day_sound = pygame.mixer.Sound('assets/sounds/day.mp3')     # Som de dia
night_sound = pygame.mixer.Sound('assets/sounds/night.mp3') # Som de noite

# Ajustando volumes
rain_sound.set_volume(0.3)
day_sound.set_volume(0.5)
night_sound.set_volume(0.5)

# Variáveis de ambiente
is_day = True
is_raining = False

# Arrays de diálogos e respostas
dialogos_personagem1 = ["Salve"]
respostas_personagem2 = ["Bão"]

# Criando os personagens
personagem1 = Character(50, 420, dialogos_personagem1, respostas_personagem2)
personagem2 = Character(100, 420, respostas_personagem2, dialogos_personagem1)
tree1 = Tree(x=150, y=300)  # Posição da árvore no mapa
tree2 = Tree(x=500, y=300)  # Posição da árvore no mapa


# Classe para representar gotas de chuva
class Raindrop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2, 10))  # Uma gota de 2px de largura e 10px de altura
        self.image.fill((173, 216, 230))  # Azul-claro para a chuva
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1200)
        self.rect.y = random.randint(-700, 0)
        self.speed = random.randint(5, 10)  # Velocidade de queda variada para cada gota

    def update(self):
        self.rect.y += self.speed
        # Quando a gota passa da tela, ela volta ao topo
        if self.rect.y > 700:
            self.rect.y = random.randint(-50, -10)
            self.rect.x = random.randint(0, 1200)

# Grupo para gerenciar todas as gotas de chuva
raindrops = pygame.sprite.Group()
for _ in range(100):  # Número de gotas de chuva
    raindrop = Raindrop()
    raindrops.add(raindrop)


# Adicionando tudo ao grupo de sprites

house_image = pygame.image.load('assets/images/house.png')
# Redimensionar a imagem da casa
class House(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = house_image  # Definir a imagem da casa
        self.rect = self.image.get_rect()  # Definir o retângulo para colisão e posição
        self.rect.x = x  # Posição X da casa
        self.rect.y = y  # Posição Y da casa

    def draw(self, surface):
        # Método para desenhar a casa na tela
        surface.blit(self.image, self.rect)  # Desenha a casa na tela

house = House(700, 100)  # Posição X, Y da casa
all_sprites = pygame.sprite.Group(personagem1, personagem2,tree1,tree2)

# Funções para alternar o ambiente
def toggle_day_night():
    global is_day
    is_day = not is_day
    if is_day:
        night_sound.stop()  # Para o som da noite
        day_sound.play(-1)  # Inicia o som do dia em loop
    else:
        day_sound.stop()  # Para o som do dia
        night_sound.play(-1)  # Inicia o som da noite em loop

def toggle_rain():
    global is_raining
    is_raining = not is_raining
    if is_raining:
        rain_sound.play(-1)  # Reproduz o som em loop
    else:
        rain_sound.stop()  # Para o som quando a chuva cessa

# Função para desenhar o menu
def draw_menu():
    font = pygame.font.Font(None, 36)
    options = ["1 - Tornar Dia/Noite", "2 - Chover/Parar"]
    for i, option in enumerate(options):
        text = font.render(option, True, (255, 255, 255))
        screen.blit(text, (20, 20 + i * 40))

# Loop principal do jogo
running = True
ultimo_falante = None

# Inicia o som de dia
day_sound.play(-1)  # Som de dia em loop no início

while running:
    screen.fill((0, 0, 0))

    # Exibir o fundo correto
    if is_day:
        screen.blit(grass_day, (0, 0))
    else:
        screen.blit(grass_night, (0, 0))

    # Desenha o menu na tela
    draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:  # Alterna entre dia e noite
                toggle_day_night()
            elif event.key == pygame.K_2:  # Alterna chuva
                toggle_rain()

    # Atualiza e desenha os personagens
    dt = clock.tick(30)
    house.draw(screen)
    all_sprites.update(dt)

    # Verifica colisão e inicia diálogo se apropriado
    if personagem1.rect.colliderect(personagem2.rect):
        if not personagem1.is_speaking and not personagem2.is_speaking:
            if ultimo_falante != personagem1:
                personagem1.start_speaking()
                personagem2.start_listening()
                ultimo_falante = personagem1
            elif ultimo_falante != personagem2:
                personagem2.start_speaking()
                personagem1.start_listening()
                ultimo_falante = personagem2

    # Se estiver chovendo, atualiza e desenha as gotas de chuva
    if is_raining:
        raindrops.update()
        raindrops.draw(screen)

    # Desenha os personagens na tela
    for sprite in all_sprites:
        sprite.draw(screen)

    pygame.display.flip()

# Finaliza os sons e o Pygame ao fechar
day_sound.stop()
night_sound.stop()
rain_sound.stop()
pygame.quit()
