import tkinter as tk

import customtkinter as ctk

from src.db import Database
from ui.get_article_slots import GetArticleSlots
from ui.get_free_slots import GetFreeSlots
from ui.get_slot import GetSlot
from ui.register_inbound import RegisterInbound
from ui.swap_pallets import SwapPallets


class GUI(ctk.CTk):
    def __init__(self, db: Database) -> None:
        super().__init__()
        self.title("RackMaster")

        self.container = ctk.CTkFrame(self)
        self.container.pack(expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(self)
        self.config(menu=menubar)

        filemenu = tk.Menu(menubar, tearoff=0)

        inbound = tk.Menu(menubar, tearoff=0)
        inbound.add_command(label="Get slot", command=lambda: self.show_frame(GetSlot))
        inbound.add_command(
            label="Get free slots", command=lambda: self.show_frame(GetFreeSlots)
        )
        inbound.add_command(
            label="Get article slots", command=lambda: self.show_frame(GetArticleSlots)
        )
        inbound.add_command(
            label="Register inbound", command=lambda: self.show_frame(RegisterInbound)
        )

        internal_movement = tk.Menu(menubar, tearoff=0)
        internal_movement.add_command(
            label="Swap pallets", command=lambda: self.show_frame(SwapPallets)
        )

        outbound = tk.Menu(menubar, tearoff=0)

        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Inbound operations", menu=inbound)
        menubar.add_cascade(label="Internal movement", menu=internal_movement)
        menubar.add_cascade(label="Outbound operations", menu=outbound)

        self.frames = {}
        for F in (
            GetSlot,
            GetFreeSlots,
            GetArticleSlots,
            RegisterInbound,
            SwapPallets,
        ):
            frame = F(self.container, self, db)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(GetSlot)

    def show_frame(self, frame_class):
        """Show the frame corresponding to the given frame class."""
        frame = self.frames[frame_class]
        frame.tkraise()

    def run(self) -> None:
        self.mainloop()
