from pathlib import Path
from pdf2image import convert_from_path

in_dir, out_dir = Path("assets"), Path("static/assets")
out_dir.mkdir(parents=True, exist_ok=True)

for pdf in in_dir.glob("*.pdf"):
    img = convert_from_path(pdf, dpi=150, first_page=1, last_page=1)[0]
    img.save(out_dir / f"{pdf.stem}.png", "PNG")