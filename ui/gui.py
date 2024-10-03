import tkinter as tk

import customtkinter as ctk

from src.db import Database
from ui.swap_pallets import SwapPallets


class GUI(ctk.CTk):
    def __init__(self, db: Database) -> None:
        super().__init__()
        self.title("RackMaster")

        self.container = ctk.CTkFrame(self)
        self.container.pack(expand=True)

        menubar = tk.Menu(self)
        self.config(menu=menubar)

        filemenu = tk.Menu(menubar, tearoff=0)

        inbound = tk.Menu(menubar, tearoff=0)

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
        for F in (SwapPallets,):
            frame = F(self.container, self, db)
            self.frames[F] = frame
            frame.pack(anchor="center")

        self.show_frame(SwapPallets)

    def show_frame(self, frame_class):
        """Show the frame corresponding to the given frame class."""
        frame = self.frames[frame_class]
        frame.tkraise()

    def run(self) -> None:
        self.mainloop()
