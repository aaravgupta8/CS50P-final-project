from pathlib import Path
import os, stat, pytest
from project import categorize_file, move_file_safe, scan_folder

def test_categorize_file_basic():
    assert categorize_file(Path("photo.JPG")) == "Images"
    assert categorize_file(Path("report.pdf")) == "Documents"
    assert categorize_file(Path("unknown.xyz")) == "Other"

def test_move_file_safe_dry_run(tmp_path: Path):
    src = tmp_path / "a.txt"
    src.write_text("hello")
    dest_dir = tmp_path / "Documents"
    res = move_file_safe(src, dest_dir, dry_run=True)
    assert res.action == "moved"
    assert res.dest.name == "a.txt"
    assert src.exists()

def test_move_file_safe_permission_denied_on_dest(tmp_path: Path):
    src = tmp_path / "a.txt"
    src.write_text("hello")
    dest_dir = tmp_path / "locked"
    dest_dir.mkdir()
    if os.name == "nt":
        pytest.skip("chmod test unreliable on Windows")
    mode = dest_dir.stat().st_mode
    dest_dir.chmod(mode & ~stat.S_IWUSR)
    try:
        res = move_file_safe(src, dest_dir, dry_run=False)
        assert res.action == "skipped"
        assert "no-write-permission" in res.reason
        assert src.exists()
    finally:
        dest_dir.chmod(mode)

def test_scan_folder_exclude(tmp_path: Path):
    (tmp_path / "photo.jpg").write_text("img")
    (tmp_path / "secret.key").write_text("secret")
    results = scan_folder(tmp_path, tmp_path, dry_run=True, exclude=["*.key"])
    reasons = {r.path.name: r.reason for r in results}
    assert reasons["secret.key"] == "excluded"
