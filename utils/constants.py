"""
🫧 BUBBLETECH - Constantes del Juego
"""
import pygame

# ============================================================================
# CONFIGURACIÓN DE PANTALLA
# ============================================================================
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# ============================================================================
# PALETA DE COLORES - Estilo Cyber-Cartoon Neón
# ============================================================================
class Colors:
    # Fondos
    BG_DARK = (12, 12, 28)
    BG_GRID = (20, 25, 50)
    
    # Burbujas base
    BUBBLE_CYAN = (0, 255, 220)
    BUBBLE_PINK = (255, 80, 200)
    BUBBLE_GOLD = (255, 200, 0)
    
    # Elementos especiales
    FIRE_ORANGE = (255, 100, 50)
    ICE_BLUE = (100, 200, 255)
    ELECTRIC_PURPLE = (200, 50, 255)
    
    # Jugador
    PLAYER_TEAL = (0, 230, 255)
    PLAYER_GLOW = (100, 255, 255)
    
    # Enemigos
    ENEMY_RED = (255, 60, 80)
    ENEMY_GREEN = (100, 255, 100)
    ENEMY_PURPLE = (180, 80, 255)
    
    # UI
    TEXT_WHITE = (255, 255, 255)
    TEXT_GLOW = (200, 240, 255)
    TEXT_GRAY = (150, 150, 180)
    TEXT_DARK = (80, 80, 100)
    SCORE_GOLD = (255, 220, 100)
    
    # Plataformas
    PLATFORM_BASE = (60, 70, 120)
    PLATFORM_GLOW = (100, 150, 255)

# ============================================================================
# FÍSICA
# ============================================================================
GRAVITY = 0.6
JUMP_FORCE = -14
MOVE_SPEED = 5
MAX_FALL_SPEED = 12
BUBBLE_SPEED = 8
BUBBLE_LIFETIME = 240  # 4 segundos a 60 FPS

# ============================================================================
# TIPOS DE BURBUJAS
# ============================================================================
class BubbleType:
    NORMAL = "normal"
    FIRE = "fire"
    ICE = "ice"
    ELECTRIC = "electric"
    MEGA = "mega"  # Fusión de 2 burbujas

BUBBLE_COLORS = {
    BubbleType.NORMAL: Colors.BUBBLE_CYAN,
    BubbleType.FIRE: Colors.FIRE_ORANGE,
    BubbleType.ICE: Colors.ICE_BLUE,
    BubbleType.ELECTRIC: Colors.ELECTRIC_PURPLE,
    BubbleType.MEGA: Colors.BUBBLE_GOLD,
}

# ============================================================================
# DIFICULTAD
# ============================================================================
ENEMY_SPAWN_BASE = 180  # Frames entre spawns
ENEMY_SPAWN_MIN = 60
MAX_BUBBLES = 6  # Burbujas simultáneas del jugador
LEVEL_GOAL_ENEMIES = 15  # Enemigos que deben ser eliminados para pasar de nivel

# ============================================================================
# DIMENSIONES de ENTIDADES
# ============================================================================
PLAYER_SIZE = 32
BUBBLE_RADIUS = 24
ENEMY_SIZE = 28
PLATFORM_HEIGHT = 16

# Inicialización de fuentes (se carga en main)
fonts = {}

def init_fonts():
    """Inicializa las fuentes del juego"""
    pygame.font.init()
    fonts['title'] = pygame.font.Font(None, 72)
    fonts['large'] = pygame.font.Font(None, 48)
    fonts['medium'] = pygame.font.Font(None, 32)
    fonts['small'] = pygame.font.Font(None, 24)
