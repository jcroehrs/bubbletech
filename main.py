"""
🫧 BUBBLETECH - Motor Principal
Motor multiplataforma (Desktop + Android)
"""
import pygame
import sys
import random
import platform
from typing import List, Tuple
import os

# Forzar la ruta de importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.constants import *
from utils.particles import ParticleSystem
from utils.levels import get_level
from entities.player import Player
from entities.bubble import Bubble
from entities.enemy import Enemy
from ui.manager import UIManager
from utils.score_manager import ScoreManager

# Detección de plataforma
IS_ANDROID = platform.system() == "Linux" and os.environ.get("ANDROID_ARGUMENT") is not None

if IS_ANDROID:
    from ui.touch_overlay import TouchOverlay


class BubbleTech:
    def __init__(self):
        pygame.init()
        init_fonts()

        # Detectar si es Android
        self.is_android = IS_ANDROID

        # Configuración de pantalla
        if self.is_android:
            # En Android, usar pantalla completa sin bordes
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
            info = pygame.display.Info()
            self.screen_w, self.screen_h = info.current_w, info.current_h
            # Controles táctiles
            self.touch = TouchOverlay(self.screen_w, self.screen_h)
        else:
            # Desktop: fullscreen con resolución real
            info = pygame.display.Info()
            screen_w, screen_h = info.current_w, info.current_h
            self.screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN)
            self.screen_w = screen_w
            self.screen_h = screen_h
            self.touch = None

        pygame.display.set_caption("🫧 BUBBLETECH - Modern Bubble Burst")
        self.clock = pygame.time.Clock()

        # Sistemas
        self.particles = ParticleSystem()
        self.ui = UIManager()
        self.scores = ScoreManager()

        # Estado del juego
        self.state = "MENU"
        self.score = 0
        self.level = 1
        self.lives = 3
        self.input_name = ""
        self.show_help = False

        # Anuncio de nivel
        self.level_announce_timer = 0
        self.level_announce_name = ""

        self.reset_game()
        self.running = True

    def reset_game(self):
        """Inicializa el estado de una nueva partida"""
        self.level = 1
        self.lives = 3
        layout = get_level(self.level)
        px, py = layout.player_start if layout.player_start else (100, self.screen_h - 100)
        self.player = Player(px, py, self.particles, self.screen_w, self.screen_h)
        self.bubbles: List[Bubble] = []
        self.enemies: List[Enemy] = []
        self.platforms: List[pygame.Rect] = []
        self.score = 0
        self.enemies_eliminated = 0
        self.spawn_timer = 0

        self.generate_level()
        self.particles.clear()

        # Activar anuncio de nivel
        self.level_announce_timer = 180  # 3 segundos a 60 FPS
        self.level_announce_name = layout.name

    def generate_level(self):
        """Crea plataformas basadas en el nivel"""
        layout = get_level(self.level)
        self.platforms = []

        for px, py, pw, ph in layout.platforms:
            self.platforms.append(pygame.Rect(px, py, pw, ph))

    def spawn_enemy(self):
        """Crea un enemigo en una posición aleatoria"""
        # Elegir una plataforma al azar para spawnear
        plat = random.choice(self.platforms)
        x = plat.centerx + random.randint(-20, 20)
        y = plat.top - 20

        types = ["walker", "jumper", "chaser", "floater"]
        enemy_type = random.choice(types)
        self.enemies.append(Enemy(x, y, enemy_type, self.particles, self.screen_w, self.screen_h))

    def level_complete(self):
        """Maneja la transición al siguiente nivel"""
        self.level += 1
        self.enemies_eliminated = 0
        # Efecto visual de victoria de nivel
        self.particles.emit_burst(self.screen_w // 2, self.screen_h // 2,
                                 Colors.BUBBLE_GOLD, 50, 10)
        # Regenerar nivel y limpiar pantalla
        self.generate_level()
        for e in self.enemies[:]:
            e.dead = True
        self.bubbles = []
        # Bonus de vida cada 3 niveles
        if self.level % 3 == 0:
            self.lives += 1
        # Activar anuncio del nuevo nivel
        layout = get_level(self.level)
        self.level_announce_timer = 180
        self.level_announce_name = layout.name

    def _get_keys(self):
        """Obtiene el estado de teclas (teclado o táctil)"""
        if self.is_android and self.touch:
            return self.touch.get_keys()
        return pygame.key.get_pressed()

    def _shoot_bubble(self):
        """Dispara una burbuja"""
        if not self.player.can_shoot():
            return
        direction = 1 if self.player.facing_right else -1
        new_bubble = Bubble(
            self.player.x + self.player.width // 2,
            self.player.y + self.player.height // 2,
            direction,
            self.player.bubble_element,
            self.particles,
            shooter=self.player,
            screen_w=self.screen_w,
            screen_h=self.screen_h
        )
        self.bubbles.append(new_bubble)
        self.player.shoot_cooldown = 20
        self.particles.emit_burst(new_bubble.x, new_bubble.y, Colors.BUBBLE_CYAN, 10, 2)

    def handle_input(self):
        """Procesa eventos de entrada (teclado + táctil)"""
        keys = self._get_keys()

        if self.state == "PLAYING":
            # Disparo (K o botón táctil)
            if keys[pygame.K_k]:
                self._shoot_bubble()

        for event in pygame.event.get():
            # Eventos táctiles (Android)
            if self.is_android and self.touch:
                if event.type in (pygame.FINGERDOWN, pygame.FINGERMOTION, pygame.FINGERUP):
                    self.touch.handle_event(event)
                    # Si tocó fuera de controles, usar como teclas direccionales
                    # El touch overlay ya maneja las teclas, no necesitamos procesar más aquí
                    # excepto para menú/navegación

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                # Salir del juego con la tecla Q
                if event.key == pygame.K_q:
                    self.running = False

                # Mostrar/Ocultar Ayuda con la tecla H
                if event.key == pygame.K_h:
                    self.show_help = not self.show_help

                # Salir de la ayuda con ESC si está abierta
                if event.key == pygame.K_ESCAPE and self.show_help:
                    self.show_help = False

                # Navegación por estados
                if self.state == "MENU" and event.key == pygame.K_SPACE:
                    self.state = "PLAYING"
                    self.reset_game()
                elif self.state == "INPUT_NAME":
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        name = self.input_name if self.input_name else "AAA"
                        self.scores.add_score(name[:3], self.score)
                        self.state = "MENU"
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_name = self.input_name[:-1]
                    elif len(self.input_name) < 3 and event.unicode.isalnum():
                        self.input_name += event.unicode
                elif self.state == "PLAYING":
                    if event.key == pygame.K_ESCAPE:
                        self.state = "PAUSED"
                elif self.state == "PAUSED":
                    if event.key == pygame.K_SPACE:
                        self.state = "PLAYING"
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                elif self.state == "GAME_OVER":
                    if event.key == pygame.K_SPACE:
                        if self.scores.is_top_score(self.score):
                            self.input_name = ""
                            self.state = "INPUT_NAME"
                        else:
                            self.state = "PLAYING"
                            self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "MENU"

            # Toques para navegación de menú (Android)
            if self.is_android and event.type == pygame.FINGERDOWN:
                # En menú o game over, tocar la pantalla = SPACE
                if self.state == "MENU":
                    self.state = "PLAYING"
                    self.reset_game()
                elif self.state == "GAME_OVER":
                    if self.scores.is_top_score(self.score):
                        self.input_name = ""
                        self.state = "INPUT_NAME"
                    else:
                        self.state = "PLAYING"
                        self.reset_game()
                elif self.state == "PAUSED":
                    self.state = "PLAYING"

    def update(self):
        """Ciclo de lógica"""
        if self.state != "PLAYING":
            return

        dt = self.clock.get_time() / 1000.0

        # Anuncio de nivel
        if self.level_announce_timer > 0:
            self.level_announce_timer -= 1

        # 1. Actualizar Jugador
        keys = self._get_keys()
        self.player.update(keys, self.platforms)

        # 2. Actualizar Burbujas
        for b in self.bubbles[:]:
            if not b.update(self.platforms, self.enemies, self.bubbles):
                self.bubbles.remove(b)

            # Jugador puede subirse a la burbuja
            if not self.player.in_bubble and b.can_ride(self.player):
                if self.player.get_rect().colliderect(b.get_rect()):
                    self.player.enter_bubble(b)

        # 3. Actualizar Enemigos
        for e in self.enemies[:]:
            if not e.trapped:
                e.update(self.platforms, self.player.x, self.player.y)
                # Colisión con jugador (solo si no es invulnerable)
                if self.player.invincible_timer <= 0 and e.get_rect().colliderect(self.player.get_rect()):
                    self.lives -= 1
                    self.player.invincible_timer = 90  # 1.5 segundos de invulnerabilidad
                    self.particles.emit_burst(self.player.x, self.player.y, Colors.ENEMY_RED, 30, 8)
                    if self.lives <= 0:
                        self.state = "GAME_OVER"

            if e.dead:
                self.enemies.remove(e)

        # 4. Gestión de burbujas atrapadas y eliminación
        for b in self.bubbles[:]:
            if b.trapped_enemy:
                # El jugador puede explotar la burbuja tocándola
                if b.get_rect().colliderect(self.player.get_rect()):
                    enemy = b.trapped_enemy
                    self.score += enemy._get_points() * 2  # Bonus por eliminar
                    self.particles.emit_bubble_pop(b.x, b.y, Colors.BUBBLE_GOLD, b.radius)
                    self.particles.emit_burst(b.x, b.y, enemy.color, 20, 6)
                    enemy.dead = True
                    b.start_pop()

                    # Objetivo de nivel
                    self.enemies_eliminated += 1
                    if self.enemies_eliminated >= LEVEL_GOAL_ENEMIES:
                        self.level_complete()

        # 5. Spawner de enemigos
        self.spawn_timer += 1
        if self.spawn_timer >= ENEMY_SPAWN_BASE:
            self.spawn_enemy()
            self.spawn_timer = 0
            # Aumentar dificultad
            if len(self.enemies) % 5 == 0:
                self.level += 1

        # 6. Partículas
        self.particles.update()

    def draw(self):
        """Renderizado"""
        self.screen.fill(Colors.BG_DARK)

        # Fondo grid adaptado a resolución
        for x in range(0, self.screen_w, 64):
            pygame.draw.line(self.screen, Colors.BG_GRID, (x, 0), (x, self.screen_h), 1)
        for y in range(0, self.screen_h, 64):
            pygame.draw.line(self.screen, Colors.BG_GRID, (0, y), (self.screen_w, y), 1)

        # Plataformas
        for plat in self.platforms:
            pygame.draw.rect(self.screen, Colors.PLATFORM_BASE, plat, border_radius=5)
            pygame.draw.rect(self.screen, Colors.PLATFORM_GLOW, plat, 2, border_radius=5)

        # Burbujas
        for b in self.bubbles:
            b.draw(self.screen)

        # Enemigos
        for e in self.enemies:
            e.draw(self.screen)

        # Jugador
        self.player.draw(self.screen)

        # Partículas
        self.particles.draw(self.screen)

        # HUD
        if self.show_help:
            self.ui.draw_help_overlay(self.screen, self.screen_w, self.screen_h)
        elif self.state == "MENU":
            self.ui.draw_menu(self.screen, self.scores.scores, self.screen_w, self.screen_h)
        elif self.state == "PLAYING":
            self.ui.draw_hud(self.screen, self.player, self.score, self.level, self.lives, self.enemies_eliminated, self.screen_w)
            # Anuncio de nivel
            if self.level_announce_timer > 0:
                progress = self.level_announce_timer / 180.0
                self.ui.draw_level_announce(self.screen, self.level, self.level_announce_name,
                                            self.screen_w, self.screen_h, progress)
            # Controles táctiles (Android)
            if self.is_android and self.touch:
                self.touch.draw(self.screen)
        elif self.state == "INPUT_NAME":
            self.ui.draw_score_input(self.screen, self.input_name, self.screen_w, self.screen_h)
        elif self.state == "GAME_OVER":
            self.ui.draw_game_over(self.screen, self.score, self.screen_w, self.screen_h)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = BubbleTech()
    game.run()
