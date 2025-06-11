#!/usr/bin/python3

import requests
import subprocess
import sys
import os
from PIL import Image
from io import BytesIO

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

def get_headers():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}

def get_user_data(username):
    user_url = f"https://api.github.com/users/{username}"
    response = requests.get(user_url, headers=get_headers())
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.json().get('message')}")
    return response.json()

def get_starred_count(username):
    user_url = f"https://api.github.com/users/{username}/starred"
    response = requests.get(user_url, headers=get_headers())
    if response.status_code != 200:
        return 0
    return len(response.json())

def fetch_contributions(username):
    url = "https://api.github.com/graphql"
    headers = get_headers()
    query = """
    query($login:String!) {
      user(login:$login) {
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }"""
    variables = {"login": username}
    resp = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
    data = resp.json()
    weeks_data = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    weeks = []
    for week in weeks_data:
        levels = []
        for day in week["contributionDays"]:
            count = day["contributionCount"]
            levels.append(classify_level(count))
        weeks.append(levels)
    return weeks

def classify_level(count):
    if count == 0:
        return 0
    elif count < 3:
        return 1
    elif count < 6:
        return 2
    elif count < 10:
        return 3
    else:
        return 4

def display_contributions(weeks):
    colors = {
        0: "\x1b[48;5;232m",  # dark gray
        1: "\x1b[48;5;22m",   # dark green
        2: "\x1b[48;5;28m",   # green
        3: "\x1b[48;5;34m",   # bright green
        4: "\x1b[48;5;40m",   # light green
    }
    reset = "\x1b[0m"
    print("\n" + " " * 22 + "GitHub Contributions (Past Year):")
    for row in range(7):
        line = " " * 22
        for week in weeks:
            if row < len(week):
                level = week[row]
                color_block = f"{colors.get(level, colors[0])}  {reset}"
                line += color_block
            else:
                line += "  "
        print(line)

def display_avatar(image_url):
    try:
        subprocess.run([
                "kitten", "icat", "--align",
                "left", "--scale-up", "--place",
                "20x20@0x2", image_url])
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


## Rending ASCII
use_ascii = True
align_bottom = False

def render_ascii(image_url, width=30):
    try:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content)).convert('L')
        aspect_ratio = image.height / image.width
        height = int(aspect_ratio * width * 0.55)
        image = image.resize((width, height))

        chars = ".,:;irsXA253hMHGS#9B&@"[::-1]
        ascii_image = []

        for y in range(height):
            line = ""
            for x in range(width):
                pixel = image.getpixel((x, y))
                char = chars[pixel * len(chars) // 256]
                color_code = f"\x1b[38;5;{232 + int(pixel / 255 * 23)}m"
                line += f"{color_code}{char}{color.reset}"
            ascii_image.append(line)

        return ascii_image
    except Exception as e:
        print(color.color(color.red, f"[!] ASCII rendering failed: {e}"))
        return []

## Render Layout
def render_layout(ascii_lines, info_lines, align='top'):
    max_lines = max(len(ascii_lines), len(info_lines))
    pad_ascii = max_lines - len(ascii_lines)
    pad_info = max_lines - len(info_lines)

    ascii_lines += [''] * pad_ascii
    info_lines += [''] * pad_info

    for a, b in zip(ascii_lines, info_lines):
        print(f"{a:<45}  {b}")

def get_user_info_lines(data, starred_count, username):
    url = f"{username}@github.com"
    lines = [
        f"{color.color(color.blue, 'Username:')} {data.get('login')}",
        f"{color.color(color.yellow, 'Repos:')} {data.get('public_repos')}",
        f"{color.color(color.green, 'Bio:')} {data.get('bio') or 'N/A'}",
        f"{color.color(color.red, 'From:')} {data.get('location') or 'Not Provided'}",
        f"{color.color(color.light_red, 'Followers:')} {data.get('followers')}",
        f"{color.color(color.light_blue, 'Following:')} {data.get('following')}",
        f"{color.color(color.yellow, 'Starred repos:')} {starred_count}"
    ]
    return [f"{' ' * 2}{url}", ' ' * 2 + '-' * len(url)] + lines

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: githubfetch <username> [--heatmap]")
        sys.exit(1)

    if sys.argv[1] in ['--help', '-h']:
        print("Usage: githubfetch <username> [--ascii] [--heatmap]")
        print("  --ascii : show avatar as ASCII art")
        print("  --heatmap : show contribution graph (requires GITHUB_TOKEN)")
        print("  -h, --help : show this help message and exit")
        sys.exit(0)

    username = sys.argv[1]
    heatmap = '--heatmap' in sys.argv

    try:
        user_data = get_user_data(username)
        starred_count = get_starred_count(username)
        if '--ascii' in sys.argv:
            ascii_block = render_ascii(user_data.get('avatar_url'))
            info_block = get_user_info_lines(user_data, starred_count, username)
            render_layout(ascii_block, info_block)
        else:
            display_avatar(user_data.get('avatar_url'))
            display_user_info(user_data, starred_count, username)


        if heatmap:
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                print(color.color(color.yellow, "Warning: GITHUB_TOKEN not set. Skipping heatmap."))
            else:
                contributions = fetch_contributions(username)
                display_contributions(contributions)

    except Exception as e:
        print(color.color(color.red, str(e)))
        sys.exit(1)