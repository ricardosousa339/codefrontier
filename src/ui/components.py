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
        
        # Efeito de brilho quando hover
        if self.is_hovered:
            glow_size = int(10 + 5 * math.sin(self.pulse))
            glow_rect = self.rect.inflate(glow_size * 2, glow_size * 2)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.ellipse(glow_surface, (*self.module_data["color"], 80), 
                              (0, 0, glow_rect.width, glow_rect.height))
            screen.blit(glow_surface, glow_rect.topleft)
        
        # Ícone do módulo (círculo com cor)
        if self.icon:
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
        
        # Mensagens
        y_offset = 10
        small_font = pygame.font.Font(None, 20)
        for msg in self.messages[-3:]:  # Mostrar últimas 3
            color = Colors.CYAN if msg["is_ai"] else Colors.WHITE
            text = small_font.render(msg["text"][:50], True, color)
            screen.blit(text, (self.rect.x + 10, self.rect.y + y_offset))
            y_offset += 25
            
        # Campo de input
        pygame.draw.rect(screen, (60, 60, 70), self.input_rect, border_radius=5)
        pygame.draw.rect(screen, Colors.WHITE if self.is_active else (100, 100, 100), 
                        self.input_rect, 1, border_radius=5)
        
        # Texto placeholder ou input
        if self.input_text:
            input_surface = small_font.render(self.input_text[-30:], True, Colors.WHITE)
        else:
            input_surface = small_font.render("Digite sua dúvida aqui...", True, (150, 150, 150))
        screen.blit(input_surface, (self.input_rect.x + 5, self.input_rect.y + 8))
        
        # Ícone do assistente
        if assistant_img:
            # Redimensionar assistente para caber melhor
            assist_scaled = pygame.transform.scale(assistant_img, (60, 60))
            screen.blit(assist_scaled, (self.rect.right - 65, self.rect.bottom - 75))
            
        # Label "Ajuda CinthIA!" - dentro do rect
        tiny_font = pygame.font.Font(None, 16)
        label = tiny_font.render("Ajuda CinthIA!", True, Colors.GOLD)
        screen.blit(label, (self.rect.right - 75, self.rect.bottom - 12))


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
        self.rect = pygame.Rect(x - 60, y - 60, 120, 120)
        self.is_hovered = False
        
    def update(self, mouse_pos):
        """Atualiza a área"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def draw(self, screen, font):
        """Desenha a área"""
        # Placeholder para ícone da área
        if self.icon:
            icon_rect = self.icon.get_rect(center=(self.x, self.y))
            screen.blit(self.icon, icon_rect)
        else:
            pygame.draw.circle(screen, Colors.BROWN_LIGHT, (self.x, self.y), 50)
            
        # Placa indicadora
        sign_rect = pygame.Rect(self.x - 50, self.y + 55, 100, 30)
        
        # Poste da placa
        pygame.draw.rect(screen, (139, 90, 43), (self.x - 5, self.y + 60, 10, 40))
        
        # Placa
        pygame.draw.rect(screen, (180, 140, 100), sign_rect, border_radius=3)
        pygame.draw.rect(screen, (100, 70, 40), sign_rect, 2, border_radius=3)
        
        # Texto
        small_font = pygame.font.Font(None, 22)
        text = small_font.render(self.area_data["name"], True, Colors.TEXT_DARK)
        text_rect = text.get_rect(center=sign_rect.center)
        screen.blit(text, text_rect)
        
        # Highlight quando hover
        if self.is_hovered:
            pygame.draw.circle(screen, (*Colors.GOLD, 100), (self.x, self.y), 55, 3)
            
    def is_clicked(self, event):
        """Verifica se a área foi clicada"""
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False
