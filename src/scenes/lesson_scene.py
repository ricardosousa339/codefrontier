# Cena de lição (protótipo estático)

import pygame
from .base_scene import Scene
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.utils import assets

class LessonScene(Scene):
    """Cena estática que exibe a imagem lesson.png"""
    
    def __init__(self, game):
        super().__init__(game)
        self.original_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.lesson_size = (1280, 800)
        
    def on_enter(self):
        """Redimensiona a tela para caber a imagem"""
        pygame.display.set_mode(self.lesson_size)
        
    def handle_event(self, event):
        """Processa eventos - qualquer clique ou tecla volta ao menu"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._restore_and_exit()
        
        if event.type == pygame.MOUSEBUTTONUP:
            self._restore_and_exit()
            
    def _restore_and_exit(self):
        """Restaura a resolução original e volta ao menu"""
        pygame.display.set_mode(self.original_size)
        self.game.screen = pygame.display.get_surface()
        self.next_scene = "menu"
                
    def update(self, dt):
        """Atualiza a cena"""
        pass
        
    def draw(self, screen):
        """Desenha a imagem lesson.png"""
        # Pegar a surface atual (pode ter mudado de tamanho)
        current_screen = pygame.display.get_surface()
        
        lesson_img = assets.get_image("lesson")
        if lesson_img:
            # Exibir imagem em tamanho original
            current_screen.blit(lesson_img, (0, 0))
        else:
            # Fallback se a imagem não existir
            current_screen.fill((50, 50, 80))
            font = pygame.font.SysFont("arial", 32)
            text = font.render("Lição Python - Clique para voltar", True, (255, 255, 255))
            text_rect = text.get_rect(center=(640, 400))
            current_screen.blit(text, text_rect)
