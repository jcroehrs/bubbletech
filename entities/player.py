"""
🫧 Jugador - BubbleTech
"""
import pygame
import math
from typing import List, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import Colors, GRAVITY, JUMP_FORCE, MOVE_SPEED, MAX_FALL_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT
from utils.particles import ParticleSystem

class Player:
    """Bubby - El héroe burbujero"""
    def __init__(self, x: float, y: float, particles: ParticleSystem, screen_w: int = 1024, screen_h: int = 768):
        self.x, self.y = x, y
        self.width, self.height = 32, 40
        self.vx, self.vy = 0, 0
        self.particles = particles
        self.screen_w = screen_w
        self.screen_h = screen_h
        
        # Estados
        self.on_ground = False
        self.in_bubble = False  # Dentro de su propia burbuja
        self.facing_right = True
        
        # Animación
        self.anim_frame = 0
        self.blink_timer = 0
        
        # Power-ups
        self.has_double_jump = False
        self.can_double_jump = True
        self.bubble_element = "normal"  # normal, fire, ice, electric
        self.power_timer = 0
        
        # Cooldowns
        self.shoot_cooldown = 0
        self.bubble_ride_cooldown = 0
        self.invincible_timer = 0  # Tiempo de invulnerabilidad tras recibir daño
        
    def update(self, keys: dict, platforms: List[pygame.Rect]):
        """Actualiza el jugador"""
        # Movimiento horizontal
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -MOVE_SPEED
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = MOVE_SPEED
            self.facing_right = True
        else:
            self.vx *= 0.8  # Fricción
            if abs(self.vx) < 0.5:
                self.vx = 0
        
        # Salto
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]):
            if self.on_ground:
                self.vy = JUMP_FORCE
                self.on_ground = False
                self.can_double_jump = True
                # Partículas de salto
                self.particles.emit_burst(self.x + self.width/2, self.y + self.height,
                                        Colors.PLATFORM_GLOW, 8, 3)
            elif self.has_double_jump and self.can_double_jump and not self.in_bubble:
                self.vy = JUMP_FORCE * 0.8
                self.can_double_jump = False
                # Efecto doble salto
                self.particles.emit_burst(self.x + self.width/2, self.y + self.height,
                                        Colors.BUBBLE_GOLD, 12, 4)
        
        # Dentro de burbuja (flotar)
        if self.in_bubble:
            self.vy -= 0.3  # Flotación
            if self.vy < -4:
                self.vy = -4

            # Control horizontal limitado
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.vx = -2
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.vx = 2

            # Salir de la burbuja
            if keys[pygame.K_SPACE] and self.bubble_ride_cooldown <= 0:
                self.in_bubble = False
                self.vy = -5  # Impulso al salir
                self.particles.emit_burst(self.x + self.width/2, self.y + self.height/2,
                                        Colors.BUBBLE_CYAN, 15, 5)
        else:
            # Gravedad normal
            self.vy += GRAVITY
            if self.vy > MAX_FALL_SPEED:
                self.vy = MAX_FALL_SPEED
        
        # Actualizar posición
        self.x += self.vx
        self.y += self.vy
        
        # Cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.bubble_ride_cooldown > 0:
            self.bubble_ride_cooldown -= 1
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        if self.power_timer > 0:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.bubble_element = "normal"
        
        # Colisiones con plataformas
        self.check_platform_collisions(platforms)
        
        # Límites de pantalla adaptados a resolución real
        if self.x < 0:
            self.x = 0
            self.vx = 0
        if self.x + self.width > self.screen_w:
            self.x = self.screen_w - self.width
            self.vx = 0
        if self.y > self.screen_h + 100:  # Caída al vacío
            self.y = -50
            self.vy = 0
        # Si está en burbuja y llega al techo, detener y salir
        if self.in_bubble and self.y < 0:
            self.y = 0
            self.vy = 0
            self.in_bubble = False
            self.bubble_ride_cooldown = 15
        
        # Animación
        if abs(self.vx) > 0.5:
            self.anim_frame += 0.2
        else:
            self.anim_frame = 0
        
        # Rastro
        if abs(self.vx) > 2 or abs(self.vy) > 2:
            self.particles.emit_trail(self.x + self.width/2, self.y + self.height/2,
                                    Colors.PLAYER_GLOW)
    
    def check_platform_collisions(self, platforms: List[pygame.Rect]):
        """Colisiones con plataformas"""
        self_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.on_ground = False
        
        for plat in platforms:
            if self_rect.colliderect(plat):
                # Colisión por arriba
                if self.vy > 0 and self_rect.bottom <= plat.centery:
                    self.y = plat.top - self.height
                    self.vy = 0
                    self.on_ground = True
                    self.can_double_jump = True
                # Colisión por abajo
                elif self.vy < 0 and self_rect.top >= plat.centery:
                    self.y = plat.bottom
                    self.vy = 0
                # Colisión lateral
                elif self.vx > 0:
                    self.x = plat.left - self.width
                    self.vx = 0
                elif self.vx < 0:
                    self.x = plat.right
                    self.vx = 0
                
                self_rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def can_shoot(self) -> bool:
        """Puede disparar?"""
        return self.shoot_cooldown <= 0
    
    def enter_bubble(self, bubble):
        """Entra en una burbuja para flotar"""
        if not self.in_bubble and self.bubble_ride_cooldown <= 0:
            self.in_bubble = True
            self.bubble_ride_cooldown = 30
            self.vy = -2
            self.particles.emit_gravity_float(self.x + self.width/2, self.y + self.height/2)
    
    def set_power_up(self, element: str, duration: int):
        """Activa un power-up elemental"""
        self.bubble_element = element
        self.power_timer = duration
        color = {
            "fire": Colors.FIRE_ORANGE,
            "ice": Colors.ICE_BLUE,
            "electric": Colors.ELECTRIC_PURPLE
        }.get(element, Colors.BUBBLE_GOLD)
        self.particles.emit_burst(self.x + self.width/2, self.y + self.height/2,
                                 color, 25, 6)
    
    def get_rect(self) -> pygame.Rect:
        """Rectángulo de colisión"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, surface: pygame.Surface):
        """Dibuja al jugador"""
        # Efecto de parpadeo cuando es invulnerable
        if self.invincible_timer > 0:
            # Parpadeo: alternar frames visibles e invisibles
            blink_phase = (self.invincible_timer // 4) % 2
            if blink_phase == 0:
                return  # No dibujar en este frame (efecto de parpadeo)

        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        
        # Si está en burbuja, dibujar burbuja alrededor
        if self.in_bubble:
            self._draw_riding_bubble(surface, center_x, center_y)
        
        # Glow del personaje
        for i in range(3, 0, -1):
            pygame.draw.ellipse(surface, (*Colors.PLAYER_GLOW, 30),
                              (int(self.x - i*2), int(self.y - i*2),
                               self.width + i*4, self.height + i*4))
        
        # Color según power-up
        body_color = Colors.PLAYER_TEAL
        if self.bubble_element == "fire":
            body_color = Colors.FIRE_ORANGE
        elif self.bubble_element == "ice":
            body_color = Colors.ICE_BLUE
        elif self.bubble_element == "electric":
            body_color = Colors.ELECTRIC_PURPLE
        
        # Cuerpo (cápsula)
        pygame.draw.ellipse(surface, body_color,
                          (int(self.x), int(self.y), self.width, self.height))
        
        # Brillo
        pygame.draw.ellipse(surface, (*Colors.TEXT_WHITE, 100),
                          (int(self.x + 5), int(self.y + 3), self.width - 10, self.height//2))
        
        # Ojos
        eye_y = self.y + 12
        if self.facing_right:
            pygame.draw.circle(surface, Colors.BG_DARK, (int(self.x + 22), int(eye_y)), 5)
            pygame.draw.circle(surface, Colors.TEXT_WHITE, (int(self.x + 23), int(eye_y - 1)), 2)
        else:
            pygame.draw.circle(surface, Colors.BG_DARK, (int(self.x + 10), int(eye_y)), 5)
            pygame.draw.circle(surface, Colors.TEXT_WHITE, (int(self.x + 9), int(eye_y - 1)), 2)
        
        # Cuernos
        horn_y = self.y + 3
        if self.facing_right:
            pygame.draw.polygon(surface, Colors.BUBBLE_GOLD,
                              [(self.x + 28, horn_y), (self.x + 32, horn_y - 8), (self.x + 24, horn_y)])
        else:
            pygame.draw.polygon(surface, Colors.BUBBLE_GOLD,
                              [(self.x + 4, horn_y), (self.x, horn_y - 8), (self.x + 8, horn_y)])
    
    def _draw_riding_bubble(self, surface: pygame.Surface, cx: float, cy: float):
        """Dibuja la burbuja en la que flota"""
        radius = 35
        
        # Glow
        for i in range(4, 0, -1):
            pygame.draw.circle(surface, (*Colors.BUBBLE_CYAN, 25),
                             (int(cx), int(cy)), radius + i * 5)
        
        # Burbuja transparente
        bubble_surf = pygame.Surface((radius * 2 + 20, radius * 2 + 20), pygame.SRCALPHA)
        pygame.draw.circle(bubble_surf, (*Colors.BUBBLE_CYAN, 60),
                          (radius + 10, radius + 10), radius)
        pygame.draw.circle(bubble_surf, Colors.BUBBLE_CYAN,
                          (radius + 10, radius + 10), radius, 2)
        surface.blit(bubble_surf, (int(cx - radius - 10), int(cy - radius - 10)))
        
        # Reflejos
        pygame.draw.circle(surface, Colors.TEXT_WHITE,
                          (int(cx - radius * 0.4), int(cy - radius * 0.4)), 5)
