from typing import Tuple


def page_not_found(error) -> Tuple[dict, int]:
    return {"detail": "This url does not found on the server"}, 404
