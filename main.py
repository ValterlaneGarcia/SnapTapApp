import tkinter as tk
from tkinter import messagebox
from pynput import keyboard

class SnapTapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Snap Tap Emulator")
        
        self.label = tk.Label(root, text="Pressione as teclas para configurar Snap Tap")
        self.label.pack(pady=10)
        
        self.a_key_var = tk.StringVar(value="A")
        self.d_key_var = tk.StringVar(value="D")
        
        self.a_key_entry = tk.Entry(root, textvariable=self.a_key_var, width=3)
        self.a_key_entry.pack(pady=5)
        
        self.d_key_entry = tk.Entry(root, textvariable=self.d_key_var, width=3)
        self.d_key_entry.pack(pady=5)
        
        self.start_button = tk.Button(root, text="Iniciar Snap Tap", command=self.start_snaptap)
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, text="Parar Snap Tap", command=self.stop_snaptap)
        self.stop_button.pack(pady=10)
        
        self.listener = None
        self.keys_pressed = set()
    
    def start_snaptap(self):
        if self.listener is None:
            self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            self.listener.start()
            messagebox.showinfo("Snap Tap", "Snap Tap Iniciado")
        else:
            messagebox.showwarning("Snap Tap", "Snap Tap já está em execução")
    
    def stop_snaptap(self):
        if self.listener:
            self.listener.stop()
            self.listener = None
            messagebox.showinfo("Snap Tap", "Snap Tap Parado")
    
    def on_press(self, key):
        try:
            key_char = key.char.lower()
            if key_char in [self.a_key_var.get().lower(), self.d_key_var.get().lower()]:
                self.keys_pressed.add(key_char)
                if len(self.keys_pressed) > 1:
                    last_key = key_char
                    self.keys_pressed.clear()
                    self.keys_pressed.add(last_key)
                    print(f"Priorizando {last_key}")
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
