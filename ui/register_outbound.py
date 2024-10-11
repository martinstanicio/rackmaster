import tkinter as tk

import customtkinter as ctk

from src.i18n import t
from ui.base_frame import BaseFrame


class RegisterOutbound(BaseFrame):
    items = 5
    article_codes = [None] * items
    quantities = [None] * items

    def __init__(self, parent, controller, db):
        super().__init__(parent, controller, db)

        title = ctk.CTkLabel(self, text=t("register_outbound"), font=("Arial", 24))
        title.pack(padx=20, pady=20)

        grid = ctk.CTkFrame(self)
        grid.pack(expand=True, fill="x", padx=20, pady=20)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        label1 = ctk.CTkLabel(grid, text=t("article_code"))
        label1.grid(row=0, column=0)
        label2 = ctk.CTkLabel(grid, text=t("quantity"))
        label2.grid(row=0, column=1)

        for i in range(self.items):
            self.article_codes[i] = ctk.CTkEntry(grid)
            self.article_codes[i].grid(
                row=i + 1, column=0, padx=10, pady=10, sticky="ew"
            )
            self.quantities[i] = ctk.CTkEntry(
                grid,
                validate="all",
                validatecommand=(self.register(self.validate_quantity_input), "%P"),
            )
            self.quantities[i].grid(row=i + 1, column=1, padx=10, pady=10, sticky="ew")

        register_button = ctk.CTkButton(
            self, text=t("register_outbound"), command=self.register_outbound
        )
        register_button.pack(padx=20, pady=20)

        self.message = ctk.CTkTextbox(self)
        self.message.pack(padx=20, pady=20, expand=True, fill="both")
        self.message.configure(state="disabled")

    def register_outbound(self) -> None:
        self.message.configure(state="normal")
        self.message.delete("1.0", "end")
        self.message.configure(state="disabled")

        articles_with_quantity: list[tuple[str, int]] = []

        for i in range(self.items):
            article_code = self.article_codes[i].get().strip()
            if article_code == "":
                continue

            try:
                quantity = int(self.quantities[i].get())
            except ValueError:
                tk.messagebox.showerror(
                    "RackMaster", f"{t('quantity_must_be_integer')}."
                )
                return

            articles_with_quantity.append((article_code, quantity))

        if len(articles_with_quantity) == 0:
            tk.messagebox.showwarning(
                "RackMaster", f"{t('please_enter_article_code')}."
            )
            return

        try:
            ans = self.db.register_outbound(*articles_with_quantity)
        except Exception as e:
            tk.messagebox.showerror("RackMaster", str(e))
            self.message.configure(state="normal")
            self.message.insert("end", f"{str(e)}\n")
            self.message.configure(state="disabled")
            return

        self.reset()
        self.message.configure(state="normal")
        for slot in ans:
            self.message.insert("end", f"{str(slot)}\n")
        self.message.configure(state="disabled")
        tk.messagebox.showinfo(
            "RackMaster", f"{t('outbound_registered_successfully')}."
        )

    def reset(self) -> None:
        for i in range(self.items):
            self.article_codes[i].delete(0, "end")
            self.quantities[i].delete(0, "end")

        self.message.configure(state="normal")
        self.message.delete("1.0", "end")
        self.message.configure(state="disabled")

    def validate_quantity_input(self, P: str) -> bool:
        return str.isdigit(P) or P == ""
