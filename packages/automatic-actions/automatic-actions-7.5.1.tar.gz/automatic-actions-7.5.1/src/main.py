import requests

# https://api.github.com/repos/{owner}/{target_repos}/releases/latest

response = requests.get("https://api.github.com/repos/cxnt/automate-actions/releases/latest")
print(response.json()["name"])
