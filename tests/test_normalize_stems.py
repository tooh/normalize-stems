import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from normalize_stems import (
    TRACK_ORDER,
    build_new_name,
    parse_stem_name,
    process,
    track_number,
)


class TestNormalizeStems(unittest.TestCase):
    def test_parse_stem_name(self):
        self.assertEqual(
            parse_stem_name("Song Title (Drums)_1.wav"), "Drums"
        )
        self.assertEqual(
            parse_stem_name("My Song (Bass).aiff"), "Bass"
        )
        self.assertEqual(
            parse_stem_name("Track 01 (Piano)_12.wav"), "Piano"
        )
        self.assertEqual(
            parse_stem_name("Live Show (Vocals).flac"), "Vocals"
        )
        self.assertIsNone(parse_stem_name("Unmatched_Filename.wav"))

    def test_track_number(self):
        self.assertEqual(track_number("Drums"), 1)
        self.assertEqual(track_number("drums"), 1)
        self.assertEqual(track_number("Bass"), 2)
        self.assertEqual(track_number("bass"), 2)
        self.assertEqual(track_number("Piano"), 3)
        self.assertEqual(track_number("Guitar"), 4)
        self.assertEqual(track_number("Other"), 5)
        self.assertEqual(track_number("Vocals"), 6)
        self.assertIsNone(track_number("UnknownInstrument"))

    def test_build_new_name(self):
        self.assertEqual(
            build_new_name("drums", 1, ".wav"), "01_Drums.wav"
        )
        self.assertEqual(
            build_new_name("VOCALS", 6, ".wav"), "06_Vocals.wav"
        )

    def test_process_rename_in_place(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            source = Path(tmp_dir)
            f1 = source / "Song (Drums)_1.wav"
            f2 = source / "Song (Bass)_1.wav"
            f1.touch()
            f2.touch()

            process(source, dest_dir=None, dry_run=False)

            self.assertFalse(f1.exists())
            self.assertFalse(f2.exists())
            self.assertTrue((source / "01_Drums.wav").exists())
            self.assertTrue((source / "02_Bass.wav").exists())

    def test_process_copy_to_dest(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            source = root / "source"
            dest = root / "dest"
            source.mkdir()

            f1 = source / "Song (Piano)_1.wav"
            f1.touch()

            process(source, dest_dir=dest, dry_run=False)

            # Original should still exist
            self.assertTrue(f1.exists())
            # Copied target should exist
            self.assertTrue((dest / "03_Piano.wav").exists())

    def test_process_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            source = Path(tmp_dir)
            f1 = source / "Song (Guitar)_1.wav"
            f1.touch()

            process(source, dest_dir=None, dry_run=True)

            # File should not be renamed
            self.assertTrue(f1.exists())
            self.assertFalse((source / "04_Guitar.wav").exists())


if __name__ == "__main__":
    unittest.main()
