import tkinter as tk

import customtkinter as ctk

from src.i18n import t
from ui.base_frame import BaseFrame


class GetArticleSlots(BaseFrame):
    def __init__(self, parent, controller, db):
        super().__init__(parent, controller, db)

        title = ctk.CTkLabel(self, text=t("get_article_slots"), font=("Arial", 24))
        title.pack(padx=20, pady=20)

        frame = ctk.CTkFrame(self)
        frame.pack(padx=20, pady=20, expand=True, fill="both")

        label2 = ctk.CTkLabel(frame, text=t("article_code"))
        label2.pack()
        self.article_code = ctk.CTkEntry(frame)
        self.article_code.pack(padx=10, pady=10, expand=True, fill="x")

        get_button = ctk.CTkButton(
            self, text=t("get_article_slots"), command=self.get_article_slots
        )
        get_button.pack(padx=20, pady=20)

        self.result = ctk.CTkTextbox(self)
        self.result.pack(padx=20, pady=20, expand=True, fill="both")
        self.result.configure(state="disabled")

    def get_article_slots(self) -> None:
        article_code = self.article_code.get().strip()

        if article_code == "":
            tk.messagebox.showerror("RackMaster", f"{t("please_enter_article_code")}.")
            return

        try:
            slots = self.db.get_article_slots(article_code)
            stock = self.db.get_article_stock(article_code)
        except Exception as e:
            tk.messagebox.showerror("RackMaster", str(e))
            return

        self.result.configure(state="normal")
        self.result.delete("1.0", "end")
        self.result.insert("end", f"{t("slots")}: {len(slots)}\n")
        self.result.insert("end", f"{t("stock")}: {stock}\n")
        for slot in slots:
            self.result.insert("end", f"{str(slot)}\n")
        self.result.configure(state="disabled")

    def reset(self) -> None:
        self.result.configure(state="normal")
        self.result.delete("1.0", "end")
        self.result.configure(state="disabled")
