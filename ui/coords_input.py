import tkinter as tk

import customtkinter as ctk


class CoordsInput(ctk.CTkFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        cmd = self.register(self.validate_input)

        self.xx = ctk.CTkEntry(
            self, placeholder_text="XX", validate="all", validatecommand=(cmd, "%P")
        )
        self.yyy = ctk.CTkEntry(
            self, placeholder_text="YYY", validate="all", validatecommand=(cmd, "%P")
        )
        self.zz = ctk.CTkEntry(
            self, placeholder_text="ZZ", validate="all", validatecommand=(cmd, "%P")
        )

        self.xx.grid(row=0, column=1)
        self.yyy.grid(row=0, column=2, padx=5)
        self.zz.grid(row=0, column=3)

    def get_coords(self) -> tuple[int, int, int] | None:
        """
        Returns the coordinates as a tuple `(xx, yyy, zz)`.

        Shows a `tkinter.messagebox` and returns `None` if the coordinates are invalid.
        """
        try:
            xx = int(self.xx.get())
            yyy = int(self.yyy.get())
            zz = int(self.zz.get())
        except ValueError:
            tk.messagebox.showerror("RackMaster", "Please enter valid coordinates.")
            return

        return (xx, yyy, zz)

    def reset(self) -> None:
        self.xx.delete(0, "end")
        self.yyy.delete(0, "end")
        self.zz.delete(0, "end")

    def validate_input(self, P: str) -> bool:
        return str.isdigit(P) or P == ""
