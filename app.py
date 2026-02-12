import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="E3選物店-裝箱單", page_icon="📦")
st.title("📦 蝦皮裝箱單自動生成器 (萬能讀取版)")

# 上傳區
uploaded_file = st.file_uploader("請拖入蝦皮 CSV 訂單檔案", type=['csv'])

if uploaded_file is not None:
    try:
        # 嘗試 1：用標準 UTF-8 讀取
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except:
        try:
            # 嘗試 2：用 CP950 (繁體中文 Big5) 讀取 <--- 這是專門為蝦皮加的！
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding='cp950')
        except:
            # 嘗試 3：用 Big5 讀取
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding='big5')

    st.success(f"✅ 成功讀取 {len(df)} 筆訂單！")

    # 建立紅框裝箱單樣式
    html_content = """<style>
        @media print { .page-break { page-break-after: always; } }
        body { font-family: "Microsoft JhengHei", sans-serif; padding: 20px; }
        .slip { border: 2px solid #000; padding: 20px; margin-bottom: 30px; position: relative; }
        .seller-note-box { 
            border: 6px solid red !important; background: #ffe6e6 !important; 
            color: red !important; padding: 15px; font-size: 32px; 
            font-weight: 900; margin-top: 20px; display: inline-block;
        }
    </style>"""

    # 產生內容
    for _, row in df.iterrows():
        # 處理可能的空值
        products = str(row.get('product_info', '')).replace('; ', '<br>')
        note = str(row.get('seller_note', ''))
        if note == 'nan': note = ''

        slip = f"""
        <div class="slip page-break">
            <h2 style="color:#ee4d2d;">E3 選物店 - 裝箱單</h2>
            <p><strong>訂單編號:</strong> {row.get('order_sn', '未知')}</p>
            <div style="border:1px solid #ddd; padding:10px;">{products}</div>
            <div class="seller-note-box">賣家備註：{note}</div>
        </div>"""
        html_content += slip

    # 下載按鈕
    b64 = base64.b64encode(html_content.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="紅框裝箱單.html"><button style="background-color:#ee4d2d;color:white;padding:15px;border:none;border-radius:5px;cursor:pointer;font-size:20px;">📥 點我下載列印檔</button></a>'
    st.markdown(href, unsafe_allow_html=True)
