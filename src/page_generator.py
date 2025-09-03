# src/page_generator.py
import os
import re
from markdown_to_html import markdown_to_html_node  # your earlier function

def extract_title(markdown: str) -> str:
    """
    Return the first H1 ('# ...') text in the markdown.
    If none is found, raise ValueError.
    """
    for line in markdown.splitlines():
        line = line.strip()
        m = re.match(r"^# (.+)$", line)
        if m:
            return m.group(1).strip()
    raise ValueError("No H1 ('# ') title found in markdown")

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    """
    Read markdown and template files, convert markdown to HTML, inject
    {{ Title }} and {{ Content }}, and write the full page to dest_path.
    Creates parent directories as needed.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read files
    with open(from_path, "r", encoding="utf-8") as f_md:
        markdown = f_md.read()
    with open(template_path, "r", encoding="utf-8") as f_tpl:
        template = f_tpl.read()

    # Convert and extract title
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    # Inject into template
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write out the page
    with open(dest_path, "w", encoding="utf-8") as f_out:
        f_out.write(page)
