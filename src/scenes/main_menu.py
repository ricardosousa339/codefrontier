# Menu principal do jogo

import pygame
import math
from .base_scene import Scene
from src.config import Colors, MODULES, SCREEN_WIDTH, SCREEN_HEIGHT
from src.ui import Button, ModuleCard, HealthBar
from src.utils import assets

class MainMenuScene(Scene):
    """Cena do menu principal com seleção de módulos"""
    
    def __init__(self, game):
        super().__init__(game)
        
        # Botões do menu
        center_x = SCREEN_WIDTH // 2
        
        self.buttons = {
            "play": Button(center_x - 100, 550, 200, 50, "JOGAR", 
                          Colors.GREEN, (80, 220, 80)),
            "village": Button(center_x - 100, 610, 200, 50, "VILAREJO"),
            "settings": Button(center_x - 250, 670, 150, 40, "Configurações"),
            "quit": Button(center_x + 100, 670, 150, 40, "Sair", 
                          Colors.RED, (250, 80, 80))
        }
        
        # Cards dos módulos (posicionados como na imagem)
        self.module_cards = []
        positions = [
            (200, 200),   # C# - Canto superior esquerdo
            (1080, 200),  # PHP - Canto superior direito
            (200, 520),   # Python - Canto inferior esquerdo
            (1080, 520)   # JavaScript - Canto inferior direito
        ]
        
        for i, (module_id, module_data) in enumerate(MODULES.items()):
            x, y = positions[i]
            icon = assets.get_image(f"{module_id}_icon")
            card = ModuleCard(x, y, module_id, module_data, icon)
            self.module_cards.append(card)
            
        # Sistema de vida
        self.health_bar = HealthBar(SCREEN_WIDTH - 200, 20, 5)
        
        # Estado de seleção de módulo
        self.selected_module = None
        self.show_module_select = False
        
        # Animação do portal
        self.portal_pulse = 0
        
    def handle_event(self, event):
        """Processa eventos"""
        # Verificar cliques nos botões
        if self.buttons["play"].is_clicked(event):
            self.show_module_select = True
            
        if self.buttons["village"].is_clicked(event):
            self.next_scene = "village"
            
        if self.buttons["quit"].is_clicked(event):
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            
        # Verificar cliques nos cards de módulo
        if self.show_module_select:
            for card in self.module_cards:
                if card.is_clicked(event):
                    self.selected_module = card.module_id
                    self.next_scene = "challenge"
                    
    def update(self, dt):
        """Atualiza a cena"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        # Atualizar botões
        for button in self.buttons.values():
            button.update(mouse_pos, mouse_pressed)
            
        # Atualizar cards
        for card in self.module_cards:
            card.update(mouse_pos, dt)
            
        # Animação do portal
        self.portal_pulse = (self.portal_pulse + dt * 2) % (2 * math.pi)
        
    def draw(self, screen):
        """Desenha a cena"""
        # Fundo espacial
        bg = assets.get_image("space_bg")
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill(Colors.SPACE_DARK)
            
        # Adicionar mais estrelas animadas
        self._draw_animated_stars(screen)
        
        # Desenhar portal no centro
        self._draw_portal(screen)
        
        # Desenhar personagem
        player = assets.get_image("player")
        if player:
            player_scaled = pygame.transform.scale(player, (128, 128))
            screen.blit(player_scaled, (SCREEN_WIDTH//2 - 64, SCREEN_HEIGHT//2 - 30))
            
        # Desenhar pet (pequeno cachorro/gato ao lado)
        self._draw_pet(screen)
        
        # Desenhar cards dos módulos
        font = assets.get_font("medium")
        for card in self.module_cards:
            card.draw(screen, font)
            
        # Desenhar barra de vida
        heart_full = assets.get_image("heart_full")
        heart_empty = assets.get_image("heart_empty")
        if heart_full and heart_empty:
            self.health_bar.draw(screen, heart_full, heart_empty)
            
        # Desenhar botões
        for button in self.buttons.values():
            button.draw(screen, font)
            
        # Título do jogo
        title_font = assets.get_font("huge")
        title = title_font.render("CODE FRONTIER", True, Colors.GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
        # Sombra do título
        shadow = title_font.render("CODE FRONTIER", True, (50, 30, 0))
        screen.blit(shadow, (title_rect.x + 3, title_rect.y + 3))
        screen.blit(title, title_rect)
        
        # Subtítulo
        sub_font = assets.get_font("medium")
        subtitle = sub_font.render("Aprenda Programação Jogando!", True, Colors.TEXT_LIGHT)
        screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH//2, 95)))
        
    def _draw_animated_stars(self, screen):
        """Desenha estrelas animadas"""
        import random
        # Usar o pulse para criar brilho
        brightness = int(200 + 55 * math.sin(self.portal_pulse * 2))
        for i in range(50):
            random.seed(i + 100)
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            if random.random() > 0.5:
                size = 2 + int(math.sin(self.portal_pulse + i) * 1)
                pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), max(1, size))
                
    def _draw_portal(self, screen):
        """Desenha o portal animado"""
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80
        
        # Efeito de brilho do portal
        for i in range(8):
            offset = math.sin(self.portal_pulse + i * 0.5) * 5
            alpha = 150 - i * 15
            width = 100 - i * 8
            height = 140 - i * 10
            
            surface = pygame.Surface((width + 20, height + 20), pygame.SRCALPHA)
            color = (100 + i * 10, 150 + i * 10, 255, alpha)
            pygame.draw.ellipse(surface, color, (10, 10, width, height), 4)
            
            screen.blit(surface, (cx - width//2 - 10 + offset, cy - height//2 - 10))
            
        # Centro do portal (mais brilhante)
        inner_surface = pygame.Surface((60, 80), pygame.SRCALPHA)
        pygame.draw.ellipse(inner_surface, (200, 220, 255, 100), (0, 0, 60, 80))
        screen.blit(inner_surface, (cx - 30, cy - 40))
        
    def _draw_pet(self, screen):
        """Desenha o pet ao lado do personagem"""
        # Pet simples (cachorrinho/gato com roupa)
        pet_x = SCREEN_WIDTH // 2 + 80
        pet_y = SCREEN_HEIGHT // 2 + 50
        
        # Corpo do pet
        pygame.draw.ellipse(screen, (200, 180, 160), (pet_x, pet_y, 40, 30))
        # Cabeça
        pygame.draw.circle(screen, (200, 180, 160), (pet_x + 35, pet_y + 5), 15)
        # Orelhas
        pygame.draw.polygon(screen, (180, 160, 140), 
                          [(pet_x + 25, pet_y - 5), (pet_x + 30, pet_y + 5), (pet_x + 35, pet_y - 8)])
        pygame.draw.polygon(screen, (180, 160, 140), 
                          [(pet_x + 40, pet_y - 8), (pet_x + 35, pet_y + 5), (pet_x + 45, pet_y - 5)])
        # Olhos
        pygame.draw.circle(screen, (0, 0, 0), (pet_x + 32, pet_y + 3), 3)
        pygame.draw.circle(screen, (0, 0, 0), (pet_x + 40, pet_y + 3), 3)
        # Roupa laranja (como na imagem)
        pygame.draw.rect(screen, (255, 140, 0), (pet_x + 5, pet_y + 15, 30, 15), border_radius=3)
