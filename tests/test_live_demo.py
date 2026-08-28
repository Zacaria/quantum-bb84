import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LiveDemoSetupTests(unittest.TestCase):
    BINDER_URL = (
        "https://mybinder.org/v2/gh/Zacaria/quantum-bb84/master"
        "?urlpath=tree/demo.ipynb"
    )

    def test_demo_notebook_has_one_clear_control_cell(self):
        notebook = json.loads((ROOT / "demo.ipynb").read_text())
        control_cells = [
            cell
            for cell in notebook["cells"]
            if "demo-controls" in cell.get("metadata", {}).get("tags", [])
        ]

        self.assertEqual(len(control_cells), 1)
        source = "".join(control_cells[0]["source"])
        for setting in (
            "MESSAGE_LENGTH = 12",
            "SIFTING_LENGTH = 12",
            "EVE_RATE = 0",
            'DEMO_MESSAGE = "Hi"',
            "SIFTING_RATE = 100",
            "ENABLE_HASH = False",
            "RANDOM_SEED = 7",
            "DEBUG = False",
            "DEFAULT_TIMES = 100",
        ):
            self.assertIn(setting, source)

    def test_demo_notebook_starts_clean_and_uses_the_controls(self):
        notebook = json.loads((ROOT / "demo.ipynb").read_text())
        code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
        source = "\n".join("".join(cell["source"]) for cell in code_cells)

        self.assertTrue(all(cell.get("execution_count") is None for cell in code_cells))
        self.assertTrue(all(not cell.get("outputs") for cell in code_cells))
        self.assertNotIn("SIFITING_RATE", source)
        self.assertIn("sifting_length = int(len(binary_message) * (SIFTING_RATE / 100))", source)
        self.assertIn("send_secure_message(DEMO_MESSAGE, ENABLE_HASH)", source)
        self.assertIn("seed_simulator=RANDOM_SEED + measurement_number", source)
        self.assertIn("sifting_length = min(sifting_length, len(bob_no_none_pairs))", source)
        self.assertNotIn("import jovian", source)

    def test_binder_environment_pins_the_historical_runtime(self):
        environment = (ROOT / "binder" / "environment.yml").read_text()

        for dependency in (
            "python=3.9",
            "notebook=6.4.12",
            "qiskit==0.37.0",
            "qiskit-aer==0.10.4",
            "qiskit-terra==0.21.0",
        ):
            self.assertIn(dependency, environment)

    def test_just_exposes_start_for_the_demo_notebook(self):
        listing = subprocess.run(
            ["just", "--list"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        justfile = (ROOT / "justfile").read_text()

        self.assertIn("start", listing)
        self.assertIn("demo.ipynb", justfile)
        self.assertIn("requirements.txt", justfile)

    def test_readme_and_pages_link_to_the_live_demo(self):
        self.assertIn(self.BINDER_URL, (ROOT / "README.md").read_text())
        self.assertIn(self.BINDER_URL, (ROOT / "docs" / "index.html").read_text())


if __name__ == "__main__":
    unittest.main()
