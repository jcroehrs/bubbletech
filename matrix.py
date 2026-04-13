#!/usr/bin/env python3
import os
import sys
import time
import random
import threading
import platform

def main():
    # Configuración de seguridad para caracteres especiales en Windows
    if platform.system() == "Windows":
        sys.stdout.reconfigure(encoding='utf-8')
        os.system('')  # Activa el soporte ANSI en Windows 10/11

    try:
        cols, rows = os.get_terminal_size()
    except OSError:
        cols, rows = 80, 24  # Tamaño por defecto si no es una terminal

    # Caracteres estilo Matrix (Katakana + Números + Letras)
    MATRIX_CHARS = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Estado de cada columna: [posición_y, velocidad, carácter_actual]
    drops = [[random.uniform(-rows, -5), random.uniform(0.8, 2.5), random.choice(MATRIX_CHARS)] for _ in range(cols)]

    # Códigos ANSI
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"
    CLEAR_SCREEN = "\033[2J"
    CURSOR_HOME = "\033[H"
    SET_BLACK_BG = "\033[40m"
    SET_GREEN_FG = "\033[32m"
    RESET = "\033[0m"

    # Preparar terminal
    sys.stdout.write(SET_BLACK_BG + HIDE_CURSOR + CLEAR_SCREEN + CURSOR_HOME + SET_GREEN_FG)
    sys.stdout.flush()

    # Evento para detener el programa
    stop_event = threading.Event()

    def wait_for_key():
        """Detecta pulsación de tecla de forma no bloqueante (multiplataforma)"""
        try:
            if platform.system() == "Windows":
                import msvcrt
                while not stop_event.is_set():
                    if msvcrt.kbhit():
                        msvcrt.getch()
                        stop_event.set()
                        return
                    time.sleep(0.05)
            else:
                import select
                import tty
                import termios
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setcbreak(fd)  # Modo raw para capturar teclas individuales
                    while not stop_event.is_set():
                        if select.select([sys.stdin], [], [], 0.05)[0]:
                            sys.stdin.read(1)
                            stop_event.set()
                            return
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except Exception:
            stop_event.set()  # Fallback seguro ante errores de terminal

    # Hilo dedicado a esperar tecla sin bloquear la animación
    key_thread = threading.Thread(target=wait_for_key, daemon=True)
    key_thread.start()

    try:
        # Bucle de animación (~25 FPS)
        while not stop_event.is_set():
            sys.stdout.write(CURSOR_HOME)
            frame_parts = []
            
            for x, drop in enumerate(drops):
                drop[0] += drop[1]  # Actualizar posición Y
                
                # Si sale de pantalla, reiniciar arriba con nueva velocidad y carácter
                if drop[0] >= rows:
                    drop[0] = random.uniform(-rows, -5)
                    drop[1] = random.uniform(0.8, 2.5)
                    drop[2] = random.choice(MATRIX_CHARS)

                y = int(drop[0])
                if 0 <= y < rows:
                    # \033[fila;columnaH posiciona el cursor (1-based)
                    frame_parts.append(f"\033[{y+1};{x+1}H{drop[2]}")

            sys.stdout.write("".join(frame_parts))
            sys.stdout.flush()
            time.sleep(0.04)  # ~25 FPS

    except KeyboardInterrupt:
        pass
    finally:
        # Restaurar terminal al estado original
        stop_event.set()
        key_thread.join(timeout=0.5)
        sys.stdout.write(SHOW_CURSOR + RESET + CLEAR_SCREEN + CURSOR_HOME)
        sys.stdout.flush()

if __name__ == "__main__":
    main()
