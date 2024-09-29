import tkinter as tk


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RackMaster")
        self.geometry("600x400")

        self.container = tk.Frame(self)
        self.container.pack(expand=True)

        menubar = tk.Menu(self)
        self.config(menu=menubar)

        filemenu = tk.Menu(menubar, tearoff=0)

        inbound = tk.Menu(menubar, tearoff=0)

        internal_movement = tk.Menu(menubar, tearoff=0)

        outbound = tk.Menu(menubar, tearoff=0)

        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Inbound operations", menu=inbound)
        menubar.add_cascade(label="Internal movement", menu=internal_movement)
        menubar.add_cascade(label="Outbound operations", menu=outbound)

        self.frames = {}
        for F in ():
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.pack(anchor="center")

    def show_frame(self, frame_class):
        """Show the frame corresponding to the given frame class."""
        frame = self.frames[frame_class]
        frame.tkraise()

    def run(self) -> None:
        self.mainloop()


if __name__ == "__main__":
    gui = GUI()
    gui.run()
