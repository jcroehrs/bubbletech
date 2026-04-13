"""
🫧 Burbujas - BubbleTech
"""
import pygame
import math
import random
from typing import Optional, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import Colors, BUBBLE_SPEED, BUBBLE_LIFETIME, BUBBLE_RADIUS, BUBBLE_COLORS, BubbleType, SCREEN_WIDTH, SCREEN_HEIGHT
from utils.particles import ParticleSystem

class Bubble:
    """Burbuja disparada por el jugador"""
    def __init__(self, x: float, y: float, direction: int, element: str,
                 particles: ParticleSystem, shooter=None, screen_w: int = 1024, screen_h: int = 768):
        self.x = x
        self.y = y
        self.radius = BUBBLE_RADIUS
        self.element = element
        self.direction = direction  # 1 = derecha, -1 = izquierda
        self.particles = particles
        self.shooter = shooter  # Referencia al jugador que disparó
        self.screen_w = screen_w
        self.screen_h = screen_h
        
        # Física
        self.vx = BUBBLE_SPEED * direction
        self.vy = 0
        self.lifetime = BUBBLE_LIFETIME
        
        # Estado
        self.trapped_enemy = None
        self.is_mega = False
        self.bouncing = True
        
        # Animación
        self.wobble = 0
        self.pop_timer = 0
        
    def update(self, platforms: List[pygame.Rect], enemies: List,
               other_bubbles: List['Bubble']) -> bool:
        """Actualiza la burbuja. Retorna False si debe destruirse"""
        if self.pop_timer > 0:
            self.pop_timer -= 1
            if self.pop_timer <= 0:
                return False
            return True
        
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.start_pop()
            return True
        
        # Movimiento
        self.x += self.vx
        self.y += self.vy
        self.wobble += 0.15
        
        # Rebotar en paredes
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = abs(self.vx)
            self._spawn_bounce_particles()
        elif self.x + self.radius > self.screen_w:
            self.x = self.screen_w - self.radius
            self.vx = -abs(self.vx)
            self._spawn_bounce_particles()

        # Rebotar en el techo
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = abs(self.vy)
            self._spawn_bounce_particles()
        
        # Flotación suave
        if abs(self.vy) < 0.5:
            self.y += math.sin(self.wobble) * 0.3
        
        # Colisiones con plataformas
        self._check_platform_collisions(platforms)
        
        # Colisiones con enemigos (si no tiene enemigo atrapado)
        if not self.trapped_enemy:
            self._check_enemy_collisions(enemies)
        
        # Colisiones con otras burbujas (fusión)
        self._check_bubble_fusion(other_bubbles)
        
        # Subir si tiene enemigo
        if self.trapped_enemy:
            self.vy -= 0.15
            if self.vy < -3:
                self.vy = -3
            # Partículas de flotación
            if random.random() < 0.1:
                self.particles.emit_gravity_float(self.x, self.y)
        
        return True
    
    def _spawn_bounce_particles(self):
        """Partículas al rebotar"""
        color = BUBBLE_COLORS.get(self.element, Colors.BUBBLE_CYAN)
        self.particles.emit_burst(self.x, self.y, color, 8, 3)
    
    def _check_platform_collisions(self, platforms: List[pygame.Rect]):
        """Colisiones con plataformas"""
        bubble_rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                               self.radius * 2, self.radius * 2)
        
        for plat in platforms:
            if bubble_rect.colliderect(plat):
                # Rebotar
                if self.vx > 0:
                    self.x = plat.left - self.radius
                else:
                    self.x = plat.right + self.radius
                self.vx *= -0.8
                self._spawn_bounce_particles()
    
    def _check_enemy_collisions(self, enemies: List):
        """Intenta atrapar enemigos"""
        for enemy in enemies:
            if not enemy.trapped:
                dist = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
                if dist < self.radius + enemy.radius:
                    # ¡Atrapado!
                    self.trap_enemy(enemy)
                    break
    
    def _check_bubble_fusion(self, other_bubbles: List['Bubble']):
        """Verifica fusión con otras burbujas"""
        if self.is_mega or self.trapped_enemy:
            return
            
        for other in other_bubbles:
            if other is self or other.is_mega or other.trapped_enemy:
                continue
                
            dist = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
            if dist < self.radius + other.radius:
                # Fusionar
                self.fuse_with(other)
                break
    
    def trap_enemy(self, enemy):
        """Atrapa un enemigo en la burbuja"""
        self.trapped_enemy = enemy
        enemy.trapped = True
        self.vx *= 0.3
        self.vy = -1
        self.lifetime = BUBBLE_LIFETIME * 1.5  # Más tiempo con enemigo
        
        # Efecto visual
        color = BUBBLE_COLORS.get(self.element, Colors.BUBBLE_CYAN)
        self.particles.emit_burst(self.x, self.y, color, 20, 4)
        self.particles.emit_sparkle(self.x, self.y, color)
    
    def fuse_with(self, other: 'Bubble'):
        """Se fusiona con otra burbuja"""
        self.is_mega = True
        self.radius = int(self.radius * 1.5)
        self.lifetime = max(self.lifetime, other.lifetime)
        self.vx = (self.vx + other.vx) / 2
        
        # Efecto de fusión
        self.particles.emit_fusion(self.x, self.y)
        
        # Marcar la otra para destrucción
        other.pop_timer = 1
    
    def start_pop(self):
        """Inicia la explosión de la burbuja"""
        self.pop_timer = 10
        color = BUBBLE_COLORS.get(self.element, Colors.BUBBLE_CYAN)
        self.particles.emit_bubble_pop(self.x, self.y, color, self.radius)
        
        # Liberar enemigo si había uno
        if self.trapped_enemy:
            self.trapped_enemy.trapped = False
            self.trapped_enemy.vy = -3  # Rebote al caer
            self.trapped_enemy = None
    
    def get_rect(self) -> pygame.Rect:
        """Rectángulo de colisión"""
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)
    
    def can_ride(self, player) -> bool:
        """Puede el jugador subirse a esta burbuja?"""
        if self.trapped_enemy or self.is_mega:
            return False
        # Debe estar relativamente quieta
        return abs(self.vx) < 3
    
    def draw(self, surface: pygame.Surface):
        """Dibuja la burbuja"""
        if self.pop_timer > 0:
            # Animación de explosión
            progress = 1 - (self.pop_timer / 10)
            radius = int(self.radius * (1 + progress))
            alpha = int(255 * (1 - progress))
            
            color = BUBBLE_COLORS.get(self.element, Colors.BUBBLE_CYAN)
            pygame.draw.circle(surface, (*color, alpha),
                             (int(self.x), int(self.y)), radius)
            return
        
        color = BUBBLE_COLORS.get(self.element, Colors.BUBBLE_CYAN)
        
        # Glow
        glow_layers = 4 if self.is_mega else 3
        for i in range(glow_layers, 0, -1):
            glow_surf = pygame.Surface((self.radius * 2 + i * 10, self.radius * 2 + i * 10), pygame.SRCALPHA)
            alpha = int(40 / i)
            pygame.draw.circle(glow_surf, (*color, alpha),
                             (glow_surf.get_width()//2, glow_surf.get_height()//2),
                             self.radius + i * 5)
            surface.blit(glow_surf, (int(self.x - glow_surf.get_width()//2),
                                    int(self.y - glow_surf.get_height()//2)))
        
        # Cuerpo de burbuja
        bubble_surf = pygame.Surface((self.radius * 2 + 4, self.radius * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(bubble_surf, (*color, 100),
                          (self.radius + 2, self.radius + 2), self.radius)
        pygame.draw.circle(bubble_surf, color,
                          (self.radius + 2, self.radius + 2), self.radius, 2)
        surface.blit(bubble_surf, (int(self.x - self.radius - 2), int(self.y - self.radius - 2)))
        
        # Reflejos
        pygame.draw.circle(surface, Colors.TEXT_WHITE,
                          (int(self.x - self.radius * 0.3), int(self.y - self.radius * 0.3)),
                          4 if self.is_mega else 3)
        
        # Enemigo atrapado
        if self.trapped_enemy:
            self.trapped_enemy.draw_trapped(surface, self.x, self.y, self.radius)
        
        # Indicador de mega burbuja
        if self.is_mega:
            font = pygame.font.Font(None, 20)
            text = font.render("★", True, Colors.BUBBLE_GOLD)
            text_rect = text.get_rect(center=(self.x, self.y))
            surface.blit(text, text_rect)
