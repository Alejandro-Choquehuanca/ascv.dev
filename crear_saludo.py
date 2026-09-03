from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


# ============================================================
# CONFIGURACIÓN
# ============================================================

OUTPUT_FILE = Path("assets/greeting.gif")

TEXT = "Hola, soy Alejandro Samir"

BACKGROUND = (5, 10, 9)
TEXT_COLOR = (0, 255, 170)

FONT_PATH = r"C:\Windows\Fonts\consola.ttf"
FONT_SIZE = 28

PADDING_X = 35
PADDING_Y = 20

FRAME_DURATION = 90
PAUSE_FRAMES = 15


# ============================================================
# FUENTE
# ============================================================

if Path(FONT_PATH).exists():
    font = ImageFont.truetype(
        FONT_PATH,
        FONT_SIZE
    )
else:
    font = ImageFont.load_default()


# ============================================================
# CALCULAR TAMAÑO
# ============================================================

dummy = Image.new(
    "RGB",
    (10, 10)
)

draw = ImageDraw.Draw(dummy)

bbox = draw.textbbox(
    (0, 0),
    TEXT,
    font=font
)

text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

width = text_width + PADDING_X * 2
height = text_height + PADDING_Y * 2


# ============================================================
# CREAR FRAMES
# ============================================================

frames = []


for i in range(len(TEXT) + 1):

    visible_text = TEXT[:i]

    image = Image.new(
        "RGB",
        (width, height),
        BACKGROUND
    )

    draw = ImageDraw.Draw(image)

    draw.text(
        (
            PADDING_X,
            PADDING_Y
        ),
        visible_text,
        font=font,
        fill=TEXT_COLOR
    )

    # Cursor
    cursor_text = visible_text

    cursor_bbox = draw.textbbox(
        (0, 0),
        cursor_text,
        font=font
    )

    cursor_x = PADDING_X + (
        cursor_bbox[2] - cursor_bbox[0]
    )

    draw.rectangle(
        [
            cursor_x + 3,
            PADDING_Y + 2,
            cursor_x + 7,
            PADDING_Y + text_height
        ],
        fill=TEXT_COLOR
    )

    frames.append(
        image.convert(
            "P",
            palette=Image.ADAPTIVE
        )
    )


# ============================================================
# PAUSA AL FINAL
# ============================================================

for _ in range(PAUSE_FRAMES):

    frames.append(
        frames[-1].copy()
    )


# ============================================================
# GUARDAR
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


print()
print("======================================")
print("       SALUDO CREADO CORRECTAMENTE")
print("======================================")
print()
print(f"Archivo: {OUTPUT_FILE}")
print()