import tkinter as tk
from tkinter import messagebox
import cv2
import threading
import pygame
class Block:
    def __init__(self, size):
        self.size = size

class Peg:
    def __init__(self):
        self.blocks = []

    def push(self, block):
        self.blocks.append(block)

    def pop(self):
        if not self.is_empty():
            return self.blocks.pop()

    def is_empty(self):
        return len(self.blocks) == 0

    def peek(self):
        if not self.is_empty():
            return self.blocks[-1]

    def size(self):
        return len(self.blocks)

class TowersOfHanoi:
    def __init__(self, root, n, source, auxiliary, target):
        self.root = root
        self.root.title("Tower of Hanoi")
        self.n = n
        self.source_peg = source
        self.auxiliary_peg = auxiliary
        self.target_peg = target

        first = Peg()
        for i in range(n, 0, -1):
            first.push(Block(i))
        self.pegs = {
            'A': first,
            'B': Peg(),
            'C': Peg()
        }
        self.moves = 0

        self.root.configure(bg='lightgray')

        self.canvas = tk.Canvas(root, width=600, height=300, bg='white')
        self.canvas.pack()

        self.custom_font = ("Arial", 14)

        self.message_label = tk.Label(root, text="Moves: 0", font=self.custom_font, bg='lightgray')
        self.message_label.pack()

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_game, font=self.custom_font, bg='lightblue')
        self.reset_button.pack()

        self.from_peg = None

        button_frame = tk.Frame(root, bg='lightgray')
        button_frame.pack()
        for peg in self.pegs.keys():
            button = tk.Button(button_frame, text=peg, command=lambda peg=peg: self.set_from_peg(peg),
                               font=self.custom_font, width=6, bg='lightgreen')
            button.pack(side=tk.LEFT, padx=10)

        self.selected_peg = None
        self.selected_label = tk.Label(root, text="Selected Peg: None", font=self.custom_font, bg='lightgray')
        self.selected_label.pack()

        self.draw_blocks()

    def draw_blocks(self):
        self.canvas.delete("blocks")
        for peg, peg_object in self.pegs.items():
            x = 150 + (ord(peg) - ord('A')) * 150
            y = 250
            for i, block in enumerate(peg_object.blocks):
                size = block.size
                self.canvas.create_rectangle(
                    x - size * 25, y - 20 * i,
                    x + size * 25, y - 20 * i + 20,
                    fill='blue',
                    tags="blocks"
                )

    def set_from_peg(self, peg):
        if self.from_peg is None:
            self.from_peg = peg
            self.selected_peg = peg
            self.update_selected_label()
        else:
            self.move_block(peg)
            self.from_peg = None

    def move_block(self, to_peg):
        if self.selected_peg and self.selected_peg != to_peg:
            from_peg = self.selected_peg
            if not self.pegs[from_peg].is_empty():
                if self.pegs[to_peg].is_empty() or self.pegs[from_peg].peek().size < self.pegs[to_peg].peek().size:
                    block = self.pegs[from_peg].pop()
                    self.pegs[to_peg].push(block)
                    self.moves += 1
                    self.message_label.config(text=f"Moves: {self.moves}")
                    self.draw_blocks()
                    if self.pegs[self.target_peg].size() == self.n:
                        self.show_congratulations_message()
                else:
                    self.show_error_message("Cannot place a larger block on a smaller one. Try again.")
            else:
                self.show_error_message("Source peg is empty. Try again.")
            self.selected_peg = None
            self.update_selected_label()

    def update_selected_label(self):
        self.selected_label.config(text=f"Selected Peg: {self.selected_peg}")

    def reset_game(self):
        self.pegs = {
            'A': Peg(),
            'B': Peg(),
            'C': Peg()
        }
        for i in range(self.n, 0, -1):
            self.pegs['A'].push(Block(i))
        self.moves = 0
        self.message_label.config(text=f"Moves: {self.moves}")
        self.draw_blocks()

    def show_congratulations_message(self):
        video_path = "TOHFinal.mp4"  # Replace with the actual path to your video
        audio_path = "TOHFinal.mp3"  # Replace with the path to your audio file

        thread = threading.Thread(target=self.play_video_thread, args=(video_path,))
        thread.start()

        self.play_audio(audio_path)

    def play_audio(self, audio_path):
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

    def show_error_message(self, message):
        messagebox.showerror("Error", message)
        self.root.update_idletasks()

    def play_video_thread(self, video_path):
        cap = cv2.VideoCapture(video_path)
        if cap.isOpened():
            video_root = tk.Toplevel()
            video_root.title("Congratulations")

            label = tk.Label(video_root)
            label.pack()

            # Get the screen width and height
            screen_width = video_root.winfo_screenwidth()
            screen_height = video_root.winfo_screenheight()

            # Set the window's position and dimensions to cover the full screen
            video_root.geometry(f"{screen_width}x{screen_height}+0+0")

            def update_video():
                ret, frame = cap.read()
                if ret:
                    label.img = self.cv2_to_tkinter(frame)
                    label.config(image=label.img)
                    video_root.after(30, update_video)
                else:
                    video_root.destroy()

            update_video()
        else:
            self.show_error_message("Failed to open video file.")

    def cv2_to_tkinter(self, frame):
        import PIL.Image, PIL.ImageTk
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(image=img)
        return img

if __name__ == "__main__":
    n = 3
    source_peg = 'A'
    auxiliary_peg = 'B'
    target_peg = 'C'

    root = tk.Tk()

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    x = (screen_width - 600) / 2  # Set the width explicitly
    y = (screen_height - 300) / 2 - 100  # Adjust the value as needed

    # Set the window's position
    root.geometry("+%d+%d" % (x, y))

    game = TowersOfHanoi(root, n, source_peg, auxiliary_peg, target_peg)
    root.mainloop()