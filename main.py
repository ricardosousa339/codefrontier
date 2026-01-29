# CodeFrontier - Jogo Educacional de Programação
# Arquivo principal do jogo

import pygame
import sys
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, Colors
from src.utils import assets
from src.scenes import MainMenuScene, VillageHubScene, ChallengeScene, LessonScene

class Game:
    """Classe principal do jogo CodeFrontier"""
    
    def __init__(self):
        # Inicializar Pygame
        pygame.init()
        pygame.mixer.init()
        
        # Configurar tela
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        
        # Clock para controle de FPS
        self.clock = pygame.time.Clock()
        
        # Estado do jogo
        self.running = True
        self.current_scene = None
        
        # Dados do jogador
        self.player_data = {
            "health": 5,
            "max_health": 5,
            "xp": 0,
            "level": 1,
            "completed_modules": [],
            "current_module": None
        }
        
        # Carregar assets
        self._load_assets()
        
        # Inicializar cenas
        self._init_scenes()
        
    def _load_assets(self):
        """Carrega todos os assets do jogo"""
        print("Carregando assets...")
        assets.load_all_assets()
        print("Assets carregados com sucesso!")
        
    def _init_scenes(self):
        """Inicializa as cenas do jogo"""
        self.scenes = {
            "menu": MainMenuScene(self),
            "village": VillageHubScene(self),
            "challenge": ChallengeScene(self),
            "lesson": LessonScene(self)
        }
        
        # Começar no menu principal
        self.current_scene = self.scenes["menu"]
        self.current_scene.on_enter()
        
    def change_scene(self, scene_name, **kwargs):
        """Muda para uma nova cena"""
        if self.current_scene:
            self.current_scene.on_exit()
            
        if scene_name == "challenge":
            # Criar nova cena de desafio com parâmetros
            module_id = kwargs.get("module_id", "csharp")
            self.scenes["challenge"] = ChallengeScene(self, module_id)
            
        self.current_scene = self.scenes.get(scene_name)
        if self.current_scene:
            self.current_scene.on_enter()
            
    def run(self):
        """Loop principal do jogo"""
        print("Iniciando CodeFrontier...")
        print("Pressione ESC para voltar ao menu ou sair")
        
        while self.running:
            # Calcular delta time
            dt = self.clock.tick(FPS) / 1000.0
            
            # Processar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.current_scene != self.scenes["menu"]:
                            self.change_scene("menu")
                        else:
                            self.running = False
                            
                # Passar evento para a cena atual
                if self.current_scene:
                    self.current_scene.handle_event(event)
                    
            # Atualizar cena atual
            if self.current_scene:
                self.current_scene.update(dt)
                
                # Verificar mudança de cena
                if self.current_scene.next_scene:
                    next_scene = self.current_scene.next_scene
                    self.current_scene.next_scene = None
                    
                    # Pegar módulo selecionado se aplicável
                    if hasattr(self.current_scene, 'selected_module'):
                        module_id = self.current_scene.selected_module
                        self.change_scene(next_scene, module_id=module_id)
                    else:
                        self.change_scene(next_scene)
                        
            # Desenhar
            if self.current_scene:
                self.current_scene.draw(self.screen)
                
            # Atualizar display
            pygame.display.flip()
            
        # Finalizar
        self._quit()
        
    def _quit(self):
        """Finaliza o jogo"""
        print("Encerrando CodeFrontier...")
        pygame.mixer.quit()
        pygame.quit()
        sys.exit()


def main():
    """Função principal"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
