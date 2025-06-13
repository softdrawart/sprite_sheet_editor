import os
import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk #, ImageSequence
from tkinterdnd2 import DND_FILES, TkinterDnD

IMAGE_EXTENSIONS = ('.png', '.jpeg', '.jpg', '.bmp')
pattern = ';'.join(f'*{ext}' for ext in IMAGE_EXTENSIONS)

class SpriteSheetToGif:

    def __init__(self, root):
        self.root = root
        self.root.title("Sprite Sheet to GIF")

        self.sprite_paths = []
        self.slice_width = tk.IntVar(value=64)
        self.slice_height = tk.IntVar(value=64)
        self.fps = tk.IntVar(value=10)
        self.alpha_enabled = tk.BooleanVar(value=True)
        self.bg_color = "#ffffff"

        self.build_ui()
        self.run_player()

    def run_player(self):
        selected_indicies = self.listbox.curselection()
        if self.sprite_paths and len(selected_indicies)>0:
            #if multiple selected only show first item
            path = self.sprite_paths[selected_indicies]
            if os.path.isfile(path) and path.lower().endswith((IMAGE_EXTENSIONS)):
                image = Image.open(path)
                self.image_tk = ImageTk.PhotoImage(image)

    def build_ui(self):
        #### LOAD IMAGES ####

        tk.Button(self.root, text="Load Sprite Sheet", command=self.load_image).pack()

        self.listbox = tk.Listbox(self.root, width=60, height=6)
        self.listbox.pack()
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.on_drop)
        self.listbox.bind('<Delete>', self.remove_selected_path)
        

        #### PLAYER ####
        self.player = tk.Label(self.root, text="waiting for image...", bg='white', width=200, height=200)
        self.player.pack()
        

        #### PARAMETERS ####
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
#####   EXTRA FUNCTIONS #####
    def slice_frames(self, path):
        image = Image.open(path)
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
        
    def insert_files(self, paths: list[str]):
        for path in paths:
            if os.path.isfile(path) and path.lower().endswith((IMAGE_EXTENSIONS)):
                if path not in self.sprite_paths:
                    self.sprite_paths.append(path)
                    self.listbox.insert(tk.END, os.path.basename(path))

#####   BUTTON FUNCTIONS #####
    def load_image(self):
        paths = self.root.tk.splitlist(filedialog.askopenfilenames(filetypes=[("Image files", pattern)]))
        self.insert_files(paths)

    def remove_selected_path(self, event=None):
        selected_indicies = self.listbox.curselection()
        for index in reversed(selected_indicies):
            self.listbox.delete(index)
            del self.sprite_paths[index]

    def choose_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.bg_color = color
            print(f"Selected background color: {self.bg_color}")

    def on_drop(self, event):
        paths = self.root.tk.splitlist(event.data)
        self.insert_files(paths)
    def on_resize(self, event):
        pass
    def export_gif(self):
        if not self.sprite_paths or len(self.sprite_paths) == 0:
            print("No sprite sheet loaded.")
            return
        for path in self.sprite_paths:
            frames = self.slice_frames(path)
            file_name, _ = os.path.splitext(os.path.basename(path))
            output_path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF files", "*.gif")], initialfile=file_name)
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
    root = TkinterDnD.Tk()
    app = SpriteSheetToGif(root)
    root.mainloop()
