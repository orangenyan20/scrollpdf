import streamlit as st
import base64
from streamlit.components.v1 import html

st.set_page_config(layout="wide")
st.title("PDF 自動スクロールビューア")

uploaded_file = st.file_uploader("PDFをアップロード", type="pdf")

scroll_speed = st.slider(
    "スクロール速度（px / 秒）",
    min_value=10,
    max_value=300,
    value=60,
    step=10
)

start = st.button("▶ 自動スクロール開始")
stop = st.button("■ 停止")

if uploaded_file:
    # PDFをbase64に変換
    pdf_bytes = uploaded_file.read()
    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

    # JS制御用フラグ
    auto_scroll = "true" if start else "false"
    stop_scroll = "true" if stop else "false"

    html_code = f"""
    <html>
    <head>
        <style>
            body {{
                margin: 0;
            }}
            iframe {{
                width: 100%;
                height: 90vh;
                border: none;
            }}
        </style>
    </head>
    <body>
        <iframe id="pdfFrame"
            src="data:application/pdf;base64,{pdf_base64}">
        </iframe>

        <script>
            let scrolling = false;
            let speed = {scroll_speed} / 10;

            if ({auto_scroll}) {{
                scrolling = true;
            }}
            if ({stop_scroll}) {{
                scrolling = false;
            }}

            function autoScroll() {{
                if (scrolling) {{
                    window.scrollBy(0, speed);
                }}
            }}

            setInterval(autoScroll, 100);
        </script>
    </body>
    </html>
    """

    html(html_code, height=900)

