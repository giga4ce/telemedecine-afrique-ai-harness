import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HARNESS_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = HARNESS_ROOT / "scripts" / "install-context"


class InstallContextTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.product = self.root / "product"
        self.create_product_fixture(self.product)

    def tearDown(self):
        self.tmp.cleanup()

    def run_cmd(self, *args, cwd=HARNESS_ROOT, check=False):
        result = subprocess.run(
            [str(SCRIPT), *args],
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if check and result.returncode != 0:
            self.fail(
                f"command failed with {result.returncode}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            )
        return result

    def base_args(self, llm="codex"):
        return [
            "--llm",
            llm,
            "--profile",
            "telemedecine-afrique",
            "--target",
            str(self.product),
        ]

    def create_product_fixture(self, root):
        required_files = [
            "README.md",
            "docs/README.md",
            "docs/poc/scope.md",
            "docs/poc/architecture.md",
            "docs/product/vision.md",
            "docs/product/roadmap.md",
            "docs/product/glossary.md",
            "docs/domain/legal-reserves-by-country.md",
            "docs/target-platform/ai-functional-agents/README.md",
            "data/README.md",
        ]
        (root / ".git").mkdir(parents=True)
        for relative in required_files:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# {relative}\n", encoding="utf-8")

    def test_codex_installation_creates_manifest(self):
        result = self.run_cmd(*self.base_args("codex"), check=True)

        self.assertIn("CREATE AGENTS.md", result.stdout)
        self.assertTrue((self.product / "AGENTS.md").is_file())
        self.assertTrue((self.product / ".codex/context/reading-order.md").is_file())
        manifest_path = self.product / ".codex/harness-manifest.json"
        self.assertTrue(manifest_path.is_file())
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual("telemedecine-afrique", manifest["profile"])
        self.assertEqual("codex", manifest["llm"])
        self.assertIn("AGENTS.md", manifest["files"])

    def test_codex_agents_references_installed_runtime_paths(self):
        self.run_cmd(*self.base_args("codex"), check=True)

        content = (self.product / "AGENTS.md").read_text(encoding="utf-8")

        self.assertNotIn("profiles/telemedecine-afrique/", content)
        self.assertNotIn("llms/codex/", content)
        self.assertNotIn("telemedecine-afrique-ai-harness/", content)
        self.assertIn(".codex/context/project-rules.md", content)
        self.assertIn(".codex/context/poc-boundaries.md", content)
        self.assertIn(".codex/skills/", content)
        self.assertIn("docs/poc/scope.md", content)

    def test_idempotence_second_install_is_noop(self):
        self.run_cmd(*self.base_args("codex"), check=True)
        before = snapshot(self.product)

        result = self.run_cmd(*self.base_args("codex"), check=True)

        self.assertIn("Context already up to date.", result.stdout)
        self.assertEqual(before, snapshot(self.product))

    def test_local_modification_refuses_install(self):
        self.run_cmd(*self.base_args("codex"), check=True)
        (self.product / "AGENTS.md").write_text("manual edit\n", encoding="utf-8")

        result = self.run_cmd(*self.base_args("codex"))

        self.assertEqual(3, result.returncode)
        self.assertIn("CONFLICT: AGENTS.md was modified locally.", result.stdout + result.stderr)

    def test_force_replaces_modified_file_and_creates_backup(self):
        self.run_cmd(*self.base_args("codex"), check=True)
        expected = (self.product / "AGENTS.md").read_text(encoding="utf-8")
        (self.product / "AGENTS.md").write_text("manual edit\n", encoding="utf-8")

        result = self.run_cmd(*self.base_args("codex"), "--force", check=True)

        self.assertIn("BACKUP AGENTS.md", result.stdout)
        self.assertEqual(expected, (self.product / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertTrue((self.product / ".codex/.harness-backups/AGENTS.md.bak").is_file())

    def test_check_exit_codes(self):
        missing = self.run_cmd(*self.base_args("codex"), "--check")
        self.assertEqual(2, missing.returncode)

        self.run_cmd(*self.base_args("codex"), check=True)
        valid = self.run_cmd(*self.base_args("codex"), "--check")
        self.assertEqual(0, valid.returncode)

        (self.product / ".codex/context/workflow.md").write_text("stale\n", encoding="utf-8")
        conflict = self.run_cmd(*self.base_args("codex"), "--check")
        self.assertEqual(3, conflict.returncode)

    def test_dry_run_does_not_modify_target(self):
        before = snapshot(self.product)

        result = self.run_cmd(*self.base_args("codex"), "--dry-run", check=True)

        self.assertIn("CREATE AGENTS.md", result.stdout)
        self.assertEqual(before, snapshot(self.product))

    def test_claude_installation_creates_context_and_agents(self):
        result = self.run_cmd(*self.base_args("claude"), check=True)

        self.assertIn("CREATE CLAUDE.md", result.stdout)
        self.assertTrue((self.product / "CLAUDE.md").is_file())
        self.assertTrue((self.product / ".claude/context/project-rules.md").is_file())
        self.assertTrue((self.product / ".claude/agents/devops-infra.md").is_file())
        self.assertFalse((self.product / ".claude/skills/conditional").exists())

    def test_sensitive_source_is_refused(self):
        temp_harness = self.root / "harness-copy"
        shutil.copytree(
            HARNESS_ROOT,
            temp_harness,
            ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"),
        )
        sensitive_skill = temp_harness / "skills/common/secret-token"
        sensitive_skill.mkdir(parents=True)
        (sensitive_skill / "SKILL.md").write_text("secret fixture\n", encoding="utf-8")
        skills_yaml = temp_harness / "profiles/telemedecine-afrique/skills.yaml"
        text = skills_yaml.read_text(encoding="utf-8")
        text = text.replace(
            "    - skills/common/architecture-review\n",
            "    - skills/common/architecture-review\n    - skills/common/secret-token\n",
        )
        skills_yaml.write_text(text, encoding="utf-8")
        temp_script = temp_harness / "scripts/install-context"

        result = subprocess.run(
            [
                str(temp_script),
                *self.base_args("codex"),
            ],
            cwd=temp_harness,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.assertEqual(1, result.returncode)
        self.assertIn("sensitive source refused", result.stderr)


def snapshot(root):
    files = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            files[path.relative_to(root).as_posix()] = path.read_bytes()
    return files


if __name__ == "__main__":
    unittest.main()
