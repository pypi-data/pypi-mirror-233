import json
import logging
import random
import sys
import typing as t

if sys.version_info >= (3, 10):
    import importlib.resources as ilr
else:
    import importlib_resources as ilr  # pragma: nocover

logger = logging.getLogger(__package__)


def load_user_agents() -> list[dict[str, t.Any]]:
    try:
        json_lines = (
            ilr.files("rand_useragent.data").joinpath("browsers.jsonl").read_text()
        )
        data = [json.loads(line) for line in json_lines.splitlines()]
    except Exception as exc:  # pragma: nocover
        data = []
        logger.warning(
            "Unable to find local data/json file or could not parse the contents using importlib-resources.",  # noqa
            exc_info=exc,
        )
    if not data:
        raise ValueError("Data list is empty", data)  # pragma: nocover
    return data


def randua(
    browsers: t.Union[list, str] = ["chrome", "safari", "edge"],
    os: t.Union[list, str] = ["windows", "linux", "mac os x"],
    min_percent: float = 0.0,
    fallback: str = "",
) -> str:
    assert isinstance(browsers, (list, str)), "browsers must be list or string"
    assert isinstance(os, (list, str)), "OS must be list or string"
    assert isinstance(min_percent, float), "Minimum usage percentage must be float"
    assert isinstance(fallback, str), "fallback must be string"
    browsers = [browsers] if isinstance(browsers, str) else browsers
    os = [os] if isinstance(os, str) else os
    fallback = (
        fallback
        or "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
    )
    try:
        filtered_browsers = list(
            filter(
                lambda x: x["browser"] in browsers
                and x["os"] in os
                and x["percent"] >= min_percent,
                load_user_agents(),
            )
        )
        return random.choice(filtered_browsers).get("string")
    except (KeyError, IndexError):
        m = (
            "browser"
            + ("s" if len(browsers) > 1 else "")
            + f": [{', '.join(browsers)}]"
        )
        if not fallback:
            raise ValueError(f"Error occurred while getting {m}")  # pragma: nocover
        else:
            logger.warning(
                f"Error occurred while getting {m}, but was suppressed with fallback."
            )
        return fallback
