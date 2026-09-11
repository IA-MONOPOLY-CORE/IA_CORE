"""Fail-closed test boundaries loaded before any repository test module."""

from __future__ import annotations

import ipaddress
import os
import socket
import urllib.request


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
