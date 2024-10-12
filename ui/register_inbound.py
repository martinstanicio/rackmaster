import tkinter as tk

import customtkinter as ctk

from src.i18n import t
from src.util import format_coordinates
from ui.base_frame import BaseFrame
from ui.coords_input import CoordsInput


class RegisterInbound(BaseFrame):
    def __init__(self, parent, controller, db):
        super().__init__(parent, controller, db)

        title = ctk.CTkLabel(self, text=t("register_inbound"), font=("Arial", 24))
        title.pack(padx=20, pady=20)

        frame = ctk.CTkFrame(self)
        frame.pack(padx=20, pady=20)
        label1 = ctk.CTkLabel(frame, text=t("slot_coordinates"))
        label1.pack()
        self.slot = CoordsInput(frame)
        self.slot.pack(padx=10, pady=10)

        grid = ctk.CTkFrame(self)
        grid.pack(expand=True, fill="x", padx=20, pady=20)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        label2 = ctk.CTkLabel(grid, text=t("article_code"))
        label2.grid(row=0, column=0)
        self.article_code = ctk.CTkEntry(grid)
        self.article_code.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        label3 = ctk.CTkLabel(grid, text=t("quantity"))
        label3.grid(row=0, column=1)
        self.quantity = ctk.CTkEntry(
            grid,
            validate="all",
            validatecommand=(self.register(self.validate_quantity_input), "%P"),
        )
        self.quantity.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        register_button = ctk.CTkButton(
            self, text=t("register_inbound"), command=self.register_inbound
        )
        register_button.pack(padx=20, pady=20)

    def register_inbound(self) -> None:
        coords = self.slot.get_coords()
        if coords is None:
            return

        article_code = self.article_code.get()
        if article_code == "":
            tk.messagebox.showerror("RackMaster", f"{t('please_enter_article_code')}.")
            return

        try:
            quantity = int(self.quantity.get())
        except ValueError:
            tk.messagebox.showerror("RackMaster", f"{t("quantity_must_be_integer")}.")
            return

        slot = self.db.get_slot(*coords)
        if slot is None:
            raise Exception(f"{t('slot_does_not_exist')}.")

        try:
            if not slot.is_empty():
                if article_code == slot.article_code:
                    self.db.update_stock(*coords, quantity)
                else:
                    raise Exception(
                        f"{t("slot_at")} {format_coordinates(*coords)} {t("slot_at_not_empty")}."
                    )
            else:
                use_full_pallet = tk.messagebox.askyesno(
                    "RackMaster",
                    f"{t('use_full_pallet')}?",
                )
                self.db.register_inbound(
                    article_code, quantity, *coords, use_full_pallet
                )
        except Exception as e:
            tk.messagebox.showerror("RackMaster", str(e))
            return

        self.reset()
        tk.messagebox.showinfo("RackMaster", f"{t('inbound_registered_successfully')}.")

    def reset(self) -> None:
        self.slot.reset()
        self.article_code.delete(0, "end")
        self.quantity.delete(0, "end")

    def validate_quantity_input(self, P: str) -> bool:
        return str.isdigit(P) or P == ""
