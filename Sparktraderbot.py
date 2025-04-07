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

# Dashboard title
st.set_page_config(page_title="SparkTraderBot", layout="wide")
st.title("SparkTraderBot - Live Trading Dashboard")

# Section: Account & Risk Settings
st.sidebar.header("Trade Configuration")

capital_per_trade = st.sidebar.number_input("Capital per Trade (₹)", min_value=100, max_value=100000, value=1000, step=100)
stop_loss_percent = st.sidebar.slider("Stop Loss (%)", 0.1, 10.0, 2.0)
target_percent = st.sidebar.slider("Target (%)", 0.1, 10.0, 4.0)
margin = st.sidebar.number_input("Margin Multiplier", min_value=1.0, max_value=10.0, value=1.0, step=0.1)
num_stocks = st.sidebar.number_input("Number of Stocks", min_value=1, max_value=20, value=1)

# Indicator Selection
st.sidebar.subheader("Indicators")
indicator = st.sidebar.selectbox("Select Indicator", ["None", "RSI", "MACD", "EMA", "VWAP"])

# Strategy Mode
strategy = st.sidebar.selectbox("Strategy Type", ["Breakout", "Reversal", "Momentum", "Custom"])

# Symbol input
symbol = st.text_input("Enter Symbol (e.g., RELIANCE)", "RELIANCE")

# Mock Price Fetching - Replace with actual API call later
mock_price = 2725.50
st.metric(label=f"Live Price - {symbol.upper()}", value=f"₹{mock_price}")

# Trade calculation
stop_loss_price = mock_price - (mock_price * stop_loss_percent / 100)
target_price = mock_price + (mock_price * target_percent / 100)
qty = int((capital_per_trade * margin) // mock_price)

st.write(f"**Buy Qty:** {qty} shares at ₹{mock_price}")
st.write(f"**Stop Loss Price:** ₹{round(stop_loss_price, 2)}")
st.write(f"**Target Price:** ₹{round(target_price, 2)}")

# Telegram Alert Simulation (replace with actual token/chat_id)
if st.button("Send Alert to Telegram"):
    token = "YOUR_TELEGRAM_BOT_TOKEN"
    chat_id = "YOUR_CHAT_ID"
    message = f"""
    SparkTraderBot Alert:
    Symbol: {symbol}
    Strategy: {strategy}
    Indicator: {indicator}
    Entry: ₹{mock_price}
    Stop Loss: ₹{round(stop_loss_price, 2)}
    Target: ₹{round(target_price, 2)}
    Qty: {qty}
    """
    try:
        requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}")
        st.success("Telegram alert sent!")
    except:
        st.error("Failed to send Telegram alert.")

# Footer
st.caption("Built with Streamlit - Updated for Mobile Trading")
