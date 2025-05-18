import os
import base64
import io
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox
from PIL import Image

def resize_and_generate_svg(png_folder, output_file, frame_duration, scale_percent):
    files = sorted(f for f in os.listdir(png_folder) if f.lower().endswith(".png"))
    if not files:
        messagebox.showerror("Error", "No PNG files found.")
        return

    encoded_images = []
    width, height = None, None

    for file in files:
        img_path = os.path.join(png_folder, file)
        with Image.open(img_path) as img:
            img = img.convert("RGBA")
            w, h = img.size
            w = int(w * scale_percent / 100)
            h = int(h * scale_percent / 100)
            img = img.resize((w, h), Image.LANCZOS)

            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
            encoded_images.append(encoded)

            if width is None:
                width, height = w, h

    with open(output_file, "w") as f:
        f.write(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
.frame {{ display: none; }}
.active {{ display: block; }}
</style>
<script><![CDATA[
let i = 0;
const frames = [];
window.onload = function () {{
    for (let j = 0; j < {len(encoded_images)}; j++) {{
        frames.push(document.getElementById("f" + j));
    }}
    function loop() {{
        frames.forEach(f => f.setAttribute("class", "frame"));
        frames[i].setAttribute("class", "frame active");
        i = (i + 1) % frames.length;
    }}
    setInterval(loop, {frame_duration});
    loop();
}};
]]></script>
''')
        for idx, data in enumerate(encoded_images):
            f.write(f'<image id="f{idx}" class="frame" width="{width}" height="{height}" href="data:image/png;base64,{data}"/>\n')
        f.write("</svg>")
    messagebox.showinfo("Done", f"Saved to {output_file}")

def browse_folder():
    path = filedialog.askdirectory()
    if path:
        folder_entry.delete(0, "end")
        folder_entry.insert(0, path)

def browse_output():
    path = filedialog.asksaveasfilename(defaultextension=".svg")
    if path:
        output_entry.delete(0, "end")
        output_entry.insert(0, path)

def start():
    folder = folder_entry.get()
    output = output_entry.get()
    try:
        duration = int(duration_entry.get())
        scale = int(scale_entry.get())
        if scale <= 0:
            raise ValueError
    except:
        messagebox.showerror("Error", "Invalid duration or scale.")
        return
    resize_and_generate_svg(folder, output, duration, scale)

# UI
root = Tk()
root.title("SVG Animator")

Label(root, text="PNG Folder:").grid(row=0, column=0)
folder_entry = Entry(root, width=40)
folder_entry.grid(row=0, column=1)
Button(root, text="Browse", command=browse_folder).grid(row=0, column=2)

Label(root, text="Output SVG:").grid(row=1, column=0)
output_entry = Entry(root, width=40)
output_entry.grid(row=1, column=1)
Button(root, text="Browse", command=browse_output).grid(row=1, column=2)

Label(root, text="Frame Duration (ms):").grid(row=2, column=0)
duration_entry = Entry(root)
duration_entry.insert(0, "300")
duration_entry.grid(row=2, column=1)

Label(root, text="Scale (%):").grid(row=3, column=0)
scale_entry = Entry(root)
scale_entry.insert(0, "100")
scale_entry.grid(row=3, column=1)

Button(root, text="Generate SVG", command=start, bg="green", fg="white").grid(row=4, column=1, pady=10)

root.mainloop()
