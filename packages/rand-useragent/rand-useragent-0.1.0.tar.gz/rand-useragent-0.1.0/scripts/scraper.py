from __future__ import annotations

import json
import os

import anyio
import bs4
import httpx
import json5
from ua_parser.user_agent_parser import Parse as ua_parser


def format_version(major: str, minor: str, patch: str) -> str:
    return ".".join(filter(lambda x: x is not None, (major, minor, patch)))


async def get_user_agents(
    url: str, headers: dict = None
) -> list[dict[str, str | float]]:
    agents = []
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, headers=headers)
        except httpx.HTTPError:
            exit()
        soup = bs4.BeautifulSoup(resp.content, "html.parser")
        data = soup.select("textarea.get-the-list")[1].text
        for agent in json5.loads(data):
            info = ua_parser(agent["useragent"])
            agents.append(
                {
                    "string": info["string"],
                    "os": info["os"]["family"].lower(),
                    "browser": info["user_agent"]["family"].lower(),
                    "version": format_version(
                        info["user_agent"]["major"],
                        info["user_agent"]["minor"],
                        info["user_agent"]["patch"],
                    ),
                    "percent": float(agent["percent"][:-1]),
                }
            )
        await resp.aclose()
    return agents


async def dump_user_agents(file: str, url: str, headers: dict = None) -> None:
    os.makedirs(
        os.path.join(os.path.realpath(os.curdir), os.path.dirname(file)), exist_ok=True
    )
    async with (await anyio.open_file(file, mode="w")) as fileobj:
        for agent in await get_user_agents(url, headers=headers):
            await fileobj.write(json.dumps(agent))
            await fileobj.write("\n")


if __name__ == "__main__":
    anyio.run(
        dump_user_agents,
        "website/cache.jsonl",
        "https://webcache.googleusercontent.com/search?q=cache:https%3A%2F%2Ftechblog.willshouse.com%2F2012%2F01%2F03%2Fmost-common-user-agents%2F",
        {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"  # noqa
        },
    )
