import os
import base64

def generate_svg_animation(png_folder, output_svg_path, frame_duration=500):
    png_files = sorted(
        [f for f in os.listdir(png_folder) if f.lower().endswith('.png')]
    )

    if not png_files:
        print("No PNG files found in the directory.")
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

    print(f"SVG animation saved to {output_svg_path}")

# 🔽 مسیر پوشه PNG و مسیر فایل خروجی رو اینجا وارد کن:
generate_svg_animation("my_pngs", "loop.svg", frame_duration=300)