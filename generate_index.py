import os
import re
from pathlib import Path
from natsort import natsorted

chapter_dir = Path("chapter1")
output_file = Path("index.html")

# Natural sort with optional groups
def parse_filename(filename):
    # Matches parts like 1_2_3 or 1_5_1_HomogSystems
    base = filename.stem
    parts = base.split('_')
    chapter = parts[1] if len(parts) > 1 else ''
    section = parts[2] if len(parts) > 2 else ''
    label = base.replace('_', '.')
    return chapter, section, base, label

# Collect and sort .html files
html_files = [f for f in chapter_dir.glob("*.html")]
html_files = natsorted(html_files, key=lambda f: f.stem)

# Group by major section (e.g., 1_5_*)
grouped = {}
for f in html_files:
    chapter, section, base, label = parse_filename(f)
    key = f"1.{chapter}" if chapter else "Misc"
    grouped.setdefault(key, []).append((f, label))

# Generate HTML
with open(output_file, "w", encoding="utf-8") as out:
    out.write("<!DOCTYPE html>\n<html lang='en'>\n<head>\n")
    out.write("  <meta charset='UTF-8'>\n  <title>Chapter 1 Index</title>\n")
    out.write("  <style>\n    body { font-family: sans-serif; margin: 2rem; }\n")
    out.write("    h2 { margin-top: 2rem; }\n    a { display: block; margin: 0.3rem 0; }\n  </style>\n")
    out.write("</head>\n<body>\n<h1>Chapter 1 Contents</h1>\n")

    for group, files in grouped.items():
        out.write(f"<h2>{group}</h2>\n")
        for f, label in files:
            href = f.as_posix()
            out.write(f'  <a href="{href}">{label}</a>\n')

    out.write("</body>\n</html>\n")
