"""Write one out-of-office auto-reply line to /output/entry.txt.

Deterministic: no network, no randomness, no time dependence. The line is a
fixed constant, validated before writing.
"""

import os

MIN_LENGTH = 1
MAX_LENGTH = 140

ENTRY_LINE = "Out until Monday. If this is urgent, it isn't \u2014 I checked before I left."


def validate_line(line):
    """Return True only if line is a valid single-line entry (1-140 chars)."""
    if not isinstance(line, str):
        return False
    if not (MIN_LENGTH <= len(line) <= MAX_LENGTH):
        return False
    if line.strip() == "":
        return False
    if "\n" in line or "\r" in line:
        return False
    return True


def write_entry(output_dir):
    """Validate the entry line and write it to <output_dir>/entry.txt."""
    if not validate_line(ENTRY_LINE):
        raise ValueError("entry line failed validation")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY_LINE)
    # Read-back gate: the file on disk must be exactly the winning line.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    assert written == ENTRY_LINE, "entry.txt does not match ENTRY_LINE"
    assert validate_line(written), "written entry failed validation"
    return path


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    write_entry(output_dir)


if __name__ == "__main__":
    main()
