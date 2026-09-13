from PIL import Image, ImageDraw, ImageFont
import math

def make_icon(size, path):
    img = Image.new("RGB", (size, size), (7, 5, 15))
    draw = ImageDraw.Draw(img)

    cx, cy = size * 0.5, size * 0.38
    max_r = size * 0.62
    steps = 80
    for i in range(steps, 0, -1):
        t = i / steps
        r = max_r * t
        if t > 0.7:
            mix = (t - 0.7) / 0.3
            color = (
                int(255 * (1 - mix) + 140 * mix),
                int(61 * (1 - mix) + 82 * mix),
                int(129 * (1 - mix) + 255 * mix),
            )
        else:
            mix = t / 0.7
            color = (
                int(255 * (1 - mix) + 255 * mix),
                int(154 * (1 - mix) + 61 * mix),
                int(61 * (1 - mix) + 129 * mix),
            )
        alpha = max(0.0, 1 - t) * 0.9 + 0.1
        bg = (7, 5, 15)
        blended = tuple(int(bg[j] * (1 - alpha) + color[j] * alpha) for j in range(3))
        draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            fill=blended,
        )

    import random
    random.seed(42)
    for _ in range(int(size * size / 900)):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        b = random.randint(120, 255)
        s = 1 if size < 300 else random.choice([1, 1, 2])
        draw.ellipse([x, y, x + s, y + s], fill=(b, b, b))

    font_size = int(size * 0.42)
    font = None
    for fp in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]:
        try:
            font = ImageFont.truetype(fp, font_size)
            break
        except Exception:
            continue
    if font is None:
        font = ImageFont.load_default()

    text = "N"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = size / 2 - tw / 2 - bbox[0]
    ty = size / 2 - th / 2 - bbox[1] + size * 0.03

    draw.text((tx + size * 0.012, ty + size * 0.012), text, font=font, fill=(0, 0, 0))
    draw.text((tx, ty), text, font=font, fill=(245, 242, 255))

    img.save(path, "PNG")

make_icon(192, "www/icon-192.png")
make_icon(512, "www/icon-512.png")
print("done")
