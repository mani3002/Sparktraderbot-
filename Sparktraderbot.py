import streamlit as st

# Set this as the FIRST Streamlit command
st.set_page_config(page_title="SparkTraderBot", layout="wide")

# Imports
from SmartApi import SmartConnect
import pandas as pd
import datetime
import pytz
import requests

# --- Config ---
API_KEY = "smartapi-key-dh1Js5Nc"
CLIENT_ID = "E57123237"
PIN = "2603"
TOTP = ""  # You mentioned TOTP is not used
TOKEN = "6965075156:AAGnzYQy6AiJ3TcmVRAAyA23oQQU7zttTxI"
CHAT_ID = "5232913886"

# --- Telegram Alert ---
def telegram_alert(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    try:
        requests.get(url)
    except Exception as e:
        st.warning(f"Telegram alert failed: {e}")

# --- UI ---
st.title("SparkTraderBot")
st.markdown("## Algo Trading Bot Dashboard")

run_trade = st.button("Run Trade")

# --- Trade Logic ---
def trade():
    try:
        obj = SmartConnect(api_key=API_KEY)
        data = obj.generateSession(CLIENT_ID, PIN)

        refreshToken = data['data']['refreshToken']
        res = obj.getProfile(refreshToken)

        st.success("Login Successful!")
        telegram_alert("SparkTraderBot Login Successful!")

        # Show holdings
        holdings = obj.holding()
        st.write("Holdings:", holdings)

    except Exception as e:
        st.error(f"Login Failed: {e}")
        telegram_alert(f"Login Failed: {e}")

if run_trade:
    trade()
