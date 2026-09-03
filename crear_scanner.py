from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path


# ============================================================
# CONFIGURACIÓN
# ============================================================

ASCII_FILE = Path("assets/ascii-art.txt")
OUTPUT_FILE = Path("assets/profile-scanner.gif")

CHAR_WIDTH = 8
CHAR_HEIGHT = 16

PADDING_X = 35
PADDING_Y = 35

FRAMES = 40
FRAME_DURATION = 70

BACKGROUND = (5, 10, 9)
ASCII_COLOR = (0, 190, 150)
SCANNER_COLOR = (0, 255, 170)


# ============================================================
# COMPROBAR ARCHIVO ASCII
# ============================================================

if not ASCII_FILE.exists():
    raise FileNotFoundError(
        f"No se encontró el archivo: {ASCII_FILE}"
    )


# ============================================================
# LEER ASCII
# ============================================================

text = ASCII_FILE.read_text(encoding="utf-8")

lines = text.splitlines()

# Quitar "# ascv.dev" si existe como primera línea
if lines and lines[0].strip().lower() == "# ascv.dev":
    lines = lines[1:]

lines = [line.rstrip() for line in lines]

if not lines:
    raise ValueError("El archivo ascii-art.txt está vacío.")


# ============================================================
# FUENTE MONOESPACIADA
# ============================================================

font_paths = [
    r"C:\Windows\Fonts\consola.ttf",
    r"C:\Windows\Fonts\lucon.ttf",
    r"C:\Windows\Fonts\cour.ttf",
]

font = None

for path in font_paths:
    if Path(path).exists():
        font = ImageFont.truetype(path, 14)
        print(f"Fuente utilizada: {path}")
        break


if font is None:
    print("No se encontró Consolas.")
    print("Usando fuente predeterminada de Pillow.")
    font = ImageFont.load_default()


# ============================================================
# DIMENSIONES
# ============================================================

max_length = max(len(line) for line in lines)

width = max_length * CHAR_WIDTH + PADDING_X * 2
height = len(lines) * CHAR_HEIGHT + PADDING_Y * 2

print()
print(f"Resolución: {width}x{height}")
print(f"Líneas: {len(lines)}")
print(f"Columnas: {max_length}")
print()


# ============================================================
# CREAR ANIMACIÓN
# ============================================================

frames = []


for frame_number in range(FRAMES):

    # --------------------------------------------------------
    # FONDO
    # --------------------------------------------------------

    image = Image.new(
        "RGBA",
        (width, height),
        BACKGROUND + (255,)
    )

    draw = ImageDraw.Draw(image)


    # --------------------------------------------------------
    # ASCII
    # --------------------------------------------------------

    y = PADDING_Y

    for line in lines:

        draw.text(
            (PADDING_X, y),
            line,
            font=font,
            fill=ASCII_COLOR + (255,)
        )

        y += CHAR_HEIGHT


    # --------------------------------------------------------
    # POSICIÓN DEL SCANNER
    # --------------------------------------------------------

    scanner_y = int(
        PADDING_Y
        + (height - PADDING_Y * 2)
        * frame_number
        / (FRAMES - 1)
    )


    # --------------------------------------------------------
    # BRILLO DEL SCANNER
    # --------------------------------------------------------

    glow = Image.new(
        "RGBA",
        (width, height),
        (0, 0, 0, 0)
    )

    glow_draw = ImageDraw.Draw(glow)

    glow_lines = [
        (-14, 15),
        (-10, 25),
        (-7, 45),
        (-5, 70),
        (-3, 100),
        (0, 255),
        (3, 100),
        (5, 70),
        (7, 45),
        (10, 25),
        (14, 15),
    ]

    for offset, alpha in glow_lines:

        glow_draw.line(
            [
                (0, scanner_y + offset),
                (width, scanner_y + offset)
            ],
            fill=SCANNER_COLOR + (alpha,),
            width=2
        )


    # Difuminar el brillo
    glow = glow.filter(
        ImageFilter.GaussianBlur(5)
    )

    image = Image.alpha_composite(
        image,
        glow
    )


    # --------------------------------------------------------
    # LÍNEA PRINCIPAL
    # --------------------------------------------------------

    draw = ImageDraw.Draw(image)

    draw.line(
        [
            (0, scanner_y),
            (width, scanner_y)
        ],
        fill=SCANNER_COLOR + (255,),
        width=2
    )


    # --------------------------------------------------------
    # PUNTO DE LUZ
    # --------------------------------------------------------

    draw.ellipse(
        [
            width - 20,
            scanner_y - 4,
            width - 12,
            scanner_y + 4
        ],
        fill=SCANNER_COLOR + (255,)
    )


    # --------------------------------------------------------
    # CONVERTIR A PALETA GIF
    # --------------------------------------------------------

    frames.append(
        image.convert(
            "P",
            palette=Image.ADAPTIVE
        )
    )


# ============================================================
# GUARDAR GIF
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

frames[0].save(
    OUTPUT_FILE,
    save_all=True,
    append_images=frames[1:],
    duration=FRAME_DURATION,
    loop=0,
    optimize=False
)


print("============================================")
print("      SCANNER CREADO CORRECTAMENTE")
print("============================================")
print()
print(f"Archivo generado:")
print(f"  {OUTPUT_FILE}")
print()