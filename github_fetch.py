import requests
import subprocess
import sys

if len(sys.argv) < 2:
    print("Usage: ./github_fetch.py <your-github-name>")
    sys.exit()
class Color:
    def __init__(self):
        self.red = "\x1b[38;5;1m"
        self.green = "\x1b[38;5;2m"
        self.yellow = "\x1b[38;5;3m"
        self.blue = "\x1b[38;5;4m"
        self.light_red = "\x1b[38;5;9m"
        self.dark_blue = "\x1b[38;5;17m"
        self.reset = "\x1b[00m"
        
color = Color()
indent = " " * 25
username = sys.argv[1]
url = f"https://api.github.com/users/{username}"

response = requests.get(url)
if not response.ok:
    print(f"{color.red}Error:{response.status_code}")
    sys.exit()
data = response.json()
subprocess.run(["kitten","icat","--align","left","--scale-up","--place","20x20@0x0",data.get('avatar_url')])

print(f"{color.blue + indent} Username:{color.reset}{data.get('login')} ")
print(f"{color.yellow + indent} Repos:{color.reset}{data.get('public_repos')} ")
print(f"{color.green + indent} Bio:{color.reset}{data.get('bio','...')}")
print(f"{color.red + indent} From:{color.reset}{data.get('location','Undefined')}")
print(f"{color.light_red + indent} Followers:{color.reset}{data.get('followers')}")
print(f"{color.dark_blue + indent} Following:{color.reset}{data.get('following')}")
print("\n\n\n\n")
