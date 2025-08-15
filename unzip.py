import gzip
import shutil
from pathlib import Path

# Configuration
ROOT = Path(".")          # Project root (current directory)
RECURSIVE = True          # True: search in subfolders; False: only in ROOT

def dest_without_gz(src: Path) -> Path:
    """
    Returns the destination path by removing ONLY the final .gz extension.
    E.g.: 'a.jsonl.gz' -> 'a.jsonl', 'backup.tar.gz' -> 'backup.tar'
    """
    if src.suffix != ".gz":
        return src
    return src.with_suffix("")  # remove the last extension

def decompress_gz(src: Path, dst: Path) -> None:
    """
    Decompresses 'src' (.gz) into 'dst' (without .gz).
    Overwrites if dst exists but has size 0.
    """
    dst.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(src, "rb") as f_in, open(dst, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

def main():
    pattern = "**/*.gz" if RECURSIVE else "*.gz"
    gz_files = sorted(ROOT.glob(pattern))

    total = len(gz_files)
    done = 0
    skipped = 0
    failed = 0

    if total == 0:
        print("No .gz files found.")
        return

    print(f"Found {total} .gz file(s) in {ROOT.resolve()} (recursive={RECURSIVE}).\n")

    for i, src in enumerate(gz_files, 1):
        dst = dest_without_gz(src)

        # Skip if already decompressed and size > 0
        if dst.exists() and dst.stat().st_size > 0:
            print(f"[{i}/{total}] Already exists, skipping: {dst}")
            skipped += 1
            continue

        try:
            decompress_gz(src, dst)

            # Optionally keep original timestamps from the .gz
            try:
                src_stat = src.stat()
                Path(dst).touch(exist_ok=True)
                os_utime = __import__("os").utime
                os_utime(dst, (src_stat.st_atime, src_stat.st_mtime))
            except Exception:
                pass

            done += 1
            print(f"[{i}/{total}] OK → {dst}")
        except Exception as e:
            failed += 1
            print(f"[{i}/{total}] ERROR decompressing {src}: {e}")

    print("\nSummary:")
    print(f"  .gz processed   : {total}")
    print(f"  Decompressed    : {done}")
    print(f"  Skipped (exists): {skipped}")
    print(f"  Errors          : {failed}")

if __name__ == "__main__":
    main()
