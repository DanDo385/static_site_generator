# src/page_generator.py
import os
import re
from pathlib import Path
from markdown_to_html import markdown_to_html_node  # your earlier function

def _normalize_basepath(base: str) -> str:
    # Ensure starts and ends with a slash.  "/" -> "/" ; "myrepo" -> "/myrepo/"
    if not base.startswith("/"):
        base = "/" + base
    if not base.endswith("/"):
        base = base + "/"
    return base

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

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str = "/") -> None:
    base = _normalize_basepath(basepath)
    print(f"Generating page from {from_path} to {dest_path} using {template_path} (base={base})")

    with open(from_path, "r", encoding="utf-8") as f_md:
        md = f_md.read()
    with open(template_path, "r", encoding="utf-8") as f_tpl:
        template = f_tpl.read()

    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    # IMPORTANT: rewrite ONLY root-absolute URLs to include the repo basepath
    page = page.replace('href="/', f'href="{base}')
    page = page.replace('src="/',  f'src="{base}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f_out:
        f_out.write(page)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str = "/") -> None:
    content_root = Path(dir_path_content)
    dest_root    = Path(dest_dir_path)
    for md_path in content_root.rglob("*.md"):
        rel_md   = md_path.relative_to(content_root)      # e.g. blog/majesty/index.md
        rel_html = rel_md.with_suffix(".html")            # -> blog/majesty/index.html
        dest     = dest_root / rel_html                   # -> docs/blog/majesty/index.html
        generate_page(str(md_path), template_path, str(dest), basepath)
