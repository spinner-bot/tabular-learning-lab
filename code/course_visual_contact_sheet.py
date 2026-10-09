from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reports" / "browser_artifacts" / "course_visual_2026-10-10"
OUT = SOURCE / "contact_sheets"
OUT.mkdir(parents=True, exist_ok=True)

for viewport in ("desktop", "mobile"):
    files = sorted(SOURCE.glob(f"*_{viewport}.png"))
    for batch in range(0, len(files), 10):
        group = files[batch : batch + 10]
        thumbs = []
        for path in group:
            image = Image.open(path).convert("RGB")
            crop_height = min(image.height, 1100)
            image = image.crop((0, 0, image.width, crop_height))
            image.thumbnail((260, 420))
            canvas = Image.new("RGB", (280, 460), "white")
            canvas.paste(image, ((280 - image.width) // 2, 24))
            draw = ImageDraw.Draw(canvas)
            draw.text((8, 5), path.stem.replace(f"_{viewport}", ""), fill="black")
            thumbs.append(canvas)
        sheet = Image.new("RGB", (280 * 5, 460 * 2), "#e8edff")
        for index, thumb in enumerate(thumbs):
            sheet.paste(thumb, ((index % 5) * 280, (index // 5) * 460))
        output = OUT / f"{viewport}_{batch // 10 + 1}.png"
        sheet.save(output)
        print(output.relative_to(ROOT))
