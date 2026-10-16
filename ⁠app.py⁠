import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="AI Stock Screener", page_icon="📈", layout="wide")

st.title("🚀 סורק מניות ומנוע AI")
st.caption("זיהוי מומנטום ונפחי מסחר חריגים בזמן אמת")

TICKERS = [
    'SGRX', 'XLAB', 'SOUN', 'MARA', 'RIOT', 'LCID', 'NIO', 'BBAI', 
    'AMD', 'NVDA', 'PLTR', 'SMCI', 'TSLA', 'AAPL', 'AMZN', 'GOOGL', 'META', 'MSFT'
]

if st.button("🔎 הרץ סריקה עכשיו", type="primary"):
    with st.spinner("סורק את השוק ומחשב נתונים..."):
        results = []
        for symbol in TICKERS:
            try:
                stock = yf.Ticker(symbol)
                hist = stock.history(period="5d")
                
                if len(hist) >= 2:
                    prev_close = hist['Close'].iloc[-2]
                    curr_price = hist['Close'].iloc[-1]
                    volume = hist['Volume'].iloc[-1]
                    avg_vol = hist['Volume'].mean()
                    
                    change_percent = ((curr_price - prev_close) / prev_close) * 100
                    vol_ratio = volume / avg_vol if avg_vol > 0 else 1
                    
                    if change_percent > 3 and vol_ratio > 1.1:
                        signal = "פריצה חדה 🚀" if change_percent > 8 else "מומנטום חיובי 📈"
                        score = 90 if change_percent > 8 else 75
                        
                        results.append({
                            'מניה': symbol,
                            'מחיר ($)': round(curr_price, 2),
                            'שינוי (%)': round(change_percent, 2),
                            'יחס נפח': f"{round(vol_ratio, 1)}x",
                            'אות AI': signal,
                            'ציון': score
                        })
            except Exception:
                continue
                
        if results:
            df = pd.DataFrame(results).sort_values(by='ציון', ascending=False)
            st.success(f"נמצאו {len(df)} מניות במומנטום חיובי!")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("לא נמצאו מניות העונות לקריטריונים כרגע.")
