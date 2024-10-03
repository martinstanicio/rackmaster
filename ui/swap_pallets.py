import tkinter as tk

import customtkinter as ctk

from ui.base_frame import BaseFrame


class SwapPallets(BaseFrame):
    def __init__(self, parent, controller, db):
        super().__init__(parent, controller, db)

        label = ctk.CTkLabel(self, text="Swap pallets", font=("Arial", 24))
        label.pack(padx=20, pady=20)

        frame1 = ctk.CTkFrame(self)
        frame1.pack(padx=20, pady=20)
        label1 = ctk.CTkLabel(frame1, text="Slot 1")
        label1.pack()
        grid1 = ctk.CTkFrame(frame1)
        grid1.pack(padx=10, pady=10)
        self.xx1 = ctk.CTkEntry(grid1, placeholder_text="XX")
        self.xx1.grid(row=0, column=1)
        self.yyy1 = ctk.CTkEntry(grid1, placeholder_text="YYY")
        self.yyy1.grid(row=0, column=2, padx=5)
        self.zz1 = ctk.CTkEntry(grid1, placeholder_text="ZZ")
        self.zz1.grid(row=0, column=3)

        frame2 = ctk.CTkFrame(self)
        frame2.pack(padx=20, pady=20)
        label2 = ctk.CTkLabel(frame2, text="Slot 2")
        label2.pack()
        grid2 = ctk.CTkFrame(frame2)
        grid2.pack(padx=10, pady=10)
        self.xx2 = ctk.CTkEntry(grid2, placeholder_text="XX")
        self.xx2.grid(row=0, column=1)
        self.yyy2 = ctk.CTkEntry(grid2, placeholder_text="YYY")
        self.yyy2.grid(row=0, column=2, padx=5)
        self.zz2 = ctk.CTkEntry(grid2, placeholder_text="ZZ")
        self.zz2.grid(row=0, column=3)

        swap_button = ctk.CTkButton(self, text="Swap pallets", command=self.on_click)
        swap_button.pack(padx=20, pady=20)

    def on_click(self) -> None:
        try:
            self.swap(
                int(self.xx1.get()),
                int(self.yyy1.get()),
                int(self.zz1.get()),
                int(self.xx2.get()),
                int(self.yyy2.get()),
                int(self.zz2.get()),
            )
        except ValueError:
            tk.messagebox.showerror("RackMaster", "Please enter valid coordinates.")

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
                raise Exception("Slot 1 does not exist.")

            slot2 = self.db.get_slot(xx2, yyy2, zz2)
            if slot2 is None:
                raise Exception("Slot 2 does not exist.")

            self.db.swap_pallets(slot1, slot2)
            tk.messagebox.showinfo("RackMaster", "Pallets swapped successfully.")
        except Exception as e:
            tk.messagebox.showerror("RackMaster", str(e))
            return
