import pygame
import random

# Carregar as imagens das árvores
tree_images = [
    pygame.image.load(f'assets/images/tree/arvore{i}.png') for i in range(1, 16)
]

# Transformar as imagens para o tamanho adequado, se necessário
tree_images = [pygame.transform.scale(img, (170, 250)) for img in tree_images]

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = tree_images  # Lista das imagens das árvores
        self.current_image = 0  # Índice inicial da imagem da árvore
        self.image = self.images[self.current_image]  # Definir a imagem inicial
        self.rect = self.image.get_rect()  # Definir o retângulo para colisão e posição
        self.rect.x = x  # Posição X da árvore
        self.rect.y = y  # Posição Y da árvore
        self.time_since_last_change = 0  # Para controlar a troca de imagem
        self.change_interval = 200  # Intervalo em milissegundos para trocar a imagem

    def update(self, dt):
        # Controla o tempo para troca de imagem
        self.time_since_last_change += dt
        
        if self.time_since_last_change > self.change_interval:
            # Atualizar a imagem da árvore
            self.current_image = (self.current_image + 1) % len(self.images)
            self.image = self.images[self.current_image]
            self.time_since_last_change = 0  # Resetar o tempo para a próxima troca

    def draw(self, surface):
        # Método para desenhar a árvore na tela usando blit
        surface.blit(self.image, self.rect)  # Desenha a árvore na tela