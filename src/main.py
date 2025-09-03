# src/main.py
import os
import sys
import shutil
from page_generator import generate_pages_recursive

def copy_dir(src: str, dst: str) -> None:
    """
    Recursively copy src -> dst after ensuring dst exists.
    """
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory not found: {src}")
    os.makedirs(dst, exist_ok=True)  # ensure dest exists (recursive)

    for name in os.listdir(src):  # list directory entries
        s_path = os.path.join(src, name)
        d_path = os.path.join(dst, name)
        if os.path.isdir(s_path):
            copy_dir(s_path, d_path)
        else:
            shutil.copy2(s_path, d_path)  # copy with metadata
            print(f"Copied: {s_path} -> {d_path}")

def main():
    # NEW: basepath from CLI or default "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir   = os.path.join(project_root, "static")
    docs_dir     = os.path.join(project_root, "docs")     # <— build to docs now
    template     = os.path.join(project_root, "template.html")
    content_dir  = os.path.join(project_root, "content")

    # Clean docs for a fresh build
    if os.path.exists(docs_dir):
        print(f"Removing: {docs_dir}")
        shutil.rmtree(docs_dir)

    # Copy static -> docs  (your existing copy_dir function works fine)
    print("Copying static assets...")
    copy_dir(static_dir, docs_dir)

    # Generate ALL pages from content -> docs with the basepath
    generate_pages_recursive(content_dir, template, docs_dir, basepath)

    print("✅ Build complete (docs/)")

if __name__ == "__main__":
    main()
