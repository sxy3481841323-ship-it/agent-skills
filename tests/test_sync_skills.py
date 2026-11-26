import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


PATH = Path(__file__).resolve().parents[1] / "scripts" / "sync_skills.py"
SPEC = importlib.util.spec_from_file_location("shared_skill_sync", PATH)
SYNC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SYNC)


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "source" / "example"
        self.source.mkdir(parents=True)
        (self.source / "SKILL.md").write_text('---\nname: example\ndescription: "An example skill"\n---\nUse the example.\n')
        (self.source / "LICENSE").write_text("Example license\n")
        (self.source / "references").mkdir()
        (self.source / "references" / "detail.md").write_text("Nested detail\n")
        (self.source / "sample.bin").write_bytes(bytes([0, 1, 128, 255]))
        self.target = self.root / "global"

    def tearDown(self):
        self.temp.cleanup()

    def test_installs_complete_binary_and_reference_files(self):
        state, name = SYNC.sync_one(self.source, self.target)
        self.assertEqual((state, name), ("installed", "example"))
        self.assertEqual((self.target / name / "sample.bin").read_bytes(), bytes([0, 1, 128, 255]))
        self.assertEqual((self.target / name / "references/detail.md").read_text(), "Nested detail\n")
        self.assertEqual((self.target / name / "LICENSE").read_text(), "Example license\n")

    def test_dry_run_writes_nothing(self):
        self.assertEqual(SYNC.sync_one(self.source, self.target, dry_run=True)[0], "would-install")
        self.assertFalse(self.target.exists())

    def test_repeat_install_is_idempotent(self):
        SYNC.sync_one(self.source, self.target)
        self.assertEqual(SYNC.sync_one(self.source, self.target)[0], "unchanged")

    def test_declared_name_detects_existing_renamed_directory(self):
        SYNC.sync_one(self.source, self.target)
        (self.target / "example").rename(self.target / "skill-existing-id")
        self.assertEqual(SYNC.sync_one(self.source, self.target)[0], "unchanged")
        self.assertFalse((self.target / "example").exists())

    def test_unmanaged_existing_skill_is_never_overwritten(self):
        SYNC.copy_complete(self.source, self.target / "example")
        local = self.target / "example" / "references/detail.md"
        local.write_text("Someone else's changes")
        self.assertEqual(SYNC.sync_one(self.source, self.target, update=True)[0], "conflict")
        self.assertEqual(local.read_text(), "Someone else's changes")

    def test_update_replaces_only_unedited_managed_installation(self):
        SYNC.sync_one(self.source, self.target)
        (self.source / "references/detail.md").write_text("Updated upstream")
        self.assertEqual(SYNC.sync_one(self.source, self.target, update=True)[0], "updated")
        self.assertEqual((self.target / "example/references/detail.md").read_text(), "Updated upstream")

    def test_update_keeps_local_agent_edits(self):
        SYNC.sync_one(self.source, self.target)
        local = self.target / "example/references/detail.md"
        local.write_text("Local agent edit")
        (self.source / "references/detail.md").write_text("Upstream change")
        self.assertEqual(SYNC.sync_one(self.source, self.target, update=True)[0], "conflict")
        self.assertEqual(local.read_text(), "Local agent edit")

    def test_import_filters_environment_and_version_control_files(self):
        (self.source / ".env").write_text("LOCAL_SECRET=example")
        (self.source / ".git").mkdir()
        (self.source / ".git/config").write_text("local settings")
        SYNC.sync_one(self.source, self.target, importing=True)
        self.assertFalse((self.target / "example/.env").exists())
        self.assertFalse((self.target / "example/.git").exists())
        self.assertFalse((self.target / "example/.shared-skill.json").exists())

    def test_import_rejects_credential_like_content(self):
        (self.source / "settings.txt").write_text("TOKEN=" + "ghp_" + "X" * 40)
        with self.assertRaisesRegex(ValueError, "Possible credential"):
            SYNC.check_secrets(self.source)

    def test_symlink_cannot_copy_unrelated_files(self):
        outside = self.root / "outside.txt"
        outside.write_text("Do not copy")
        (self.source / "outside-link").symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "Symlinks"):
            SYNC.sync_one(self.source, self.target)
        self.assertFalse(self.target.exists())

    def test_parent_rule_preserves_existing_text_without_duplicate_blocks(self):
        parent = self.root / "workspace"
        parent.mkdir()
        (parent / "AGENTS.md").write_text("Existing workspace rule\n")
        SYNC.install_workspace_rule(parent)
        SYNC.install_workspace_rule(parent)
        result = (parent / "AGENTS.md").read_text()
        self.assertTrue(result.startswith("Existing workspace rule"))
        self.assertEqual(result.count("<!-- shared-agent-skills:start -->"), 1)


if __name__ == "__main__":
    unittest.main()
