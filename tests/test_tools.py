from tools.manager import ToolManager


def _write_tool(path, name: str, body: str) -> None:
    path.write_text(
        f'TOOL_NAME = "{name}"\n\n{body}\n',
        encoding="utf-8",
    )


def test_discovers_and_calls_tools(tmp_path):
    modules_dir = tmp_path / "modules"
    modules_dir.mkdir()
    _write_tool(
        modules_dir / "greet.py",
        "greet",
        'def execute(name="world"):\n    return f"hi {name}"',
    )

    manager = ToolManager(modules_dir=modules_dir)
    manager.start()

    assert "greet" in manager.list_names()
    assert manager.call("greet", "alice") == "hi alice"
    manager.stop()


def test_skips_broken_module(tmp_path):
    modules_dir = tmp_path / "modules"
    modules_dir.mkdir()
    _write_tool(
        modules_dir / "ok.py",
        "ok",
        "def execute():\n    return True",
    )
    (modules_dir / "broken.py").write_text("raise RuntimeError('boom')", encoding="utf-8")

    manager = ToolManager(modules_dir=modules_dir)
    count = manager.load_modules()

    assert count == 1
    assert manager.call("ok") is True


def test_skips_invalid_module(tmp_path):
    modules_dir = tmp_path / "modules"
    modules_dir.mkdir()
    (modules_dir / "no_name.py").write_text("def execute(): pass\n", encoding="utf-8")
    _write_tool(
        modules_dir / "valid.py",
        "valid",
        "def execute():\n    return 1",
    )

    manager = ToolManager(modules_dir=modules_dir)
    assert manager.load_modules() == 1


def test_builtin_modules_load(tmp_path):
    import config

    manager = ToolManager(modules_dir=config.TOOLS_MODULES_DIR)
    manager.start()

    assert "echo" in manager.list_names()
    assert manager.call("echo", text="hola")["text"] == "hola"
    assert manager.call("uppercase", text="hola") == "HOLA"
    manager.stop()
