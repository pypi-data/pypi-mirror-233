"""Miscellaneous functions to support for Battle.net

Functions:
    currency_convertor(value)
    slugify(value)
    localize(locale)
    api_host(region_tag)
    auth_host(region_tag)
    render_host(region_tag)

Misc Variables:
    WOW_CLASSICS


Misc Variables:
    __version__
    __author__

Author: David "Gahd" Couples
License: GPL v3
Copyright: February 24, 2022
"""
from typing import Tuple, Optional, Union
from battlenet_client.exceptions import BNetValueError


__version__ = '1.0.0'
__author__ = 'David \'Gahd\' Couples'


def currency_convertor(value: int) -> Tuple[int, int, int]:
    """Returns the value into gold, silver and copper

    Args:
        value (int): the value to be converted

    Returns:
        tuple: gold (int), silver (int) and copper (int)
    """
    value = int(value)

    if value < 0:
        raise BNetValueError("Value cannot be negative")

    return value // 10000, (value % 10000) // 100, value % 100


def slugify(value: Union[str, int]) -> Union[str, int]:
    """Returns value as a slug

    Args:
        value (str): the string to be converted into a slug

    Returns:
        str: the slug
    """
    if isinstance(value, int):
        return value

    return value.lower().replace("'", "").replace(" ", "-")


def localize(locale: Optional[str] = None) -> Union[None, str]:
    """Returns the standardized locale

    Args:
        locale (str): the locality to be standardized

    Returns:
        str: the locale in the format of "<language>_<COUNTRY>"

    Raise:
        TypeError: when locale is not a string
        ValueError: when the lang and country are not in the given lists
    """
    if locale is None:
        return None

    if not isinstance(locale, str):
        raise BNetValueError("Locale must be a string")

    languages = ("en", "es", "pt", "fr", "ru", "de", "it", "ko", "zh")
    if locale[:2].lower() not in languages:
        raise BNetValueError("Invalid language")

    countries = ("us", "mx", "br", "gb", "es", "fr", "ru", "de", "pt", "it", "kr", "tw", "cn")
    if locale[-2:].lower() not in countries:
        raise BNetValueError("Invalid country")

    return f"{locale[:2].lower()}_{locale[-2:].upper()}"


def api_host(region_tag: str) -> str:
    """Returns the API endpoint hostname and protocol

    Args:
        region_tag (str): the region abbreviation

    Returns:
        str: The API endpoint hostname and protocol
    """
    if region_tag.lower() == "cn":
        return "https://gateway.battlenet.com.cn"

    return f"https://{region_tag.lower()}.api.blizzard.com"


def auth_host(region_tag: str):
    """Returns the authorization endpoint hostname and protocol

    Args:
        region_tag (str): the region abbreviation

    Returns:
        str: The authorization endpoint hostname and protocol
    """
    if region_tag.lower() == "cn":
        return "https://www.battlenet.com.cn"

    if region_tag.lower() in ("kr", "tw"):
        return "https://apac.battle.net"

    return f"https://{region_tag.lower()}.battle.net"


def render_host(region_tag: str):
    """Returns the render endpoint hostname and protocol

    Args:
        region_tag (str): the region abbreviation

    Returns:
        str: The render endpoint hostname and protocol
    """
    if region_tag.lower() == "cn":
        return "https://render.worldofwarcraft.com.cn"

    return f"https://render-{region_tag.lower()}.worldofwarcraft.com"
