"""Test to prevent hardcoded agent config paths (ensure everyone uses config.AGENTS_CONFIG_DIR)."""
import pathlib
from pathlib import Path


def test_no_hardcoded_agent_paths():
    root_dir = Path(__file__).parent.parent

    # Patterns to look for (hardcoded paths instead of using config.AGENTS_CONFIG_DIR)
    forbidden_patterns = [
        'ROOT / "agents" / "config"',
        'Path("agents/config")',
        'Path("agents", "config")',
        '"agents/config"',
    ]

    errors = []

    # Scan only relevant directories to make the test fast
    scan_dirs = [
        root_dir / "agents",
        root_dir / "core",
        root_dir / "providers",
        root_dir / "domains",
        root_dir / "ui",
    ]
    # Also scan root-level .py files
    scan_files = list(root_dir.glob("*.py"))

    # Collect all files to scan
    all_files = []
    for d in scan_dirs:
        if d.exists():
            all_files.extend(d.rglob("*.py"))
    all_files.extend(scan_files)

    for py_file in all_files:
        if "tests" in str(py_file):
            continue
        if "__pycache__" in str(py_file):
            continue
        # Skip config.py since it's where AGENTS_CONFIG_DIR is defined!
        if py_file.name == "config.py":
            continue

        # Try reading the file with multiple encodings
        content = None
        for encoding in ["utf-8", "latin-1", "big5"]:
            try:
                with open(py_file, "r", encoding=encoding) as f:
                    content = f.read()
                break
            except (UnicodeDecodeError, UnicodeError):
                continue
        if content is None:
            continue  # Skip if we can't read it

        lines = content.splitlines()
        for line_num, line in enumerate(lines, 1):
            for pattern in forbidden_patterns:
                if pattern in line:
                    errors.append(
                        f"{py_file}:{line_num}: Found hardcoded path pattern '{pattern}'. Use config.AGENTS_CONFIG_DIR instead!"
                    )

    # If we found any errors, fail the test!
    assert not errors, "Found hardcoded agent config paths:\n" + "\n".join(errors)
