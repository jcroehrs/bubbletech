"""
🫧 Sistema de Partículas - BubbleTech
"""
import pygame
import math
import random
from typing import List, Tuple
from .constants import Colors

class Particle:
    """Partícula individual con efectos físicos"""
    def __init__(self, x: float, y: float, vx: float, vy: float,
                 lifetime: int, color: Tuple[int, ...], size: float,
                 gravity: float = 0.0, shrink: float = 0.95):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color
        self.size = size
        self.gravity = gravity
        self.shrink = shrink
        self.alpha = 255
        
    def update(self) -> bool:
        """Actualiza la partícula"""
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.lifetime -= 1
        
        # Fade out
        self.alpha = int(255 * (self.lifetime / self.max_lifetime))
        self.size *= self.shrink
        
        return self.lifetime > 0 and self.size > 0.5
    
    def draw(self, surface: pygame.Surface):
        """Dibuja la partícula con glow"""
        if self.alpha <= 0 or len(self.color) < 3:
            return
            
        # Glow
        glow_size = self.size * 2
        glow_surf = pygame.Surface((int(glow_size * 2), int(glow_size * 2)), pygame.SRCALPHA)
        glow_alpha = max(0, min(100, self.alpha // 3))
        pygame.draw.circle(glow_surf, (*self.color[:3], glow_alpha), 
                          (int(glow_size), int(glow_size)), int(glow_size))
        surface.blit(glow_surf, (int(self.x - glow_size), int(self.y - glow_size)))
        
        # Núcleo
        pygame.draw.circle(surface, self.color[:3], 
                          (int(self.x), int(self.y)), int(self.size))

class ParticleSystem:
    """Gestor global de partículas"""
    def __init__(self):
        self.particles: List[Particle] = []
        self.bubbles: List['BubbleParticle'] = []
        
    def emit_burst(self, x: float, y: float, color: Tuple[int, ...],
                   count: int = 20, speed: float = 5.0):
        """Explosión de partículas"""
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            vel = random.uniform(speed * 0.3, speed)
            vx = math.cos(angle) * vel
            vy = math.sin(angle) * vel
            lifetime = random.randint(20, 40)
            size = random.uniform(3, 8)
            self.particles.append(Particle(x, y, vx, vy, lifetime, color, size,
                                           gravity=0.2, shrink=0.96))
    
    def emit_trail(self, x: float, y: float, color: Tuple[int, ...]):
        """Rastro suave"""
        self.particles.append(Particle(
            x + random.uniform(-3, 3), y + random.uniform(-3, 3),
            random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5),
            random.randint(15, 30), color, random.uniform(2, 4),
            shrink=0.95
        ))
    
    def emit_sparkle(self, x: float, y: float, color: Tuple[int, ...]):
        """Destello de brillo"""
        for _ in range(5):
            self.particles.append(Particle(
                x, y,
                random.uniform(-2, 2), random.uniform(-3, -1),
                random.randint(10, 25), color, random.uniform(2, 4),
                gravity=0.1, shrink=0.92
            ))
    
    def emit_bubble_pop(self, x: float, y: float, color: Tuple[int, ...], radius: float):
        """Efecto al explotar burbuja"""
        # Anillo exterior
        for i in range(16):
            angle = i * (math.pi * 2 / 16)
            vx = math.cos(angle) * 4
            vy = math.sin(angle) * 4
            self.particles.append(Particle(
                x + math.cos(angle) * radius * 0.8,
                y + math.sin(angle) * radius * 0.8,
                vx, vy, random.randint(20, 35), color, random.uniform(4, 7),
                shrink=0.94
            ))
        # Centrales
        self.emit_burst(x, y, Colors.TEXT_WHITE, 10, 3)
    
    def emit_fusion(self, x: float, y: float):
        """Efecto de fusión de burbujas"""
        # Espiral de partículas doradas
        for i in range(30):
            angle = i * 0.5
            dist = i * 2
            px = x + math.cos(angle) * dist
            py = y + math.sin(angle) * dist
            vx = -math.cos(angle) * 3
            vy = -math.sin(angle) * 3
            self.particles.append(Particle(
                px, py, vx, vy, random.randint(30, 50),
                Colors.BUBBLE_GOLD, random.uniform(4, 10), shrink=0.97
            ))
        # Flash central
        self.particles.append(Particle(x, y, 0, 0, 20, 
                                      Colors.TEXT_WHITE, 40, shrink=0.8))
    
    def emit_gravity_float(self, x: float, y: float):
        """Partículas de gravedad cero"""
        for _ in range(3):
            self.particles.append(Particle(
                x + random.uniform(-20, 20), y + random.uniform(-20, 20),
                random.uniform(-1, 1), random.uniform(-2, -0.5),
                random.randint(40, 60), Colors.PLATFORM_GLOW, 
                random.uniform(2, 4), gravity=-0.05, shrink=0.98
            ))
    
    def update(self):
        """Actualiza todas las partículas"""
        self.particles = [p for p in self.particles if p.update()]
        self.bubbles = [b for b in self.bubbles if b.update()]
    
    def draw(self, surface: pygame.Surface):
        """Dibuja todas las partículas"""
        for p in self.particles:
            p.draw(surface)
        for b in self.bubbles:
            b.draw(surface)
    
    def clear(self):
        """Limpia todas las partículas"""
        self.particles.clear()
        self.bubbles.clear()

class BubbleParticle:
    """Partícula de burbuja flotante decorativa"""
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-1, -0.3)
        self.radius = random.uniform(5, 15)
        self.lifetime = random.randint(100, 200)
        self.max_lifetime = self.lifetime
        self.wobble = random.random() * math.pi * 2
        
    def update(self) -> bool:
        self.x += self.vx + math.sin(self.wobble) * 0.5
        self.y += self.vy
        self.wobble += 0.05
        self.lifetime -= 1
        return self.lifetime > 0
    
    def draw(self, surface: pygame.Surface):
        alpha = int(100 * (self.lifetime / self.max_lifetime))
        color = (*Colors.BUBBLE_CYAN[:3], alpha)
        
        # Glow
        pygame.draw.circle(surface, (*Colors.BUBBLE_CYAN[:3], alpha // 3),
                          (int(self.x), int(self.y)), int(self.radius + 3))
        
        # Borde
        pygame.draw.circle(surface, Colors.BUBBLE_CYAN[:3],
                          (int(self.x), int(self.y)), int(self.radius), 2)
        
        # Reflejo
        pygame.draw.circle(surface, Colors.TEXT_WHITE,
                          (int(self.x - self.radius * 0.3), int(self.y - self.radius * 0.3)), 3)
