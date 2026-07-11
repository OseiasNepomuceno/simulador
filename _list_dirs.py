import os

for lang in ['es', 'en']:
    p = os.path.join(lang, 'produtos')
    print(f"=== {lang}/produtos/ ===")
    print(f"  exists: {os.path.exists(p)}")
    print(f"  is_dir: {os.path.isdir(p)}")
    print(f"  is_file: {os.path.isfile(p)}")
    print(f"  is_symlink: {os.path.islink(p)}")
    if os.path.exists(p):
        try:
            contents = os.listdir(p)
            print(f"  contents ({len(contents)}): {contents}")
        except Exception as e:
            print(f"  ERROR listing: {e}")
    print()
