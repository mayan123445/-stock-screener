import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# הגדרת תצורת העמוד
st.set_page_config(
    page_title="StockAI - סורק המניות החכם שלך", 
    page_icon="🚀", 
    layout="wide"
)

# עיצוב מותאם אישית - שמח, חגיגי ומודרני
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .welcome-card {
        background: linear-gradient(135deg, #1e2640 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #3b82f6;
        margin-bottom: 25px;
    }
    .stMetric { 
        background-color: #1e222d; 
        padding: 12px; 
        border-radius: 10px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# כותרת מזמינה ושמחה
st.title("🚀 StockAI - המצפן שלך בשוק ההון!")
st.markdown("""
<div class="welcome-card">
    <h3>👋 ברוכים הבאים לסורק המניות והניתוח החכם!</h3>
    <p>רוצים למצוא את ההזדמנויות החמות בשוק עוד לפני כולם? המערכת שלנו סורקת את השוק בזמן אמת, מזהה מניות במומנטום חריג, ומצליבה נתונים טכניים עם <b>צפי אנליסטים בוול סטריט</b>.</p>
    <p>💡 <i>טיפ: השתמשו בסרגל הצד כדי להתאים את רגישות הסריקה בדיוק לרצון שלכם!</i></p>
</div>
""", unsafe_allow_html=True)

# רשימת מניות לסריקה
TICKERS = [
    'SGRX', 'XLAB', 'SOUN', 'MARA', 'RIOT', 'LCID', 'NIO', 'BBAI', 
    'AMD', 'NVDA', 'PLTR', 'SMCI', 'TSLA', 'AAPL', 'AMZN', 'GOOGL', 'META', 'MSFT'
]

# סרגל צדדי מעוצב
st.sidebar.header("⚙️ מרכז שליטה והגדרות")
st.sidebar.write("התאימו את קריטריוני הסריקה:")
min_change = st.sidebar.slider("🔥 שינוי מחיר מינימלי (%)", 1.0, 15.0, 3.0)
min_vol = st.sidebar.slider("📊 יחס נפח מסחר מינימלי (פי כמה מהממוצע)", 1.0, 5.0, 1.2)

# כפתור הפעלה שמח ובולט
if st.button("🌟 הרץ סריקה חכמה עכשיו!", type="primary", use_container_width=True):
    with st.spinner("🔍 סורק את השוק, מנתח נתוני אנליסטים ומפיק גרפים..."):
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
                        
                        # שליפת נתוני אנליסטים
                        target_price = info.get('targetMeanPrice', None)
                        recommendation = info.get('recommendationKey', 'N/A').replace('_', ' ').title()
                        
                        upside = None
                        if target_price and curr_price > 0:
                            upside = ((target_price - curr_price) / curr_price) * 100
                        
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
                            'target_price': target_price,
                            'recommendation': recommendation,
                            'upside': upside,
                            'hist': hist
                        })
            except Exception:
                continue

        if matched_stocks:
            st.balloons()  # חגיגת בלונים כשמוצאים מניות!
            st.success(f"🎉 איזה יופי! נמצאו {len(matched_stocks)} מניות חמות שעונות לקריטריונים שלך!")
            
            for s in matched_stocks:
                # כרטיסיה נפתחת מפורטת
                with st.expander(f"📌 **{s['symbol']}** | {s['name']} | עליה של **+{s['change']:.2f}%** 🚀 | נפח: **{s['vol_ratio']:.1f}x**"):
                    
                    # מדדים מרכזיים
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("מחיר נוכחי", f"${s['price']:.2f}", f"{s['change']:.2f}%")
                    col2.metric("יחס נפח מסחר", f"{s['vol_ratio']:.1f}x")
                    col3.metric("שיא 52 שבועות", f"${s['high_52']:.2f}")
                    col4.metric("שפל 52 שבועות", f"${s['low_52']:.2f}")
                    
                    st.markdown("---")
                    
                    # חלק צפי אנליסטים
                    st.subheader("🎯 צפי ותחזית אנליסטים (וול סטריט)")
                    acol1, acol2, acol3 = st.columns(3)
                    
                    if s['target_price']:
                        acol1.metric("מחיר יעד ממוצע", f"${s['target_price']:.2f}")
                    else:
                        acol1.metric("מחיר יעד ממוצע", "אין נתון")
                        
                    if s['upside'] is not None:
                        acol2.metric("פוטנציאל שינוי (Upside)", f"{s['upside']:.1f}%")
                    else:
                        acol2.metric("פוטנציאל שינוי", "אין נתון")
                        
                    acol3.metric("המלצת קונצנזוס", f"⭐ {s['recommendation']}")
                    
                    st.markdown("---")
                    
                    # ניתוח AI מפורט ומזמין
                    st.subheader("🤖 ניתוח מנוע ה-AI שלנו")
                    ai_text = f"""
                    * **ניתוח מומנטום:** המנייה טסה למעלה עם עליה מרשימה של **{s['change']:.2f}%**!
                    * **זיהוי כסף כבד (נפח מסחר):** נפח המסחר כעת גבוה פי **{s['vol_ratio']:.1f}** מהממוצע, מה שמתרחש בדרך כלל כשגופים מוסדיים נכנסים לפוזיציה.
                    * **תחום פופולרי:** מיוחסת למגזר ה-**{s['sector']}**.
                    """
                    st.markdown(ai_text)
                    
                    with st.popover("📖 קרא עוד על החברה ופועלה"):
                        st.write(s['summary'])
                    
                    st.markdown("---")
                    
                    # גרף מחירים
                    st.subheader("📈 גרף נרות יפניים אינטראקטיבי")
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
            st.info("😊 לא נמצאו מניות העונות בדיוק לקריטריונים האלה כרגע. נסו להוריד מעט את רף השינוי בסרגל הצד!")
