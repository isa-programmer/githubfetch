
# GitHubFetch

A **Neofetch-like** CLI tool that beautifully displays GitHub profile information in your terminal — complete with ASCII art and contribution heatmaps.


## ✨ Features

- GitHub user info with bio, followers, repos, etc.
- ASCII-rendered GitHub profile picture (multiple styles)
- Contribution heatmap visualization
- Works in your terminal — especially tailored for **Kitty**


## 🔧 Requirements

For local (non-Docker) usage:

- Python 3.7+
- [Kitty Terminal](https://sw.kovidgoyal.net/kitty/) (for advanced rendering)
- [ImageMagick](https://imagemagick.org/) (for image-to-ASCII conversion)


## Installing (Standalone)

```bash
sudo curl https://raw.githubusercontent.com/isa-programmer/githubfetch/refs/heads/main/githubfetch.py -o /usr/local/bin/githubfetch
sudo chmod +x /usr/local/bin/githubfetch
````


## Development Setup

Clone the repository:

```bash
git clone git@github.com:isa-programmer/githubfetch.git
cd githubfetch/
```

Set up virtual environment (optional but recommended):

### For Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
```

### For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run locally:

```bash
python githubfetch.py <github-username>
```

---

## Docker Usage

### Build the image

```bash
docker build -t gitfetch:latest .
```

### ▶️ Run the CLI

```bash
docker run -it gitfetch:latest <github-username> [options]
```

### ✅ Examples

```bash
# Basic usage
docker run -it gitfetch:latest <github-username> --ascii --heatmap

# With GitHub token (inline)
docker run -it --env GITHUB_TOKEN="your_token" gitfetch:latest <github-username> --ascii --heatmap

# Using .env file
docker run -it --env-file .env gitfetch:latest <github-username> --ascii --heatmap
```

> **Note**: Always use `-it` for proper terminal output support.

---

## ⚙️ Options & Flags

### 🔹 Basic Info

```bash
githubfetch <github-username>
```

### 🔹 With ASCII Avatar

```bash
githubfetch <github-username> --ascii[=style]
```

### 🔹 With Contribution Heatmap

```bash
githubfetch <github-username> --heatmap
```

### 🔹 ASCII Styles

| Style   | Description               | Example Characters   |
| ------- | ------------------------- | -------------------- |
| `bold`  | Thick, high-contrast      | `@%#*+=-:.`          |
| `fine`  | Thin, detailed characters | `.,:;i1tfLCG08@`     |
| `retro` | Classic terminal style    | ` .'`^",:;Il!i><\~\` |
| `block` | Solid block-based look    | ` ░▒▓█`              |

You can also disable color rendering with `--nocolor`.

---

## Using GitHub Token (for heatmap or high-rate API access)

Authenticated requests are needed for:

* Contribution heatmap
* Higher API rate limits
* Private info (if token has permissions)

### Set the token:

#### Option 1: Shell Config (recommended for local use)

```bash
export GITHUB_TOKEN="your_personal_access_token"
```

#### Option 2: Docker `.env` file

Create `.env` file:

```env
GITHUB_TOKEN=your_personal_access_token
```

Then run with:

```bash
docker run -it --env-file .env gitfetch:latest <username> --ascii --heatmap
```
---

## Examples

```bash
# Default style
githubfetch <github-username> --ascii

# Retro ASCII
githubfetch <github-username> --ascii=retro

# Block style, no color
githubfetch <github-username> --ascii=block --nocolor

# Heatmap with ASCII
githubfetch <github-username> --ascii --heatmap
```


## 🤝 Contributing

Contributions, issues and feature requests are welcome!

1. Fork the repo
2. Create a new branch
3. Submit a PR


## Example output
![example image](https://i.imgur.com/NdmszFZ.png)

![another example](https://imgur.com/KW47JGm.png)
