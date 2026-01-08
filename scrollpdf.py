import streamlit as st
import base64
from streamlit.components.v1 import html

st.set_page_config(layout="wide")
st.title("PDF自動スクロール")

pdf = st.file_uploader("PDFアップロード", type="pdf")
speed = st.slider(
    "スクロール速度(px/秒)",
    1,    # ← 最低 1px/秒
    50,   # ← 最高 50px/秒（楽譜向け）
    10
)


if pdf:
    pdf_base64 = base64.b64encode(pdf.read()).decode()

    html_code = f"""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>

    <style>
        #viewer {{
            height: 90vh;
            overflow-y: scroll;
            background: #111;
            padding: 10px;
        }}

        #controls {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
            display: flex;
            gap: 10px;
        }}

        .btn {{
            background: rgba(0,0,0,0.7);
            color: white;
            border: none;
            padding: 14px 18px;
            font-size: 18px;
            border-radius: 50%;
            cursor: pointer;
        }}

        .btn:active {{
            background: rgba(255,255,255,0.2);
        }}
    </style>

    <div id="viewer"></div>

    <div id="controls">
        <button class="btn" onclick="startScroll()">▶</button>
        <button class="btn" onclick="stopScroll()">⏸</button>
    </div>

    <script>
        const pdfData = atob("{pdf_base64}");
        const loadingTask = pdfjsLib.getDocument({{data: pdfData}});
        const container = document.getElementById("viewer");

        let scrolling = false;
        let speed = {speed} / 10;

        function startScroll() {{
            scrolling = true;
        }}

        function stopScroll() {{
            scrolling = false;
        }}

        loadingTask.promise.then(pdf => {{
            for (let i = 1; i <= pdf.numPages; i++) {{
                pdf.getPage(i).then(page => {{
                    const scale = 1.5;
                    const viewport = page.getViewport({{ scale }});

                    const canvas = document.createElement("canvas");
                    const ctx = canvas.getContext("2d");
                    canvas.width = viewport.width;
                    canvas.height = viewport.height;

                    container.appendChild(canvas);

                    page.render({{
                        canvasContext: ctx,
                        viewport: viewport
                    }});
                }});
            }}
        }});

        setInterval(() => {{
            if (scrolling) {{
                const pxPerTick = {speed} / 10; // 100msごと

setInterval(() => {{
    if (scrolling) {{
        container.scrollBy(0, pxPerTick);
    }}
}}, 100);

            }}
        }}, 100);
    </script>
    """

    html(html_code, height=900)


