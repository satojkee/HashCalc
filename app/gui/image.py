from os import path

from PIL import Image
from customtkinter import CTkImage

from ..loc import IMAGE_DIR


__all__ = (
    'explorer_image',
    'notification_image_path',
    'app_icon_path'
)


def explorer_image() -> CTkImage:
    """Returns an explorer image.
    :return: CTkImage
    """
    return CTkImage(Image.open(path.join(IMAGE_DIR, 'explorer.png')))


def notification_image_path() -> str:
    """Returns a notification icon path.
    :return: str
    """
    return path.join(IMAGE_DIR, 'notification.png')


def app_icon_path() -> str:
    """Returns an application icon path.
    :return: str
    """
    return path.join(IMAGE_DIR, 'icon.ico')
