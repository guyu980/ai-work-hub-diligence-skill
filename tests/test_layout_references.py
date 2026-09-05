import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "ai-work-hub-diligence/scripts/migrate_project_layout.py"
spec = importlib.util.spec_from_file_location("layout_migration", SCRIPT)
layout = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = layout
spec.loader.exec_module(layout)


class LayoutReferenceTests(unittest.TestCase):
    def test_source_links_move_but_generated_indexes_are_not_edited(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project = root / "项目" / "Example"
            old = project / "输出文档" / "04_正式交付" / "editppt_run"
            old.mkdir(parents=True)
            (old / "result.txt").write_text("original artifact")
            new = project / "工作区" / "editppt_run"
            note = project / "note.md"
            old_relative = old.relative_to(project).as_posix() + "/result.txt"
            note.write_text("[artifact](" + old_relative + ")")
            index = root / "Memory Graph" / "00_索引" / "项目索引.jsonl"
            index.parent.mkdir(parents=True)
            index.write_text(old.as_posix())
            move = layout.Move(old=old, new=new, project_root=project, reason="test")
            layout.apply_moves(root, [project], [move])
            self.assertEqual((new / "result.txt").read_text(), "original artifact")
            self.assertIn("工作区/editppt_run/result.txt", note.read_text())
            self.assertEqual(index.read_text(), old.as_posix())
            self.assertFalse(old.exists())


if __name__ == "__main__":
    unittest.main()
