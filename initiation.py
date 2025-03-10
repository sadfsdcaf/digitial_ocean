import streamlit as st
import requests
import yfinance as yf
import os
from dotenv import load_dotenv
import pandas as pd

# Load API Key from environment variable or .env file
load_dotenv()
api_token = "dop_v1_f78e2f80785703b9ed54b41c412c8ea0cf2b1926563de3ca65f2005e0bb33002"

# Set up request headers
headers = {"Authorization": f"Bearer {api_token}"}

# Streamlit App Title
st.title("🔹 DigitalOcean Dashboard")

### 📌 **1. Fetch DigitalOcean Service Status**
st.subheader("🔹 DigitalOcean Service Status")

try:
    url_status = "https://status.digitalocean.com/api/v2/status.json"
    response = requests.get(url_status)
    status = response.json()
    st.write(f"Current Status: **{status['status']['description']}**")
except Exception as e:
    st.error(f"Error fetching service status: {e}")



### 📌 **2. Fetch DigitalOcean API Data**
if api_token:
    st.subheader("🔹 DigitalOcean API Data")

    try:
        # Fetch account details
        url_account = "https://api.digitalocean.com/v2/account"
        account_data = requests.get(url_account, headers=headers).json()["account"]
        st.write(f"**Account Email:** {account_data['email']}")
        st.write(f"**Droplet Limit:** {account_data['droplet_limit']}")
        st.write(f"**Status:** {account_data['status']}")

        # Fetch all droplets
        url_droplets = "https://api.digitalocean.com/v2/droplets"
        droplets = requests.get(url_droplets, headers=headers).json()["droplets"]

        if droplets:
            droplet_data = []
            for droplet in droplets:
                droplet_data.append({
                    "ID": droplet["id"],
                    "Name": droplet["name"],
                    "Region": droplet["region"]["slug"],
                    "IP Address": droplet["networks"]["v4"][0]["ip_address"] if droplet["networks"]["v4"] else "N/A",
                    "Status": droplet["status"],
                    "Created At": droplet["created_at"]
                })

            df_droplets = pd.DataFrame(droplet_data)
            st.subheader("🖥️ Active Droplets")
            st.dataframe(df_droplets)
        else:
            st.write("No active droplets found.")

        # Fetch billing information
        url_billing = "https://api.digitalocean.com/v2/customers/my/balance"
        billing_data = requests.get(url_billing, headers=headers).json()
        st.subheader("💰 Billing Information")
        st.write(f"**Balance:** ${billing_data['month_to_date_balance']:.2f}")
        st.write(f"**Month to Date Usage:** ${billing_data['month_to_date_usage']:.2f}")

    except Exception as e:
        st.error(f"Error fetching API data: {e}")

else:
    st.warning("⚠️ API Key is missing! Please add your DigitalOcean API key.")

---

### 📌 **3. Fetch DigitalOcean Stock Price**
st.subheader("📈 DigitalOcean Stock Price (Last 1 Month)")

try:
    docn = yf.Ticker("DOCN")
    stock_data = docn.history(period="1mo")
    st.dataframe(stock_data)
except Exception as e:
    st.error(f"Error fetching stock data: {e}")
