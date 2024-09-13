import hashlib

from notifypy import Notify

from .gui.props import VIEWPORT_TITLE
from .gui.image import notification_image_path


__all__ = (
    'HASH_MAPPING',
    'hash_data',
    'get_file_data',
    'send_notification'
)


HASH_MAPPING: dict = {
    'MD5': hashlib.md5,
    'SHA1': hashlib.sha1,
    'SHA224': hashlib.sha224,
    'SHA256': hashlib.sha256,
    'SHA384': hashlib.sha384,
    'SHA512': hashlib.sha512
}


def hash_data(data: bytes, hf: list[str]) -> dict:
    """Calculates a hash for a given data with each provided hash-function.
    * Supported function: -> `HASH_MAPPING`

    :param hf: list[str] -> the list of hash-functions names.
    :param data: bytes -> data to process
    :return: dict -> in format: {hf_name: hash_value}
    """
    output = {}
    for name, func in HASH_MAPPING.items():
        if name in hf:
            output.setdefault(name, func(data).hexdigest())

    return output


def get_file_data(path_: str) -> bytes:
    """This function is used to read files and return its data as bytes.

    :param path_: str -> target file location
    :return: bytes -> targeted file data
    """
    with open(path_, 'rb') as handler:
        return handler.read()


def send_notification(title: str = '', message: str = '') -> None:
    """Use it to send notification to the user.
    It uses `notify_py` library.

    :param title: str -> notification title
    :param message: str -> notification message
    :return: None
    """
    Notify(
        default_notification_application_name=VIEWPORT_TITLE,
        default_notification_title=title,
        default_notification_message=message,
        default_notification_icon=notification_image_path()
    ).send()
