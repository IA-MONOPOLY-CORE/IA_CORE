from ui.i18n.manager import I18nManager


def test_spanish_default():
    i18n = I18nManager()
    i18n.load_language("es")
    assert i18n.translate("sidebar.connect") == "Conectar supervisor"


def test_english():
    i18n = I18nManager()
    i18n.load_language("en")
    assert i18n.translate("sidebar.connect") == "Connect supervisor"


def test_fallback_to_english_for_missing_key():
    i18n = I18nManager()
    i18n.load_language("es")
    assert i18n.translate("nonexistent.key.xyz") == "nonexistent.key.xyz"


def test_format_kwargs():
    i18n = I18nManager()
    i18n.load_language("es")
    text = i18n.translate("agents.done", ms=42)
    assert "42" in text


def test_available_languages():
    i18n = I18nManager()
    codes = [lang["code"] for lang in i18n.available_languages()]
    assert "es" in codes and "en" in codes
