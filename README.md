# GZ File Decompressor

This Python script **recursively scans** your project folder for all files ending with `.gz` and decompresses them into their original format.  
It is **safe to re-run** multiple times, as it will skip files that have already been decompressed.

## Features
- **Recursive search** for `.gz` files starting from the project root (configurable).
- **Same-folder extraction** — the `.gz` is removed from the filename.
- **Skip existing files** — avoids overwriting if the decompressed file already exists and is not empty.
- **Re-run safe** — process only missing files.
- **Preserves timestamps** from the original `.gz` file.

## Requirements
- Python 3.7+
- No external dependencies (uses only Python standard library).

## Usage

1. **Place the script** in your project root (or anywhere you want to run it from).
2. **Run it**:
   ```bash
   python decompress_gz.py
   ```

3. The script will:
   - Find all `.gz` files.
   - Decompress them into the same folder.
   - Skip files that are already decompressed.

## Configuration
Edit the variables at the top of the script:

```python
ROOT = Path(".")     # Project root directory
RECURSIVE = True     # True: search in subfolders, False: only in ROOT
```

## Example Output
```
Found 5 .gz file(s) in /path/to/project (recursive=True).

[1/5] OK → ./files/accelerations_2025-01-27.jsonl
[2/5] Already exists, skipping: ./files/accelerations_2025-01-28.jsonl
[3/5] OK → ./files/accelerations_2025-01-29.jsonl
[4/5] OK → ./files/accelerations_2025-01-30.jsonl
[5/5] ERROR decompressing ./files/bad_file.gz: Not a gzipped file

Summary:
  .gz processed   : 5
  Decompressed    : 3
  Skipped (exists): 1
  Errors          : 1
```

## Notes
- The script **does not delete** the `.gz` files after decompression.  
  If you want to remove them to save space, you can easily add that behavior after confirming the extraction was successful.
- Large `.gz` files will take longer to process — progress is shown as files are processed.
