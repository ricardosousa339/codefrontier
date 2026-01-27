# Cena base para todas as cenas do jogo

import pygame
from abc import ABC, abstractmethod

class Scene(ABC):
    """Classe base abstrata para todas as cenas"""
    
    def __init__(self, game):
        self.game = game
        self.next_scene = None
        
    @abstractmethod
    def handle_event(self, event):
        """Processa eventos de input"""
        pass
        
    @abstractmethod
    def update(self, dt):
        """Atualiza a lógica da cena"""
        pass
        
    @abstractmethod
    def draw(self, screen):
        """Desenha a cena na tela"""
        pass
        
    def on_enter(self):
        """Chamado quando a cena é ativada"""
        pass
        
    def on_exit(self):
        """Chamado quando a cena é desativada"""
        pass
