import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="E3選物店-自動裝箱單", page_icon="📦")
st.title("📦 蝦皮裝箱單自動生成器")

# 上傳區
file = st.file_uploader("請拖入蝦皮下載的 CSV 檔案", type=['csv'])

if file:
    df = pd.read_csv(file)
    st.success(f"已讀取 {len(df)} 筆訂單")
    
    # CSS 樣式：定義 32px 紅框
    html_content = """<style>
        @media print { .page-break { page-break-after: always; } }
        body { font-family: sans-serif; }
        .slip { border: 2px solid #000; padding: 20px; margin-bottom: 20px; position: relative; }
        .seller-note { 
            border: 6px solid red !important; background: #ffe6e6 !important; 
            color: red !important; padding: 15px; font-size: 32px; 
            font-weight: bold; margin-top: 15px; display: inline-block;
        }
    </style>"""

    for _, row in df.iterrows():
        products = str(row['product_info']).replace('; ', '<br>')
        slip = f"""
        <div class="slip page-break">
            <h2>E3 選物店 裝箱單</h2>
            <p>訂單編號: {row['order_sn']}</p>
            <div style="border: 1px solid #ddd; padding: 10px;">{products}</div>
            <div class="seller-note">賣家備註：{row['seller_note']}</div>
        </div>"""
        html_content += slip

    # 下載按鈕
    b64 = base64.b64encode(html_content.encode()).decode()
    st.markdown(f'<a href="data:text/html;base64,{b64}" download="裝箱單.html"><button style="background:#ee4d2d;color:white;padding:10px;border:none;border-radius:5px;cursor:pointer;">📥 下載紅框列印檔</button></a>', unsafe_allow_html=True)