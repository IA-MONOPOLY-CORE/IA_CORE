"""Fail-closed test boundaries loaded before any repository test module."""

from __future__ import annotations

import ipaddress
import os
import socket
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path


EXTERNAL_TESTS_ENABLED = os.environ.get("IA_CORE_ALLOW_EXTERNAL_TESTS") == "1"
BLOCK_MESSAGE = (
    "IA_CORE_EXTERNAL_NETWORK_BLOCKED: outbound network is disabled by default; "
    "set IA_CORE_ALLOW_EXTERNAL_TESTS=1 for an explicitly authorized integration run"
)


def _host_from_address(address: object) -> str:
    if isinstance(address, tuple) and address:
        return str(address[0])
    return str(address)


def _is_local_host(host: str) -> bool:
    normalized = host.strip().lower().strip("[]")
    if normalized == "localhost":
        return True
    try:
        return ipaddress.ip_address(normalized).is_loopback
    except ValueError:
        return False


if not EXTERNAL_TESTS_ENABLED:

    def _blocked_network(*_args, **_kwargs):
        raise RuntimeError(BLOCK_MESSAGE)


    def _blocked_connect(_self, address):
        host = _host_from_address(address)
        if not _is_local_host(host):
            raise RuntimeError(BLOCK_MESSAGE)
        return _ORIGINAL_SOCKET_CONNECT(_self, address)


    def _blocked_create_connection(address, *args, **kwargs):
        host = _host_from_address(address)
        if not _is_local_host(host):
            raise RuntimeError(BLOCK_MESSAGE)
        return _ORIGINAL_CREATE_CONNECTION(address, *args, **kwargs)


    def _blocked_getaddrinfo(host, *args, **kwargs):
        if not _is_local_host(str(host)):
            raise RuntimeError(BLOCK_MESSAGE)
        return _ORIGINAL_GETADDRINFO(host, *args, **kwargs)


    _ORIGINAL_SOCKET_CONNECT = socket.socket.connect
    _ORIGINAL_CREATE_CONNECTION = socket.create_connection
    _ORIGINAL_GETADDRINFO = socket.getaddrinfo
    socket.socket.connect = _blocked_connect
    socket.create_connection = _blocked_create_connection
    socket.getaddrinfo = _blocked_getaddrinfo
    urllib.request.urlopen = _blocked_network

    try:
        import requests

        requests.sessions.Session.request = _blocked_network
    except ImportError:
        pass


_REPOSITORY_ROOT = Path(__file__).resolve().parent
_TEST_LOG_ROOT = Path(tempfile.mkdtemp(prefix="ia-core-pytest-"))
try:
    import config as _test_config

    _test_config.LOG_DIR = _TEST_LOG_ROOT
except ImportError:
    pass

_PROTECTED_ROOTS = {
    (_REPOSITORY_ROOT / "memory").resolve(),
    (_REPOSITORY_ROOT / "memoria_agentes").resolve(),
    (_REPOSITORY_ROOT / "memoria_vectorial").resolve(),
    (_REPOSITORY_ROOT / "logs").resolve(),
}


def _tracked_paths() -> set[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=_REPOSITORY_ROOT,
        check=True,
        capture_output=True,
    )
    return {
        (_REPOSITORY_ROOT / item.decode("utf-8")).resolve()
        for item in result.stdout.split(b"\0")
        if item
    }


_TRACKED_PATHS = _tracked_paths()


def _resolve_audit_path(value: object) -> Path | None:
    if not isinstance(value, (str, bytes, os.PathLike)):
        return None
    if isinstance(value, bytes):
        value = os.fsdecode(value)
    return Path(value).resolve()


def _inside(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def _write_is_protected(value: object) -> bool:
    path = _resolve_audit_path(value)
    if path is None:
        return False
    return path in _TRACKED_PATHS or any(_inside(path, root) for root in _PROTECTED_ROOTS)


def _audit_test_write(event: str, args: tuple[object, ...]) -> None:
    if event == "open":
        path, mode, flags = args
        writes_requested = isinstance(mode, str) and any(token in mode for token in "wax+")
        if not writes_requested and isinstance(flags, int):
            writes_requested = bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC))
        if writes_requested and _write_is_protected(path):
            raise RuntimeError(
                "IA_CORE_TEST_WRITE_BLOCKED: tracked or product persistence path is "
                "outside the temporary test root"
            )
    elif event in {"os.mkdir", "os.remove", "os.rename", "os.replace", "os.rmdir"}:
        if args and _write_is_protected(args[0]):
            raise RuntimeError(
                "IA_CORE_TEST_WRITE_BLOCKED: tracked or product persistence path is "
                "outside the temporary test root"
            )


sys.addaudithook(_audit_test_write)


def _git_status_without_untracked() -> str:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=_REPOSITORY_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def pytest_sessionstart(session) -> None:
    session.config._ia_core_status_before = _git_status_without_untracked()


def pytest_sessionfinish(session, exitstatus) -> None:
    before = getattr(session.config, "_ia_core_status_before", "")
    after = _git_status_without_untracked()
    if after != before:
        session.config._ia_core_tree_changed = True
        session.exitstatus = 1
        print("IA_CORE_REPOSITORY_TRACKED_STATE_CHANGED_DURING_TESTS")
