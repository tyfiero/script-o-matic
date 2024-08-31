import tkinter as tk
from tkinter import colorchooser, filedialog
import math
class EmojiKaleidoscope(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Emoji Kaleidoscope Art")
        self.geometry("800x600")
        self.configure(bg="black")
        # Create a canvas to draw the kaleidoscope
        self.canvas = tk.Canvas(self, width=600, height=600, bg="black", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        # Create a frame for controls
        controls_frame = tk.Frame(self, bg="black")
        controls_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH)
        # Create a label and entry for the emoji
        emoji_label = tk.Label(controls_frame, text="Enter Emoji:", fg="white", bg="black")
        emoji_label.pack(pady=5)
        self.emoji_entry = tk.Entry(controls_frame, font=("Arial", 20), justify="center")
        self.emoji_entry.pack(pady=5)
        # Create a button to choose the emoji color
        self.emoji_color = "yellow"
        choose_color_button = tk.Button(controls_frame, text="Choose Color", command=self.choose_color, fg="white", bg="black")
        choose_color_button.pack(pady=5)
        # Create sliders for rotation and shift
        rotation_label = tk.Label(controls_frame, text="Rotation:", fg="white", bg="black")
        rotation_label.pack(pady=5)
        self.rotation_slider = tk.Scale(controls_frame, from_=0, to=360, orient=tk.HORIZONTAL, fg="white", bg="black")
        self.rotation_slider.pack(pady=5)
        shift_label = tk.Label(controls_frame, text="Shift:", fg="white", bg="black")
        shift_label.pack(pady=5)
        self.shift_slider = tk.Scale(controls_frame, from_=0, to=200, orient=tk.HORIZONTAL, fg="white", bg="black")
        self.shift_slider.pack(pady=5)
        # Create a button to save the pattern
        save_button = tk.Button(controls_frame, text="Save Pattern", command=self.save_pattern, fg="white", bg="black")
        save_button.pack(pady=5)
        # Set initial values
        self.emoji_entry.insert(0, "🌺")
        self.rotation_slider.set(0)
        self.shift_slider.set(0)
        # Bind events
        self.emoji_entry.bind("<Return>", self.update_pattern)
        self.rotation_slider.bind("<B1-Motion>", self.update_pattern)
        self.shift_slider.bind("<B1-Motion>", self.update_pattern)
        # Draw the initial pattern
        self.draw_pattern()
    def choose_color(self):
        """Opens a color chooser dialog and updates the emoji color."""
        color = colorchooser.askcolor(title="Choose Emoji Color")[1]
        if color:
            self.emoji_color = color
            self.draw_pattern()
    def draw_pattern(self):
        """Draws the kaleidoscope pattern on the canvas."""
        self.canvas.delete("all")
        emoji = self.emoji_entry.get()
        rotation = self.rotation_slider.get()
        shift = self.shift_slider.get()
        for x in range(0, 600, 50):
            for y in range(0, 600, 50):
                # Calculate the rotated and shifted position
                rotated_x = x * math.cos(math.radians(rotation)) - y * math.sin(math.radians(rotation))
                rotated_y = x * math.sin(math.radians(rotation)) + y * math.cos(math.radians(rotation))
                shifted_x = rotated_x + shift
                shifted_y = rotated_y + shift
                # Draw the emoji at the rotated and shifted position
                self.canvas.create_text(shifted_x, shifted_y, text=emoji, fill=self.emoji_color, font=("Arial", 20))
    def update_pattern(self, event=None):
        """Updates the kaleidoscope pattern based on user input."""
        self.draw_pattern()
    def save_pattern(self):
        """Saves the current pattern as an image file."""
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
            if file_path:
                x = self.winfo_rootx() + self.canvas.winfo_x()
                y = self.winfo_rooty() + self.canvas.winfo_y()
                x1 = x + self.canvas.winfo_width()
                y1 = y + self.canvas.winfo_height()
                image = tk.PhotoImage(subsample=2)
                canvas = tk.Canvas(width=self.canvas.winfo_width(), height=self.canvas.winfo_height(), bg="black")
                self.canvas.create_image(0, 0, image=image, anchor=tk.NW)
                canvas.pack()
                canvas.postscript(file=file_path, colormode="color", x=x, y=y, width=x1-x, height=y1-y)
                canvas.destroy()
        except Exception as e:
            print(f"Error saving pattern: {e}")
if __name__ == "__main__":
    app = EmojiKaleidoscope()
    app.mainloop()