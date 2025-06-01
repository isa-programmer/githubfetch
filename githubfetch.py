#!/usr/bin/python3
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
        self.light_blue = "\x1b[38;5;4m"
        self.light_red = "\x1b[38;5;9m"
        self.blue = "\x1b[38;5;21m"
        self.reset = "\x1b[00m"
    def color(self,color_name,text):
        return f"{color_name}{text}{color.reset}"
        
color = Color()
indent = " " * 25
username = sys.argv[1]
url = f"https://api.github.com/users/{username}"

response = requests.get(url)
if not response.ok:
    print(f"{color.red}Error:{response.status_code}")
    sys.exit()

data = response.json()

try:
    subprocess.run([
                "kitten","icat","--align",
                "left","--scale-up","--place"
                ,"20x20@0x0",data.get('avatar_url')])
except FileNotFoundError:
    print(color.red,"Kitty not installed!")
    sys.exit()
    
elements = [
    {"text":color.color(color.light_blue,"Username:"),"value":data.get('login')},
    {"text":color.color(color.yellow,"Repos:"),"value":data.get('public_repos')},
    {"text":color.color(color.green,"Bio:"),"value":data.get('bio','N/A')},
    {"text":color.color(color.red,"From:"),"value":data.get('location','Not Provided')},
    {"text":color.color(color.light_red,"Followers:"),"value":data.get('followers')},
    {"text":color.color(color.blue,"Following:"),"value":data.get('following')},
]

bar_color = color.yellow
vertical_bar = color.color(bar_color,"║")
top_bar = color.color(bar_color,"╔══════════════════════════════════════════╗")
bottom_bar = color.color(bar_color,"╚══════════════════════════════════════════╝")

print(f"{indent}{top_bar}")

for element in elements:
    print(f"{indent}{vertical_bar} {element['text']} {element['value']}")
    
print(f"{indent}{bottom_bar}")

print("\n\n\n")
