import os
import requests

# https://api.github.com/repos/{owner}/{target_repos}/releases/latest



def string():
    try:
        response = requests.get("https://api.github.com/repos/cxnt/automate-actions/releases/latest")
        version = response.json()["name"]
        if version:
                return version
    except:
        pass
    return "unknown (git checkout)"
