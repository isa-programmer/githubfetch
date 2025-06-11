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

## Example output
![example image](https://i.imgur.com/NdmszFZ.png)
