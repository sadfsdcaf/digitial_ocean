import requests

api_token = "dop_v1_f78e2f80785703b9ed54b41c412c8ea0cf2b1926563de3ca65f2005e0bb33002"
headers = {"Authorization": f"Bearer {api_token}"}
url = "https://api.digitalocean.com/v2/account"

response = requests.get(url, headers=headers)
print(response.json())
