import requests

api_token = "dop_v1_1718be1e4d7b0a5e789868df3b6fba2ef0c403ee21f3d31cf91bf0419900aa1c"
headers = {"Authorization": f"Bearer {api_token}"}
url = "https://api.digitalocean.com/v2/account"

response = requests.get(url, headers=headers)

# Debug: Print response
print(response.status_code)  # Check HTTP response code
print(response.json())  # See the full API response
