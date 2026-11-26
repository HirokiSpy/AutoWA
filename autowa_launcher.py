from AutoWA import AutoWAApp
import tkinter as tk


def main() -> None:
    """Launch the AutoWA desktop application."""
    root = tk.Tk()
    AutoWAApp(root)
    root.mainloop()
