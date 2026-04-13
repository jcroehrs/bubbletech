"""
🫧 Niveles - BubbleTech
Mapas predefinidos por nivel con ruta garantizada al techo
"""
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLATFORM_HEIGHT

class LevelLayout:
    """Layout de un nivel"""
    def __init__(self, name, platforms, player_start=None, bg_color=None, theme=None):
        self.name = name
        self.platforms = platforms  # Lista de (x, y, w, h)
        self.player_start = player_start  # (x, y)
        self.bg_color = bg_color  # Color de fondo alternativo
        self.theme = theme  # Tema visual

# ============================================================================
# NIVEL 01 — "Iniciación"
# Layout clásico simple con escalera central al techo
# ============================================================================
LEVEL_01 = LevelLayout(
    name="INICIACIÓN",
    player_start=(100, SCREEN_HEIGHT - 100),
    theme="cyber",
    platforms=[
        # Suelo
        (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
        # Plataformas bajas
        (100, SCREEN_HEIGHT - 180, 200, PLATFORM_HEIGHT),
        (400, SCREEN_HEIGHT - 180, 200, PLATFORM_HEIGHT),
        (700, SCREEN_HEIGHT - 180, 200, PLATFORM_HEIGHT),
        # Plataformas medias
        (250, SCREEN_HEIGHT - 320, 180, PLATFORM_HEIGHT),
        (550, SCREEN_HEIGHT - 320, 180, PLATFORM_HEIGHT),
        # 🛤️ ESCALERA AL TECHO — zigzag central
        (150, SCREEN_HEIGHT - 440, 160, PLATFORM_HEIGHT),
        (450, SCREEN_HEIGHT - 520, 160, PLATFORM_HEIGHT),
        (200, SCREEN_HEIGHT - 620, 200, PLATFORM_HEIGHT),
        # 🏁 PLATAFORMA SUPERIOR COMPLETA — zona de recolección
        (0, SCREEN_HEIGHT - 700, SCREEN_WIDTH, PLATFORM_HEIGHT + 4),
    ]
)

# ============================================================================
# NIVEL 02 — "Ascenso"
# Dos torres laterales conectadas por puente superior
# ============================================================================
LEVEL_02 = LevelLayout(
    name="ASCENSO",
    player_start=(80, SCREEN_HEIGHT - 100),
    theme="neon_green",
    platforms=[
        # Suelo
        (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
        # Torre izquierda
        (50, SCREEN_HEIGHT - 200, 150, PLATFORM_HEIGHT),
        (50, SCREEN_HEIGHT - 360, 150, PLATFORM_HEIGHT),
        (50, SCREEN_HEIGHT - 520, 150, PLATFORM_HEIGHT),
        # Torre derecha
        (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200, 150, PLATFORM_HEIGHT),
        (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 360, 150, PLATFORM_HEIGHT),
        (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 520, 150, PLATFORM_HEIGHT),
        # 🛤️ PUENTE SUPERIOR — conecta ambas torres
        (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 580, 400, PLATFORM_HEIGHT),
        # 🏁 PLATAFORMA SUPERIOR COMPLETA — zona de recolección
        (0, SCREEN_HEIGHT - 680, SCREEN_WIDTH, PLATFORM_HEIGHT + 4),
    ]
)

# ============================================================================
# NIVEL 03 — "Laberinto"
# Plataformas densas con pasillos y ruta al techo por el centro
# ============================================================================
LEVEL_03 = LevelLayout(
    name="LABERINTO",
    player_start=(80, SCREEN_HEIGHT - 100),
    theme="purple_storm",
    platforms=[
        # Suelo
        (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
        # Nivel inferior
        (0, SCREEN_HEIGHT - 200, SCREEN_WIDTH // 3, PLATFORM_HEIGHT),
        (SCREEN_WIDTH * 2 // 3, SCREEN_HEIGHT - 200, SCREEN_WIDTH // 3, PLATFORM_HEIGHT),
        # Nivel medio — puente con hueco central
        (0, SCREEN_HEIGHT - 340, SCREEN_WIDTH // 3, PLATFORM_HEIGHT),
        (SCREEN_WIDTH // 3 + 60, SCREEN_HEIGHT - 340, SCREEN_WIDTH // 3, PLATFORM_HEIGHT),
        (SCREEN_WIDTH * 2 // 3 + 60, SCREEN_HEIGHT - 340, SCREEN_WIDTH // 3 - 60, PLATFORM_HEIGHT),
        # 🛤️ ESCALERA AL TECHO — por el hueco central
        (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT - 440, 140, PLATFORM_HEIGHT),
        (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT - 540, 120, PLATFORM_HEIGHT),
        # 🏁 PLATAFORMA SUPERIOR COMPLETA — zona de recolección
        (0, SCREEN_HEIGHT - 640, SCREEN_WIDTH, PLATFORM_HEIGHT + 4),
    ]
)

# ============================================================================
# NIVEL 04 — "Torres Gemelas"
# Dos torres con rampa espiral al centro
# ============================================================================
LEVEL_04 = LevelLayout(
    name="TORRES GEMELAS",
    player_start=(150, SCREEN_HEIGHT - 100),
    theme="ice_blue",
    platforms=[
        # Suelo
        (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
        # Torre izquierda
        (50, SCREEN_HEIGHT - 200, 120, PLATFORM_HEIGHT),
        (50, SCREEN_HEIGHT - 360, 120, PLATFORM_HEIGHT),
        (50, SCREEN_HEIGHT - 520, 120, PLATFORM_HEIGHT),
        # Torre derecha
        (SCREEN_WIDTH - 170, SCREEN_HEIGHT - 200, 120, PLATFORM_HEIGHT),
        (SCREEN_WIDTH - 170, SCREEN_HEIGHT - 360, 120, PLATFORM_HEIGHT),
        (SCREEN_WIDTH - 170, SCREEN_HEIGHT - 520, 120, PLATFORM_HEIGHT),
        # 🛤️ RAMPA CENTRAL — zigzag al techo
        (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT - 300, 120, PLATFORM_HEIGHT),
        (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 430, 160, PLATFORM_HEIGHT),
        # 🏁 PLATAFORMA SUPERIOR COMPLETA — zona de recolección
        (0, SCREEN_HEIGHT - 640, SCREEN_WIDTH, PLATFORM_HEIGHT + 4),
    ]
)

# ============================================================================
# NIVEL 05 — "Arena Final"
# Circuito completo con doble escalera lateral
# ============================================================================
LEVEL_05 = LevelLayout(
    name="ARENA FINAL",
    player_start=(SCREEN_WIDTH // 2 - 16, SCREEN_HEIGHT - 100),
    theme="golden_fury",
    platforms=[
        # Suelo
        (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
        # Cuadrícula 3x2
        (100, SCREEN_HEIGHT - 200, 160, PLATFORM_HEIGHT),
        (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 200, 160, PLATFORM_HEIGHT),
        (SCREEN_WIDTH - 260, SCREEN_HEIGHT - 200, 160, PLATFORM_HEIGHT),
        (50, SCREEN_HEIGHT - 350, 140, PLATFORM_HEIGHT),
        (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT - 350, 140, PLATFORM_HEIGHT),
        (SCREEN_WIDTH - 190, SCREEN_HEIGHT - 350, 140, PLATFORM_HEIGHT),
        # 🛤️ DOBLE ESCALERA LATERAL al techo
        (100, SCREEN_HEIGHT - 480, 130, PLATFORM_HEIGHT),
        (SCREEN_WIDTH - 230, SCREEN_HEIGHT - 480, 130, PLATFORM_HEIGHT),
        # 🏁 PLATAFORMA SUPERIOR COMPLETA — zona de recolección
        (0, SCREEN_HEIGHT - 620, SCREEN_WIDTH, PLATFORM_HEIGHT + 4),
    ]
)

# ============================================================================
# GENERADOR PROCEDURAL (niveles 6+)
# Siempre incluye ruta al techo
# ============================================================================
import random

def generate_procedural_level(level_num):
    """Genera un layout aleatorio con ruta garantizada al techo"""
    random.seed(level_num * 42)

    platforms = [
        # Suelo siempre
        (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
    ]

    # 🛤️ ESCALERA GARANTIZADA al techo (siempre presente)
    num_steps = 4 + min(level_num // 2, 3)  # 4-6 escalones
    step_height = (SCREEN_HEIGHT - 120) / num_steps
    for i in range(num_steps):
        y = SCREEN_HEIGHT - 120 - int(step_height * (i + 1))
        if y < 80:
            y = 80
        # Zigzag: alterna izquierda-derecha
        if i % 2 == 0:
            x = random.randint(30, SCREEN_WIDTH // 3)
        else:
            x = random.randint(SCREEN_WIDTH * 2 // 3 - 100, SCREEN_WIDTH - 160)
        w = random.randint(120, 180)
        platforms.append((x, y, w, PLATFORM_HEIGHT))

    # 🏁 PLATAFORMA SUPERIOR COMPLETA — zona de recolección
    platforms.append((0, SCREEN_HEIGHT - 700, SCREEN_WIDTH, PLATFORM_HEIGHT + 4))

    # Plataformas extra decorativas (más por nivel)
    extra_count = 3 + level_num
    for _ in range(extra_count):
        w = random.randint(80, 180)
        x = random.randint(0, SCREEN_WIDTH - w)
        y = random.randint(SCREEN_HEIGHT - 500, SCREEN_HEIGHT - 120)
        # Evitar que bloquee la escalera al techo
        platforms.append((x, y, w, PLATFORM_HEIGHT))

    # Posición del jugador
    player_x = random.randint(80, SCREEN_WIDTH - 200)

    # Tema rotativo
    themes = ["cyber", "neon_green", "purple_storm", "ice_blue", "golden_fury", "fire_red"]
    theme = themes[level_num % len(themes)]

    names = [
        "PROTOCOLO AVANZADO", "DIMENSIÓN BURBUJA", "CAOS NEÓN",
        "MATRIX ROTO", "TORBELINO", "ABISMO", "FALLO CRÍTICO",
        "ULTRAMUNDO", "SINGULARIDAD", "OMEGA"
    ]
    name = names[(level_num - 1) % len(names)]

    return LevelLayout(
        name=name,
        player_start=(player_x, SCREEN_HEIGHT - 100),
        theme=theme,
        platforms=platforms
    )

# ============================================================================
# MAPA DE NIVELES
# ============================================================================
LEVELS = {
    1: LEVEL_01,
    2: LEVEL_02,
    3: LEVEL_03,
    4: LEVEL_04,
    5: LEVEL_05,
}

def get_level(level_num):
    """Obtiene el layout de un nivel (predefinido o procedural)"""
    if level_num in LEVELS:
        return LEVELS[level_num]
    return generate_procedural_level(level_num)
