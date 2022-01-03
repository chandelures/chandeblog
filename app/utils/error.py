from typing import Tuple


def page_not_found(error) -> Tuple[dict, int]:
    return {"message": "This url does not found on the server"}, 404


def invalid_api_usage(message: str, status_code: int) -> Tuple[dict, int]:
    return {"message": message}, status_code
