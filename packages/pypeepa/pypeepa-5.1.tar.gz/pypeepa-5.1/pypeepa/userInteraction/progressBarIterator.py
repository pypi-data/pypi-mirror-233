from alive_progress import alive_bar
from typing import Iterable, Any, Optional


def progressBarIterator(
    iterable: Iterable[Any],
    iterableLength: Optional[int] = None,
    description: Optional[str] = "Progress",
    **kwargs
):
    if iterableLength == None:
        iterableLength = len(iterable)
    with alive_bar(
        iterableLength, force_tty=True, bar="filling", spinner="waves", **kwargs
    ) as bar:
        bar.title = description
        for item in iterable:
            yield item
            bar()
