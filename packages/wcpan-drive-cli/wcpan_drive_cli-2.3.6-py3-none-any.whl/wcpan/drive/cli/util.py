import asyncio
from concurrent.futures import Executor
import datetime
import functools
import json
from logging import getLogger
import math
import mimetypes
import pathlib
import sys
from typing import AsyncGenerator, Any

from PIL import Image
from wcpan.drive.core.abc import Hasher
from wcpan.drive.core.drive import Drive
from wcpan.drive.core.types import Node, ChangeDict, MediaInfo
from wcpan.drive.core.exceptions import UnauthorizedError
import yaml


async def get_node_by_id_or_path(drive: Drive, id_or_path: str) -> Node:
    if id_or_path[0] == "/":
        node = await drive.get_node_by_path(id_or_path)
    else:
        node = await drive.get_node_by_id(id_or_path)
    return node


async def traverse_node(drive: Drive, node: Node, level: int) -> None:
    if node.is_root:
        print_node("/", level)
    elif level == 0:
        top_path = await drive.get_path(node)
        print_node(top_path, level)
    else:
        print_node(node.name, level)

    if node.is_folder:
        children = await drive.get_children_by_id(node.id_)
        for child in children:
            await traverse_node(drive, child, level + 1)


async def trash_node(drive: Drive, id_or_path: str) -> str | None:
    """
    :returns: None if succeed, id_or_path if failed
    """
    node = await get_node_by_id_or_path(drive, id_or_path)
    if not node:
        return id_or_path
    try:
        await drive.trash_node(node)
    except Exception as e:
        getLogger(__name__).exception("trash failed")
        return id_or_path
    return None


async def wait_for_value(k, v) -> tuple[str, Any]:
    return k, await v


def get_hash(local_path: pathlib.Path, hasher: Hasher) -> str:
    CHUNK_SIZE = 64 * 1024
    with open(local_path, "rb") as fin:
        while True:
            chunk = fin.read(CHUNK_SIZE)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


async def chunks_of(
    ag: AsyncGenerator[ChangeDict, None],
    size: int,
) -> AsyncGenerator[list[ChangeDict], None]:
    chunk = []
    async for item in ag:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def print_node(name: str, level: int) -> None:
    level = " " * level
    print(level + name)


def print_as_yaml(data: Any) -> None:
    yaml.safe_dump(
        data,
        stream=sys.stdout,
        allow_unicode=True,
        encoding=sys.stdout.encoding,
        default_flow_style=False,
    )


def print_id_node_dict(data: Any) -> None:
    pairs = sorted(data.items(), key=lambda _: _[1])
    for id_, path in pairs:
        print(f"{id_}: {path}")


async def get_media_info(local_path: pathlib.Path) -> MediaInfo:
    type_, dummy_ext = mimetypes.guess_type(local_path)
    if not type_:
        return None

    if type_.startswith("image/"):
        return get_image_info(local_path)

    if type_.startswith("video/"):
        return await get_video_info(local_path)

    return None


def get_image_info(local_path: pathlib.Path) -> MediaInfo:
    image = Image.open(str(local_path))
    width, height = image.size
    return MediaInfo.image(width=width, height=height)


async def get_video_info(local_path: pathlib.Path) -> MediaInfo:
    cmd = (
        "ffprobe",
        "-v",
        "error",
        "-show_format",
        "-show_streams",
        "-select_streams",
        "v:0",
        "-print_format",
        "json",
        "-i",
        str(local_path),
    )
    cp = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, dummy_err = await cp.communicate()
    data = json.loads(out)
    format_ = data["format"]
    ms_duration = math.floor(float(format_["duration"]) * 1000)
    video = data["streams"][0]
    width = video["width"]
    height = video["height"]
    return MediaInfo.video(width=width, height=height, ms_duration=ms_duration)


async def get_usage(drive: Drive, node: Node) -> int:
    if not node.is_folder:
        return node.size

    rv = 0
    async for dummy_root, dummy_folders, files in drive.walk(node):
        rv += sum((_.size for _ in files))

    return rv


def get_utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def humanize(n: int) -> str:
    UNIT_LIST = ["", "KiB", "MiB", "GiB", "TiB", "PiB"]
    e = 0
    while n >= 1024:
        n = n // 1024
        e += 1
    return f"{n}{UNIT_LIST[e]}"


def require_authorized(fn):
    @functools.wraps(fn)
    async def action(*args, **kwargs):
        try:
            return await fn(*args, **kwargs)
        except UnauthorizedError:
            print("not authorized")
            return 1

    return action
