import customtkinter as ctk

from src.db import Database


class BaseFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, db: Database):
        super().__init__(parent)
        self.controller = controller
        self.db = db
