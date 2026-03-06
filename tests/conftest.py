import keepachangelog


def to_dict_ignore_header(changelog, **kwargs):
    mapping = keepachangelog.to_dict(changelog, **kwargs)
    return dict_ignore_header(mapping) if mapping else {}


def dict_ignore_header(mapping):
    mapping = mapping.copy()
    mapping.pop("header")
    return mapping
