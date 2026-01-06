import streamlit as st
import base64
from streamlit.components.v1 import html

st.set_page_config(layout="wide")
st.title("PDF自動スクロール")

pdf = st.file_uploader("PDFアップロード", type="pdf")
speed = st.slider("スクロール速度(px/秒)", 10, 300, 80)

start = st.button("▶ 再生")
stop = st.button("⏸ 停止")

if pdf:
    pdf_base64 = base64.b64encode(pdf.read()).decode()

    auto = "true" if start else "false"
    stopf = "true" if stop else "false"

    html_code = f"""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>

    <div id="viewer" style="
        height:90vh;
        overflow-y:scroll;
        background:#111;
        padding:10px;
    "></div>

    <script>
    const pdfData = atob("{pdf_base64}");
    const loadingTask = pdfjsLib.getDocument({{data: pdfData}});
    const container = document.getElementById("viewer");

    let scrolling = {auto};
    if ({stopf}) scrolling = false;

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
            container.scrollBy(0, {speed}/10);
        }}
    }}, 100);
    </script>
    """

    html(html_code, height=900)
