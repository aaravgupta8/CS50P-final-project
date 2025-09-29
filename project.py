# project.py
from pathlib import Path
import os
import shutil
from dataclasses import dataclass
from rich.console import Console
from rich.table import Table

console = Console()

@dataclass
class MoveResult:
    path: Path
    action: str          # "moved" | "skipped" | "error"
    reason: str | None
    dest: Path | None

CATEGORY_MAP = {
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images",
    ".pdf": "Documents", ".docx": "Documents", ".txt": "Documents",
    ".zip": "Archives", ".tar": "Archives", ".gz": "Archives",
    ".mp3": "Audio", ".wav": "Audio",
    ".mp4": "Video", ".mov": "Video",
    ".py": "Code", ".ipynb": "Code",
}

def categorize_file(path: Path) -> str:
    """Return category folder name for a file based on extension."""
    return CATEGORY_MAP.get(path.suffix.lower(), "Other")

def has_permissions(path: Path, write: bool = False) -> bool:
    """Check read/write permissions for a file or directory."""
    mode = os.R_OK | (os.W_OK if write else 0)
    try:
        return os.access(path, mode)
    except OSError:
        return False

def unique_destination(dest_dir: Path, name: str) -> Path:
    """Ensure no overwrite collisions by adding (2), (3)..."""
    candidate = dest_dir / name
    if not candidate.exists():
        return candidate
    stem, suffix = Path(name).stem, Path(name).suffix
    i = 2
    while True:
        c = dest_dir / f"{stem} ({i}){suffix}"
        if not c.exists():
            return c
        i += 1

def move_file_safe(src: Path, dest_dir: Path, dry_run: bool = True) -> MoveResult:
    """Try to move file, skip safely if permission denied."""
    if not src.is_file():
        return MoveResult(src, "skipped", "not-a-file", None)
    if not has_permissions(src):
        return MoveResult(src, "skipped", "no-read-permission", None)

    dest = unique_destination(dest_dir, src.name)

    # Dry-run: just plan the move
    if dry_run:
        return MoveResult(src, "moved", "dry-run", dest)

    if not dest_dir.exists():
        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as e:
            return MoveResult(src, "error", f"dest-mkdir-failed: {e}", None)

    if not has_permissions(dest_dir, write=True):
        return MoveResult(src, "skipped", "no-write-permission-dest", dest)

    try:
        shutil.move(str(src), str(dest))
        return MoveResult(src, "moved", None, dest)
    except PermissionError as e:
        return MoveResult(src, "skipped", f"permission-denied: {e}", dest)
    except OSError as e:
        return MoveResult(src, "error", f"oserror: {e}", dest)

def scan_folder(root: Path, out_root: Path, dry_run: bool = True, exclude: list[str] | None = None):
    """Scan a folder and organize files into categories."""
    exclude = exclude or []
    results: list[MoveResult] = []
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        if any(p.match(pattern) for pattern in exclude):
            results.append(MoveResult(p, "skipped", "excluded", None))
            continue
        category = categorize_file(p)
        dest_dir = out_root / category
        results.append(move_file_safe(p, dest_dir, dry_run=dry_run))
    return results

def pretty_print(results: list[MoveResult]):
    """Print a nice colored table with per-file outcomes."""
    table = Table(title="Digital Declutter Report", show_lines=True)
    table.add_column("File", style="cyan")
    table.add_column("Action", style="magenta")
    table.add_column("Destination", style="green")
    table.add_column("Reason", style="yellow")

    for r in results:
        table.add_row(str(r.path), r.action, str(r.dest) if r.dest else "-", r.reason or "-")

    console.print(table)

def generate_report(results: list[MoveResult]) -> str:
    """Summarize the cleanup run."""
    total = len(results)
    moved = sum(r.action == "moved" and r.reason != "dry-run" for r in results)
    planned = sum(r.action == "moved" and r.reason == "dry-run" for r in results)
    skipped = sum(r.action == "skipped" for r in results)
    errors = [r for r in results if r.action == "error"]
    lines = [
        f"Total files: {total}",
        f"Planned moves (dry-run): {planned}",
        f"Moved: {moved}",
        f"Skipped: {skipped}",
        f"Errors: {len(errors)}",
    ]
    return "\n".join(lines)

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Digital Declutter Assistant")
    parser.add_argument("source", type=Path, help="Folder to clean up")
    parser.add_argument("--dest", type=Path, default=None, help="Where to move organized files")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Preview without changes")
    parser.add_argument("--execute", action="store_true", help="Actually perform the moves")
    parser.add_argument("--exclude", nargs="*", default=[], help="Glob patterns to skip")
    args = parser.parse_args()

    src = args.source.expanduser().resolve()
    dest = args.dest.expanduser().resolve() if args.dest else None

    if not src.exists() or not src.is_dir():
        parser.error(f"Source path does not exist or is not a directory: {src}")

    dry_run = not args.execute
    out_root = dest or src

    results = scan_folder(src, out_root, dry_run=dry_run, exclude=args.exclude)

    # Always pretty-print full per-file report
    pretty_print(results)
    console.print("[bold green]" + generate_report(results) + "[/bold green]")

if __name__ == "__main__":
    main()
