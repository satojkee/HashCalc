import pyperclip
import customtkinter as ctk

from .font import *
from .image import *
from ..tools import *


__all__ = ('Content',)


class LinkedEntry(ctk.CTkEntry):
    """Similar to the `ctk.Entry` class, except of additional positional argument
    That argument is used as key to control the state of the entry.
    """
    def __init__(self, master, key, **kwargs):
        super().__init__(master, **kwargs)

        self.key = key


class Content(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self._v_filepath = ctk.StringVar(value='path/to/the/file')

        self._c_input = ctk.CTkFrame(self)
        self._c_input.grid_columnconfigure(0, weight=1)
        self._c_input.grid_columnconfigure(1, weight=3)

        self._c_output = ctk.CTkFrame(self)
        self._c_output.grid_columnconfigure(0, weight=1)
        self._c_output.grid_columnconfigure(1, weight=9)

        self._c_controls = ctk.CTkFrame(self)

        self._c_input.pack(fill=ctk.BOTH, padx=10, pady=(10, 0))
        self._c_output.pack(fill=ctk.BOTH, padx=10, pady=(10, 0), expand=True)
        self._c_controls.pack(fill=ctk.BOTH, side=ctk.BOTTOM, padx=10, pady=10)

        # This zone contains a file-input field
        f_input_lbl = ctk.CTkLabel(
            self._c_input,
            text='Data:',
            font=font_primary()
        )
        f_input_btn = ctk.CTkButton(
            self._c_input,
            text='Browse',
            font=font_button(),
            image=explorer_image(),
            width=24,
            cursor='hand2',
            compound=ctk.RIGHT,
            command=lambda: self._v_filepath.set(
                ctk.filedialog.askopenfilename()
            ),
        )
        f_input_ent = ctk.CTkEntry(
            self._c_input,
            font=font_input(),
            textvariable=self._v_filepath
        )

        f_input_lbl.pack(side=ctk.LEFT, padx=(20, 5), pady=20)
        f_input_btn.pack(side=ctk.RIGHT, padx=(0, 20), pady=20)
        f_input_ent.pack(
            side=ctk.RIGHT,
            fill=ctk.X,
            expand=True,
            padx=(5, 5),
            pady=20
        )

        # This zone contains output fields and controls associated with that fields
        # Items in this zone are generated dynamically and are linked to the hash func.
        for _, pair in enumerate(HASH_MAPPING.items()):
            name, func = pair

            checkbox = ctk.CTkCheckBox(
                self._c_output,
                text=name,
                command=self.__set_states,
                font=font_primary()
            )
            checkbox.grid(
                row=_,
                column=0,
                padx=(20, 0),
                pady=20,
                sticky=ctk.W
            )

            entry = LinkedEntry(
                self._c_output,
                name,
                font=font_output(),
                textvariable=ctk.StringVar(),
                state=ctk.DISABLED
            )
            entry.bind('<Button-1>', self.__to_clipboard)
            entry.grid(
                row=_,
                column=1,
                padx=(0, 20),
                pady=20,
                sticky=ctk.EW,
                columnspan=9
            )

        # Calculate button is an only widget in controls zone
        # It's used to calculate the selected hash-functions
        calc_btn = ctk.CTkButton(
            self._c_controls,
            text='CALCULATE',
            cursor='hand2',
            command=self.__calculate,
            font=font_button()
        )
        calc_btn.pack(anchor=ctk.CENTER, padx=20, pady=20, ipady=5, ipadx=5)

    def __get_checked(self) -> list[str]:
        """This method is used to get the list of selected hash-function.
        These names are used to access the `HASH_MAPPING` dictionary.

        :return: list[str] -> the list of names
        """
        return [
            widget.cget('text')
            for widget in self._c_output.winfo_children()
            if isinstance(widget, ctk.CTkCheckBox) and widget.get()
        ]

    def __calculate(self) -> None:
        """This method is used to calculate the selected hash-functions.
        It receives the list of selected hash-functions first. (using .__get_checked)
        Then collects the data from the targeted data-file.
        Finally, it calculates the hash.

        * IF provided file does not exist, it sends a notification.

        :return: None
        """
        try:
            filedata = get_file_data(self._v_filepath.get())
            mapping = hash_data(filedata, self.__get_checked())

            self.__set_values(mapping)
        except FileNotFoundError:
            send_notification(
                'Specified file does not exist!',
                'Please check the path and try again.'
            )

    def __get_linked_entries(self) -> list[LinkedEntry]:
        """This method fast checks all widgets in the _c_output container.
        IF the widget is an instance of `LinkedEntry` THEN it adds it to the list.

        :return: list[LinkedEntry]
        """
        return [
            widget
            for widget in self._c_output.winfo_children()
            if isinstance(widget, LinkedEntry)
        ]

    def __set_values(self, mapping: dict) -> None:
        """This functon sets the values of the output entries.
        Identifies the keys and values in `mapping` and sets the values of the output entries accordingly.

        :param mapping: dict -> in format: {hash_algo_name: hash_value}
        :return: None
        """
        for e in self.__get_linked_entries():
            if e.key in mapping.keys():
                e.cget('textvariable').set(mapping.get(e.key))
            else:
                e.cget('textvariable').set('')

            e.update()

    def __set_states(self) -> None:
        """This method is used to control output entries based on the associated checkbox state.
        IF `checkbox` is checked (.get() returns 1) THEN `entry` is enabled and vice versa.
        Don't forget to call this method every time you change checkbox state (*command=self.__set_states)

        :return: None
        """
        for e in self.__get_linked_entries():
            if e.key not in self.__get_checked():
                e.configure(state=ctk.DISABLED)
            else:
                e.configure(state=ctk.NORMAL)

    @staticmethod
    def __to_clipboard(event) -> None:
        """This method copies the content of an entry widget to the clipboard.
        Bind an entry widget to this function to copy its content each time the user clicks on it.

        :return: None
        """
        if event.widget.cget('state') == ctk.NORMAL:
            pyperclip.copy(event.widget.get())
