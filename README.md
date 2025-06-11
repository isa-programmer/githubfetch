# Githubfetch

A Neofetch-Like program for Github profiles

## Requirements
- Kitty terminal
- python3

## Installing
```
$ sudo curl https://raw.githubusercontent.com/isa-programmer/githubfetch/refs/heads/main/githubfetch.py -o /usr/local/bin/githubfetch
$ sudo chmod +x /usr/local/bin/githubfetch
```

### Optional: Contribution heatmap
Displaying the contribution heatmap along with basic user info requires a GitHub personal access token. Create one from [here](https://github.com/settings/tokens) with ```read:user``` scope, then add this line to your .bashrc or other shell config
```
export GITHUB_TOKEN="your_personal_access_token_here"
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
