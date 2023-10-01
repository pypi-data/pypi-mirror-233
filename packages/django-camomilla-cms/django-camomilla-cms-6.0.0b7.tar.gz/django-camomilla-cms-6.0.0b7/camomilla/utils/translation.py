import re
from typing import Any, Sequence, Iterator

from django.db.models import Model, Q
from django.utils.translation.trans_real import activate, get_language
from modeltranslation.settings import AVAILABLE_LANGUAGES, DEFAULT_LANGUAGE
from modeltranslation.utils import build_localized_fieldname
from camomilla.settings import BASE_URL


def activate_languages(languages: Sequence[str] = AVAILABLE_LANGUAGES) -> Iterator[str]:
    old = get_language()
    for language in languages:
        activate(language)
        yield language
    activate(old)


def set_nofallbacks(instance: Model, attr: str, value: Any, **kwargs) -> None:
    language = kwargs.pop("language", get_language())
    local_fieldname = build_localized_fieldname(attr, language)
    if hasattr(instance, local_fieldname):
        attr = local_fieldname
    return setattr(instance, attr, value)


def get_nofallbacks(instance: Model, attr: str, *args, **kwargs) -> Any:
    language = kwargs.pop("language", get_language())
    local_fieldname = build_localized_fieldname(attr, language)
    if hasattr(instance, local_fieldname):
        attr = local_fieldname
    return getattr(instance, attr, *args, **kwargs)


def url_lang_decompose(url):
    if BASE_URL and url.startswith(BASE_URL):
        url = url[len(BASE_URL):]
    data = {"url": url, "permalink": url, "language": DEFAULT_LANGUAGE}
    result = re.match(
        f"^\/?({'|'.join(AVAILABLE_LANGUAGES)})?\/(.*)", url
    )  # noqa: W605
    groups = result and result.groups()
    if groups and len(groups) == 2:
        data["language"] = groups[0]
        data["permalink"] = "/%s" % groups[1]
    return data


def get_field_translations(instance: Model, field_name: str, *args, **kwargs):
    return {
        lang: get_nofallbacks(instance, field_name, language=lang, *args, **kwargs)
        for lang in AVAILABLE_LANGUAGES
    }


def lang_fallback_query(**kwargs):
    current_lang = get_language()
    query = Q()
    for lang in AVAILABLE_LANGUAGES:
        query |= Q(**{f"{key}_{lang}": value for key, value in kwargs.items()})
    if current_lang:
        query = query & Q(
            **{f"{key}_{current_lang}__isnull": True for key in kwargs.keys()}
        )
        query |= Q(**{f"{key}_{current_lang}": value for key, value in kwargs.items()})
    return query


def is_translatable(model: Model) -> bool:
    from modeltranslation.translator import translator

    return model in translator.get_registered_models()
