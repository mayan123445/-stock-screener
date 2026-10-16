import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Pro AI Stock Screener", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e222d; padding: 10px; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ סורק מניות ומנוע ניתוח AI מתקדם")
st.caption("סריקה חכמה בזמן אמת, ניתוח טכני מפורט וגרפים אינטראקטיביים")

TICKERS = [
    'SGRX', 'XLAB', 'SOUN', 'MARA', 'RIOT', 'LCID', 'NIO', 'BBAI', 
    'AMD', 'NVDA', 'PLTR', 'SMCI', 'TSLA', 'AAPL', 'AMZN', 'GOOGL', 'META', 'MSFT'
]

st.sidebar.header("⚙️ הגדרות סריקה")
min_change = st.sidebar.slider("שינוי מינימלי (%)", 1.0, 15.0, 3.0)
min_vol = st.sidebar.slider("יחס נפח מסחר מינימלי", 1.0, 5.0, 1.2)

if st.button("🔎 הרץ סריקה מקיפה", type="primary", use_container_width=True):
    with st.spinner("סורק את השוק, מנתח נתונים ומפיק גרפים..."):
        matched_stocks = []
        
        for symbol in TICKERS:
            try:
                stock = yf.Ticker(symbol)
                hist = stock.history(period="1y")
                
                if len(hist) >= 20:
                    prev_close = hist['Close'].iloc[-2]
                    curr_price = hist['Close'].iloc[-1]
                    volume = hist['Volume'].iloc[-1]
                    avg_vol_20 = hist['Volume'].iloc[-20:].mean()
                    high_52 = hist['High'].max()
                    low_52 = hist['Low'].min()
                    
                    change_percent = ((curr_price - prev_close) / prev_close) * 100
                    vol_ratio = volume / avg_vol_20 if avg_vol_20 > 0 else 1
                    
                    if change_percent >= min_change and vol_ratio >= min_vol:
                        info = stock.info
                        matched_stocks.append({
                            'symbol': symbol,
                            'price': curr_price,
                            'change': change_percent,
                            'vol_ratio': vol_ratio,
                            'volume': volume,
                            'name': info.get('shortName', symbol),
                            'sector': info.get('sector', 'לא מוגדר'),
                            'summary': info.get('longBusinessSummary', 'אין תיאור זמין.'),
                            'high_52': high_52,
                            'low_52': low_52,
                            'hist': hist
                        })
            except Exception:
                continue

        if matched_stocks:
            st.success(f"🎯 נמצאו {len(matched_stocks)} מניות עונות לקריטריונים!")
            
            for s in matched_stocks:
                with st.expander(f"📌 **{s['symbol']}** | {s['name']} | שינוי: **+{s['change']:.2f}%** | נפח: **{s['vol_ratio']:.1f}x**"):
                    
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("מחיר נוכחי", f"${s['price']:.2f}", f"{s['change']:.2f}%")
                    col2.metric("יחס נפח מסחר", f"{s['vol_ratio']:.1f}x")
                    col3.metric("שיא 52 שבועות", f"${s['high_52']:.2f}")
                    col4.metric("שפל 52 שבועות", f"${s['low_52']:.2f}")
                    
                    st.markdown("---")
                    
                    st.subheader("🤖 ניתוח מנוע AI")
                    ai_analysis = f"""
                    * **מצב מומנטום:** המנייה מציגה פריצה חזקה עם עליה של **{s['change']:.2f}%** ביום המסחר האחרון.
                    * **ניתוח נפח מסחר:** נפח המסחר גדל פי **{s['vol_ratio']:.1f}** מהממוצע ב-20 הימים האחרונים, מה שמעיד על כניסת כסף מוסדי.
                    * **מגזר:** {s['sector']}.
                    """
                    st.markdown(ai_analysis)
                    
                    with st.popover("📖 קרא תיאור חברה מלא"):
                        st.write(s['summary'])
                    
                    st.markdown("---")
                    
                    st.subheader("📈 גרף מחיר אינטראקטיבי")
                    timeframe = st.radio(
                        "בחר פרק זמן לגרף:",
                        ["יומי (חודש אחרון)", "שבועי (חצי שנה)", "חודשי (שנה אחרונה)"],
                        key=f"tf_{s['symbol']}",
                        horizontal=True
                    )
                    
                    df_chart = s['hist'].copy()
                    if timeframe == "יומי (חודש אחרון)":
                        df_chart = df_chart.tail(30)
                    elif timeframe == "שבועי (חצי שנה)":
                        df_chart = df_chart.tail(120)
                    
                    fig = go.Figure(data=[go.Candlestick(
                        x=df_chart.index,
                        open=df_chart['Open'],
                        high=df_chart['High'],
                        low=df_chart['Low'],
                        close=df_chart['Close'],
                        name="מחיר"
                    )])
                    
                    fig.update_layout(
                        template="plotly_dark",
                        xaxis_rangeslider_visible=False,
                        height=400,
                        margin=dict(l=10, r=10, t=10, b=10)
                    )
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("לא נמצאו מניות העונות לקריטריונים. נסה להוריד את רף הגירוי בסרגל הצד.")
