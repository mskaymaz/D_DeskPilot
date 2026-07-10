import math
from pathlib import Path

from PIL import Image, ImageDraw


ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT_DIR / "assets" / "icon.ico"

# Create a 256x256 icon.
img = Image.new("RGBA", (256, 256), (255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# Draw clock face.
draw.ellipse([20, 20, 236, 236], fill=(255, 255, 255), outline=(0, 0, 0), width=5)

# Draw numbers 1-12.
for i in range(12):
    angle = i * 30
    x = 128 + 90 * math.cos(math.radians(angle - 90))
    y = 128 + 90 * math.sin(math.radians(angle - 90))
    draw.text((x - 10, y - 10), str(i + 1 if i != 0 else 12), fill=(0, 0, 0))

# Draw hour hand.
draw.line(
    [128, 128, 128 + 50 * math.cos(math.radians(0)), 128 + 50 * math.sin(math.radians(0))],
    fill=(0, 0, 0),
    width=5,
)

# Draw minute hand.
draw.line(
    [128, 128, 128 + 70 * math.cos(math.radians(0)), 128 + 70 * math.sin(math.radians(0))],
    fill=(0, 0, 0),
    width=3,
)

# Draw second hand.
draw.line(
    [128, 128, 128 + 80 * math.cos(math.radians(0)), 128 + 80 * math.sin(math.radians(0))],
    fill=(255, 0, 0),
    width=2,
)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
img.save(OUTPUT_FILE)
print(f"Icon created: {OUTPUT_FILE}")
