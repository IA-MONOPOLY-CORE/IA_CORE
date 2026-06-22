import json

from memory.manager import MemoryManager


def test_load_creates_file_when_missing(tmp_path):
    state_file = tmp_path / "state.json"
    memory = MemoryManager(state_path=state_file)

    memory.load()

    assert state_file.exists()
    assert memory.get("x") is None


def test_save_and_load_roundtrip(tmp_path):
    state_file = tmp_path / "state.json"
    memory = MemoryManager(state_path=state_file)

    memory.set("user", "alice")
    memory.set("count", 3)
    memory.save()

    other = MemoryManager(state_path=state_file)
    other.load()

    assert other.get("user") == "alice"
    assert other.get("count") == 3


def test_persists_between_sessions(tmp_path):
    state_file = tmp_path / "state.json"

    first = MemoryManager(state_path=state_file)
    first.start()
    first.set("session", "one")
    first.stop()

    second = MemoryManager(state_path=state_file)
    second.start()

    assert second.get("session") == "one"
    second.stop()


def test_corrupt_file_recovers_safely(tmp_path):
    state_file = tmp_path / "state.json"
    state_file.write_text("{ not valid json", encoding="utf-8")

    memory = MemoryManager(state_path=state_file)
    memory.load()

    assert memory.get("any") is None
    assert state_file.exists()
    payload = json.loads(state_file.read_text(encoding="utf-8"))
    assert payload["version"] == 1
    assert payload["data"] == {}
