from os import listdir, path

from customtkinter import FontManager, CTkFont

from ..loc import FONT_DIR


__all__ = (
    'font_primary',
    'font_output',
    'font_input',
    'font_button'
)


# Font family name
FAMILY: str = 'Dogica'

for font in listdir(r'resources/font'):
    FontManager.load_font(path.join(FONT_DIR, font))


def font_primary() -> CTkFont:
    """This function returns a proper `CTkFont` object
    :return: CTkFont -> `CTkFont` object
    """
    return CTkFont(FAMILY, 14, 'bold')


def font_output() -> CTkFont:
    """This function returns a proper `CTkFont` object
    :return: CTkFont -> `CTkFont` object
    """
    return CTkFont('Consolas', 14)


def font_input() -> CTkFont:
    """This function returns a proper `CTkFont` object
    :return: CTkFont -> `CTkFont` object
    """
    return CTkFont(FAMILY, 12)


def font_button() -> CTkFont:
    """This function returns a proper `CTkFont` object
    :return: CTkFont -> `CTkFont` object
    """
    return CTkFont(FAMILY, 11, 'bold')
