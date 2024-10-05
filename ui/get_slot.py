import tkinter as tk

import customtkinter as ctk

from ui.base_frame import BaseFrame
from ui.coords_input import CoordsInput


class GetSlot(BaseFrame):
    def __init__(self, parent, controller, db):
        super().__init__(parent, controller, db)

        title = ctk.CTkLabel(self, text="Get slot", font=("Arial", 24))
        title.pack(padx=20, pady=20)

        frame = ctk.CTkFrame(self)
        frame.pack(padx=20, pady=20)
        label = ctk.CTkLabel(frame, text="Slot coordinates")
        label.pack()
        self.slot = CoordsInput(frame, controller)
        self.slot.pack(padx=10, pady=10)

        get_button = ctk.CTkButton(self, text="Get slot", command=self.get_slot)
        get_button.pack(padx=20, pady=20)

        self.result = ctk.CTkTextbox(self)
        self.result.pack(padx=20, pady=20, expand=True, fill="both")
        self.result.configure(state="disabled")

    def get_slot(self) -> None:
        coords = self.slot.get_coords()
        if coords is None:
            return

        try:
            slot = self.db.get_slot(*coords)
        except Exception as e:
            tk.messagebox.showerror("RackMaster", str(e))
            return

        if slot is None:
            tk.messagebox.showwarning("RackMaster", "Slot does not exist.")
            return

        self.result.configure(state="normal")
        self.result.insert("1.0", f"{str(slot)}\n")
        self.result.configure(state="disabled")
