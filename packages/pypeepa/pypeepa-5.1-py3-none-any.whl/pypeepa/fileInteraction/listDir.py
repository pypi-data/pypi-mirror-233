import os
from typing import List, Optional


def listDir(dir: str, get: Optional[str] = None) -> List[str]:
    content = []

    for content_path in os.listdir(dir):
        full_path = os.path.join(dir, content_path)

        if get is None:
            content.append(content_path)
        elif get == "files" and os.path.isfile(full_path):
            content.append(content_path)
        elif get == "folders" and os.path.isdir(full_path):
            content.append(content_path)

    return content
