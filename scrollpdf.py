import streamlit as st
import base64
from streamlit.components.v1 import html

st.set_page_config(layout="wide")
st.title("🎸 楽譜用 PDF 自動スクロール")

pdf = st.file_uploader("PDFアップロード", type="pdf")

speed = st.slider("スクロール速度(px/秒)", 10, 300, 80)
start_pos = st.number_input(
    "スクロール開始位置(px)",
    min_value=0,
    value=0,
    step=100
)

play = st.button("▶ 再生")
pause = st.button("⏸ 停止")
jump = st.button("⤵ 開始位置へ移動")

if pdf:
    pdf_base64 = base64.b64encode(pdf.read()).decode()

    play_js = "true" if play else "false"
    pause_js = "true" if pause else "false"
    jump_js = "true" if jump else "false"

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

    let scrolling = false;

    // ▶ 再生
    if ({play_js}) {{
        scrolling = true;
    }}

    // ⏸ 停止
    if ({pause_js}) {{
        scrolling = false;
    }}

    // ⤵ 開始位置ジャンプ
    if ({jump_js}) {{
        container.scrollTop = {start_pos};
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
            container.scrollBy(0, {speed} / 10);
        }}
    }}, 100);
    </script>
    """

    html(html_code, height=900)
