# CodeFrontier 🎮🎓

Um jogo educacional estilo RPG para aprender programação, desenvolvido com Pygame.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📖 Sobre o Projeto

CodeFrontier é um jogo educacional que ensina conceitos de programação através de desafios interativos em um ambiente de RPG. Os jogadores podem escolher entre diferentes módulos de linguagens de programação e completar tarefas enquanto exploram um mundo mágico.

### 🎯 Módulos Disponíveis

- **Colhendo com C#** - Aprenda fundamentos do C# cuidando de um pomar
- **Loops Mágicos com Python** - Domine loops com magia Python
- **Desafios Arcanos com PHP** - Enfrente desafios usando PHP
- **Aprimorando Recursos com JavaScript** - Aprimore habilidades com JS

### 🏰 Áreas do Vilarejo

- **Treinamento** - Pratique suas habilidades de programação
- **Poções** - Crie soluções mágicas de código
- **Arena** - Desafie outros programadores
- **Estufa** - Cultive seus projetos

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- Pygame 2.5 ou superior

### Instalação

1. Clone ou acesse o repositório:
```bash
cd /home/ricardohenrique/projetos/codefrontier
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o jogo:
```bash
python main.py
```

## 🎮 Controles

| Tecla | Ação |
|-------|------|
| Mouse | Navegar e selecionar opções |
| ESC | Voltar ao menu / Sair |
| Enter | Confirmar (no chat) |

## 📁 Estrutura do Projeto

```
codefrontier/
├── main.py                 # Arquivo principal do jogo
├── requirements.txt        # Dependências Python
├── README.md              # Documentação
├── assets/                # Pasta para imagens, sons e fontes
│   ├── images/
│   ├── sounds/
│   └── fonts/
└── src/
    ├── config.py          # Configurações globais
    ├── utils/
    │   ├── __init__.py
    │   └── asset_manager.py  # Gerenciador de assets
    ├── ui/
    │   ├── __init__.py
    │   └── components.py     # Componentes de UI
    └── scenes/
        ├── __init__.py
        ├── base_scene.py     # Classe base de cenas
        ├── main_menu.py      # Menu principal
        ├── village_hub.py    # Hub do vilarejo
        └── challenge_scene.py # Cena de desafios
```

## 🎨 Recursos

O jogo atualmente usa assets placeholder gerados programaticamente. Para usar suas próprias imagens:

1. Coloque os arquivos na pasta `assets/images/`
2. Modifique o `AssetManager` em `src/utils/asset_manager.py` para carregar as imagens

### Imagens Recomendadas

- Ícones dos módulos (100x100 px)
- Sprite do personagem (64x64 px)
- Backgrounds (1280x720 px)
- Corações de vida (30x30 px)
- Sprites do assistente IA (80x80 px)

## 🔧 Desenvolvimento

### Adicionando Novos Módulos

1. Edite `MODULES` em `src/config.py`
2. Adicione o código de exemplo em `ChallengeScene._get_example_code()`
3. Adicione os dados do desafio em `ChallengeScene._get_challenge_data()`

### Adicionando Novas Áreas

1. Edite `VILLAGE_AREAS` em `src/config.py`
2. Adicione a lógica na `VillageHubScene`

## 📝 Próximos Passos

- [ ] Adicionar sistema de progressão real
- [ ] Implementar validação de código
- [ ] Adicionar mais desafios por módulo
- [ ] Sistema de conquistas
- [ ] Multiplayer (Arena)
- [ ] Integração com IA real para assistente
- [ ] Adicionar sons e música
- [ ] Animações mais elaboradas

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature
3. Fazer commit das mudanças
4. Abrir um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

---

Desenvolvido com 💜 para ensinar programação de forma divertida!
