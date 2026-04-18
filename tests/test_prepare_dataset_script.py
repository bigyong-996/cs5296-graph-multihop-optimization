from pathlib import Path
import subprocess
import sys


def test_prepare_dataset_writes_closure_file(tmp_path: Path) -> None:
    output_dir = tmp_path / "facebook_tiny"
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/prepare_dataset.py",
            "--input",
            "tests/fixtures/raw/facebook_tiny.txt",
            "--dataset-name",
            "facebook_tiny",
            "--symmetrize",
            "--output-dir",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert (output_dir / "nodes.csv").exists()
    assert (output_dir / "edges.csv").exists()
    assert (output_dir / "metadata.json").exists()
    assert (output_dir / "closure_3.csv").exists()
