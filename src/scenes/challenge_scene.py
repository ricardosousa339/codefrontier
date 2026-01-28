# Cena de desafio/fase de programação

import pygame
from .base_scene import Scene
from src.config import Colors, SCREEN_WIDTH, SCREEN_HEIGHT
from src.ui import Button, CodeEditor, ChatBox, HealthBar
from src.utils import assets

class ChallengeScene(Scene):
    """Cena de desafio de programação com editor de código"""
    
    def __init__(self, game, module_id="csharp"):
        super().__init__(game)
        self.module_id = module_id
        
        # Layout dividido: visual à esquerda, código à direita
        self.visual_area = pygame.Rect(0, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT)
        self.code_area = pygame.Rect(SCREEN_WIDTH // 2, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT)
        
        # Editor de código
        self.code_editor = CodeEditor(
            SCREEN_WIDTH // 2 + 20, 80,
            SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 - 50
        )
        
        # Código de exemplo baseado nas imagens
        example_code = self._get_example_code(module_id)
        self.code_editor.set_code(example_code)
        
        # Chat box para assistente IA
        self.chat_box = ChatBox(
            SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT - 180,
            SCREEN_WIDTH // 2 - 40, 160
        )
        self.chat_box.add_message("Caso esteja com dúvida em alguma coisa ou travado em alguma parte do código, basta me perguntar!")
        
        # Barra de vida
        self.health_bar = HealthBar(SCREEN_WIDTH - 200, 20, 5)
        
        # Botões
        self.back_button = Button(20, 20, 140, 40, "VOLTAR", font_size="small")
        self.run_button = Button(
            SCREEN_WIDTH // 2 + 30, SCREEN_HEIGHT // 2 + 50,
            180, 45, "EXECUTAR", Colors.GREEN, (80, 220, 80), font_size="small"
        )
        self.hint_button = Button(
            SCREEN_WIDTH // 2 + 230, SCREEN_HEIGHT // 2 + 50,
            120, 45, "DICA", Colors.BLUE, (100, 150, 255), font_size="small"
        )
        
        # Estado do desafio
        self.challenge_data = self._get_challenge_data(module_id)
        self.player_input = ""
        self.show_result = False
        self.result_correct = False
        
        # Animação da cena visual
        self.animation_time = 0
        self.fruits_collected = 0
        
    def _get_example_code(self, module_id):
        """Retorna código de exemplo baseado no módulo"""
        codes = {
            "csharp": """using x.y;
using x.y.z;

private class GetMangos : MonoBehaviour {

    private void SpawnMango(5);
    
    // Digite o código a partir daqui
    
    private void Awake() {
        // ...
    }
}""",
            "python": """# Loops Mágicos com Python

def colher_frutas(quantidade):
    frutas = []
    
    # Digite o código a partir daqui
    for i in range(quantidade):
        frutas.append(f"fruta_{i}")
    
    return frutas

# Teste sua função
resultado = colher_frutas(5)
print(resultado)""",
            "php": """<?php
// Desafios Arcanos com PHP

class Mago {
    private $poder;
    private $mana;
    
    // Digite o código a partir daqui
    
    public function lancarFeitico($nome) {
        // ...
    }
}
?>""",
            "javascript": """import x from 'y';
import z from 'y';

// Aprimorando Recursos com JavaScript

class ForjaDeItens {
    constructor() {
        this.recursos = [];
    }
    
    // Digite o código a partir daqui
    
    criarItem(nome, materiais) {
        // ...
    }
}"""
        }
        return codes.get(module_id, codes["csharp"])
        
    def _get_challenge_data(self, module_id):
        """Retorna dados do desafio"""
        challenges = {
            "csharp": {
                "title": "Ajude Kayan a cuidar do pomar e coletar seus frutos",
                "hint": "Obs: Lembre-se que estudamos recentemente o que função X e Y faziam...",
                "objective": "Chame a função SpawnMango dentro do método Awake"
            },
            "python": {
                "title": "Complete o loop mágico para colher todas as frutas",
                "hint": "Use um loop for com range() para iterar sobre a quantidade",
                "objective": "Complete a função colher_frutas"
            },
            "php": {
                "title": "Implemente o método lancarFeitico do Mago",
                "hint": "O método deve verificar se há mana suficiente",
                "objective": "Complete a classe Mago"
            },
            "javascript": {
                "title": "Crie o sistema de forja de itens",
                "hint": "Use arrays para armazenar os materiais necessários",
                "objective": "Implemente o método criarItem"
            }
        }
        return challenges.get(module_id, challenges["csharp"])
        
    def handle_event(self, event):
        """Processa eventos"""
        if self.back_button.is_clicked(event):
            self.next_scene = "menu"
            
        if self.run_button.is_clicked(event):
            self._run_code()
            
        if self.hint_button.is_clicked(event):
            self.chat_box.add_message(self.challenge_data["hint"])
            
        # Input de texto no chat
        if event.type == pygame.KEYDOWN:
            if self.chat_box.is_active:
                if event.key == pygame.K_RETURN:
                    if self.chat_box.input_text:
                        self.chat_box.add_message(self.chat_box.input_text, is_ai=False)
                        self.chat_box.input_text = ""
                        # Resposta da IA (placeholder)
                        self.chat_box.add_message("Boa pergunta! Vou te ajudar com isso...")
                elif event.key == pygame.K_BACKSPACE:
                    self.chat_box.input_text = self.chat_box.input_text[:-1]
                else:
                    self.chat_box.input_text += event.unicode
                    
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.chat_box.is_active = self.chat_box.input_rect.collidepoint(event.pos)
            
    def update(self, dt):
        """Atualiza a cena"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        self.back_button.update(mouse_pos, mouse_pressed)
        self.run_button.update(mouse_pos, mouse_pressed)
        self.hint_button.update(mouse_pos, mouse_pressed)
        
        self.animation_time += dt
        
    def _run_code(self):
        """Simula execução do código"""
        self.show_result = True
        self.result_correct = True  # Placeholder - sempre sucesso por enquanto
        self.fruits_collected = 5
        self.chat_box.add_message("🎉 Parabéns! Código executado com sucesso!")
        
    def draw(self, screen):
        """Desenha a cena"""
        # Fundo da tela inteira
        bg = assets.get_image("challenge_bg")
        if bg:
            bg_scaled = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(bg_scaled, (0, 0))
        else:
            screen.fill((135, 206, 235))  # Fallback: céu azul
        
        # Dividir a tela
        # Lado esquerdo: elementos dinâmicos da cena (personagens, frutas, etc)
        self._draw_visual_scene(screen)
        
        # Lado direito: código e chat (painel por cima do fundo)
        self._draw_code_area(screen)
        
        # Elementos de UI
        font = assets.get_font("medium")
        self.back_button.draw(screen, font)
        
        # Barra de vida
        heart_full = assets.get_image("heart_full")
        heart_empty = assets.get_image("heart_empty")
        if heart_full and heart_empty:
            self.health_bar.draw(screen, heart_full, heart_empty)
            
    def _draw_visual_scene(self, screen):
        """Desenha a cena visual do desafio"""
        # O fundo challenge_bg já contém as árvores e cenário
        # Aqui apenas desenhamos os personagens e a caixa de missão
        
        # Personagens coletando (Kayan e amiga)
        self._draw_collecting_characters(screen)
        
        # Caixa de missão
        self._draw_mission_box(screen)
        
    def _draw_trees_background(self, screen):
        """Desenha árvores de fundo"""
        for i in range(5):
            x = 50 + i * 120
            y = 200
            # Copa da árvore
            pygame.draw.circle(screen, (34, 100, 34), (x, y), 60)
            pygame.draw.circle(screen, (50, 120, 50), (x - 30, y + 20), 40)
            pygame.draw.circle(screen, (50, 120, 50), (x + 30, y + 20), 40)
            # Tronco
            pygame.draw.rect(screen, (139, 69, 19), (x - 15, y + 40, 30, 80))
            
    def _draw_main_tree(self, screen):
        """Desenha a árvore principal com frutas"""
        cx = SCREEN_WIDTH // 4
        cy = SCREEN_HEIGHT // 2
        
        # Tronco grande
        pygame.draw.rect(screen, (101, 67, 33), (cx - 30, cy, 60, 150))
        
        # Copa grande
        pygame.draw.circle(screen, (34, 139, 34), (cx, cy - 50), 120)
        pygame.draw.circle(screen, (50, 160, 50), (cx - 80, cy), 80)
        pygame.draw.circle(screen, (50, 160, 50), (cx + 80, cy), 80)
        pygame.draw.circle(screen, (40, 150, 40), (cx, cy + 30), 90)
        
        # Frutas (mangas/laranjas)
        import math
        fruit_color = (255, 165, 0)  # Laranja
        if self.module_id == "csharp":
            fruit_color = (255, 200, 50)  # Manga (amarelo)
            
        fruit_positions = [
            (cx - 60, cy - 80), (cx + 40, cy - 70), (cx - 20, cy - 30),
            (cx + 70, cy - 20), (cx - 80, cy + 10), (cx + 30, cy + 20),
            (cx - 40, cy + 50), (cx + 60, cy + 40)
        ]
        
        for i, (fx, fy) in enumerate(fruit_positions):
            if i < 8 - self.fruits_collected:  # Remover frutas coletadas
                # Animação suave
                offset = math.sin(self.animation_time * 2 + i) * 3
                pygame.draw.ellipse(screen, fruit_color, 
                                  (fx - 12, fy + offset - 15, 24, 30))
                pygame.draw.ellipse(screen, (fruit_color[0] - 30, fruit_color[1] - 30, 0), 
                                  (fx - 12, fy + offset - 15, 24, 30), 2)
                                  
    def _draw_collecting_characters(self, screen):
        """Desenha personagem Kayan"""
        import math
        
        # Kayan - maior e mais para baixo
        char1_x = 80
        char1_y = SCREEN_HEIGHT - 180
        bounce = math.sin(self.animation_time * 3) * 5
        
        kayan = assets.get_image("npc_kayan")
        if kayan:
            # Aumentado para 120x120
            kayan_scaled = pygame.transform.scale(kayan, (120, 120))
            screen.blit(kayan_scaled, (char1_x, char1_y + bounce))
        else:
            # Fallback (Corpo Vermelho)
            pygame.draw.rect(screen, (200, 50, 50), (char1_x, char1_y + bounce, 50, 70))
            pygame.draw.circle(screen, (139, 90, 43), (char1_x + 25, char1_y - 20 + bounce), 25)
                        
    def _draw_mission_box(self, screen):
        """Desenha a caixa de missão"""
        # Fundo da caixa - aumentado para caber o texto
        box_rect = pygame.Rect(20, 60, SCREEN_WIDTH // 2 - 40, 120)
        pygame.draw.rect(screen, (255, 230, 150), box_rect, border_radius=10)
        pygame.draw.rect(screen, (200, 150, 50), box_rect, 3, border_radius=10)
        
        # Ícone de missão
        pygame.draw.circle(screen, (100, 100, 200), (box_rect.right - 30, box_rect.top + 30), 20)
        
        # Título da missão (com quebra de linha automática)
        font = assets.get_font("small")
        small_font = assets.get_font("tiny")
        
        # Quebrar título se for muito longo
        title_text = self.challenge_data["title"]
        max_width = box_rect.width - 80  # Espaço para o ícone
        
        # Renderiza e verifica se cabe
        words = title_text.split(" ")
        lines = []
        current_line = []
        for word in words:
            test_line = " ".join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))
        
        y_pos = box_rect.y + 12
        for line in lines[:2]:  # Máximo 2 linhas
            title = font.render(line, True, Colors.TEXT_DARK)
            screen.blit(title, (box_rect.x + 15, y_pos))
            y_pos += 22
        
        # Dica (também com quebra)
        hint_text = self.challenge_data["hint"]
        hint_words = hint_text.split(" ")
        hint_lines = []
        current_hint_line = []
        for word in hint_words:
            test_line = " ".join(current_hint_line + [word])
            if small_font.size(test_line)[0] <= max_width:
                current_hint_line.append(word)
            else:
                if current_hint_line:
                    hint_lines.append(" ".join(current_hint_line))
                current_hint_line = [word]
        if current_hint_line:
            hint_lines.append(" ".join(current_hint_line))
        
        y_pos += 5
        for line in hint_lines[:2]:  # Máximo 2 linhas
            hint = small_font.render(line, True, (100, 100, 100))
            screen.blit(hint, (box_rect.x + 15, y_pos))
            y_pos += 18
        
    def _draw_code_area(self, screen):
        """Desenha a área de código"""
        # Sem fundo escuro - apenas os painéis por cima do challenge_bg
        
        # Título "Editor de Código" com fundo semi-transparente
        font = assets.get_font("large")
        title = font.render(f"Editor de Código", True, Colors.TEXT_LIGHT)
        # Fundo do título
        title_bg = pygame.Surface((SCREEN_WIDTH // 2 - 20, 50), pygame.SRCALPHA)
        pygame.draw.rect(title_bg, (35, 35, 50, 200), (0, 0, SCREEN_WIDTH // 2 - 20, 50), border_radius=8)
        screen.blit(title_bg, (SCREEN_WIDTH // 2 + 10, 10))
        screen.blit(title, (SCREEN_WIDTH // 2 + 20, 20))
        
        # Editor de código
        self.code_editor.draw(screen, font)
        
        # Botões
        font = assets.get_font("medium")
        self.run_button.draw(screen, font)
        self.hint_button.draw(screen, font)
        
        # Linha divisória
        pygame.draw.line(screen, (60, 60, 80), 
                        (SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 110),
                        (SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2 + 110), 2)
        
        # Chat box
        assistant = assets.get_image("assistant")
        self.chat_box.draw(screen, font, assistant)
