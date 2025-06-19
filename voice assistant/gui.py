import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from threading import Thread
import time
from assistant import run_assistant

class VoiceAssistantGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("AI Voice Assistant")
        self.master.geometry("600x500")
        self.master.resizable(False, False)
        self.center_window()

        self.bg_image = Image.open("background.jpeg")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image.resize((600, 500)))
        self.bg_label = tk.Label(self.master, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.mic_on_img = ImageTk.PhotoImage(Image.open("mic_on.jpeg").resize((50, 50)))
        self.mic_off_img = ImageTk.PhotoImage(Image.open("mic_off.jpeg").resize((50, 50)))

        self.status_label = tk.Label(master, text="Assistant is idle", font=("Arial", 16, "bold"), bg="#f0f0f0")
        self.status_label.place(x=180, y=20)

        self.mic_label = tk.Label(master, image=self.mic_off_img, bg="#f0f0f0")
        self.mic_label.place(x=20, y=15)

        self.log_box = tk.Text(master, height=15, width=70, font=("Consolas", 10), bg="#ffffff", wrap="word")
        self.log_box.place(x=20, y=80)
        self.log_box.config(state=tk.DISABLED)

        self.toggle_button = tk.Button(master, text="Start Assistant", command=self.toggle_assistant,
                                       bg="green", fg="white", font=("Arial", 12), width=18)
        self.toggle_button.place(x=120, y=430)

        self.exit_button = tk.Button(master, text="Exit", command=self.exit_app,
                                     bg="red", fg="white", font=("Arial", 12), width=18)
        self.exit_button.place(x=320, y=430)

        self.is_running = False
        self.stop_signal = False

    def center_window(self):
        self.master.update_idletasks()
        w = self.master.winfo_width()
        h = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (w // 2)
        y = (self.master.winfo_screenheight() // 2) - (h // 2)
        self.master.geometry(f"+{x}+{y}")

    def toggle_assistant(self):
        if not self.is_running:
            self.status_label.config(text="Assistant is running", fg="green")
            self.mic_label.config(image=self.mic_on_img)
            self.toggle_button.config(text="Stop Assistant", bg="orange")
            self.stop_signal = False
            self.thread = Thread(target=run_assistant, args=(self.log_command, self.get_stop_signal))
            self.thread.start()
            self.is_running = True
        else:
            self.stop_signal = True
            self.status_label.config(text="Assistant is stopping...", fg="gray")
            self.toggle_button.config(text="Start Assistant", bg="green")
            self.mic_label.config(image=self.mic_off_img)
            self.is_running = False

    def get_stop_signal(self):
        return self.stop_signal

    def log_command(self, command):
        self.log_box.config(state=tk.NORMAL)
        self.log_box.insert(tk.END, f"> {command}\n")
        self.log_box.see(tk.END)
        self.log_box.config(state=tk.DISABLED)

    def exit_app(self):
        self.stop_signal = True
        time.sleep(1)
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    root.mainloop()
