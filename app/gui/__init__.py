import customtkinter as ctk

from .props import *
from .content import Content
from .image import app_icon_path


__all__ = ('build_and_run', )


class Viewport(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(VIEWPORT_TITLE)
        self.iconbitmap(app_icon_path())
        self.overrideredirect(VIEWPORT_OVERRIDEREDIRECT)
        self.geometry('{}x{}'.format(*VIEWPORT_METRICS))
        self.resizable(*VIEWPORT_RESIZABLE)

        self.wm_attributes('-alpha', VIEWPORT_ALPHA)
        self.wm_attributes('-topmost', VIEWPORT_TOPMOST)

        ctk.set_appearance_mode(VIEWPORT_APPEARANCE_MODE)
        ctk.set_default_color_theme(VIEWPORT_THEME)

        self.__to_center()

        Content(self).pack(fill=ctk.BOTH, expand=True)

    def __to_center(self) -> None:
        """This method is used to position window to the center of the screen.
        It uses display resolution and current viewport size for offset calculation.

        :return: None
        """
        d_w, d_h = self.winfo_screenwidth(), self.winfo_screenheight()
        o_x, o_y = (d_w - self.winfo_width()) // 2, (d_h - self.winfo_height()) // 2

        self.geometry('+{}+{}'.format(o_x, o_y))
        self.update()


def build_and_run() -> None:
    """Use it to start the application."""
    Viewport().mainloop()
