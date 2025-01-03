import random
import pygame

character_frames = [
    pygame.image.load('../assets/images/character/walk-1.png'),
    pygame.image.load('../assets/images/character/walk-2.png'),
    pygame.image.load('../assets/images/character/walk-3.png'),
    pygame.image.load('../assets/images/character/walk-4.png'),
    pygame.image.load('../assets/images/character/walk-5.png')
]
character_frames = [pygame.transform.scale(frame, (int(frame.get_width() * 0.3), int(frame.get_height() * 0.3))) for frame in character_frames]

# Classe Character
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, dialogs, responses):
        super().__init__()
        self.frames = character_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.time_since_last_update = 0
        self.dialogs = dialogs
        self.responses = responses
        self.current_dialog_index = 0
        self.is_paused = False
        self.is_speaking = False
        self.is_listening = False  # Adicionando a propriedade listening
        self.speech_text = None
        self.speech_duration = 2000  # Tempo de fala em milissegundos
        self.speech_start_time = 0
        self.response_wait_time = 1000  # 2 segundos para o outro responder
        self.response_start_time = None  # Quando o segundo personagem deve começar a responder
        self.is_big = False
    def update(self, dt):
        # Só atualiza a animação e movimento se o personagem não estiver falando ou ouvindo
        if not self.is_paused and not self.is_listening:
            self.time_since_last_update += dt
            if self.time_since_last_update > 100:
                self.time_since_last_update = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
                if self.direction == -1:
                    self.image = pygame.transform.flip(self.image, True, False)
            self.rect.x += self.direction * 2
            if self.rect.x <= 0 or self.rect.x >= 1200 - self.rect.width:
                self.direction *= -1

        # Verifica se a fala deve terminar
        self.check_speech_end()

    def start_speaking(self):
        # Inicia a fala
        if (self.current_dialog_index< len(self.dialogs)):
            self.speech_text = self.dialogs[self.current_dialog_index]
            self.speech_start_time = pygame.time.get_ticks()
            self.is_paused = True
            self.is_speaking = True
            self.is_listening = False  # Começou a falar, não está ouvindo
        else:
            self.is_paused = False
            self.is_speaking = False
            self.is_listening = False  # Começou a falar, não está ouvindo
          
    def talk_again(self):
        # Reinicia o diálogo caso o número sorteado seja par
        num = random.randint(1, 10)
        if(num % 2 == 0):
            self.current_dialog_index = 0
            
        # Mudar tamanho do boneco 
        
    def change_size(self):
    # Alterna entre o tamanho normal e o tamanho grande
        self.is_big = not self.is_big
        if self.is_big:
            # Redimensiona todas as imagens no self.frames para o dobro do tamanho
            for i in range(len(self.frames)):
                self.frames[i] = pygame.transform.scale(self.frames[i], 
                                                        (self.frames[i].get_width() * 2, 
                                                        self.frames[i].get_height() * 2))
            
            # Atualiza o rect da imagem atual após redimensionamento
            # Mantém o centro original (posição do personagem) após o redimensionamento
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            # Redimensiona todas as imagens de volta ao tamanho original
            for i in range(len(self.frames)):
                self.frames[i] = pygame.transform.scale(self.frames[i], 
                                                        (self.frames[i].get_width() // 2, 
                                                        self.frames[i].get_height() // 2))
            
            # Atualiza o rect da imagem original, garantindo que a posição não seja alterada
            

            
    def start_responding(self):
        # Inicia a resposta
        if self.speech_text is None and self.current_dialog_index < len(self.responses):
            self.speech_text = self.responses[self.current_dialog_index]
            self.speech_start_time = pygame.time.get_ticks()
            self.is_paused = True
            self.is_speaking = True
            self.is_listening = False  # Começou a responder, não está ouvindo
        else:
            self.is_paused = False
            self.is_speaking = False
            self.is_listening = False
    def start_listening(self):
        # Inicia a escuta
        if(self.current_dialog_index < len(self.dialogs)):
            self.is_listening = True
            self.is_paused = True  # Pausa o movimento enquanto escuta
            self.is_speaking = False

    def check_speech_end(self):
        # Verifica se a fala ou resposta terminou
        if self.speech_text and pygame.time.get_ticks() - self.speech_start_time > self.speech_duration:
            self.speech_text = None
            self.is_paused = False
            self.is_speaking = False
            self.is_listening = False  # Termina de escutar
            self.current_dialog_index += 1  # Mover para o próximo diálogo
            if self.response_start_time is None:
                self.response_start_time = pygame.time.get_ticks()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.speech_text:
            font = pygame.font.Font(None, 24)
            text_surface = font.render(self.speech_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.top - 10))
            surface.blit(text_surface, text_rect)
