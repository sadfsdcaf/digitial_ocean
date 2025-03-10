import digitalocean

# Replace with your API key
api_token = "dop_v1_f78e2f80785703b9ed54b41c412c8ea0cf2b1926563de3ca65f2005e0bb33002"

# Initialize manager
manager = digitalocean.Manager(token=api_token)

# Get all droplets
droplets = manager.get_all_droplets()

for droplet in droplets:
    print(f"Droplet ID: {droplet.id}, Name: {droplet.name}, Status: {droplet.status}")
