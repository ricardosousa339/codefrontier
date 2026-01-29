# Menu principal do jogo

import pygame
import math
import random
from .base_scene import Scene
from src.config import Colors, MODULES, SCREEN_WIDTH, SCREEN_HEIGHT
from src.ui import Button, ModuleCard, HealthBar
from src.utils import assets

class MainMenuScene(Scene):
    """Cena do menu principal com seleção de módulos"""
    
    def __init__(self, game):
        super().__init__(game)
        
        # Botões do menu - centralizados
        center_x = SCREEN_WIDTH // 2
        
        # Larguras dos botões
        btn_next_w = 240
        btn_settings_w = 240
        btn_quit_w = 150
        btn_spacing = 20
        
        # Largura total dos 3 botões + espaçamentos
        total_width = btn_next_w + btn_settings_w + btn_quit_w + (btn_spacing * 2)
        start_x = center_x - total_width // 2
        
        self.buttons = {
            "next_phase": Button(start_x, 670, btn_next_w, 40, "PRÓXIMA FASE", 
                                Colors.GOLD, (255, 220, 100), Colors.TEXT_DARK, font_size="small"),
            "settings": Button(start_x + btn_next_w + btn_spacing, 670, btn_settings_w, 40, "CONFIGURAÇÕES", 
                               font_size="small"),
            "quit": Button(start_x + btn_next_w + btn_settings_w + btn_spacing * 2, 670, btn_quit_w, 40, "SAIR", 
                          Colors.RED, (250, 80, 80), font_size="medium")
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
        self.portal_frames = []
        self.portal_frame_index = 0
        self.portal_anim_timer = 0.0
        self.portal_anim_fps = 10
        
    def handle_event(self, event):
        """Processa eventos"""
        # Verificar cliques nos botões
        if self.buttons["next_phase"].is_clicked(event):
            # Escolher um módulo aleatório
            modules = list(MODULES.keys())
            random_module = random.choice(modules)
            self.selected_module = random_module
            
            # Python e C# vão para lesson, outros para challenge
            if random_module in ["python", "csharp"]:
                self.next_scene = "lesson"
            else:
                self.next_scene = "challenge"
        
        if self.buttons["quit"].is_clicked(event):
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            
        # Verificar cliques nos cards de módulo (sempre disponíveis)
        for card in self.module_cards:
            if card.is_clicked(event):
                self.selected_module = card.module_id
                # Python e C# vão para a tela de lição
                if card.module_id in ["python", "csharp"]:
                    self.next_scene = "lesson"
                else:
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
        self._update_portal_animation(dt)

    def _update_portal_animation(self, dt):
        """Atualiza o frame do portal animado"""
        # Lazy-load do spritesheet
        if not self.portal_frames:
            sheet = assets.get_image("portal_animated")
            if sheet:
                frame_count = 8
                frame_w = sheet.get_width() // frame_count
                frame_h = sheet.get_height()
                for i in range(frame_count):
                    frame = sheet.subsurface(pygame.Rect(i * frame_w, 0, frame_w, frame_h)).copy()
                    self.portal_frames.append(frame)

        if not self.portal_frames:
            return

        self.portal_anim_timer += dt
        if self.portal_anim_timer >= 1.0 / self.portal_anim_fps:
            self.portal_anim_timer = 0.0
            self.portal_frame_index = (self.portal_frame_index + 1) % len(self.portal_frames)
        
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
        
        # Desenhar plataforma embaixo do personagem
        platform = assets.get_image("platform")
        if platform:
            # Proporção original 177x123, escalar 1.5x
            platform_scaled = pygame.transform.scale(platform, (265, 185))
            screen.blit(platform_scaled, (SCREEN_WIDTH//2 - 132, SCREEN_HEIGHT//2 + 20))
        
        # Desenhar personagem
        player = assets.get_image("player")
        if player:
            # Aumentado 1.5x (de 128 para 192)
            player_scaled = pygame.transform.scale(player, (192, 192))
            screen.blit(player_scaled, (SCREEN_WIDTH//2 - 96, SCREEN_HEIGHT//2 - 80))
            
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
            button.draw(screen)
            
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
        
        # Tentar usar spritesheet animado se existir
        if self.portal_frames:
            frame = self.portal_frames[self.portal_frame_index]
            base_scale = 4.0
            scale = base_scale * (1.0 + 0.05 * math.sin(self.portal_pulse))
            
            scaled_w = int(frame.get_width() * scale)
            scaled_h = int(frame.get_height() * scale)
            
            portal_scaled = pygame.transform.scale(frame, (scaled_w, scaled_h))
            portal_rect = portal_scaled.get_rect(center=(cx, cy))
            screen.blit(portal_scaled, portal_rect)
            return

        # Tentar usar sprite estático se existir
        portal_img = assets.get_image("portal")
        if portal_img:
            base_scale = 1.5
            scale = base_scale * (1.0 + 0.05 * math.sin(self.portal_pulse))
            
            scaled_w = int(portal_img.get_width() * scale)
            scaled_h = int(portal_img.get_height() * scale)
            
            portal_scaled = pygame.transform.scale(portal_img, (scaled_w, scaled_h))
            portal_rect = portal_scaled.get_rect(center=(cx, cy))
            screen.blit(portal_scaled, portal_rect)
            return

        # Fallback para desenho vetorial caso imagem falhe ou não exista o asset
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
        """Desenha o pet ao lado do personagem com animação flutuante"""
        # Posição base ajustada para a nova escala do player
        base_x = SCREEN_WIDTH // 2 + 50
        base_y = SCREEN_HEIGHT // 2 + 16
        
        # Animação flutuante em círculo (astronauta no espaço)
        float_radius = 8
        pet_x = base_x + math.cos(self.portal_pulse * 0.8) * float_radius
        pet_y = base_y + math.sin(self.portal_pulse * 0.8) * float_radius
        
        # Leve rotação para dar efeito de flutuação
        rotation_angle = math.sin(self.portal_pulse * 0.5) * 5  # ±5 graus
        
        # Tentar carregar imagem do pet
        pet_img = assets.get_image("pet")
        if pet_img:
            # Aumentado 1.5x (de 64 para 96 pixels)
            pet_scaled = pygame.transform.scale(pet_img, (96, 96))
            # Aplicar rotação
            pet_rotated = pygame.transform.rotate(pet_scaled, rotation_angle)
            pet_rect = pet_rotated.get_rect(center=(pet_x + 48, pet_y + 48))
            screen.blit(pet_rotated, pet_rect)
            return

        # Fallback: Pet simples (cachorrinho/gato com roupa)
        # Reajustando fallback para a nova escala
        scale_f = 1.3
        # Corpo do pet
        pygame.draw.ellipse(screen, (200, 180, 160), (pet_x, pet_y + 15, 40*scale_f, 30*scale_f))
        # Cabeça
        pygame.draw.circle(screen, (200, 180, 160), (int(pet_x + 35*scale_f), int(pet_y + 15 + 5*scale_f)), int(15*scale_f))
        # Orelhas
        pygame.draw.polygon(screen, (180, 160, 140), 
                          [(pet_x + int(25*scale_f), pet_y + 15 - int(5*scale_f)), 
                           (pet_x + int(30*scale_f), pet_y + 15 + int(5*scale_f)), 
                           (pet_x + int(35*scale_f), pet_y + 15 - int(8*scale_f))])
        pygame.draw.polygon(screen, (180, 160, 140), 
                          [(pet_x + 40, pet_y - 8), (pet_x + 35, pet_y + 5), (pet_x + 45, pet_y - 5)])
        # Olhos
        pygame.draw.circle(screen, (0, 0, 0), (int(pet_x + 32), int(pet_y + 3)), 3)
        pygame.draw.circle(screen, (0, 0, 0), (int(pet_x + 40), int(pet_y + 3)), 3)
        # Roupa laranja (como na imagem)
        pygame.draw.rect(screen, (255, 140, 0), (int(pet_x + 5), int(pet_y + 15), 30, 15), border_radius=3)
