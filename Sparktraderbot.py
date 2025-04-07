import streamlit as st
import requests
import datetime

# --- USER CONFIGURABLE ---
TELEGRAM_TOKEN = "7728754112:AAHFMGpaVY1RebbFRxoxkvQfrDbnAQVqYMo"
CHAT_ID = "1110291664"

# --- DASHBOARD UI ---
st.set_page_config(page_title="Angel One Trading Bot", layout="centered")
st.title("Angel One Algo Bot - Mobile Dashboard")

with st.form("trade_form"):
    st.subheader("Trade Settings")
    capital = st.number_input("Per Trade Capital (₹)", value=1000)
    target_percent = st.slider("Target %", 1.0, 10.0, 4.0)
    sl_percent = st.slider("Stop Loss %", 0.5, 5.0, 2.0)
    margin_multiplier = st.selectbox("Margin Multiplier", [1, 2, 5, 10], index=0)
    num_stocks = st.number_input("Max Stocks to Trade", min_value=1, max_value=10, value=3)
    symbols = st.text_input("Enter Stock Symbols (NSE, comma-separated)", value="INFY,SBIN,TCS")
    strategy = st.selectbox("Strategy", ["Buy-Sell at %", "EMA Crossover", "RSI Oversold", "SuperTrend"])
    mode = st.radio("Mode", ["Manual", "Auto"], index=0)
    submit = st.form_submit_button("Run Trade")

# --- MOCK STRATEGY EXECUTION ---
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

def execute_mock_trade():
    stock_list = [s.strip().upper() for s in symbols.split(",")][:num_stocks]
    executed_trades = []
    for stock in stock_list:
        buy_price = 100  # mock price
        target_price = buy_price * (1 + target_percent/100)
        sl_price = buy_price * (1 - sl_percent/100)
        quantity = int((capital * margin_multiplier) / buy_price)
        msg = f"BUY {stock}\nQty: {quantity}\nBuy: ₹{buy_price}\nTarget: ₹{target_price:.2f}\nSL: ₹{sl_price:.2f}"
        send_telegram(msg)
        executed_trades.append((stock, quantity, buy_price, target_price, sl_price))
    return executed_trades

# --- RUN ON SUBMIT ---
if submit:
    with st.spinner("Placing trades..."):
        result = execute_mock_trade()
        st.success("Trade alerts sent!")

        st.subheader("Trade Summary")
        for stock, qty, bp, tp, sl in result:
            st.write(f"**{stock}** | Qty: {qty} | Buy: ₹{bp} | TP: ₹{tp:.2f} | SL: ₹{sl:.2f}")

        st.caption(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
