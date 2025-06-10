#!/usr/bin/python3

import requests
import subprocess
import sys

if len(sys.argv) < 2:
    print(f"Usage: githubfetch <your-github-username>")
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
    
def get_user_data(username):
    user_url = f"https://api.github.com/users/{username}"
    response = requests.get(user_url)
    return response.json()

def get_starred_count(username):
    user_url = f"https://api.github.com/users/{username}/starred"
    response = requests.get(user_url)
    return response.json()

def display_avatar(image_url):
    try:
        subprocess.run([
                "kitten", "icat", "--align",
                "left", "--scale-up", "--place",
                "20x20@0x0", image_url])
    
    except FileNotFoundError:
        print(color.red,"Kitty Terminal not installed!", color.reset)
        sys.exit(1)

def display_user_info(data, starred_count, username):
    github_url = f"{username}@github.com"
    indent = " " * 22

    elements = [
        {"text":color.color(color.light_blue,"Username:"),"value":data.get('login')},
        {"text":color.color(color.yellow,"Repos:"),"value":data.get('public_repos')},
        {"text":color.color(color.green,"Bio:"),"value":data.get('bio','N/A') or 'N/A'},
        {"text":color.color(color.red,"From:"),"value":data.get('location','Not Provided')},
        {"text":color.color(color.light_red,"Followers:"),"value":data.get('followers')},
        {"text":color.color(color.light_blue,"Following:"),"value":data.get('following')},
        {"text":color.color(color.yellow,"Starred repos:"),"value":starred_count},
    ]

    print(f"{indent} {github_url}")
    print(f"{indent} {'-'*len(github_url)}")

    for element in elements:
        print(f"{indent} {element['text']} {element['value']}")

    print("\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: githubfetch <your-github-username>")
        sys.exit(1)

    color = Color()
    username = sys.argv[1]

    try:
        user_data = get_user_data(username)
        starred_count = get_starred_count(username)
        data_starred = len(starred_count)
        display_avatar(user_data.get('avatar_url'))
        display_user_info(user_data, data_starred, username)

    except Exception as e:
        print(color.color(color.red, str(e)))
        sys.exit(1)
