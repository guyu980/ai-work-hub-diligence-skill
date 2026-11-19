import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


SCRIPTS = Path(__file__).resolve().parents[1] / "ai-work-hub-diligence" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import check_install


class ProjectContinuityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.active = self.root / "项目" / "Example"
        self.archived = self.active.parent / "归档" / "Example"

    def run_cli(self, script, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / script), "--workspace-root", str(self.root), *args],
            text=True, capture_output=True,
        )

    def historical(self, outcome, *extra):
        return self.run_cli(
            "init_historical_review.py", "--project-name", "Example",
            "--sector", "Example sector", "--outcome", outcome, *extra,
        )

    def test_preserve_existing_judgment_when_adding_historical_state(self):
        output = self.active / "输出文档"
        output.mkdir(parents=True)
        note = output / "Example_项目判断与todo.md"
        note.write_bytes(b"existing investment memo")
        result = self.historical("invested")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(note.read_bytes(), b"existing investment memo")
        state = json.loads((output / "Example_项目状态.json").read_text())
        self.assertEqual(state["historical_outcome"], "invested")
        self.assertEqual(state["process_stage"], "monitoring")

    def test_reopen_uses_existing_archive_and_new_history_gets_its_template(self):
        first = self.historical("pass")
        self.assertEqual(first.returncode, 0, first.stderr)
        note = self.archived / "输出文档" / "Example_项目判断与todo.md"
        self.assertIn("当时的信息集", note.read_text())
        for result in (
            self.historical("pass", "--reopen"),
            self.run_cli("init_project_state.py", "--project-name", "Example", "--sector", "test"),
        ):
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(str(self.archived), result.stderr)
        self.assertFalse(self.active.exists())

    def test_audit_rejects_two_states_for_one_company(self):
        result = self.historical("pass")
        self.assertEqual(result.returncode, 0, result.stderr)
        shutil.copytree(self.archived, self.active)
        duplicate = self.active / "输出文档" / "Example_项目状态.json"
        state = json.loads(duplicate.read_text())
        state.update(project_status="active", process_stage="screening",
                     running_judgment_path="项目/Example/输出文档/Example_项目判断与todo.md")
        duplicate.write_text(json.dumps(state))
        result = self.run_cli("audit_workspace.py")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate project state for Example", result.stdout)

    def test_blocked_launcher_stops_before_fetch(self):
        launcher = self.root / ".tools" / "lark-workhub"
        launcher.parent.mkdir()
        launcher.touch(mode=0o755)
        results = []
        with mock.patch.object(check_install, "run_command", return_value=(77, "storage blocked")) as run:
            check_install.check_feishu(results, self.root, True, "https://example.test/doc")
        run.assert_called_once()
        self.assertEqual(run.call_args.args[0], [str(launcher), "auth", "status", "--verify"])
        self.assertEqual(results[-1].status, "fail")

    def test_workspace_without_launcher_uses_its_local_cli(self):
        cli = self.root / ".tools" / "node_modules" / ".bin" / "lark-cli"
        cli.parent.mkdir(parents=True)
        cli.touch(mode=0o755)
        with mock.patch.object(check_install, "run_command", return_value=(0, "ok")) as run:
            check_install.check_feishu([], self.root, False, "https://example.test/doc")
        self.assertEqual(run.call_args.args[0][0], str(cli))
        self.assertEqual(run.call_args.kwargs["env"]["LARKSUITE_CLI_CONFIG_DIR"],
                         str(self.root / ".home" / ".lark-cli"))
