# 📦 Guia de Assets - CodeFrontier

Este documento explica como organizar e salvar seus assets para o jogo.

---

## 📁 Estrutura de Pastas

```
assets/
├── images/
│   ├── backgrounds/     # Fundos das telas
│   ├── characters/      # Personagens e NPCs
│   ├── icons/           # Ícones do sistema (vida, etc)
│   ├── modules/         # Ícones dos módulos de programação
│   ├── locations/       # Construções e locais do vilarejo
│   └── ui/              # Elementos de interface
├── sounds/
│   ├── music/           # Músicas de fundo
│   ├── sfx/             # Efeitos sonoros
│   └── voice/           # Vozes (opcional)
└── fonts/               # Fontes personalizadas
```

---

## 🖼️ IMAGENS

### Formatos Suportados
- **PNG** (recomendado - suporta transparência)
- JPG, JPEG, BMP, GIF

### Nomenclatura dos Arquivos
O nome do arquivo (sem extensão) será usado como identificador no jogo.

---

### 📂 `images/backgrounds/`

| Arquivo | Tamanho | Descrição |
|---------|---------|-----------|
| `space_bg.png` | 1280x720 | Fundo espacial do menu principal |
| `village_bg.png` | 1280x720 | Fundo do hub do vilarejo |
| `challenge_bg.png` | 1280x720 | Fundo das telas de desafio |

---

### 📂 `images/characters/`

| Arquivo | Tamanho | Descrição |
|---------|---------|-----------|
| `player.png` | 64x64 a 128x128 | Personagem principal (cabelo verde, jaqueta laranja) |
| `assistant.png` | 80x80 a 120x120 | Assistente CinthIA |
| `npc_kayan.png` | 64x64 | NPC Kayan (menino) |
| `pet.png` | 48x48 | Mascote/pet do jogador |

---

### 📂 `images/icons/`

| Arquivo | Tamanho | Descrição |
|---------|---------|-----------|
| `heart_full.png` | 30x30 | Coração cheio (vida) |
| `heart_empty.png` | 30x30 | Coração vazio |
| `star.png` | 24x24 | Estrela (conquistas) |
| `coin.png` | 24x24 | Moeda (recursos) |

---

### 📂 `images/modules/`

| Arquivo | Tamanho | Descrição |
|---------|---------|-----------|
| `csharp_icon.png` | 100x100 | Ícone do módulo C# (tema verde/planta) |
| `python_icon.png` | 100x100 | Ícone do módulo Python (tema roxo/gato mago) |
| `php_icon.png` | 100x100 | Ícone do módulo PHP (tema dourado/escudo) |
| `javascript_icon.png` | 100x100 | Ícone do módulo JavaScript (tema laranja/forja) |

---

### 📂 `images/locations/`

| Arquivo | Tamanho | Descrição |
|---------|---------|-----------|
| `arena.png` | 150x150 | Construção da Arena |
| `training.png` | 150x150 | Centro de Treinamento |
| `greenhouse.png` | 150x150 | Estufa |
| `potions.png` | 150x150 | Loja de Poções |

---

### 📂 `images/ui/`

| Arquivo | Tamanho | Descrição |
|---------|---------|-----------|
| `portal.png` | 120x150 | Portal mágico |
| `button.png` | 200x50 | Botão padrão |
| `panel.png` | 400x300 | Painel de diálogo |
| `sign.png` | 100x60 | Placa de sinalização |

---

## 🔊 SONS

### Formatos Suportados
- **OGG** (recomendado para músicas)
- **WAV** (recomendado para efeitos)
- MP3

---

### 📂 `sounds/music/`

| Arquivo | Descrição |
|---------|-----------|
| `menu_theme.ogg` | Música do menu principal |
| `village_theme.ogg` | Música do vilarejo |
| `challenge_theme.ogg` | Música durante desafios |
| `victory.ogg` | Música de vitória |

---

### 📂 `sounds/sfx/`

| Arquivo | Descrição |
|---------|-----------|
| `click.wav` | Clique em botão |
| `hover.wav` | Mouse sobre elemento |
| `success.wav` | Código correto |
| `error.wav` | Código incorreto |
| `typing.wav` | Som de digitação |
| `portal_open.wav` | Portal abrindo |
| `level_up.wav` | Subir de nível |

---

### 📂 `sounds/voice/`

| Arquivo | Descrição |
|---------|-----------|
| `assistant_greeting.ogg` | Saudação da CinthIA |
| `assistant_hint.ogg` | Dica da assistente |

---

## 🔤 FONTES

### Formatos Suportados
- **TTF** (TrueType)
- OTF (OpenType)

### 📂 `fonts/`

| Arquivo | Uso |
|---------|-----|
| `pixel.ttf` | Fonte pixel art para textos do jogo |
| `code.ttf` | Fonte monospace para o editor de código |

---

## ⚙️ Como o Jogo Carrega os Assets

1. O jogo busca automaticamente arquivos nas subpastas de `assets/`
2. O **nome do arquivo** (sem extensão) é usado como identificador
3. Se um asset não for encontrado, um **placeholder** é usado

### Exemplo de Uso no Código:

```python
from src.utils.asset_manager import assets

# Carregar imagem
player_img = assets.get_image("player")

# Carregar som
click_sound = assets.get_sound("click")

# Carregar fonte
title_font = assets.get_font("title")
```

---

## 💡 Dicas

1. **Transparência**: Use PNG com fundo transparente para personagens e ícones
2. **Consistência**: Mantenha tamanhos similares para elementos do mesmo tipo
3. **Otimização**: Comprima imagens sem perder qualidade (TinyPNG)
4. **Nomes**: Use apenas letras minúsculas, números e underscore (`_`)
5. **Backup**: Mantenha os arquivos originais em alta resolução separados

---

## 🎨 Paleta de Cores Sugerida

| Elemento | Cor Hex | Uso |
|----------|---------|-----|
| C# Verde | `#64C864` | Módulo de colheita |
| Python Roxo | `#B464C8` | Módulo de loops |
| PHP Dourado | `#C8B450` | Desafios arcanos |
| JS Laranja | `#DC8C50` | Recursos/forja |
| Fundo Escuro | `#0F0A1E` | Céu espacial |
| Madeira | `#8B5A2B` | Vilarejo |

---

## ✅ Checklist de Assets Essenciais

- [ ] `space_bg.png` - Fundo do menu
- [ ] `village_bg.png` - Fundo do vilarejo  
- [ ] `player.png` - Personagem principal
- [ ] `assistant.png` - CinthIA
- [ ] `heart_full.png` e `heart_empty.png` - Sistema de vidas
- [ ] `csharp_icon.png`, `python_icon.png`, `php_icon.png`, `javascript_icon.png` - Módulos
- [ ] `portal.png` - Portal central
- [ ] `menu_theme.ogg` - Música do menu
- [ ] `click.wav` - Som de clique
