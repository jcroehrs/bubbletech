# 🫧 BUBBLETECH - Modern Bubble Burst

Un juego de acción y plataformas inspirado en el clásico Bubble Bobble, pero transformado en una experiencia Cyber-Cartoon neón con mecánicas modernas.

## 🚀 Innovaciones respecto al clásico

A diferencia del original, **BubbleTech** introduce:
- **Gravedad Cero**: El jugador puede entrar en sus propias burbujas para flotar y alcanzar plataformas elevadas.
- **Fusión Cuántica**: Burbujas que colisionan entre sí pueden fusionarse en **Mega-Burbujas** doradas.
- **IA Enemiga Dinámica**: 4 tipos de enemigos con comportamientos distintos (Walkers, Jumpers, Chasers y Floaters).
- **Estética Neon-HD**: Efectos de partículas, glows dinámicos y una interfaz holográfica.
- **Sistemas de Partículas**: Explosiones físicas, rastros de movimiento y efectos de "pop".

## 🎮 Guía de Juego

### Controles
- **Movimiento**: `WASD` o `Flechas`
- **Salto**: `ESPACIO`
- **Disparo de Burbujas**: `K`
- **Menú/Inicio**: `ESPACIO`

### Mecánica de Combate
1. **Atrapar**: Dispara una burbuja para encerrar a un enemigo.
2. **Eliminar**: Toca la burbuja atrapada para hacer explotar al enemigo y ganar puntos.
3. **Flotar**: Dispara una burbuja vacía, camina hacia ella y salta para entrar. Ahora podrás flotar hacia arriba.

## 📁 Estructura del Proyecto

```text
bubbletech/
├── main.py             # Motor principal y Game Loop
├── entities/
│   ├── player.py       # Lógica del héroe (Bubby)
│   ├── bubble.py       # Física y lógica de burbujas
│   └── enemy.py        # IA y comportamiento de enemigos
├── ui/
│   └── manager.py      # HUD holográfico y menús
└── utils/
    ├── constants.py    # Configuración, colores y física
    └── particles.py    # Sistema de efectos visuales
```

## 🚀 Instrucciones de Ejecución

### Requisitos
- Python 3.10+
- Pygame 2.0+

### Instalación y Lanzamiento
```bash
# Navegar a la carpeta
cd /home/jcroehrs/proyectos_claw/bubbletech

# Instalar dependencias
pip install pygame

# Ejecutar el juego
python main.py
```

## 🛠️ Notas de Desarrollo
El código está estructurado de forma modular. Para añadir nuevos tipos de burbujas o enemigos, simplemente extiende las clases en `entities/` y actualiza la paleta en `utils/constants.py`.
