# src/main.py
import os
import shutil
from page_generator import generate_page

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
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")
    template_path = os.path.join(project_root, "template.html")
    from_path = os.path.join(project_root, "content", "index.md")
    dest_path = os.path.join(public_dir, "index.html")

    # 1) Clean public
    if os.path.exists(public_dir):
        print(f"Removing: {public_dir}")
        shutil.rmtree(public_dir)  # remove directory tree

    # 2) Copy static -> public
    print("Copying static assets...")
    copy_dir(static_dir, public_dir)

    # 3) Generate content page
    generate_page(from_path, template_path, dest_path)
    print("✅ Build complete")

if __name__ == "__main__":
    main()
