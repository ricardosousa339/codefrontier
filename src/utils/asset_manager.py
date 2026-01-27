# Gerenciador de assets do jogo

import pygame
import os
from pathlib import Path

class AssetManager:
    """Gerencia todos os assets do jogo (imagens, sons, fontes)"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.base_path = Path(__file__).parent.parent.parent / "assets"
        
    def load_all_assets(self):
        """Carrega todos os assets do jogo"""
        self._load_images()
        self._load_sounds()
        self._load_fonts()
        self._create_placeholder_assets()
        
    def _load_images(self):
        """Carrega imagens das subpastas de assets/images/"""
        images_path = self.base_path / "images"
        
        if not images_path.exists():
            print(f"[AssetManager] Pasta de imagens não encontrada: {images_path}")
            return
            
        # Estrutura esperada:
        # assets/images/
        #   ├── backgrounds/    (space_bg.png, village_bg.png, challenge_bg.png)
        #   ├── characters/     (player.png, assistant.png, npc_kayan.png)
        #   ├── icons/          (heart_full.png, heart_empty.png)
        #   ├── modules/        (csharp_icon.png, python_icon.png, php_icon.png, javascript_icon.png)
        #   ├── locations/      (arena.png, training.png, greenhouse.png, potions.png)
        #   └── ui/             (portal.png, button.png, panel.png)
        
        image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}
        
        for folder in images_path.iterdir():
            if folder.is_dir():
                for image_file in folder.iterdir():
                    if image_file.suffix.lower() in image_extensions:
                        name = image_file.stem  # Nome sem extensão
                        try:
                            img = pygame.image.load(str(image_file)).convert_alpha()
                            self.images[name] = img
                            print(f"[AssetManager] Imagem carregada: {name}")
                        except pygame.error as e:
                            print(f"[AssetManager] Erro ao carregar {image_file}: {e}")
                            
    def _load_sounds(self):
        """Carrega sons e músicas de assets/sounds/"""
        sounds_path = self.base_path / "sounds"
        
        if not sounds_path.exists():
            print(f"[AssetManager] Pasta de sons não encontrada: {sounds_path}")
            return
            
        # Estrutura esperada:
        # assets/sounds/
        #   ├── music/      (menu_theme.ogg, village_theme.ogg, challenge_theme.ogg)
        #   ├── sfx/        (click.wav, success.wav, error.wav, typing.wav)
        #   └── voice/      (assistant_greeting.ogg)
        
        sound_extensions = {'.wav', '.ogg', '.mp3'}
        
        for folder in sounds_path.iterdir():
            if folder.is_dir():
                for sound_file in folder.iterdir():
                    if sound_file.suffix.lower() in sound_extensions:
                        name = sound_file.stem
                        try:
                            sound = pygame.mixer.Sound(str(sound_file))
                            self.sounds[name] = sound
                            print(f"[AssetManager] Som carregado: {name}")
                        except pygame.error as e:
                            print(f"[AssetManager] Erro ao carregar {sound_file}: {e}")
        
    def _create_placeholder_assets(self):
        """Cria assets placeholder apenas para os que não foram carregados"""
        
        # Só cria placeholder se não existe o asset real
        if "csharp_icon" not in self.images:
            module_colors = {
                "csharp": (100, 200, 100),
                "python": (180, 100, 200),
                "php": (200, 180, 80),
                "javascript": (220, 140, 80)
            }
            
            for module, color in module_colors.items():
                if f"{module}_icon" not in self.images:
                    surface = pygame.Surface((100, 100), pygame.SRCALPHA)
                    pygame.draw.circle(surface, color, (50, 50), 45)
                    pygame.draw.circle(surface, (255, 255, 255), (50, 50), 35, 3)
                    self.images[f"{module}_icon"] = surface
            
        # Placeholder para coração
        if "heart_full" not in self.images:
            heart = pygame.Surface((30, 30), pygame.SRCALPHA)
            self._draw_heart(heart, (220, 20, 60))
            self.images["heart_full"] = heart
        
        if "heart_empty" not in self.images:
            heart_empty = pygame.Surface((30, 30), pygame.SRCALPHA)
            self._draw_heart(heart_empty, (80, 80, 80))
            self.images["heart_empty"] = heart_empty
        
        # Placeholder para personagem
        if "player" not in self.images:
            player = pygame.Surface((64, 64), pygame.SRCALPHA)
            # Corpo
            pygame.draw.rect(player, (255, 140, 0), (20, 25, 24, 30))  # Jaqueta laranja
            pygame.draw.rect(player, (80, 80, 200), (22, 30, 20, 20))  # Interior
            # Cabeça
            pygame.draw.circle(player, (255, 220, 180), (32, 18), 14)  # Rosto
            # Cabelo verde
            pygame.draw.ellipse(player, (50, 200, 100), (18, 4, 28, 18))
            self.images["player"] = player
        
        # Placeholder para portal
        if "portal" not in self.images:
            portal = pygame.Surface((120, 150), pygame.SRCALPHA)
            for i in range(5):
                alpha = 255 - i * 40
                color = (100, 150, 255, alpha)
                pygame.draw.ellipse(portal, color, (10 + i*5, 10 + i*5, 100 - i*10, 130 - i*10), 3)
            self.images["portal"] = portal
        
        # Placeholder para NPC assistente (CinthIA)
        if "assistant" not in self.images:
            assistant = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.circle(assistant, (255, 200, 180), (40, 30), 20)  # Rosto
            pygame.draw.ellipse(assistant, (139, 69, 19), (20, 10, 40, 25))  # Cabelo
            pygame.draw.rect(assistant, (100, 200, 100), (25, 45, 30, 30))  # Roupa
            self.images["assistant"] = assistant
        
        # Fundo do vilarejo (hexagonal com madeira)
        if "village_bg" not in self.images:
            village_bg = pygame.Surface((1280, 720))
            village_bg.fill((200, 200, 220))  # Fundo claro
            # Desenhar hexágono de madeira
            points = self._get_hexagon_points(640, 360, 350)
            pygame.draw.polygon(village_bg, (139, 90, 43), points)
            pygame.draw.polygon(village_bg, (100, 60, 30), points, 5)
            self.images["village_bg"] = village_bg
        
        # Fundo espacial para menu
        if "space_bg" not in self.images:
            space_bg = pygame.Surface((1280, 720))
            space_bg.fill((15, 10, 30))
            # Adicionar estrelas
            import random
            random.seed(42)  # Para consistência
            for _ in range(200):
                x = random.randint(0, 1280)
                y = random.randint(0, 720)
                size = random.randint(1, 3)
                brightness = random.randint(150, 255)
                pygame.draw.circle(space_bg, (brightness, brightness, brightness), (x, y), size)
            self.images["space_bg"] = space_bg
        
    def _draw_heart(self, surface, color):
        """Desenha um coração estilo pixel art"""
        # Coração simplificado
        points = [
            (15, 8), (20, 3), (25, 3), (28, 8),
            (28, 12), (15, 27), (2, 12), (2, 8),
            (5, 3), (10, 3), (15, 8)
        ]
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, (255, 255, 255), points, 1)
        
    def _get_hexagon_points(self, cx, cy, size):
        """Retorna os pontos de um hexágono"""
        import math
        points = []
        for i in range(6):
            angle = math.pi / 3 * i - math.pi / 6
            x = cx + size * math.cos(angle)
            y = cy + size * math.sin(angle)
            points.append((x, y))
        return points
        
    def _load_fonts(self):
        """Carrega as fontes do jogo"""
        # Usar fonte padrão do pygame por enquanto
        self.fonts["small"] = pygame.font.Font(None, 20)
        self.fonts["medium"] = pygame.font.Font(None, 28)
        self.fonts["large"] = pygame.font.Font(None, 36)
        self.fonts["title"] = pygame.font.Font(None, 52)
        self.fonts["huge"] = pygame.font.Font(None, 72)
        self.fonts["code"] = pygame.font.Font(None, 22)
        
    def get_image(self, name):
        """Retorna uma imagem pelo nome"""
        return self.images.get(name)
        
    def get_font(self, size="medium"):
        """Retorna uma fonte pelo tamanho"""
        return self.fonts.get(size, self.fonts["medium"])
        
    def get_sound(self, name):
        """Retorna um som pelo nome"""
        return self.sounds.get(name)


# Singleton global
assets = AssetManager()
