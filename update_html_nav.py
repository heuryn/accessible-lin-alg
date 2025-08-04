import re
from pathlib import Path
from natsort import natsorted

chapter_dir = Path("chapter1")
html_files = natsorted([f for f in chapter_dir.glob("*.html") if f.is_file()],
                       key=lambda f: f.name)

# Prepare dropdown <option> tags
def make_dropdown(current_file):
    dropdown = ['<select onchange="location = this.value;">']
    dropdown.append(f'<option disabled selected>{current_file.name}</option>')
    for f in html_files:
        selected = " selected" if f == current_file else ""
        dropdown.append(f'<option value="{f.name}"{selected}>{f.name}</option>')
    dropdown.append("</select>")
    return "\n".join(dropdown)

for i, path in enumerate(html_files):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # Remove ```html or ``` if present
    content = re.sub(r"^\s*```html\s*", "", content, flags=re.IGNORECASE)
    content = re.sub(r"\s*```$", "", content)

    # Navigation links
    prev_link = html_files[i - 1].name if i > 0 else None
    next_link = html_files[i + 1].name if i < len(html_files) - 1 else None

    nav_html = ['<nav style="margin-bottom: 1em;">']
    nav_html.append('<a href="../index.html">← Index</a>')
    if prev_link:
        nav_html.append(f'<a href="{prev_link}">← Prev</a>')
    if next_link:
        nav_html.append(f'<a href="{next_link}">Next →</a>')
    nav_html.append('</nav>')

    dropdown = make_dropdown(path)

    # Combine all UI elements
    header_ui = "\n".join([*nav_html, dropdown, "<hr>"])

    # Insert UI elements
    if "<html" in content.lower():
        # Insert after <body>
        match = re.search(r"<body[^>]*>", content, flags=re.IGNORECASE)
        if match:
            insert_pos = match.end()
            content = content[:insert_pos] + "\n" + header_ui + "\n" + content[insert_pos:]
        else:
            content = header_ui + "\n" + content
    else:
        # Wrap as full HTML
        content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{path.stem}</title>
</head>
<body>
{header_ui}
{content}
</body>
</html>
"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

print(f"✔ Updated {len(html_files)} files with navigation, dropdown, and cleaned syntax.")
