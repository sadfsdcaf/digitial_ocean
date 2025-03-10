import streamlit as st
import requests
import yfinance as yf
import os
from dotenv import load_dotenv
import pandas as pd

# Load API Key securely
load_dotenv()
api_token = os.getenv("DIGITALOCEAN_API_KEY")

# Set up request headers
headers = {"Authorization": f"Bearer {api_token}"}

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
        account_response = requests.get(url_account, headers=headers).json()
        st.write("Account API Response:", account_response)  # Debugging

        if "account" in account_response:
            account_data = account_response["account"]
            st.write(f"**Account Email:** {account_data.get('email', 'N/A')}")
            st.write(f"**Droplet Limit:** {account_data.get('droplet_limit', 'N/A')}")
            st.write(f"**Status:** {account_data.get('status', 'N/A')}")
        else:
            st.error("❌ API Error: 'account' key not found.")

        # Fetch droplets
        url_droplets = "https://api.digitalocean.com/v2/droplets"
        droplet_response = requests.get(url_droplets, headers=headers).json()
        st.write("Droplet API Response:", droplet_response)  # Debugging

        if "droplets" in droplet_response and droplet_response["droplets"]:
            droplets = droplet_response["droplets"]
            droplet_data = [
                {
                    "ID": d["id"],
                    "Name": d["name"],
                    "Region": d["region"]["slug"],
                    "IP Address": d["networks"]["v4"][0]["ip_address"] if d["networks"]["v4"] else "N/A",
                    "Status": d["status"],
                    "Created At": d["created_at"],
                }
                for d in droplets
            ]
            df_droplets = pd.DataFrame(droplet_data)
            st.subheader("🖥️ Active Droplets")
            st.dataframe(df_droplets)
        else:
            st.write("No active droplets found or API failed.")

        # Fetch billing information
        url_billing = "https://api.digitalocean.com/v2/customers/my/balance"
        billing_response = requests.get(url_billing, headers=headers).json()
        st.write("Billing API Response:", billing_response)  # Debugging

        if "month_to_date_balance" in billing_response:
            st.subheader("💰 Billing Information")
            st.write(f"**Balance:** ${billing_response['month_to_date_balance']:.2f}")
        else:
            st.error("❌ Billing API Error: Missing balance info.")

    except Exception as e:
        st.error(f"Error fetching API data: {e}")

else:
    st.warning("⚠️ API Key is missing! Please add your DigitalOcean API key.")



### 📌 **3. Fetch DigitalOcean Stock Price**
st.subheader("📈 DigitalOcean Stock Price (Last 1 Month)")

try:
    docn = yf.Ticker("DOCN")
    stock_data = docn.history(period="1mo")
    st.dataframe(stock_data)
except Exception as e:
    st.error(f"Error fetching stock data: {e}")
