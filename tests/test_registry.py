import importlib.util
from pathlib import Path
import tempfile
import unittest


PATH = Path(__file__).resolve().parents[1] / "scripts/build_registry.py"
SPEC = importlib.util.spec_from_file_location("registry_builder", PATH)
BUILD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILD)


class RegistryMetadataTests(unittest.TestCase):
    def parse(self, description):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "SKILL.md"
            p.write_text("---\nname: demo\ndescription: " + description + "\n---\nBody\n")
            return BUILD.metadata(p)["description"]

    def test_reads_folded_descriptions_from_new_imports(self):
        self.assertEqual(self.parse(">-\n  First line\n  second line"), "First line second line")

    def test_reads_single_quoted_yaml_escapes(self):
        self.assertEqual(self.parse("'The user''s idea'"), "The user's idea")

    def test_reads_json_quoted_description(self):
        self.assertEqual(self.parse('"Create a new idea"'), "Create a new idea")


if __name__ == "__main__":
    unittest.main()
