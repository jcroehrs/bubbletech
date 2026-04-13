"""
📱 Controles Táctiles - BubbleTech
Joystick virtual + botones para Android
"""
import pygame
import math
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class TouchOverlay:
    """Sistema de controles táctiles para Android"""

    def __init__(self, screen_w=None, screen_h=None):
        self.screen_w = screen_w or SCREEN_WIDTH
        self.screen_h = screen_h or SCREEN_HEIGHT

        # Estado de controles
        self.keys_pressed = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_UP: False,
            pygame.K_SPACE: False,
            pygame.K_k: False,
        }

        # 🎮 Joystick virtual (izquierda)
        joy_size = 80
        joy_margin = 20
        joy_base_y = self.screen_h - joy_margin - joy_size
        self.joystick_base = pygame.Rect(
            joy_margin, joy_base_y, joy_size * 2, joy_size * 2
        )
        self.joystick_knob = pygame.Rect(0, 0, joy_size, joy_size)
        self.joystick_center = (
            self.joystick_base.centerx,
            self.joystick_base.centery,
        )
        self.joystick_active = False
        self.joystick_touch_id = None

        # 🅰️ Botones de acción (derecha)
        btn_size = 60
        btn_margin = 20
        btn_base_y = self.screen_h - btn_margin - btn_size

        # Botón K (disparar) - más a la derecha
        self.btn_shoot = pygame.Rect(
            self.screen_w - btn_margin - btn_size,
            btn_base_y,
            btn_size,
            btn_size,
        )
        self.btn_shoot_touch = None

        # Botón ESPACIO (salir de burbuja) - al lado
        self.btn_bubble = pygame.Rect(
            self.screen_w - btn_margin - btn_size * 2 - 10,
            btn_base_y + btn_size // 2,
            btn_size,
            btn_size,
        )
        self.btn_bubble_touch = None

        # Botón SALTO (arriba)
        self.btn_jump = pygame.Rect(
            self.screen_w - btn_margin - btn_size - 10,
            btn_base_y - btn_size - 20,
            btn_size,
            btn_size,
        )
        self.btn_jump_touch = None

        # Colores
        self.COLOR_JOY_BASE = (60, 70, 120, 150)
        self.COLOR_JOY_KNOB = (0, 230, 255, 200)
        self.COLOR_BTN = (60, 70, 120, 150)
        self.COLOR_BTN_ACTIVE = (0, 255, 220, 200)
        self.COLOR_LABEL = (255, 255, 255, 220)

        # Etiquetas
        self.font = pygame.font.SysFont("dejavusans", 16)
        self.label_shoot = self.font.render("K", True, self.COLOR_LABEL)
        self.label_bubble = self.font.render("SPC", True, self.COLOR_LABEL)
        self.label_jump = self.font.render("▲", True, self.COLOR_LABEL)

    def handle_event(self, event):
        """Procesa un evento táctil (FINGERDOWN, FINGERMOTION, FINGERUP)"""
        if event.type == pygame.FINGERDOWN:
            self._on_touch_down(event)
        elif event.type == pygame.FINGERMOTION:
            self._on_touch_motion(event)
        elif event.type == pygame.FINGERUP:
            self._on_touch_up(event)

    def _screen_pos(self, touch_event):
        """Convierte coordenadas normalizadas de touch a píxeles"""
        x = int(touch_event.x * self.screen_w)
        y = int(touch_event.y * self.screen_h)
        return x, y

    def _on_touch_down(self, event):
        touch_id = event.touch_id
        x, y = self._screen_pos(event)

        # ¿Tocó el joystick?
        if self.joystick_base.collidepoint(x, y) and self.joystick_touch_id is None:
            self.joystick_active = True
            self.joystick_touch_id = touch_id
            self._update_joystick(x, y)
            return

        # ¿Tocó un botón?
        if self.btn_shoot.collidepoint(x, y) and self.btn_shoot_touch is None:
            self.btn_shoot_touch = touch_id
            self.keys_pressed[pygame.K_k] = True
            return

        if self.btn_bubble.collidepoint(x, y) and self.btn_bubble_touch is None:
            self.btn_bubble_touch = touch_id
            self.keys_pressed[pygame.K_SPACE] = True
            return

        if self.btn_jump.collidepoint(x, y) and self.btn_jump_touch is None:
            self.btn_jump_touch = touch_id
            self.keys_pressed[pygame.K_UP] = True
            return

        # Toque fuera de controles — dirección táctil
        # Si toca la mitad izquierda de pantalla, mover hacia allá
        if x < self.screen_w // 2:
            self.keys_pressed[pygame.K_LEFT] = x < self.screen_w // 4
            self.keys_pressed[pygame.K_RIGHT] = x >= self.screen_w // 4

    def _on_touch_motion(self, event):
        touch_id = event.touch_id
        x, y = self._screen_pos(event)

        # Mover joystick
        if touch_id == self.joystick_touch_id:
            self._update_joystick(x, y)

    def _on_touch_up(self, event):
        touch_id = event.touch_id

        # Soltar joystick
        if touch_id == self.joystick_touch_id:
            self.joystick_active = False
            self.joystick_touch_id = None
            self.keys_pressed[pygame.K_LEFT] = False
            self.keys_pressed[pygame.K_RIGHT] = False
            # Centrar knob
            cx = self.joystick_center[0] - self.joystick_knob.width // 2
            cy = self.joystick_center[1] - self.joystick_knob.height // 2
            self.joystick_knob.topleft = (cx, cy)
            return

        # Soltar botón disparo
        if touch_id == self.btn_shoot_touch:
            self.btn_shoot_touch = None
            self.keys_pressed[pygame.K_k] = False
            return

        # Soltar botón burbuja
        if touch_id == self.btn_bubble_touch:
            self.btn_bubble_touch = None
            self.keys_pressed[pygame.K_SPACE] = False
            return

        # Soltar botón salto
        if touch_id == self.btn_jump_touch:
            self.btn_jump_touch = None
            self.keys_pressed[pygame.K_UP] = False
            return

    def _update_joystick(self, touch_x, touch_y):
        """Actualiza la posición del knob del joystick y las teclas"""
        cx, cy = self.joystick_center
        dx = touch_x - cx
        dy = touch_y - cy
        dist = math.sqrt(dx * dx + dy * dy)
        max_dist = self.joystick_base.width // 2

        if dist > max_dist:
            dx = dx / dist * max_dist
            dy = dy / dist * max_dist

        knob_size = self.joystick_knob.width
        self.joystick_knob.center = (cx + int(dx), cy + int(dy))

        # Dirección horizontal
        threshold = max_dist * 0.3
        self.keys_pressed[pygame.K_LEFT] = dx < -threshold
        self.keys_pressed[pygame.K_RIGHT] = dx > threshold

    def get_keys(self):
        """Devuelve un dict compatible con pygame.key.get_pressed()"""
        return self.keys_pressed.copy()

    def draw(self, surface):
        """Dibuja los controles táctiles"""
        # Joystick base
        joy_surf = pygame.Surface(
            (self.joystick_base.width, self.joystick_base.height), pygame.SRCALPHA
        )
        pygame.draw.circle(
            joy_surf,
            self.COLOR_JOY_BASE,
            (self.joystick_base.width // 2, self.joystick_base.height // 2),
            self.joystick_base.width // 2,
        )
        surface.blit(joy_surf, self.joystick_base.topleft)

        # Joystick knob
        knob_surf = pygame.Surface(
            (self.joystick_knob.width, self.joystick_knob.height), pygame.SRCALPHA
        )
        pygame.draw.circle(
            knob_surf,
            self.COLOR_JOY_KNOB,
            (self.joystick_knob.width // 2, self.joystick_knob.height // 2),
            self.joystick_knob.width // 2,
        )
        surface.blit(knob_surf, self.joystick_knob.topleft)

        # Botón disparar (K)
        color_shoot = self.COLOR_BTN_ACTIVE if self.keys_pressed[pygame.K_k] else self.COLOR_BTN
        btn_surf = pygame.Surface((self.btn_shoot.width, self.btn_shoot.height), pygame.SRCALPHA)
        pygame.draw.circle(btn_surf, color_shoot, (self.btn_shoot.width // 2, self.btn_shoot.height // 2), self.btn_shoot.width // 2)
        surface.blit(btn_surf, self.btn_shoot.topleft)
        label_rect = self.label_shoot.get_rect(center=self.btn_shoot.center)
        surface.blit(self.label_shoot, label_rect)

        # Botón burbuja (SPACE)
        color_bubble = self.COLOR_BTN_ACTIVE if self.keys_pressed[pygame.K_SPACE] else self.COLOR_BTN
        btn_surf2 = pygame.Surface((self.btn_bubble.width, self.btn_bubble.height), pygame.SRCALPHA)
        pygame.draw.circle(btn_surf2, color_bubble, (self.btn_bubble.width // 2, self.btn_bubble.height // 2), self.btn_bubble.width // 2)
        surface.blit(btn_surf2, self.btn_bubble.topleft)
        label_rect2 = self.label_bubble.get_rect(center=self.btn_bubble.center)
        surface.blit(self.label_bubble, label_rect2)

        # Botón salto (arriba)
        color_jump = self.COLOR_BTN_ACTIVE if self.keys_pressed[pygame.K_UP] else self.COLOR_BTN
        btn_surf3 = pygame.Surface((self.btn_jump.width, self.btn_jump.height), pygame.SRCALPHA)
        pygame.draw.circle(btn_surf3, color_jump, (self.btn_jump.width // 2, self.btn_jump.height // 2), self.btn_jump.width // 2)
        surface.blit(btn_surf3, self.btn_jump.topleft)
        label_rect3 = self.label_jump.get_rect(center=self.btn_jump.center)
        surface.blit(self.label_jump, label_rect3)

    def update_screen_size(self, screen_w, screen_h):
        """Actualiza las dimensiones cuando cambia la pantalla"""
        self.screen_w = screen_w
        self.screen_h = screen_h
        joy_size = 80
        joy_margin = 20
        joy_base_y = self.screen_h - joy_margin - joy_size
        self.joystick_base = pygame.Rect(
            joy_margin, joy_base_y, joy_size * 2, joy_size * 2
        )
        self.joystick_center = (
            self.joystick_base.centerx,
            self.joystick_base.centery,
        )
        cx = self.joystick_center[0] - joy_size // 2
        cy = self.joystick_center[1] - joy_size // 2
        self.joystick_knob.topleft = (cx, cy)

        btn_size = 60
        btn_margin = 20
        btn_base_y = self.screen_h - btn_margin - btn_size
        self.btn_shoot = pygame.Rect(
            self.screen_w - btn_margin - btn_size,
            btn_base_y,
            btn_size,
            btn_size,
        )
        self.btn_bubble = pygame.Rect(
            self.screen_w - btn_margin - btn_size * 2 - 10,
            btn_base_y + btn_size // 2,
            btn_size,
            btn_size,
        )
        self.btn_jump = pygame.Rect(
            self.screen_w - btn_margin - btn_size - 10,
            btn_base_y - btn_size - 20,
            btn_size,
            btn_size,
        )
