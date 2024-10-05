import tkinter as tk

import customtkinter as ctk

from ui.base_frame import BaseFrame


class GetFreeSlots(BaseFrame):
    def __init__(self, parent, controller, db):
        super().__init__(parent, controller, db)

        title = ctk.CTkLabel(self, text="Get free slots", font=("Arial", 24))
        title.pack(padx=20, pady=20)

        get_button = ctk.CTkButton(
            self, text="Get free slots", command=self.get_free_slots
        )
        get_button.pack(padx=20, pady=20)

        self.result = ctk.CTkTextbox(self)
        self.result.pack(padx=20, pady=20, expand=True, fill="both")
        self.result.configure(state="disabled")

        self.get_free_slots()

    def get_free_slots(self) -> None:
        try:
            slots = self.db.get_free_slots()
        except Exception as e:
            tk.messagebox.showerror("RackMaster", str(e))
            return

        self.result.configure(state="normal")
        self.result.delete("1.0", "end")
        self.result.insert("end", f"Free slots: {len(slots)}\n")
        for slot in slots:
            self.result.insert("end", f"{str(slot)}\n")
        self.result.configure(state="disabled")
