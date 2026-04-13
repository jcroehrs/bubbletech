"""
🫧 Enemigos - BubbleTech
"""
import pygame
import math
import random
from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import Colors, GRAVITY, SCREEN_WIDTH, SCREEN_HEIGHT
from utils.particles import ParticleSystem

class Enemy:
    """Enemigo base"""
    def __init__(self, x: float, y: float, enemy_type: str, particles: ParticleSystem,
                 screen_w: int = 1024, screen_h: int = 768):
        self.x, self.y = x, y
        self.radius = 14
        self.type = enemy_type
        self.particles = particles
        self.screen_w = screen_w
        self.screen_h = screen_h
        
        # Movimiento
        self.vx = random.choice([-1.5, 1.5])
        self.vy = 0
        
        # Estado
        self.trapped = False
        self.dead = False
        
        # Animación
        self.anim_frame = random.random() * 10
        self.direction = 1 if self.vx > 0 else -1
        
        # Color según tipo
        self.color = self._get_color()
        self.points = self._get_points()
        
    def _get_color(self) -> tuple:
        """Color según tipo"""
        colors = {
            "walker": Colors.ENEMY_RED,
            "jumper": Colors.ENEMY_GREEN,
            "chaser": Colors.ENEMY_PURPLE,
            "floater": Colors.FIRE_ORANGE,
        }
        return colors.get(self.type, Colors.ENEMY_RED)
    
    def _get_points(self) -> int:
        """Puntos al eliminar"""
        points = {
            "walker": 100,
            "jumper": 200,
            "chaser": 300,
            "floater": 400,
        }
        return points.get(self.type, 100)
    
    def update(self, platforms: List[pygame.Rect], player_x: float, player_y: float):
        """Actualiza el enemigo"""
        if self.trapped or self.dead:
            return
        
        self.anim_frame += 0.1
        
        # IA según tipo
        if self.type == "walker":
            self._ai_walker(platforms)
        elif self.type == "jumper":
            self._ai_jumper(platforms)
        elif self.type == "chaser":
            self._ai_chaser(player_x, player_y, platforms)
        elif self.type == "floater":
            self._ai_floater(player_x, player_y)
        
        # Gravedad
        if self.type != "floater":
            self.vy += GRAVITY * 0.5
            if self.vy > 6:
                self.vy = 6
        
        # Actualizar posición
        self.x += self.vx
        self.y += self.vy
        
        # Colisiones
        self._check_platforms(platforms)
        
        # Límites
        if self.x < self.radius:
            self.x = self.radius
            self.vx = abs(self.vx)
            self.direction = 1
        if self.x > self.screen_w - self.radius:
            self.x = self.screen_w - self.radius
            self.vx = -abs(self.vx)
            self.direction = -1

        if self.y > self.screen_h + 50:
            self.dead = True
    
    def _ai_walker(self, platforms: List[pygame.Rect]):
        """Camina de lado a lado"""
        # Cambiar dirección aleatoriamente
        if random.random() < 0.01:
            self.vx *= -1
            self.direction *= -1
        
        # Caer de plataformas
        self_rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                              self.radius * 2, self.radius * 2 + 5)
        on_ground = False
        for plat in platforms:
            if self_rect.colliderect(plat):
                on_ground = True
                break
        
        if not on_ground and self.vy == 0:
            # Voltear al caer
            pass
    
    def _ai_jumper(self, platforms: List[pygame.Rect]):
        """Salta constantemente"""
        self_rect = pygame.Rect(self.x - self.radius, self.y - self.radius + 5,
                              self.radius * 2, self.radius * 2)
        on_ground = False
        for plat in platforms:
            if self_rect.colliderect(plat):
                on_ground = True
                break
        
        if on_ground and random.random() < 0.03:
            self.vy = -8
            # Salto hacia el jugador
            if self.direction > 0:
                self.vx = abs(self.vx) * 1.5
            else:
                self.vx = -abs(self.vx) * 1.5
    
    def _ai_chaser(self, player_x: float, player_y: float, platforms: List[pygame.Rect]):
        """Persigue al jugador"""
        dist = abs(player_x - self.x)
        
        if dist > 50:
            if player_x > self.x:
                self.vx = min(2.5, self.vx + 0.1)
                self.direction = 1
            else:
                self.vx = max(-2.5, self.vx - 0.1)
                self.direction = -1
        
        # Saltar si el jugador está arriba
        if player_y < self.y - 100 and self.vy == 0:
            self_rect = pygame.Rect(self.x - self.radius, self.y + self.radius,
                                  self.radius * 2, 5)
            for plat in platforms:
                if self_rect.colliderect(plat):
                    if random.random() < 0.1:
                        self.vy = -10
                    break
    
    def _ai_floater(self, player_x: float, player_y: float):
        """Flota y persigue lentamente"""
        # Flotación
        self.y += math.sin(self.anim_frame) * 0.5
        
        # Perseguir lentamente
        if abs(player_x - self.x) > 30:
            if player_x > self.x:
                self.vx = 0.8
                self.direction = 1
            else:
                self.vx = -0.8
                self.direction = -1
        else:
            self.vx = 0
        
        # Perseguir verticalmente también
        if player_y < self.y - 20:
            self.vy = -0.5
        elif player_y > self.y + 20:
            self.vy = 0.5
        else:
            self.vy = 0
    
    def _check_platforms(self, platforms: List[pygame.Rect]):
        """Colisiones con plataformas"""
        self_rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                              self.radius * 2, self.radius * 2)
        
        for plat in platforms:
            if self_rect.colliderect(plat):
                # Colisión por arriba
                if self.vy > 0 and self_rect.centery < plat.centery:
                    self.y = plat.top - self.radius
                    self.vy = 0
                # Colisión lateral
                elif self.vx > 0:
                    self.x = plat.left - self.radius
                    self.vx = -abs(self.vx)
                    self.direction = -1
                else:
                    self.x = plat.right + self.radius
                    self.vx = abs(self.vx)
                    self.direction = 1
                
                self_rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                      self.radius * 2, self.radius * 2)
    
    def get_rect(self) -> pygame.Rect:
        """Rectángulo de colisión"""
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)
    
    def draw(self, surface: pygame.Surface):
        """Dibuja el enemigo"""
        if self.trapped:
            return  # Dibujado por la burbuja
        
        # Glow
        for i in range(2, 0, -1):
            pygame.draw.circle(surface, (*self.color, 50),
                             (int(self.x), int(self.y)), self.radius + i * 3)
        
        # Cuerpo
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Ojos
        eye_offset = 4 if self.direction > 0 else -4
        pygame.draw.circle(surface, Colors.BG_DARK, 
                          (int(self.x + eye_offset), int(self.y - 2)), 4)
        pygame.draw.circle(surface, Colors.TEXT_WHITE,
                          (int(self.x + eye_offset + 1), int(self.y - 3)), 2)
        
        # Cuernos según tipo
        if self.type == "walker":
            self._draw_horns(surface, small=True)
        elif self.type == "jumper":
            self._draw_horns(surface, medium=True)
        elif self.type == "chaser":
            self._draw_horns(surface, large=True)
        elif self.type == "floater":
            # Ala
            wing_y = self.y + math.sin(self.anim_frame * 2) * 3
            pygame.draw.ellipse(surface, Colors.BUBBLE_GOLD,
                               (int(self.x - 15), int(wing_y - 3), 30, 8))
    
    def _draw_horns(self, surface: pygame.Surface, small=False, medium=False, large=False):
        """Dibuja cuernos"""
        base_y = self.y - self.radius + 3
        
        if small:
            pygame.draw.polygon(surface, Colors.TEXT_WHITE,
                              [(self.x - 4, base_y), (self.x - 6, base_y - 4), (self.x - 2, base_y)])
            pygame.draw.polygon(surface, Colors.TEXT_WHITE,
                              [(self.x + 4, base_y), (self.x + 6, base_y - 4), (self.x + 2, base_y)])
        elif medium:
            pygame.draw.polygon(surface, Colors.BUBBLE_GOLD,
                              [(self.x - 5, base_y), (self.x - 7, base_y - 6), (self.x - 2, base_y)])
            pygame.draw.polygon(surface, Colors.BUBBLE_GOLD,
                              [(self.x + 5, base_y), (self.x + 7, base_y - 6), (self.x + 2, base_y)])
        elif large:
            pygame.draw.polygon(surface, Colors.ELECTRIC_PURPLE,
                              [(self.x - 6, base_y), (self.x - 9, base_y - 10), (self.x - 2, base_y)])
            pygame.draw.polygon(surface, Colors.ELECTRIC_PURPLE,
                              [(self.x + 6, base_y), (self.x + 9, base_y - 10), (self.x + 2, base_y)])
    
    def draw_trapped(self, surface: pygame.Surface, bubble_x: float, bubble_y: float, bubble_radius: float):
        """Dibujado cuando está atrapado en burbuja"""
        from utils.constants import BUBBLE_RADIUS
        # Versión pequeña y comprimida
        scale = bubble_radius / BUBBLE_RADIUS * 0.6
        size = int(self.radius * scale)
        
        pygame.draw.circle(surface, self.color, (int(bubble_x), int(bubble_y)), size)
        
        # Ojos de sorpresa
        pygame.draw.circle(surface, Colors.TEXT_WHITE, (int(bubble_x - size//2), int(bubble_y)), 2)
        pygame.draw.circle(surface, Colors.TEXT_WHITE, (int(bubble_x + size//2), int(bubble_y)), 2)
        
        # Onda de choque
        if random.random() < 0.1:
            pygame.draw.circle(surface, Colors.TEXT_WHITE, 
                             (int(bubble_x), int(bubble_y)), size + 2, 1)
