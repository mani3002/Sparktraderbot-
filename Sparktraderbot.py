import streamlit as st

# Page configuration must come first
st.set_page_config(page_title="SparkTraderBot", layout="wide")

from angelone import SmartConnect
import pandas as pd
import datetime
import pytz
import requests

# UI Controls
st.title("SparkTraderBot")
st.markdown("## Algo Trading Bot Dashboard")

api_key = st.text_input("API Key", type="password")
client_id = st.text_input("Client ID")
password = st.text_input("Password", type="password")
totp = st.text_input("TOTP", type="password", help="If TOTP is not enabled, leave this blank")

run_trade = st.button("Run Trade")

# Constants
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

# Define telegram function
def telegram_alert(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    requests.get(url)

# Trading logic
def trade():
    try:
        obj = SmartConnect(api_key=api_key)
        if totp:
            data = obj.generateSession(client_id, password, totp)
        else:
            data = obj.generateSession(client_id, password)

        refreshToken = data['data']['refreshToken']
        res = obj.getProfile(refreshToken)

        st.success("Login Successful!")
        telegram_alert("SparkTraderBot Login Successful!")

        # Sample logic (replace with your strategy)
        st.info("Running sample trade logic...")

        # Example: Get holdings or positions
        holdings = obj.holding()
        st.write("Holdings:", holdings)

    except Exception as e:
        st.error(f"Login Failed: {e}")
        telegram_alert(f"SparkTraderBot Login Failed: {e}")

if run_trade:
    trade()
