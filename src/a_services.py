"""
Async Services to provide additional helpers to the main app
"""
import anyio


async def save_file(filepath: str, content: bytes) -> None:
    """
    Writting file to disk.
    :param filepath: str the path to save the file to
    :param content: bytes content of the file
    :return: None
    """
    async with await anyio.open_file(filepath, 'wb+') as to_file:
        await to_file.write(content)
        await to_file.flush()