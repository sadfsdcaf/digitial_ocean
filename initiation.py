import yfinance as yf
import pandas as pd
import ace_tools as tools

# Fetch financial data for DigitalOcean (DOCN)
ticker = "DOCN"
docn = yf.Ticker(ticker)

# Get balance sheet & income statement data
balance_sheet = docn.balance_sheet
income_statement = docn.financials

# Transpose to align years correctly
balance_sheet = balance_sheet.T
income_statement = income_statement.T

# Extract relevant data
balance_metrics = ["Total Assets", "Total Liabilities Net Minority Interest", "Total Equity Gross Minority Interest"]
income_metrics = ["Total Revenue", "EBIT", "EBITDA"]

balance_data = balance_sheet[balance_metrics]
income_data = income_statement[income_metrics]

# Merge datasets
financial_data = pd.concat([balance_data, income_data], axis=1)

# Function to calculate CAGR
def calculate_cagr(start, end, years):
    return ((end / start) ** (1 / years)) - 1

# Extracting years
years = len(financial_data.index) - 1  # Number of years available

# Calculate CAGR for each metric
cagr_results = {}
for column in financial_data.columns:
    try:
        start_value = financial_data[column].iloc[-1]  # Earliest year
        end_value = financial_data[column].iloc[0]  # Most recent year
        cagr_results[column] = calculate_cagr(start_value, end_value, years) * 100
    except:
        cagr_results[column] = None  # Handle missing data

# Convert to DataFrame
cagr_df = pd.DataFrame.from_dict(cagr_results, orient="index", columns=["CAGR (%)"])

# Calculate EBITDA Margin
financial_data["EBITDA Margin (%)"] = (financial_data["EBITDA"] / financial_data["Total Revenue"]) * 100

# Display results
tools.display_dataframe_to_user(name="DigitalOcean Financials", dataframe=financial_data)
tools.display_dataframe_to_user(name="CAGR Analysis", dataframe=cagr_df)
tools.display_dataframe_to_user(name="EBITDA Margin Analysis", dataframe=financial_data[["EBITDA Margin (%)"]])
