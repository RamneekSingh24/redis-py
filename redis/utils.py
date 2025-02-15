from contextlib import contextmanager
from typing import Any, Dict, Mapping, Union

try:
    import hiredis  # noqa

    # Only support Hiredis >= 1.0:
    HIREDIS_AVAILABLE = not hiredis.__version__.startswith("0.")
except ImportError:
    HIREDIS_AVAILABLE = False

try:
    import cryptography  # noqa

    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False


def from_url(url, **kwargs):
    """
    Returns an active Redis client generated from the given database URL.

    Will attempt to extract the database id from the path url fragment, if
    none is provided.
    """
    from redis.client import Redis

    return Redis.from_url(url, **kwargs)


@contextmanager
def pipeline(redis_obj):
    p = redis_obj.pipeline()
    yield p
    p.execute()


def str_if_bytes(value: Union[str, bytes]) -> str:
    return (
        value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value
    )


def safe_str(value):
    return str(str_if_bytes(value))


def dict_merge(*dicts: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Merge all provided dicts into 1 dict.
    *dicts : `dict`
        dictionaries to merge
    """
    merged = {}

    for d in dicts:
        merged.update(d)

    return merged


def list_keys_to_dict(key_list, callback):
    return dict.fromkeys(key_list, callback)


def merge_result(command, res):
    """
    Merge all items in `res` into a list.

    This command is used when sending a command to multiple nodes
    and the result from each node should be merged into a single list.

    res : 'dict'
    """
    result = set()

    for v in res.values():
        for value in v:
            result.add(value)

    return list(result)
