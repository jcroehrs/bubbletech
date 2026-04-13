#!/usr/bin/env python3
import os, sys, random, math
import pygame
import pygame.freetype

def main():
    # Forzar backend Wayland si está disponible
    os.environ.setdefault('SDL_VIDEODRIVER', 'wayland')
    
    pygame.init()
    pygame.freetype.init()
    
    # Ventana fullscreen sin bordes
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
    W, H = screen.get_size()
    clock = pygame.time.Clock()
    FONT_SIZE = 24

    # 🔍 Cargar fuente monoespaciada del sistema (fallback seguro)
    font = None
    try:
        font = pygame.freetype.SysFont('monospace', FONT_SIZE)
    except Exception:
        font = pygame.freetype.Font(None, FONT_SIZE)

    # 📝 SET DE CARACTERES 100% LIBRE DE CUADROS
    # Números + Letras + Símbolos densos. Nunca fallan en Linux/Debian.
    CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz|{}[]<>/\\~!@#$%^&*()_+-=;:'\""

    # 📐 Calcular grid
    char_w = font.get_rect('A').width
    char_h = font.get_rect('A').height
    cols = W // char_w
    rows = H // char_h

    # 🎨 PRE-RENDERIZADO (VERDE ESTELA / VERDE BRILLANTE CABEZA)
    trail_cache = {c: font.render(c, (0, 190, 0))[0] for c in CHARS}
    head_cache  = {c: font.render(c, (140, 255, 140))[0] for c in CHARS}

    # 💧 LLUVIA
    drops = [{"y": random.uniform(-rows, -3), "speed": random.uniform(1.0, 3.5), "char": random.choice(CHARS)} for _ in range(cols)]

    # 🌫️ ESTELA (DESENVANECIMIENTO PROGRESIVO)
    fade = pygame.Surface((W, H), pygame.SRCALPHA)
    fade.fill((0, 6, 0, 14))  # Alpha bajo = estela larga y cinematográfica

    # 💊 PASTILLAS (ROJA / AZUL)
    pills = []
    pill_timer = 0

    # 🐇 CONEJO (BLANCO PURO)
    rabbit = {"x": -80, "y": H//2, "speed": 5.5, "active": False, "phase": 0}
    rabbit_timer = 0

    screen.fill((0, 0, 0))
    pygame.display.flip()

    running = True
    while running:
        dt = clock.tick(45) / 16.67  # ~45 FPS estables
        for ev in pygame.event.get():
            if ev.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                running = False

        # Aplicar capa de desvanecimiento verde
        screen.blit(fade, (0, 0))

        # 💧 Actualizar y dibujar lluvia
        for i, d in enumerate(drops):
            d["y"] += d["speed"] * dt
            if d["y"] >= rows:
                d["y"] = random.uniform(-5, -1)
                d["speed"] = random.uniform(1.0, 3.5)
                d["char"] = random.choice(CHARS)
            
            y = int(d["y"] * char_h)
            x = i * char_w
            if 0 <= y < H:
                screen.blit(head_cache[d["char"]], (x, y))

        # 💊 Generar y dibujar pastillas
        pill_timer += dt
        if pill_timer > random.randint(120, 280) / 45:
            pill_timer = 0
            pills.append({
                "x": random.randint(50, W-50), "y": -30,
                "speed": random.uniform(1.8, 3.2),
                "color": random.choice([(255, 40, 40), (40, 80, 255)]),
                "w": 12, "h": 26
            })

        for p in pills[:]:
            p["y"] += p["speed"] * dt
            if p["y"] > H + 30:
                pills.remove(p)
                continue
            # Mitad superior e inferior
            pygame.draw.ellipse(screen, p["color"], (p["x"], p["y"], p["w"], p["h"]//2))
            pygame.draw.ellipse(screen, p["color"], (p["x"], p["y"] + p["h"]//2, p["w"], p["h"]//2))
            # Borde sutil
            pygame.draw.ellipse(screen, (220, 220, 220), (p["x"], p["y"], p["w"], p["h"]), 1)

        # 🐇 Conejo blanco saltarín
        rabbit_timer += dt
        if not rabbit["active"] and rabbit_timer > random.randint(350, 850) / 45:
            rabbit["x"], rabbit["y"], rabbit["active"], rabbit["phase"] = -80, random.randint(H//4, H*3//4), True, 0
            rabbit_timer = 0

        if rabbit["active"]:
            rabbit["x"] += rabbit["speed"] * dt
            rabbit["phase"] += 0.16
            by = int(math.sin(rabbit["phase"]) * 5)
            rx, ry = rabbit["x"], rabbit["y"] + by
            s = 9  # escala

            # Silueta blanca pura (sin tintes verdes)
            pygame.draw.ellipse(screen, (255, 255, 255), (rx, ry, s*2, s*1.4))
            pygame.draw.circle(screen, (255, 255, 255), (rx + s*2, ry - s*0.5), s)
            pygame.draw.ellipse(screen, (255, 255, 255), (rx + s*1.4, ry - s*2.6, s*0.3, s*2.0))
            pygame.draw.ellipse(screen, (255, 255, 255), (rx + s*2.2, ry - s*2.6, s*0.3, s*2.0))
            pygame.draw.circle(screen, (0, 0, 0), (rx + s*2.3, ry - s*0.5), s*0.3)
            pygame.draw.circle(screen, (255, 255, 255), (rx - s*0.4, ry + s*0.4), s*0.7)

            if rx > W + 80: rabbit["active"] = False

        pygame.display.flip()

    # 📸 Captura automática al salir
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "matrix_capture.png")
    pygame.image.save(screen, out_path)
    print(f"\n✅ Captura guardada: {out_path}")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
