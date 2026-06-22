"""Internacionalización de la UI."""

from __future__ import annotations

from typing import Any

import streamlit as st

from ui.i18n.manager import DEFAULT_LANGUAGE, I18nManager

_SESSION_I18N_KEY = "ia_core_i18n"
_SESSION_LANG_KEY = "ia_core_lang"


def get_i18n() -> I18nManager:
    """Obtiene el gestor i18n de la sesión (persiste entre refrescos)."""
    if _SESSION_I18N_KEY not in st.session_state:
        manager = I18nManager()
        lang = st.session_state.get(_SESSION_LANG_KEY, DEFAULT_LANGUAGE)
        manager.load_language(lang)
        st.session_state[_SESSION_I18N_KEY] = manager

    manager: I18nManager = st.session_state[_SESSION_I18N_KEY]
    lang = st.session_state.get(_SESSION_LANG_KEY, manager.current_language)
    if lang != manager.current_language:
        manager.load_language(lang)
    return manager


def set_language(lang_code: str) -> None:
    st.session_state[_SESSION_LANG_KEY] = lang_code
    get_i18n().load_language(lang_code)


def t(key: str, **kwargs: Any) -> str:
    """Atajo de traducción."""
    return get_i18n().translate(key, **kwargs)


__all__ = ["I18nManager", "get_i18n", "set_language", "t", "DEFAULT_LANGUAGE"]
