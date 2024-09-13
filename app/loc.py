import pathlib


__all__ = ('FONT_DIR', 'IMAGE_DIR')


cwd = pathlib.Path.cwd()


FONT_DIR = pathlib.Path(cwd, r'resources/font')
IMAGE_DIR = pathlib.Path(cwd, r'resources/image')
