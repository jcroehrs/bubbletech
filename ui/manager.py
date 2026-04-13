"""
🫧 Interfaz de Usuario - BubbleTech
"""
import pygame
from typing import Tuple
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import Colors, SCREEN_WIDTH, SCREEN_HEIGHT

class UIManager:
    """Gestor de HUD y menús holográficos"""
    def __init__(self):
        self.font_title = pygame.font.SysFont("dejavusans", 72, bold=True)
        self.font_large = pygame.font.SysFont("dejavusans", 48)
        self.font_medium = pygame.font.SysFont("dejavusans", 32)
        self.font_small = pygame.font.SysFont("dejavusans", 24)
        self.font_tiny = pygame.font.SysFont("dejavusans", 18)

    def draw_text_centered(self, surface: pygame.Surface, text: str,
                          x: int, y: int, font: pygame.font.Font,
                          color: Tuple[int, int, int], shadow: bool = True):
        """Dibuja texto centrado con sombra neón"""
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))

        if shadow:
            shadow_surf = font.render(text, True, (20, 20, 40))
            shadow_rect = shadow_surf.get_rect(center=(x + 3, y + 3))
            surface.blit(shadow_surf, shadow_rect)

        surface.blit(text_surf, text_rect)
        return text_rect

    def draw_hud(self, surface: pygame.Surface, player, score: int, level: int, lives: int, eliminated: int, screen_w: int = SCREEN_WIDTH):
        """Dibuja el HUD holográfico"""
        # Fondo panel superior
        panel_surf = pygame.Surface((screen_w, 60), pygame.SRCALPHA)
        panel_surf.fill((20, 30, 60, 100))
        surface.blit(panel_surf, (0, 0))
        pygame.draw.line(surface, Colors.PLATFORM_GLOW, (0, 60), (screen_w, 60), 2)

        # Score
        self.draw_text_centered(surface, f"SCORE: {score:06d}", 120, 30,
                               self.font_medium, Colors.SCORE_GOLD)

        # Level
        self.draw_text_centered(surface, f"SISTEMA: LVL {level}", screen_w - 120, 30,
                               self.font_medium, Colors.TEXT_GLOW)

        # Objetivo de nivel
        goal_text = f"OBJETIVO: {eliminated}/{15}"
        self.draw_text_centered(surface, goal_text, screen_w // 2, 30,
                               self.font_small, Colors.BUBBLE_GOLD)

        # Vidas (iconos de burbujas)
        lives_x = 300
        for i in range(3):
            color = Colors.BUBBLE_CYAN if i < lives else Colors.BG_DARK
            pygame.draw.circle(surface, color, (lives_x + i * 30, 30), 10)
            if i < lives:
                pygame.draw.circle(surface, Colors.TEXT_WHITE, (lives_x + i * 30 - 3, 27), 3)

    def draw_score_input(self, surface: pygame.Surface, current_name: str, screen_w: int = SCREEN_WIDTH, screen_h: int = SCREEN_HEIGHT):
        """Pantalla para ingresar el nombre del récord"""
        overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        surface.blit(overlay, (0, 0))

        self.draw_text_centered(surface, "¡NUEVO RÉCORD!", screen_w // 2, 200,
                               self.font_title, Colors.BUBBLE_GOLD)

        self.draw_text_centered(surface, "Ingresa tus iniciales (3 caracteres):", screen_w // 2, 300,
                               self.font_medium, Colors.TEXT_WHITE)

        # Caja de texto ajustada al contenido
        text_w = self.font_large.size(current_name)[0] if current_name else 100
        box_w = max(200, text_w + 40)
        input_rect = pygame.Rect(screen_w // 2 - box_w // 2, 350, box_w, 70)
        pygame.draw.rect(surface, Colors.BG_DARK, input_rect, border_radius=10)
        pygame.draw.rect(surface, Colors.BUBBLE_CYAN, input_rect, 2, border_radius=10)

        self.draw_text_centered(surface, current_name.upper(), screen_w // 2, 385,
                               self.font_large, Colors.TEXT_WHITE)

        self.draw_text_centered(surface, "Presiona ESPACIO para guardar", screen_w // 2, 460,
                               self.font_small, Colors.TEXT_GRAY)

    def draw_highscores(self, surface: pygame.Surface, scores, screen_w: int = SCREEN_WIDTH, screen_h: int = SCREEN_HEIGHT):
        """Muestra la tabla de puntuaciones"""
        overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        surface.blit(overlay, (0, 0))

        self.draw_text_centered(surface, "TOP 5 PILOTOS", screen_w // 2, 150,
                               self.font_title, Colors.BUBBLE_CYAN)

        for i, entry in enumerate(scores):
            color = Colors.NEON_GOLD if i == 0 else Colors.TEXT_WHITE
            text = f"{i+1}. {entry['name']} --- {entry['score']:,}"
            self.draw_text_centered(surface, text, screen_w // 2, 250 + i * 60,
                                   self.font_medium, color)

        self.draw_text_centered(surface, "Presiona ESPACIO para volver", screen_w // 2, 600,
                               self.font_small, Colors.TEXT_GRAY)

    def draw_menu(self, surface: pygame.Surface, scores=None, screen_w: int = SCREEN_WIDTH, screen_h: int = SCREEN_HEIGHT):
        """Pantalla de inicio"""
        # Fondo oscuro con glow
        overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        overlay.fill((5, 5, 20, 200))
        surface.blit(overlay, (0, 0))

        # Título principal
        self.draw_text_centered(surface, "🫧 BUBBLETECH", screen_w // 2, 150,
                               self.font_title, Colors.BUBBLE_CYAN)

        # Subtítulo
        self.draw_text_centered(surface, "Modern Bubble Burst Experience",
                               screen_w // 2, 220, self.font_medium, Colors.TEXT_GLOW)

        # Top 5 Highscores en el Menú
        if scores:
            self.draw_text_centered(surface, "--- TOP 5 PILOTOS ---", screen_w // 2, 300,
                                   self.font_small, Colors.BUBBLE_GOLD)
            for i, entry in enumerate(scores):
                color = Colors.TEXT_WHITE if i > 0 else Colors.BUBBLE_GOLD
                text = f"{entry['name']} : {entry['score']:,}"
                self.draw_text_centered(surface, text, screen_w // 2, 330 + i * 30,
                                       self.font_small, color)

        # Botón Inicio
        start_rect = pygame.Rect(screen_w // 2 - 200, 500, 400, 80)
        pygame.draw.rect(surface, Colors.BG_GRID, start_rect, border_radius=15)
        pygame.draw.rect(surface, Colors.BUBBLE_CYAN, start_rect, 3, border_radius=15)
        self.draw_text_centered(surface, "INICIAR SISTEMA [SPACE]", screen_w // 2, 540,
                               self.font_medium, Colors.TEXT_WHITE)

        # Instrucciones mejoradas
        y = 620
        instr = [
            "MUEVETE: WASD / FLECHAS | DISPARA: K | SALTA: ESPACIO",
            "SALIR DEL JUEGO: [Q]"
        ]
        for line in instr:
            self.draw_text_centered(surface, line, screen_w // 2, y,
                                      self.font_small, Colors.TEXT_GRAY)
            y += 30

    def draw_game_over(self, surface: pygame.Surface, final_score: int, screen_w: int = SCREEN_WIDTH, screen_h: int = SCREEN_HEIGHT):
        """Pantalla de Game Over"""
        overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        overlay.fill((50, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        self.draw_text_centered(surface, "SISTEMA COLAPSADO", screen_w // 2, 250,
                               self.font_title, Colors.ENEMY_RED)

        self.draw_text_centered(surface, f"PUNTUACIÓN FINAL: {final_score}", screen_w // 2, 350,
                               self.font_large, Colors.TEXT_WHITE)

        self.draw_text_centered(surface, "Presiona ESPACIO para reiniciar", screen_w // 2, 450,
                               self.font_medium, Colors.BUBBLE_CYAN)

    def draw_help_overlay(self, surface: pygame.Surface, screen_w: int = SCREEN_WIDTH, screen_h: int = SCREEN_HEIGHT):
        """Dibuja la ventana de ayuda con reglas detalladas"""
        # Fondo oscuro semi-transparente
        overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        overlay.fill((10, 10, 30, 230))
        surface.blit(overlay, (0, 0))

        # Dimensiones proporcionales a la pantalla
        panel_w = int(screen_w * 0.7)
        panel_h = int(screen_h * 0.65)
        panel_x = (screen_w - panel_w) // 2
        panel_y = (screen_h - panel_h) // 2

        # Fuentes proporcionales
        font_title = pygame.font.SysFont("dejavusans", int(screen_h * 0.045), bold=True)
        font_rules = pygame.font.SysFont("dejavusans", int(screen_h * 0.022))
        font_footer = pygame.font.SysFont("dejavusans", int(screen_h * 0.018))

        # Glow del panel
        for i in range(4, 0, -1):
            glow_rect = pygame.Rect(panel_x - i*5, panel_y - i*5, panel_w + i*10, panel_h + i*10)
            pygame.draw.rect(surface, (*Colors.BUBBLE_CYAN, 30), glow_rect, border_radius=20)

        # Panel principal
        pygame.draw.rect(surface, Colors.BG_DARK, (panel_x, panel_y, panel_w, panel_h), border_radius=15)
        pygame.draw.rect(surface, Colors.BUBBLE_CYAN, (panel_x, panel_y, panel_w, panel_h), 3, border_radius=15)

        # Título
        self.draw_text_centered(surface, "MANUAL DE OPERACIONES", screen_w // 2, panel_y + int(panel_h * 0.09),
                               font_title, Colors.BUBBLE_CYAN)

        # Reglas detalladas
        rules = [
            "🎯 OBJETIVO: Elimina los enemigos atrapándolos en burbujas.",
            "💥 COMBATE: Dispara con [K]. Toca una burbuja con enemigo",
            "    para eliminarlo y ganar puntos.",
            "",
            "🫧 MECÁNICA DE BURBUJAS:",
            "• Fusión: Si dos burbujas chocan, crean una MEGA-BURBUJA dorada.",
            "• Flotación: Salta sobre una burbuja vacía para flotar hacia arriba.",
            "• Energía: Las burbujas consumen energía. Recárgate con orbes dorados.",
            "",
            "👾 ENEMIGOS:",
            "• Walkers: Patrullan el suelo. Simples.",
            "• Jumpers: Saltan erráticamente.",
            "• Chasers: Te persiguen activamente.",
            "• Floaters: Flotan en el aire y orbitan tu posición.",
            "",
            "🌟 PROGRESION:",
            "• Supera la cuota de eliminaciones para avanzar de nivel.",
            "• Cada 3 niveles superados, obtienes una VIDA EXTRA."
        ]

        y_offset = panel_y + int(panel_h * 0.18)
        line_spacing = int(panel_h * 0.04)
        for line in rules:
            color = Colors.TEXT_WHITE if line.startswith("🎯") or line.startswith("🌟") or line.startswith("🫧") else Colors.TEXT_GRAY
            font = font_rules

            # Alineación izquierda para las reglas
            text_surf = font.render(line, True, color)
            surface.blit(text_surf, (panel_x + int(panel_w * 0.07), y_offset))
            y_offset += line_spacing

        self.draw_text_centered(surface, "Presiona [H] o [ESC] para volver", screen_w // 2, panel_y + panel_h - int(panel_h * 0.06),
                               font_footer, Colors.BUBBLE_CYAN)

    def draw_level_announce(self, surface: pygame.Surface, level: int, name: str,
                            screen_w: int, screen_h: int, progress: float):
        """Anuncio de inicio de nivel con efecto de entrada/salida"""
        # progress: 1.0 = inicio (totalmente visible), 0.0 = fin
        # Easing: fade in rápido, fade out lento
        if progress > 0.8:
            alpha = int(255 * (1 - progress) / 0.2)  # Fade in (0-20%)
        elif progress < 0.3:
            alpha = int(255 * progress / 0.3)  # Fade out (70-100%)
        else:
            alpha = 255  # Totalmente visible

        alpha = max(0, min(255, alpha))

        # Fondo semi-transparente
        overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(180 * alpha / 255)))
        surface.blit(overlay, (0, 0))

        # Fuentes dinámicas
        font_level = pygame.font.SysFont("dejavusans", int(screen_h * 0.035))
        font_name = pygame.font.SysFont("dejavusans", int(screen_h * 0.07), bold=True)

        # Texto
        level_text = f"SISTEMA {level:02d}"
        name_text = name.upper() if name else f"NIVEL {level}"

        cy = screen_h // 2

        # Renderizado manual con alpha
        level_surf = font_level.render(level_text, True, Colors.BUBBLE_CYAN)
        level_rect = level_surf.get_rect(center=(screen_w // 2, cy - int(screen_h * 0.06)))
        if alpha < 255:
            level_surf.set_alpha(alpha)
        surface.blit(level_surf, level_rect)

        name_surf = font_name.render(name_text, True, Colors.BUBBLE_GOLD)
        name_rect = name_surf.get_rect(center=(screen_w // 2, cy + int(screen_h * 0.02)))
        if alpha < 255:
            name_surf.set_alpha(alpha)
        surface.blit(name_surf, name_rect)

        # Barra decorativa
        bar_w = int(screen_w * 0.3)
        bar_h = 4
        bar_y = cy + int(screen_h * 0.08)
        bar_x = (screen_w - bar_w) // 2
        bar_surf = pygame.Surface((bar_w, bar_h), pygame.SRCALPHA)
        pygame.draw.rect(bar_surf, (*Colors.BUBBLE_CYAN, alpha), (0, 0, bar_w, bar_h), border_radius=2)
        surface.blit(bar_surf, (bar_x, bar_y))
