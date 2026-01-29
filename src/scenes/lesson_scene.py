# Cena de lição (protótipo estático)

import pygame
from .base_scene import Scene
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, Colors
from src.utils import assets
from src.ui import Button

class LessonScene(Scene):
    """Cena estática que exibe a imagem de lição do módulo selecionado"""
    
    # Mapeamento de módulos para imagens de lição
    LESSON_IMAGES = {
        "python": "lesson",
        "csharp": "lesson_plants"
    }
    
    def __init__(self, game):
        super().__init__(game)
        self.original_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.lesson_size = (1280, 800)
        self.lesson_image_key = "lesson"  # Padrão
        
        # Botão VOLTAR no canto superior direito
        self.back_button = Button(
            1280 - 120 - 20, 20,  # x, y (canto superior direito com margem)
            120, 40,              # largura, altura
            "VOLTAR",
            Colors.RED, (250, 80, 80),
            font_size="small"
        )
        
    def on_enter(self):
        """Redimensiona a tela para caber a imagem"""
        # Verificar qual módulo foi selecionado e pegar a imagem correspondente
        from .main_menu import MainMenuScene
        menu_scene = self.game.scenes.get("menu")
        if menu_scene and hasattr(menu_scene, 'selected_module'):
            module = menu_scene.selected_module
            self.lesson_image_key = self.LESSON_IMAGES.get(module, "lesson")
        
        pygame.display.set_mode(self.lesson_size)
        
    def handle_event(self, event):
        """Processa eventos"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._restore_and_exit()
        
        # Verificar clique no botão VOLTAR
        if self.back_button.is_clicked(event):
            self._restore_and_exit()
            
    def _restore_and_exit(self):
        """Restaura a resolução original e volta ao menu"""
        pygame.display.set_mode(self.original_size)
        self.game.screen = pygame.display.get_surface()
        self.next_scene = "menu"
                
    def update(self, dt):
        """Atualiza a cena"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        self.back_button.update(mouse_pos, mouse_pressed)
        
    def draw(self, screen):
        """Desenha a imagem de lição"""
        # Pegar a surface atual (pode ter mudado de tamanho)
        current_screen = pygame.display.get_surface()
        
        lesson_img = assets.get_image(self.lesson_image_key)
        if lesson_img:
            # Exibir imagem em tamanho original
            current_screen.blit(lesson_img, (0, 0))
        else:
            # Fallback se a imagem não existir
            current_screen.fill((50, 50, 80))
            font = pygame.font.SysFont("arial", 32)
            text = font.render(f"Lição {self.lesson_image_key} - Imagem não encontrada", True, (255, 255, 255))
            text_rect = text.get_rect(center=(640, 400))
            current_screen.blit(text, text_rect)
        
        # Desenhar botão VOLTAR por cima da imagem
        self.back_button.draw(current_screen)
