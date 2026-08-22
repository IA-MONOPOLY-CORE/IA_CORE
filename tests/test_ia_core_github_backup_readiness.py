from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
BACKUP_DOC = ROOT / "docs" / "IA_CORE_GITHUB_BACKUP_READY.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_root_readme_exists_and_records_backup_state():
    assert README.exists()
    text = read(README)

    assert "IA_CORE" in text
    assert "8d889369" in text
    assert "PROMPT UI/UX 1.22 - Checkpoint Frontend Incongruence" in text
    assert "no-runtime/no-execution" in text
    assert "No subir secretos" in text
    assert "Restoration And Continuidad" in text
    assert "https://github.com/IA-MONOPOLY-CORE/IA_CORE" in text


def test_backup_document_exists_and_records_continuity():
    assert BACKUP_DOC.exists()
    text = read(BACKUP_DOC)

    assert "8d889369" in text
    assert "https://github.com/IA-MONOPOLY-CORE/IA_CORE" in text
    assert "PROMPT UI/UX 1.22 - Checkpoint Frontend Incongruence" in text
    assert "No usar force push" in text