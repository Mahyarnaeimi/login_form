import os
import base64
import tkinter as tk
from tkinter import filedialog, messagebox

def generate_svg_animation(png_folder, output_svg_path, frame_duration=500):
    png_files = sorted(
        [f for f in os.listdir(png_folder) if f.lower().endswith('.png')]
    )

    if not png_files:
        messagebox.showerror("Error", "No PNG files found in the selected folder.")
        return

    images_data = []
    for filename in png_files:
        with open(os.path.join(png_folder, filename), "rb") as f:
            b64_data = base64.b64encode(f.read()).decode('utf-8')
            images_data.append(b64_data)

    width = 512
    height = 512

    with open(output_svg_path, "w") as svg:
        svg.write(f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
    .frame {{ display: none; }}
    .frame.active {{ display: block; }}
</style>
<script><![CDATA[
    let current = 0;
    const frames = [];
    window.addEventListener("load", () => {{
        for (let i = 0; i < {len(images_data)}; i++) {{
            frames.push(document.getElementById("frame" + i));
        }}
        function loop() {{
            frames.forEach(f => f.setAttribute("class", "frame"));
            frames[current].setAttribute("class", "frame active");
            current = (current + 1) % frames.length;
        }}
        setInterval(loop, {frame_duration});
        loop();
    }});
]]></script>
""")
        for i, b64_img in enumerate(images_data):
            svg.write(f'<image id="frame{i}" class="frame" width="{width}" height="{height}" href="data:image/png;base64,{b64_img}"/>\n')
        svg.write("</svg>")

    messagebox.showinfo("Done", f"SVG animation saved to:\n{output_svg_path}")

# ---------- رابط گرافیکی با tkinter ----------
def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder)

def save_as():
    file = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("SVG files", "*.svg")])
    if file:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file)

def start():
    folder = folder_entry.get()
    output = output_entry.get()
    try:
        duration = int(duration_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Frame duration must be an integer (ms)")
        return

    if not os.path.isdir(folder):
        messagebox.showerror("Error", "Please select a valid PNG folder.")
        return
    if not output:
        messagebox.showerror("Error", "Please select a valid output SVG file.")
        return

    generate_svg_animation(folder, output, duration)

# ---------- طراحی رابط ----------
root = tk.Tk()
root.title("SVG Animation Maker")

tk.Label(root, text="PNG Folder:").grid(row=0, column=0, sticky="e")
folder_entry = tk.Entry(root, width=50)
folder_entry.grid(row=0, column=1)
tk.Button(root, text="Browse", command=browse_folder).grid(row=0, column=2)

tk.Label(root, text="Output SVG:").grid(row=1, column=0, sticky="e")
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1)
tk.Button(root, text="Save As", command=save_as).grid(row=1, column=2)

tk.Label(root, text="Frame Duration (ms):").grid(row=2, column=0, sticky="e")
duration_entry = tk.Entry(root, width=10)
duration_entry.insert(0, "300")
duration_entry.grid(row=2, column=1, sticky="w")

tk.Button(root, text="Generate SVG", command=start, bg="green", fg="white").grid(row=3, column=1, pady=10)

root.mainloop()
