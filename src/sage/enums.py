import enum


__all__ = ("ProgrammingLanguage", "LanguageCode")


class ProgrammingLanguage(str, enum.Enum):
    """Supported programming languages."""

    python = "python"
    text = "text-only"
    other = "other"


class LanguageCode(str, enum.Enum):
    """Supported languages for i18n."""

    bg = "bg"
    cs = "cs"
    da = "da"
    de = "de"
    el = "el"
    en_GB = "en-GB"
    en_US = "en-US"
    es_ES = "es-ES"
    fi = "fi"
    fr = "fr"
    hi = "hi"
    hr = "hr"
    it = "it"
    ja = "ja"
    ko = "ko"
    lt = "lt"
    hu = "hu"
    nl = "nl"
    no = "no"
    pl = "pl"
    pt_BR = "pt-BR"
    ro = "ro"
    ru = "ru"
    sv_SE = "sv-SE"
    th = "th"
    tr = "tr"
    uk = "uk"
    vi = "vi"
    zh_CN = "zh-CN"
    zh_TW = "zh-TW"
