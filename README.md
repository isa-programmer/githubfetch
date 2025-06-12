# Githubfetch

A Neofetch-Like program for Github profiles

## Requirements
- Kitty terminal
- python3
- ImageMagick

## Installing
```
$ sudo curl https://raw.githubusercontent.com/isa-programmer/githubfetch/refs/heads/main/githubfetch.py -o /usr/local/bin/githubfetch
$ sudo chmod +x /usr/local/bin/githubfetch
```

## Development Setup

Clone repo

```bash
git clones git@github.com:isa-programmer/githubfetch.git
```

Move to githubfetch folder

```bash
cd githubfetch/
```

Create a virtual environment (Optional):

* To Linux or MacOs:
```bash
python -m venv venv 
. ./venv/bin/activate
```

* To Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

Run locally:

```bash
python githubfetch.py <github-username>
```

## Usage
### Basic user info
```
$ githubfetch isa-programmer
```

### With contribution heatmap
```
$ githubfetch <github-username> --heatmap
```


```bash
$ githubfetch <github-username> --ascii[=style]
```

### Options

| Style   | Description                          | Example Characters |
|---------|--------------------------------------|--------------------|
| `bold`  | Thick, high-contrast characters     | `@%#*+=-:.`        |
| `fine`  | Thin, detailed characters           | `.,:;i1tfLCG08@`   |
| `retro` | Classic terminal look               | ` .'`^",:;Il!i><~` |
| `block` | Solid block characters              | ` ░▒▓█`            |

### Optional: Contribution heatmap
Displaying the contribution heatmap along with basic user info requires a GitHub personal access token. Create one from [here](https://github.com/settings/tokens) with ```read:user``` scope, then add this line to your .bashrc or other shell config
```
export GITHUB_TOKEN="your_personal_access_token_here"
```

### Examples

```bash
# Default bold style
$ githubfetch <github-username> --ascii

# Retro style
$ githubfetch <github-username> --ascii=retro

# Block style without color
$ githubfetch <github-username> --ascii=block --nocolor
```

## Example output
![example image](https://i.imgur.com/NdmszFZ.png)

![another example](https://imgur.com/KW47JGm.png)
