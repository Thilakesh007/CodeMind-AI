from pathlib import Path


def build_tree(path: Path):
    tree = {
        "name": path.name,
        "type": "folder",
        "children": []
    }

    IGNORE_DIRS = {".git", "node_modules", "__pycache__", "venv", ".idea", ".vscode", "dist", "build"}

    for item in sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
        if item.name in IGNORE_DIRS:
            continue

        if item.is_dir():
            tree["children"].append(build_tree(item))

        else:
            tree["children"].append({
                "name": item.name,
                "type": "file"
            })

    return tree