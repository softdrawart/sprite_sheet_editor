import os
import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image #, ImageTk, ImageSequence

class SpriteSheetToGif:
    def __init__(self, root):
        self.root = root
        self.root.title("Sprite Sheet to GIF")

        self.sprite_path = ""
        self.slice_width = tk.IntVar(value=64)
        self.slice_height = tk.IntVar(value=64)
        self.fps = tk.IntVar(value=10)
        self.alpha_enabled = tk.BooleanVar(value=True)
        self.bg_color = "#ffffff"

        self.build_ui()

    def build_ui(self):
        tk.Button(self.root, text="Load Sprite Sheet", command=self.load_image).pack()

        tk.Label(self.root, text="Frame Width").pack()
        tk.Entry(self.root, textvariable=self.slice_width).pack()

        tk.Label(self.root, text="Frame Height").pack()
        tk.Entry(self.root, textvariable=self.slice_height).pack()

        tk.Label(self.root, text="FPS (Frames per second)").pack()
        tk.Entry(self.root, textvariable=self.fps).pack()

        tk.Checkbutton(self.root, text="Enable Transparency (Alpha)", variable=self.alpha_enabled).pack()

        tk.Button(self.root, text="Choose Background Color", command=self.choose_bg_color).pack()

        tk.Button(self.root, text="Export as GIF", command=self.export_gif).pack()
        tk.Button(self.root, text="Export as PNG Frames", command=self.export_png_frames).pack()

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.bmp")])
        if path:
            self.sprite_path = path
            print(f"Loaded sprite sheet: {self.sprite_path}")

    def choose_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.bg_color = color
            print(f"Selected background color: {self.bg_color}")

    def slice_frames(self):
        image = Image.open(self.sprite_path)
        img_w, img_h = image.size
        frame_w = self.slice_width.get()
        frame_h = self.slice_height.get()

        frames = []
        for y in range(0, img_h, frame_h):
            for x in range(0, img_w, frame_w):
                box = (x, y, x + frame_w, y + frame_h)
                frame = image.crop(box)

                if not self.alpha_enabled.get():
                    background = Image.new("RGB", frame.size, self.bg_color)
                    background.paste(frame, mask=frame.split()[3] if frame.mode == 'RGBA' else None)
                    frame = background

                frames.append(frame)

        return frames

    def export_gif(self):
        if not self.sprite_path:
            print("No sprite sheet loaded.")
            return

        frames = self.slice_frames()
        output_path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF files", "*.gif")])
        if output_path:
            duration = int(1000 / self.fps.get())
            frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=duration, loop=0, transparency=0 if self.alpha_enabled.get() else None, disposal=2)
            print(f"GIF exported: {output_path}")

    def export_png_frames(self):
        if not self.sprite_path:
            print("No sprite sheet loaded.")
            return

        frames = self.slice_frames()
        output_dir = filedialog.askdirectory()
        if output_dir:
            for i, frame in enumerate(frames):
                filename = os.path.join(output_dir, f"frame_{i:03d}.png")
                frame.save(filename)
            print(f"{len(frames)} PNG frames exported to: {output_dir}")

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = SpriteSheetToGif(root)
    root.mainloop()
