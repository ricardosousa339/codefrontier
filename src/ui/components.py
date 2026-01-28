# Componentes de UI do jogo

import pygame
from src.config import Colors, FONT_SIZES
from src.utils import assets

class Button:
    """Botão clicável com estilo RPG"""
    
    def __init__(self, x, y, width, height, text, 
                 color=Colors.BROWN_DARK, hover_color=Colors.BROWN_LIGHT,
                 text_color=Colors.TEXT_LIGHT, font_size="medium"):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font_size = font_size
        self.is_hovered = False
        self.is_pressed = False
        self.enabled = True
        
    def update(self, mouse_pos, mouse_pressed):
        """Atualiza o estado do botão"""
        self.is_hovered = self.rect.collidepoint(mouse_pos) and self.enabled
        self.is_pressed = self.is_hovered and mouse_pressed[0]
        
    def draw(self, screen, font=None):
        """Desenha o botão na tela
        
        Args:
            screen: Superfície onde desenhar
            font: (Opcional) Fonte a ser usada. Se None, usa self.font_size do assets.
        """
        # Se nenhuma fonte for passada, pega do asset_manager usando o tamanho configurado no botão
        if font is None:
            font = assets.get_font(self.font_size)
            
        # Cor atual baseada no estado
        current_color = self.hover_color if self.is_hovered else self.color
        if not self.enabled:
            current_color = (80, 80, 80)
            
        # Sombra
        shadow_rect = self.rect.copy()
        shadow_rect.y += 4
        pygame.draw.rect(screen, (30, 20, 15), shadow_rect, border_radius=8)
        
        # Botão principal
        pygame.draw.rect(screen, current_color, self.rect, border_radius=8)
        
        # Borda
        border_color = Colors.GOLD if self.is_hovered else (100, 70, 50)
        pygame.draw.rect(screen, border_color, self.rect, 3, border_radius=8)
        
        # Texto
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, event):
        """Verifica se o botão foi clicado"""
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            return self.rect.collidepoint(event.pos) and self.enabled
        return False


class ModuleCard:
    """Card de módulo de programação (estilo das imagens)"""
    
    def __init__(self, x, y, module_id, module_data, icon=None):
        self.x = x
        self.y = y
        self.width = 220  # Aumentado para corresponder à largura visual
        self.height = 200  # Altura total: ícone + placa
        self.module_id = module_id
        self.module_data = module_data
        self.icon = icon
        # Área de clique cobre o ícone (acima) e a placa (abaixo)
        self.rect = pygame.Rect(x - self.width//2, y - 80, 
                                self.width, self.height)
        self.is_hovered = False
        self.pulse = 0
        
    def update(self, mouse_pos, dt):
        """Atualiza o card"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.pulse = (self.pulse + dt * 3) % (2 * 3.14159)
        
    def draw(self, screen, font):
        """Desenha o card na tela"""
        import math
        import random
        
        # Efeito de hover elegante estilo pixel art
        if self.is_hovered:
            color = self.module_data["color"]
            
            # Partículas pixeladas flutuando ao redor
            random.seed(42)  # Seed fixa para consistência
            for i in range(12):
                # Posição base circular ao redor do ícone
                angle = (i / 12) * 2 * math.pi + self.pulse
                base_radius = 70 + math.sin(self.pulse * 2 + i) * 10
                
                px = self.x + int(math.cos(angle) * base_radius)
                py = (self.y - 20) + int(math.sin(angle) * base_radius * 0.6)
                
                # Tamanho do pixel (varia entre 3 e 6)
                size = 3 + int(abs(math.sin(self.pulse + i)) * 3)
                
                # Alpha pulsante
                alpha = int(150 + 100 * math.sin(self.pulse * 2 + i * 0.5))
                alpha = max(50, min(255, alpha))
                
                # Desenhar pixel quadrado (estilo pixel art)
                pixel_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                pixel_surface.fill((*color, alpha))
                screen.blit(pixel_surface, (px - size//2, py - size//2))
            
            # Borda pixelada brilhante ao redor do ícone
            border_alpha = int(180 + 75 * math.sin(self.pulse * 3))
            border_surface = pygame.Surface((120, 120), pygame.SRCALPHA)
            
            # Desenhar borda quadrada estilo retro (cantos destacados)
            border_color = (*color, border_alpha)
            # Cantos superiores
            pygame.draw.rect(border_surface, border_color, (0, 0, 15, 4))
            pygame.draw.rect(border_surface, border_color, (0, 0, 4, 15))
            pygame.draw.rect(border_surface, border_color, (105, 0, 15, 4))
            pygame.draw.rect(border_surface, border_color, (116, 0, 4, 15))
            # Cantos inferiores
            pygame.draw.rect(border_surface, border_color, (0, 116, 15, 4))
            pygame.draw.rect(border_surface, border_color, (0, 105, 4, 15))
            pygame.draw.rect(border_surface, border_color, (105, 116, 15, 4))
            pygame.draw.rect(border_surface, border_color, (116, 105, 4, 15))
            
            screen.blit(border_surface, (self.x - 60, self.y - 80))
            
            # Escala sutil no ícone (efeito de "destaque")
            scale_factor = 1.0 + 0.05 * math.sin(self.pulse * 2)
        else:
            scale_factor = 1.0
        
        # Ícone do módulo
        if self.icon:
            if self.is_hovered and scale_factor != 1.0:
                new_size = (int(self.icon.get_width() * scale_factor), 
                           int(self.icon.get_height() * scale_factor))
                scaled_icon = pygame.transform.scale(self.icon, new_size)
                icon_rect = scaled_icon.get_rect(center=(self.x, self.y - 20))
                screen.blit(scaled_icon, icon_rect)
            else:
                icon_rect = self.icon.get_rect(center=(self.x, self.y - 20))
                screen.blit(self.icon, icon_rect)
        else:
            pygame.draw.circle(screen, self.module_data["color"], 
                             (self.x, self.y - 20), 50)
            pygame.draw.circle(screen, Colors.WHITE, 
                             (self.x, self.y - 20), 50, 3)
        
        # Placa de madeira com nome
        # Aumentar tamanho da placa para caber nomes longos
        label_width = 220
        label_height = 80
        label_rect = pygame.Rect(self.x - label_width//2, self.y + 35, 
                               label_width, label_height)
        
        pygame.draw.rect(screen, Colors.BROWN_DARK, label_rect, border_radius=5)
        pygame.draw.rect(screen, (80, 50, 30), label_rect, 2, border_radius=5)
        
        # Nome do módulo (quebra de linha inteligente)
        font = assets.get_font("tiny")
        full_text = self.module_data["name"]
        words = full_text.split(" ")
        name_lines = []
        current_line = []
        
        for word in words:
            # Testa se a palavra cabe na linha atual (com margem de 20px total)
            test_line = " ".join(current_line + [word])
            if font.size(test_line.upper())[0] <= label_width - 20:
                current_line.append(word)
            else:
                if current_line:
                    name_lines.append(" ".join(current_line))
                current_line = [word]
        
        if current_line:
            name_lines.append(" ".join(current_line))
        
        # Calcular altura total do texto para centralizar verticalmente
        line_height = 18
        total_text_height = len(name_lines) * line_height
        
        # Posição inicial Y para centralizar no label_rect
        start_y = label_rect.centery - (total_text_height / 2) + (line_height / 2)
        
        y_offset = 0
        for line in name_lines:
            text = font.render(line.upper(), True, Colors.TEXT_LIGHT)
            text_rect = text.get_rect(center=(self.x, start_y + y_offset))
            screen.blit(text, text_rect)
            y_offset += line_height
            
    def is_clicked(self, event):
        """Verifica se o card foi clicado"""
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False


class HealthBar:
    """Barra de vida com corações estilo pixel art"""
    
    def __init__(self, x, y, max_health=5):
        self.x = x
        self.y = y
        self.max_health = max_health
        self.current_health = max_health
        self.heart_size = 30
        self.heart_spacing = 35
        
    def set_health(self, health):
        """Define a vida atual"""
        self.current_health = max(0, min(health, self.max_health))
        
    def draw(self, screen, heart_full, heart_empty):
        """Desenha a barra de vida"""
        for i in range(self.max_health):
            x = self.x + i * self.heart_spacing
            if i < self.current_health:
                screen.blit(heart_full, (x, self.y))
            else:
                screen.blit(heart_empty, (x, self.y))


class ChatBox:
    """Caixa de chat para o assistente IA"""
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.messages = []
        self.input_text = ""
        self.input_rect = pygame.Rect(x + 10, y + height - 40, width - 100, 30)
        self.is_active = False
        
    def add_message(self, text, is_ai=True):
        """Adiciona uma mensagem ao chat"""
        self.messages.append({"text": text, "is_ai": is_ai})
        # Manter apenas as últimas 5 mensagens
        if len(self.messages) > 5:
            self.messages.pop(0)
            
    def draw(self, screen, font, assistant_img=None):
        """Desenha a caixa de chat"""
        # Fundo semi-transparente
        chat_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(chat_surface, (40, 40, 50, 230), 
                        (0, 0, self.rect.width, self.rect.height), border_radius=10)
        screen.blit(chat_surface, self.rect.topleft)
        
        # Borda
        pygame.draw.rect(screen, Colors.GOLD, self.rect, 2, border_radius=10)
        
        # Mensagens - usar fonte do sistema que suporte acentos
        small_font = pygame.font.SysFont("arial", 14)
        max_width = self.rect.width - 80  # Espaço para o ícone do assistente
        y_offset = 8
        for msg in self.messages[-3:]:  # Mostrar últimas 3
            color = Colors.CYAN if msg["is_ai"] else Colors.WHITE
            
            # Quebrar texto em múltiplas linhas se necessário
            words = msg["text"].split(" ")
            lines = []
            current_line = []
            for word in words:
                test_line = " ".join(current_line + [word])
                if small_font.size(test_line)[0] <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(" ".join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(" ".join(current_line))
            
            # Renderizar cada linha (máximo 2 linhas por mensagem)
            for line in lines[:2]:
                text = small_font.render(line, True, color)
                screen.blit(text, (self.rect.x + 10, self.rect.y + y_offset))
                y_offset += 18
            y_offset += 4  # Espaço extra entre mensagens
            
        # Campo de input
        pygame.draw.rect(screen, (60, 60, 70), self.input_rect, border_radius=5)
        pygame.draw.rect(screen, Colors.WHITE if self.is_active else (100, 100, 100), 
                        self.input_rect, 1, border_radius=5)
        
        # Texto placeholder ou input - usar fonte do sistema
        input_font = pygame.font.SysFont("arial", 14)
        if self.input_text:
            input_surface = input_font.render(self.input_text[-40:], True, Colors.WHITE)
        else:
            input_surface = input_font.render("Digite sua dúvida aqui...", True, (150, 150, 150))
        screen.blit(input_surface, (self.input_rect.x + 5, self.input_rect.y + 8))
        
        # Ícone do assistente
        if assistant_img:
            # Redimensionar assistente para caber melhor
            assist_scaled = pygame.transform.scale(assistant_img, (60, 60))
            screen.blit(assist_scaled, (self.rect.right - 58, self.rect.bottom - 95))
            
        # Label "Ajuda CinthIA!" - usar fonte do sistema
        label_font = pygame.font.SysFont("arial", 12, bold=True)
        label = label_font.render("CinthIA", True, Colors.GOLD)
        screen.blit(label, (self.rect.right - 52, self.rect.bottom - 30))


class CodeEditor:
    """Editor de código simplificado para os desafios"""
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.code_lines = []
        self.current_line = 0
        self.cursor_visible = True
        self.cursor_timer = 0
        
    def set_code(self, code_text):
        """Define o código a ser exibido"""
        self.code_lines = code_text.split("\n")
        
    def draw(self, screen, font):
        """Desenha o editor de código"""
        # Fundo escuro do editor
        pygame.draw.rect(screen, Colors.CODE_BG, self.rect, border_radius=8)
        pygame.draw.rect(screen, (60, 60, 60), self.rect, 2, border_radius=8)
        
        # Fonte monospace para código
        code_font = pygame.font.SysFont("monospace", 18)
        y_offset = 10
        
        for i, line in enumerate(self.code_lines):
            # Colorir syntax básico
            color = Colors.TEXT_LIGHT
            if line.strip().startswith("//") or line.strip().startswith("#"):
                color = Colors.CODE_GREEN
            elif "class " in line or "void " in line or "private " in line or "public " in line or "def " in line:
                color = Colors.CODE_BLUE
            elif "using " in line or "import " in line or "from " in line:
                color = Colors.CODE_PURPLE
                
            text = code_font.render(line, True, color)
            screen.blit(text, (self.rect.x + 15, self.rect.y + y_offset))
            y_offset += 22
            
            if y_offset > self.rect.height - 20:
                break


class VillageArea:
    """Área clicável do vilarejo"""
    
    def __init__(self, x, y, area_id, area_data, icon=None):
        self.x = x
        self.y = y
        self.area_id = area_id
        self.area_data = area_data
        self.icon = icon
        self.rect = pygame.Rect(x - 80, y - 80, 160, 160)
        self.is_hovered = False
        self.pulse = 0  # Para animações
        
    def update(self, mouse_pos, dt=0.016):
        """Atualiza a área"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if self.is_hovered:
            self.pulse += dt * 4
        
    def draw(self, screen, font):
        """Desenha a área com placa de seta apontando para a locação"""
        from src.utils import assets
        import math
        
        # Determinar direção da seta baseado na posição (esquerda ou direita do centro)
        center_x = 640  # SCREEN_WIDTH // 2
        is_left_side = self.x < center_x
        
        # Carregar a placa de seta apropriada (invertido: esquerda usa seta esquerda, direita usa seta direita)
        if is_left_side:
            sign_img = assets.get_image("sign_arrow_left")
        else:
            sign_img = assets.get_image("sign_arrow_right")
        
        # Calcular posição da placa (afastada da locação, em direção ao centro)
        # Offset de 45° em direção ao centro
        offset_x = 120 if is_left_side else -120
        offset_y = 80 if self.y < 360 else -50  # Ajuste baseado se está acima ou abaixo do centro
        
        sign_x = self.x + offset_x
        sign_y = self.y + offset_y
        
        if sign_img:
            # Escalar a placa para tamanho apropriado
            sign_scaled = pygame.transform.scale(sign_img, (180, 120))
            sign_rect = sign_scaled.get_rect(center=(sign_x, sign_y))
            screen.blit(sign_scaled, sign_rect)
            
            # Texto na placa - posição ajustada para dentro da seta
            small_font = pygame.font.SysFont("arial", 14, bold=True)
            text = small_font.render(self.area_data["name"], True, (60, 40, 20))
            # Centralizar texto na parte da placa (ajuste para ficar dentro do corpo da seta)
            text_offset_x = 8 if is_left_side else -8
            text_rect = text.get_rect(center=(sign_x + text_offset_x, sign_y - 20))
            screen.blit(text, text_rect)
        else:
            # Fallback: placa retangular simples
            sign_rect = pygame.Rect(sign_x - 50, sign_y - 15, 100, 30)
            pygame.draw.rect(screen, (180, 140, 100), sign_rect, border_radius=3)
            pygame.draw.rect(screen, (100, 70, 40), sign_rect, 2, border_radius=3)
            small_font = pygame.font.SysFont("arial", 14, bold=True)
            text = small_font.render(self.area_data["name"], True, (60, 40, 20))
            text_rect = text.get_rect(center=sign_rect.center)
            screen.blit(text, text_rect)
        
        # Efeito discreto quando hover
        if self.is_hovered:
            # Cor baseada na área
            area_colors = {
                "training": (255, 200, 100),    # Amarelo quente
                "potions": (150, 100, 255),     # Roxo mágico
                "arena": (255, 100, 100),       # Vermelho batalha
                "greenhouse": (100, 255, 150)   # Verde natureza
            }
            color = area_colors.get(self.area_id, Colors.GOLD)
            
            # Apenas 6 partículas pequenas orbitando
            num_particles = 6
            orbit_radius = 90
            for i in range(num_particles):
                angle = self.pulse + (i * 2 * math.pi / num_particles)
                px = self.x + math.cos(angle) * orbit_radius
                py = self.y - 30 + math.sin(angle) * (orbit_radius * 0.5)
                
                # Tamanho fixo pequeno
                size = 3
                
                # Alpha mais suave
                alpha = int(80 + 40 * math.sin(self.pulse * 2 + i * 0.5))
                
                # Desenhar partícula quadrada pequena
                particle_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.rect(particle_surface, (*color, alpha), (0, 0, size, size))
                screen.blit(particle_surface, (px - size//2, py - size//2))
            
            # Borda retro simples nos cantos
            border_alpha = int(120 + 40 * math.sin(self.pulse * 2))
            border_surface = pygame.Surface((200, 160), pygame.SRCALPHA)
            border_color = (*color, border_alpha)
            
            # Cantos superiores (menores)
            pygame.draw.rect(border_surface, border_color, (0, 0, 12, 3))
            pygame.draw.rect(border_surface, border_color, (0, 0, 3, 12))
            pygame.draw.rect(border_surface, border_color, (188, 0, 12, 3))
            pygame.draw.rect(border_surface, border_color, (197, 0, 3, 12))
            # Cantos inferiores
            pygame.draw.rect(border_surface, border_color, (0, 157, 12, 3))
            pygame.draw.rect(border_surface, border_color, (0, 148, 3, 12))
            pygame.draw.rect(border_surface, border_color, (188, 157, 12, 3))
            pygame.draw.rect(border_surface, border_color, (197, 148, 3, 12))
            
            screen.blit(border_surface, (self.x - 100, self.y - 110))
            
    def is_clicked(self, event):
        """Verifica se a área foi clicada"""
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False
