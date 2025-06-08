#!/usr/bin/python3

import requests
import subprocess
import sys

if len(sys.argv) < 2:
    print("Usage: ./github_fetch.py <your-github-name>")
    sys.exit(1)

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
indent = " " * 22
username = sys.argv[1]
github_url = f"{username}@github.com"
url = f"https://api.github.com/users/{username}"
response = requests.get(url)

if not response.ok:
    print(f"{color.red}Error:{response.status_code}")
    sys.exit(1)

data = response.json()

try:
    subprocess.run([
                "kitten", "icat", "--align",
                "left", "--scale-up", "--place",
                "20x20@0x0", data.get('avatar_url')])
    
except FileNotFoundError:
    print(color.red,"Kitty Terminal not installed!", color.reset)
    sys.exit(1)
    
elements = [
    {"text":color.color(color.light_blue,"Username:"),"value":data.get('login')},
    {"text":color.color(color.yellow,"Repos:"),"value":data.get('public_repos')},
    {"text":color.color(color.green,"Bio:"),"value":data.get('bio','N/A') or 'N/A'},
    {"text":color.color(color.red,"From:"),"value":data.get('location','Not Provided')},
    {"text":color.color(color.light_red,"Followers:"),"value":data.get('followers')},
    {"text":color.color(color.light_blue,"Following:"),"value":data.get('following')},
]


print(f"{indent} {github_url}")
print(f"{indent} {'-'*len(github_url)}")

for element in elements:
    print(f"{indent} {element['text']} {element['value']}")

print("\n\n\n")
