# Configurações globais do jogo CodeFrontier

import pygame

# Configurações da tela
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "CodeFrontier - Aprenda Programação"

# Cores do tema
class Colors:
    # Cores principais
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    # Cores do espaço/fundo
    SPACE_DARK = (15, 10, 30)
    SPACE_PURPLE = (40, 20, 60)
    
    # Cores de UI
    BROWN_DARK = (60, 40, 30)
    BROWN_LIGHT = (120, 80, 60)
    WOOD = (139, 90, 43)
    
    # Cores de destaque
    GOLD = (255, 215, 0)
    GREEN = (50, 205, 50)
    RED = (220, 20, 60)
    BLUE = (65, 105, 225)
    PURPLE = (148, 0, 211)
    ORANGE = (255, 140, 0)
    PINK = (255, 105, 180)
    CYAN = (0, 255, 255)
    
    # Cores de código
    CODE_BG = (30, 30, 30)
    CODE_GREEN = (78, 201, 176)
    CODE_BLUE = (86, 156, 214)
    CODE_YELLOW = (220, 220, 170)
    CODE_PINK = (206, 145, 120)
    CODE_PURPLE = (197, 134, 192)
    
    # Cores de texto
    TEXT_LIGHT = (240, 240, 240)
    TEXT_DARK = (40, 40, 40)
    
    # Cores de módulos
    CSHARP_GREEN = (100, 200, 100)
    PYTHON_PURPLE = (180, 100, 200)
    PHP_YELLOW = (200, 180, 80)
    JS_ORANGE = (220, 140, 80)

# Estados do jogo
class GameState:
    MENU = "menu"
    VILLAGE_HUB = "village_hub"
    MODULE_SELECT = "module_select"
    CHALLENGE = "challenge"
    SETTINGS = "settings"
    CREDITS = "credits"

# Módulos de programação
MODULES = {
    "csharp": {
        "name": "Colhendo com C#",
        "description": "Aprenda os fundamentos do C# enquanto colhe frutas no pomar!",
        "color": Colors.CSHARP_GREEN,
        "icon": "csharp_icon",
        "lessons": ["Variáveis", "Funções", "Classes", "Loops"]
    },
    "python": {
        "name": "Loops Mágicos com Python",
        "description": "Domine loops e magia com Python!",
        "color": Colors.PYTHON_PURPLE,
        "icon": "python_icon",
        "lessons": ["For Loops", "While Loops", "List Comprehension", "Funções"]
    },
    "php": {
        "name": "Desafios Arcanos com PHP",
        "description": "Enfrente desafios arcanos usando PHP!",
        "color": Colors.PHP_YELLOW,
        "icon": "php_icon",
        "lessons": ["Arrays", "Strings", "Funções", "OOP"]
    },
    "javascript": {
        "name": "Aprimorando Recursos com JavaScript",
        "description": "Aprimore suas habilidades com JavaScript!",
        "color": Colors.JS_ORANGE,
        "icon": "js_icon",
        "lessons": ["DOM", "Eventos", "Promises", "Fetch API"]
    }
}

# Áreas do vilarejo
VILLAGE_AREAS = {
    "training": {
        "name": "Treinamento",
        "description": "Pratique suas habilidades de programação",
        "position": (200, 150)
    },
    "potions": {
        "name": "Poções",
        "description": "Crie soluções mágicas de código",
        "position": (900, 150)
    },
    "arena": {
        "name": "Arena",
        "description": "Desafie outros programadores",
        "position": (200, 500)
    },
    "greenhouse": {
        "name": "Estufa",
        "description": "Cultive seus projetos",
        "position": (900, 500)
    }
}

# Configurações do jogador
PLAYER_START_HEALTH = 5
PLAYER_MAX_HEALTH = 5

# Configurações de fonte
FONT_SIZES = {
    "small": 16,
    "medium": 24,
    "large": 32,
    "title": 48,
    "huge": 64
}
