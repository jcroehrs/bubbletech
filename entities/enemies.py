"""
🫧 Enemigos - BubbleTech
IA de enemigos con comportamientos distintos
"""
import pygame
import math
import random
from typing import List
from utils.constants import *
from utils.particles import ParticleSystem

class Enemy:
    """Enemigo base"""
    def __init__(self, x: int, y: int, enemy_type: str = 'basic'):
        self.x, self.y = x, y
        self.width = ENEMY_SIZE
        self.height = ENEMY_SIZE
        self.type = enemy_type
        
        # Física
        self.vx = random.choice([-1, 1]) * random.uniform(1, 2)
        self.vy = 0
        self.on_ground = False
        
        # Estado
        self.trapped = False
        self.trap_timer = 0
        self.health = 1
        self.anim_timer = 0
        
        # Colores según tipo
        self.colors = {
            'basic': Colors.ENEMY_RED,
            'jumper': Colors.ENEMY_GREEN,
            'chaser': Colors.ENEMY_PURPLE,
            'heavy': (200, 100, 50)  # Naranja oscuro
        }
        self.color = self.colors.get(enemy_type, Colors.ENEMY_RED)
        
    def update(self, player_x: float, player_y: float,
               platforms: List[pygame.Rect], particles: ParticleSystem):
        """Actualiza el enemigo con IA según tipo"""
        self.anim_timer += 0.1
        
        if self.trapped:
            self.trap_timer -= 1
            if self.trap_timer <= 0:
                self.trapped = False
            return True
        
        # IA según tipo
        if self.type == 'basic':
            self.ai_basic()
        elif self.type == 'jumper':
            self.ai_jumper(platforms)
        elif self.type == 'chaser':
            self.ai_chaser(player_x, player_y)
        elif self.type == 'heavy':
            self.ai_heavy()
        
        # Gravedad
        self.vy += GRAVITY
        self.vy = min(self.vy, MAX_FALL_SPEED)
        
        # Aplicar movimiento
        self.x += self.vx
        self.y += self.vy
        
        # Colisiones con plataformas
        self.check_platform_collisions(platforms)
        
        # Limitar a pantalla
        if self.x < 0:
            self.x = 0
            self.vx = abs(self.vx)
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            self.vx = -abs(self.vx)
            
        return self.y < SCREEN_HEIGHT + 100
    
    def ai_basic(self):
        """IA básica: camina de lado a lado"""
        # Cambio de dirección aleatorio
        if random.random() < 0.01:
            self.vx *= -1
    
    def ai_jumper(self, platforms: List[pygame.Rect]):
        """IA saltarina: salta plataformas"""
        if self.on_ground and random.random() < 0.03:
            self.vy = JUMP_FORCE * 0.9
            self.on_ground = False
    
    def ai_chaser(self, player_x: float, player_y: float):
        """IA perseguidora: sigue al jugador"""
        if player_x < self.x:
            self.vx = -2.5
        else:
            self.vx = 2.5
            
        # Saltar si el jugador está arriba
        if player_y < self.y - 100 and self.on_ground and random.random() < 0.05:
            self.vy = JUMP_FORCE * 0.8
            self.on_ground = False
    
    def ai_heavy(self):
        """IA pesada: lenta pero resistente"""
        self.vx *= 0.95  # Fricción alta
        if abs(self.vx) < 0.3:
            self.vx = random.choice([-1, 1]) * 0.8
    
    def check_platform_collisions(self, platforms: List[pygame.Rect]):
        """Colisiones con plataformas"""
        enemy_rect = self.get_rect()
        self.on_ground = False
        
        for plat in platforms:
            if enemy_rect.colliderect(plat):
                if self.vy > 0 and enemy_rect.centery < plat.centery:
                    self.y = plat.top - self.height
                    self.vy = 0
                    self.on_ground = True
    
    def trap(self, duration: int = 300):
        """Atrapa al enemigo en burbuja"""
        self.trapped = True
        self.trap_timer = duration
        self.vx = 0
        self.vy = 0
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, surface: pygame.Surface):
        """Dibuja el enemigo"""
        if self.trapped:
            return  # No dibujar si está atrapado
            
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        # Glow
        for i in range(3, 0, -1):
            pygame.draw.circle(surface, (*self.color[:3], 40),
                              (center_x, center_y), self.width//2 + i * 3)
        
        # Cuerpo
        pygame.draw.ellipse(surface, self.color,
                           (self.x + 2, self.y + 2, self.width - 4, self.height - 4))
        pygame.draw.ellipse(surface, Colors.TEXT_WHITE,
                           (self.x + 2, self.y + 2, self.width - 4, self.height - 4), 2)
        
        # Ojos
        eye_y = self.y + 10
        eye_offset = 6 if self.vx > 0 else -6
        pygame.draw.circle(surface, Colors.TEXT_WHITE, 
                          (center_x + eye_offset, eye_y), 5)
        pygame.draw.circle(surface, Colors.BG_DARK,
                          (center_x + eye_offset + 2, eye_y), 2)
        
        # Cuernos según tipo
        if self.type == 'jumper':
            pygame.draw.polygon(surface, self.color,
                              [(center_x - 5, self.y), (center_x - 8, self.y - 8),
                               (center_x - 2, self.y)])
            pygame.draw.polygon(surface, self.color,
                              [(center_x + 5, self.y), (center_x + 8, self.y - 8),
                               (center_x + 2, self.y)])
        elif self.type == 'heavy':
            # Pico en la espalda
            pygame.draw.polygon(surface, self.color,
                              [(center_x, self.y - 2), (center_x - 6, self.y - 10),
                               (center_x + 6, self.y - 10)])
