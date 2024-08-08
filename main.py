import tkinter as tk
from tkinter import messagebox
from pynput import keyboard

class SnapTapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Snap Tap Emulator")

        # Configurações principais da janela
        self.root.geometry("400x200")
        self.root.resizable(False, False)
        self.root.configure(bg='#2e2e2e')

        # Frame principal
        self.frame = tk.Frame(root, bg='#2e2e2e')
        self.frame.pack(padx=20, pady=20, expand=True)

        # Título
        self.label = tk.Label(self.frame, text="Snap Tap Emulator", font=('Helvetica', 16, 'bold'), bg='#2e2e2e', fg='white')
        self.label.pack(pady=10)

        # Campos de configuração
        self.a_key_var = tk.StringVar(value="A")
        self.d_key_var = tk.StringVar(value="D")

        self.key_frame = tk.Frame(self.frame, bg='#2e2e2e')
        self.key_frame.pack(pady=10)

        self.a_key_label = tk.Label(self.key_frame, text="Tecla A:", font=('Helvetica', 12), bg='#2e2e2e', fg='white')
        self.a_key_label.pack(side='left', padx=5)
        self.a_key_entry = tk.Entry(self.key_frame, textvariable=self.a_key_var, width=3, font=('Helvetica', 12))
        self.a_key_entry.pack(side='left')

        self.d_key_label = tk.Label(self.key_frame, text="Tecla D:", font=('Helvetica', 12), bg='#2e2e2e', fg='white')
        self.d_key_label.pack(side='left', padx=5)
        self.d_key_entry = tk.Entry(self.key_frame, textvariable=self.d_key_var, width=3, font=('Helvetica', 12))
        self.d_key_entry.pack(side='left')

        # Botões
        self.button_frame = tk.Frame(self.frame, bg='#2e2e2e')
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_snaptap, font=('Helvetica', 12), bg='#4CAF50', fg='white', activebackground='#45a049', relief='flat')
        self.start_button.pack(side='left', padx=5)

        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop_snaptap, font=('Helvetica', 12), bg='#f44336', fg='white', activebackground='#e53935', relief='flat')
        self.stop_button.pack(side='left', padx=5)

        self.listener = None
        self.keys_pressed = set()

    def start_snaptap(self):
        if self.listener is None:
            self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            self.listener.start()
            self.show_popup("Snap Tap Started")
        else:
            self.show_popup("Snap Tap already running")

    def stop_snaptap(self):
        if self.listener:
            self.listener.stop()
            self.listener = None
            self.show_popup("Snap Tap Stopped")

    def show_popup(self, message):
        popup = tk.Toplevel(self.root)
        popup.title("Notification")
        popup.geometry("250x100+{}+{}".format(self.root.winfo_screenwidth() - 270, self.root.winfo_screenheight() - 150))
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)
        popup.attributes("-alpha", 0.9)
        popup.configure(bg='#333333')

        label = tk.Label(popup, text=message, font=('Helvetica', 12), bg='#333333', fg='white')
        label.pack(expand=True)

        self.root.after(2000, popup.destroy)

    def on_press(self, key):
        try:
            key_char = key.char.lower()
            if key_char in [self.a_key_var.get().lower(), self.d_key_var.get().lower()]:
                self.keys_pressed.add(key_char)
                if len(self.keys_pressed) > 1:
                    last_key = key_char
                    self.keys_pressed.clear()
                    self.keys_pressed.add(last_key)
                    print(f"Prioritizing {last_key}")
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            key_char = key.char.lower()
            if key_char in self.keys_pressed:
                self.keys_pressed.remove(key_char)
        except AttributeError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = SnapTapApp(root)
    root.mainloop()
