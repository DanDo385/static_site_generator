# src/main.py
import os
import shutil

def copy_dir(src: str, dst: str) -> None:
    """
    Recursively copy the entire contents of src into dst.
    - Wipes dst first for a clean build.
    - Copies files with metadata (mtime, etc.) using copy2.
    - Recreates nested directories.
    """
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory not found: {src}")

    # 1) Clean destination
    if os.path.exists(dst):
        print(f"Removing: {dst}")
        shutil.rmtree(dst)  # delete whole tree for a clean copy
    os.makedirs(dst)

    # 2) Walk source one level and recurse for subdirectories
    for name in os.listdir(src):
        s_path = os.path.join(src, name)
        d_path = os.path.join(dst, name)

        if os.path.isdir(s_path):
            os.makedirs(d_path, exist_ok=True)
            print(f"Directory: {s_path} -> {d_path}")
            copy_dir(s_path, d_path)  # recurse
        else:
            shutil.copy2(s_path, d_path)  # copy file + metadata
            print(f"Copied:    {s_path} -> {d_path}")

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")
    copy_dir(static_dir, public_dir)
    print("✅ Static copied to public")

if __name__ == "__main__":
    main()
