# normalize-stems

A lightweight Python utility to normalize exported **Logic Pro** audio stem filenames and prefix them with standardized track numbers for use in **Helix Stadium** (or other multitrack playback systems).

Translated and adapted from [tooh's GitHub Gist](https://gist.github.com/tooh/ddad0509a27262fed974552c8a836639).

---

## Overview

When bouncing stems in Apple Logic Pro, stems are typically exported with names such as:
```text
My Song (Drums)_1.wav
My Song (Bass)_1.wav
My Song (Piano)_1.wav
My Song (Guitar)_1.wav
My Song (Other)_1.wav
My Song (Vocals)_1.wav
```

`normalize-stems` parses the instrument name in parentheses, looks up its standardized track position, and renames (or copies) the files sequentially:
```text
01_Drums.wav
02_Bass.wav
03_Piano.wav
04_Guitar.wav
05_Other.wav
06_Vocals.wav
```

Supported audio formats: `.wav`, `.aif`, `.aiff`, `.flac`, `.ogg`.

---

## Default Track Order

The default ordering defined in `TRACK_ORDER` is:

| Track # | Instrument | Canonical Filename Pattern |
|---------|------------|----------------------------|
| 01      | Drums      | `01_Drums.<ext>`           |
| 02      | Bass       | `02_Bass.<ext>`            |
| 03      | Piano      | `03_Piano.<ext>`           |
| 04      | Guitar     | `04_Guitar.<ext>`          |
| 05      | Other      | `05_Other.<ext>`           |
| 06      | Vocals     | `06_Vocals.<ext>`          |

You can customize the track list or ordering directly in `normalize_stems.py`. Instrument matching is case-insensitive.

---

## Installation

No external dependencies are required. Python 3.10+ is recommended.

### Option 1: Standalone Script
Clone the repository and run the script directly:
```bash
git clone https://github.com/tooh/normalize-stems.git
cd normalize-stems
chmod +x normalize_stems.py
```

### Option 2: Pip Install (Editable / CLI)
Install locally to get the `normalize-stems` command in your terminal:
```bash
pip install -e .
```

---

## Usage

### 1. Preview changes (Dry Run)
Inspect the planned renames without modifying any files:
```bash
python3 normalize_stems.py /path/to/stems --dry-run
```

### 2. Rename in-place
Rename the stem files directly inside the source directory:
```bash
python3 normalize_stems.py /path/to/stems
```

### 3. Copy to destination
Keep original stem files intact and copy the normalized stems to a target folder:
```bash
python3 normalize_stems.py /path/to/stems --copy /path/to/output_stems
```

---

## Running Tests

Unit tests use Python's built-in `unittest` runner:
```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

---

## License

[MIT](LICENSE)
