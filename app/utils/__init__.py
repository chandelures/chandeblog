def slugify(s: str) -> str:
    return s.replace(" ", "-")


def allow_avatar_file(filename) -> bool:
    return "." in filename and \
        filename.rsplit('.', 1)[1].lower() in ["png", "jpg", "jpeg"]
