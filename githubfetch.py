#!/usr/bin/python3

import requests
import base64
import sys
import os
import sixel
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

    def color(self, color_name, text):
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
        raise Exception(
            f"Error: {response.status_code} - {response.json().get('message')}"
        )
    return response.json()


def get_starred_count(username):
    starred_url = f"https://api.github.com/users/{username}/starred"
    response = requests.get(starred_url, headers=get_headers())
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
    resp = requests.post(
        url, json={"query": query, "variables": variables}, headers=headers
    )
    data = resp.json()
    weeks_data = data["data"]["user"]["contributionsCollection"][
        "contributionCalendar"
    ]["weeks"]
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
        0: "",  # Dark gray
        1: "\x1b[48;5;22m",  # Dark green
        2: "\x1b[48;5;28m",  # Medium green
        3: "\x1b[48;5;34m",  # Bright green
        4: "\x1b[48;5;40m",  # Light green
    }
    reset = "\x1b[0m"

    print("\nGitHub Contributions (Past Year):\n")
    for row in range(7):
        line = ""
        for week in weeks:
            if row < len(week):
                level = week[row]
                line += f"{colors.get(level, colors[0])}  {reset}"
            else:
                line += "  "
        print(line)

    print("\n" + "Less " + "".join(f"{colors[i]}  {reset}" for i in range(5)) + " More")


def detect_protocol():
    term = os.environ.get("TERM", "")
    if "xterm-kitty" in term or "xterm-ghostty" in term:
        return "kitty"
    elif "foot" in term or "xterm" in term:
        return "sixel"
    else:
        return "None"


def display_avatar(image_url):
    try:
        # Download the image
        response = requests.get(image_url)
        response.raise_for_status()

        # Open the image with pillow
        img = Image.open(BytesIO(response.content))

        # Resize the image
        img = img.resize((180, 180))

        buf = BytesIO()
        img.save(buf, format="png")

        protocol = detect_protocol()
        if protocol == "kitty":
            kitty_protocol(buf)
        elif protocol == "sixel":
            sixel_protocol(buf)
        else:
            pass

    except Exception as e:
        print("Error:", e)
        sys.exit(1)


def display_user_info(data, starred_count, username):
    github_url = f"{username}@github.com"
    indent = " " * 22

    elements = [
        {
            "text": color.color(color.light_blue, "Username:"),
            "value": data.get("login"),
        },
        {
            "text": color.color(color.yellow, "Repos:"),
            "value": data.get("public_repos"),
        },
        {
            "text": color.color(color.green, "Bio:"),
            "value": data.get("bio", "N/A") or "N/A",
        },
        {
            "text": color.color(color.red, "From:"),
            "value": data.get("location", "Not Provided"),
        },
        {
            "text": color.color(color.light_red, "Followers:"),
            "value": data.get("followers"),
        },
        {
            "text": color.color(color.light_blue, "Following:"),
            "value": data.get("following"),
        },
        {"text": color.color(color.yellow, "Starred repos:"), "value": starred_count},
    ]

    print(f"{indent} {github_url}")
    print(f"{indent} {'-'*len(github_url)}")

    for element in elements:
        print(f"{indent} {element['text']} {element['value']}")

    print("\n")


## Rendering ASCII
use_ascii = True
align_bottom = False


def render_ascii(image_url, width=30, style="bold", use_color=True):
    try:
        # Dynamic style selection
        styles = {
            "bold": "@%#*+=-:. "[::-1],
            "fine": ".,:;i1tfLCG08@"[::-1],
            "block": " ░▒▓█"[::-1],
            "retro": " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$",
        }
        chars = styles.get(style, styles["bold"])

        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content)).convert("L")

        # Auto-size to terminal
        import os

        max_width = os.get_terminal_size().columns - 10
        width = min(width, max_width)

        aspect_ratio = image.height / image.width
        height = int(aspect_ratio * width * 0.55)
        image = image.resize((width, height))

        ascii_image = []
        for y in range(height):
            line = ""
            for x in range(width):
                pixel = image.getpixel((x, y))
                char = chars[min(len(chars) - 1, pixel * len(chars) // 256)]

                if use_color:
                    color_code = f"\x1b[38;5;{232 + (pixel * 23 // 255)}m"
                    line += f"{color_code}{char}\x1b[0m"
                else:
                    line += char
            ascii_image.append(line)

        return ascii_image

    except Exception as e:
        print(f"\x1b[31m[!] Error: {e}\x1b[0m", file=sys.stderr)
        return []


## Render Layout
def render_layout(ascii_lines, info_lines, align="top"):
    max_lines = max(len(ascii_lines), len(info_lines))
    pad_ascii = max_lines - len(ascii_lines)
    pad_info = max_lines - len(info_lines)

    ascii_lines += [""] * pad_ascii
    info_lines += [""] * pad_info

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
        f"{color.color(color.yellow, 'Starred repos:')} {starred_count}",
    ]
    return [f"{' ' * 2}{url}", " " * 2 + "-" * len(url)] + lines


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: githubfetch <username> [--ascii[=style]] [--heatmap] [--nocolor]")
        print("Available styles: bold, fine, block, sketch, invert, minimal, retro")
        sys.exit(1)

    if sys.argv[1] in ["--help", "-h"]:
        print("GitHub User Fetcher with Enhanced ASCII Art")
        print("Usage: githubfetch <username> [options]")
        print("\nOptions:")
        print("  --ascii[=style]  Show avatar as ASCII art (default: bold)")
        print("                   Available styles:")
        print("                   - bold: Thick characters (@%#*)")
        print("                   - fine: Thin characters (.,:;)")
        print("                   - block: Block characters (█▓▒░)")
        print("                   - retro: Classic terminal look")
        print("  --nocolor        Disable colored ASCII output")
        print("  --heatmap        Show contribution graph (requires GITHUB_TOKEN)")
        print("  -h, --help       Show this help message")
        sys.exit(0)

    username = sys.argv[1]
    heatmap = "--heatmap" in sys.argv
    use_color = "--nocolor" not in sys.argv

    # Parse ASCII style
    ascii_style = "bold"
    for arg in sys.argv:
        if arg.startswith("--ascii="):
            ascii_style = arg.split("=")[1].lower()
        elif arg == "--ascii":
            ascii_style = "bold"  # default

    try:
        user_data = get_user_data(username)
        starred_count = get_starred_count(username)

        if "--ascii" in sys.argv or any(a.startswith("--ascii=") for a in sys.argv):
            ascii_block = render_ascii(
                user_data.get("avatar_url"), style=ascii_style, use_color=use_color
            )
            info_block = get_user_info_lines(user_data, starred_count, username)
            render_layout(ascii_block, info_block)
        else:
            if use_color:
                display_avatar(user_data.get("avatar_url"))
            else:
                # Display grayscale avatar if --nocolor
                img = Image.open(
                    BytesIO(requests.get(user_data.get("avatar_url")).content).convert(
                        "L"
                    )
                )
                img.show()
            display_user_info(user_data, starred_count, username)

        if heatmap:
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                print(
                    "\x1b[33mWarning: GITHUB_TOKEN not set. Skipping heatmap.\x1b[0m",
                    file=sys.stderr,
                )
            else:
                contributions = fetch_contributions(username)
                display_contributions(contributions)

    except Exception as e:
        print(f"\x1b[31mError: {str(e)}\x1b[0m", file=sys.stderr)
        sys.exit(1)
