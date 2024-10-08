import tkinter as tk

import customtkinter as ctk

from src.i18n import t
from ui.base_frame import BaseFrame
from ui.coords_input import CoordsInput


class SwapPallets(BaseFrame):
    def __init__(self, parent, controller, db):
        super().__init__(parent, controller, db)

        title = ctk.CTkLabel(self, text=t("swap_pallets"), font=("Arial", 24))
        title.pack(padx=20, pady=20)

        frame1 = ctk.CTkFrame(self)
        frame1.pack(padx=20, pady=20)
        label1 = ctk.CTkLabel(frame1, text=f"{t("slot")} 1")
        label1.pack()
        self.slot1 = CoordsInput(frame1)
        self.slot1.pack(padx=10, pady=10)

        frame2 = ctk.CTkFrame(self)
        frame2.pack(padx=20, pady=20)
        label2 = ctk.CTkLabel(frame2, text=f"{t("slot")} 2")
        label2.pack()
        self.slot2 = CoordsInput(frame2)
        self.slot2.pack(padx=10, pady=10)

        swap_button = ctk.CTkButton(
            self,
            text=t("swap_pallets"),
            command=self.on_click,
        )
        swap_button.pack(padx=20, pady=20)

    def on_click(self) -> None:
        coords1 = self.slot1.get_coords()
        if coords1 is None:
            return

        coords2 = self.slot2.get_coords()
        if coords2 is None:
            return

        self.swap(*coords1, *coords2)

    def swap(
        self,
        xx1: int,
        yyy1: int,
        zz1: int,
        xx2: int,
        yyy2: int,
        zz2: int,
    ) -> None:
        try:
            slot1 = self.db.get_slot(xx1, yyy1, zz1)
            if slot1 is None:
                raise Exception(f"{t("slot")} 1 {t("slot_at_does_not_exist")}.")

            slot2 = self.db.get_slot(xx2, yyy2, zz2)
            if slot2 is None:
                raise Exception(f"{t("slot")} 2 {t("slot_at_does_not_exist")}.")

            self.db.swap_pallets(slot1, slot2)
            tk.messagebox.showinfo("RackMaster", f"{t('pallets_swapped_successfully')}.")
        except Exception as e:
            tk.messagebox.showerror("RackMaster", str(e))

    def reset(self) -> None:
        self.slot1.reset()
        self.slot2.reset()
