import streamlit as st
import requests

# Fetch DigitalOcean Service Status
url = "https://status.digitalocean.com/api/v2/status.json"
response = requests.get(url)
status = response.json()

# Display in Streamlit
st.title("DigitalOcean Status Checker")
st.write(f"Overall Status: {status['status']['description']}")

# Fetch Stock Data
import yfinance as yf
docn = yf.Ticker("DOCN")
data = docn.history(period="1mo")

# Display stock data in a table
st.subheader("DigitalOcean Stock Price (Last 1 Month)")
st.dataframe(data)
