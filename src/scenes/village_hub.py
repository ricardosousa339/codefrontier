# Hub do vilarejo

import pygame
import math
from .base_scene import Scene
from src.config import Colors, VILLAGE_AREAS, SCREEN_WIDTH, SCREEN_HEIGHT
from src.ui import Button, VillageArea
from src.utils import assets

class VillageHubScene(Scene):
    """Cena do hub do vilarejo com diferentes áreas"""
    
    def __init__(self, game):
        super().__init__(game)
        
        # Áreas do vilarejo
        self.areas = []
        area_positions = {
            "training": (280, 200),
            "potions": (1000, 200),
            "arena": (280, 520),
            "greenhouse": (1000, 520)
        }
        
        for area_id, area_data in VILLAGE_AREAS.items():
            x, y = area_positions.get(area_id, area_data["position"])
            area = VillageArea(x, y, area_id, area_data)
            self.areas.append(area)
            
        # Botão de voltar
        self.back_button = Button(50, 650, 150, 40, "← Voltar")
        
        # Personagem do jogador no centro
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT // 2
        self.player_animation = 0
        
        # Dica/tooltip atual
        self.current_tooltip = None
        
    def handle_event(self, event):
        """Processa eventos"""
        if self.back_button.is_clicked(event):
            self.next_scene = "menu"
            
        for area in self.areas:
            if area.is_clicked(event):
                if area.area_id == "training":
                    self.next_scene = "challenge"
                else:
                    # Por enquanto, mostrar mensagem de "em breve"
                    self.current_tooltip = f"{area.area_data['name']} - Em breve!"
                    
    def update(self, dt):
        """Atualiza a cena"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        self.back_button.update(mouse_pos, mouse_pressed)
        
        for area in self.areas:
            area.update(mouse_pos)
            
        # Animação do personagem
        self.player_animation = (self.player_animation + dt * 2) % (2 * math.pi)
        
        # Limpar tooltip se não estiver sobre nenhuma área
        hovering = any(area.is_hovered for area in self.areas)
        if not hovering:
            self.current_tooltip = None
        else:
            for area in self.areas:
                if area.is_hovered:
                    self.current_tooltip = area.area_data["description"]
                    
    def draw(self, screen):
        """Desenha a cena"""
        # Fundo do vilarejo
        bg = assets.get_image("village_bg")
        if bg:
            screen.blit(bg, (0, 0))
        else:
            self._draw_village_background(screen)
            
        # Desenhar áreas
        font = assets.get_font("medium")
        for area in self.areas:
            self._draw_area_building(screen, area)
            area.draw(screen, font)
            
        # Desenhar personagem no centro
        self._draw_player(screen)
        
        # Desenhar botão de voltar
        self.back_button.draw(screen, font)
        
        # Título
        title_font = assets.get_font("title")
        title = title_font.render("VILAREJO", True, Colors.TEXT_DARK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 40))
        screen.blit(title, title_rect)
        
        # Tooltip
        if self.current_tooltip:
            self._draw_tooltip(screen)
            
    def _draw_village_background(self, screen):
        """Desenha o fundo do vilarejo"""
        # Fundo claro
        screen.fill((210, 210, 230))
        
        # Hexágono de madeira
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        size = 380
        points = []
        for i in range(6):
            angle = math.pi / 3 * i - math.pi / 6
            x = cx + size * math.cos(angle)
            y = cy + size * math.sin(angle)
            points.append((x, y))
            
        # Piso de madeira
        pygame.draw.polygon(screen, (139, 90, 43), points)
        
        # Linhas de tábuas
        for i in range(-5, 6):
            y = cy + i * 60
            pygame.draw.line(screen, (120, 70, 35), (cx - 350, y), (cx + 350, y), 2)
            
        # Borda do hexágono
        pygame.draw.polygon(screen, (100, 60, 30), points, 5)
        
    def _draw_area_building(self, screen, area):
        """Desenha um prédio placeholder para a área"""
        x, y = area.x, area.y
        
        # Diferentes estilos por área
        if area.area_id == "training":
            # Torre de treinamento
            pygame.draw.rect(screen, (150, 130, 110), (x - 50, y - 80, 100, 100))
            pygame.draw.polygon(screen, (139, 69, 19), 
                              [(x - 55, y - 80), (x, y - 130), (x + 55, y - 80)])
            # Alvos
            pygame.draw.circle(screen, (200, 50, 50), (x + 30, y - 40), 15)
            pygame.draw.circle(screen, (255, 255, 255), (x + 30, y - 40), 10)
            pygame.draw.circle(screen, (200, 50, 50), (x + 30, y - 40), 5)
            
        elif area.area_id == "potions":
            # Caldeirão
            pygame.draw.ellipse(screen, (40, 40, 40), (x - 40, y - 30, 80, 50))
            pygame.draw.arc(screen, (60, 60, 60), (x - 45, y - 50, 90, 70), 3.5, 6, 5)
            # Líquido verde
            pygame.draw.ellipse(screen, (50, 200, 50), (x - 30, y - 25, 60, 30))
            # Bolhas
            pygame.draw.circle(screen, (100, 255, 100), (x - 10, y - 35), 8)
            pygame.draw.circle(screen, (100, 255, 100), (x + 15, y - 40), 5)
            
        elif area.area_id == "arena":
            # Coliseu/Arena
            pygame.draw.ellipse(screen, (180, 140, 100), (x - 70, y - 50, 140, 80))
            pygame.draw.ellipse(screen, (150, 110, 70), (x - 60, y - 40, 120, 60))
            # Bandeiras
            pygame.draw.line(screen, (139, 69, 19), (x - 50, y - 60), (x - 50, y - 100), 3)
            pygame.draw.polygon(screen, (200, 50, 50), 
                              [(x - 50, y - 100), (x - 30, y - 90), (x - 50, y - 80)])
            
        elif area.area_id == "greenhouse":
            # Casa/Estufa
            pygame.draw.rect(screen, (180, 150, 120), (x - 50, y - 60, 100, 80))
            pygame.draw.polygon(screen, (139, 69, 19), 
                              [(x - 55, y - 60), (x, y - 100), (x + 55, y - 60)])
            # Janela
            pygame.draw.rect(screen, (100, 150, 200), (x - 20, y - 40, 40, 30))
            pygame.draw.line(screen, (139, 69, 19), (x, y - 40), (x, y - 10), 2)
            pygame.draw.line(screen, (139, 69, 19), (x - 20, y - 25), (x + 20, y - 25), 2)
            # Porta
            pygame.draw.rect(screen, (100, 60, 30), (x - 15, y - 5, 30, 25))
            
    def _draw_player(self, screen):
        """Desenha o personagem do jogador"""
        # Plataforma brilhante
        platform_y = self.player_y + 30
        glow = int(50 + 20 * math.sin(self.player_animation))
        pygame.draw.ellipse(screen, (100, 200, 255, glow), 
                          (self.player_x - 40, platform_y, 80, 30))
        pygame.draw.ellipse(screen, (150, 220, 255), 
                          (self.player_x - 35, platform_y + 5, 70, 20))
        
        # Personagem
        player_img = assets.get_image("player")
        if player_img:
            # Pequena animação de flutuação
            offset_y = int(math.sin(self.player_animation) * 3)
            player_scaled = pygame.transform.scale(player_img, (80, 80))
            screen.blit(player_scaled, (self.player_x - 40, self.player_y - 50 + offset_y))
        else:
            # Placeholder
            pygame.draw.circle(screen, (255, 200, 180), 
                             (self.player_x, self.player_y - 30), 20)
            pygame.draw.rect(screen, (255, 140, 0), 
                           (self.player_x - 15, self.player_y - 10, 30, 40))
                           
    def _draw_tooltip(self, screen):
        """Desenha tooltip com descrição"""
        font = assets.get_font("medium")
        text = font.render(self.current_tooltip, True, Colors.TEXT_LIGHT)
        
        # Fundo do tooltip
        padding = 15
        tooltip_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        bg_rect = tooltip_rect.inflate(padding * 2, padding)
        
        pygame.draw.rect(screen, (40, 40, 50, 220), bg_rect, border_radius=8)
        pygame.draw.rect(screen, Colors.GOLD, bg_rect, 2, border_radius=8)
        
        screen.blit(text, tooltip_rect)
