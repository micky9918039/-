import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="E3選物店-裝箱單", page_icon="📦")
st.title("📦 蝦皮裝箱單自動生成器 (瘦身版)")

# 上傳區
uploaded_file = st.file_uploader("請拖入蝦皮 CSV 訂單檔案", type=['csv'])

if uploaded_file is not None:
    try:
        # 萬能讀取邏輯 (保留防亂碼功能)
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        except:
            try:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='cp950')
            except:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='big5')

        st.success(f"✅ 成功讀取 {len(df)} 筆訂單！")

        # CSS 樣式：寬度限制 + 32px 紅框
        html_content = """<style>
            @media print { 
                .page-break { page-break-after: always; } 
                body { background-color: white; }
                .slip { box-shadow: none !important; margin: 0 !important; width: 100%; }
            }
            body { font-family: "Microsoft JhengHei", sans-serif; background-color: #f0f2f6; padding: 20px; }
            
            /* 這裡控制裝箱單的外觀 */
            .slip { 
                border: 2px solid #000; 
                padding: 40px; 
                margin: 20px auto;       /* 上下留白，左右自動置中 */
                max-width: 700px;        /* <--- 關鍵！限制最大寬度為 700px */
                background-color: white; /* 背景白色 */
                box-shadow: 0 4px 10px rgba(0,0,0,0.1); /* 加點陰影，讓它浮起來像張紙 */
                position: relative; 
            }
            
            .seller-note-box { 
                border: 6px solid red !important; background: #ffe6e6 !important; 
                color: red !important; padding: 15px; font-size: 32px; 
                font-weight: 900; margin-top: 20px; display: inline-block;
                width: 100%; box-sizing: border-box; /* 讓紅框也乖乖待在寬度內 */
            }
            .product-info {
                border: 1px solid #ddd; padding: 15px; background: #f9f9f9; line-height: 1.6;
            }
        </style>"""

        # 產生內容
        for _, row in df.iterrows():
            products = str(row.get('product_info', '')).replace('; ', '<br><br>') # 這裡多加一個 br 讓商品間距大一點，更好讀
            note = str(row.get('seller_note', ''))
            if note == 'nan': note = ''

            slip = f"""
            <div class="slip page-break">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:3px solid #ee4d2d; padding-bottom:10px; margin-bottom:20px;">
                    <h2 style="margin:0; color:#ee4d2d;">E3 選物店</h2>
                    <span style="font-size:14px; color:#666;">裝箱單</span>
                </div>
                <p><strong>訂單編號:</strong> {row.get('order_sn', '未知')}</p>
                <div class="product-info">{products}</div>
                <div class="seller-note-box">賣家備註：{note}</div>
                <div style="margin-top:20px; text-align:center; color:#999; font-size:12px;">全台唯一最多元牌尺品牌</div>
            </div>"""
            html_content += slip

        # 下載按鈕
        b64 = base64.b64encode(html_content.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="E3裝箱單_窄版.html"><button style="background-color:#ee4d2d;color:white;padding:15px 30px;border:none;border-radius:5px;cursor:pointer;font-size:18px;font-weight:bold;">📥 下載列印檔 (窄版)</button></a>'
        st.markdown(href, unsafe_allow_html=True)
        
        # 直接在網頁上預覽第一張單子的樣子 (讓您確認寬度)
        st.markdown("### 👀 裝箱單預覽 (第一筆)")
        st.components.v1.html(html_content.split('<div class="slip page-break">')[1].split('<div class="slip page-break">')[0].replace('</div>', '</div></div>'), height=600, scrolling=True)

    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
