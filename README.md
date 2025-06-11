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
Create a GitHub personal access token [here]("https://github.com/settings/tokens") with the ```read:user``` scope, then add this line to your .bashrc or other shell config and source it.
```
export GITHUB_TOKEN="your_personal_access_token_here"
```

## Usage
```
$ githubfetch isa-programmer
```
## Example output
![example image](https://i.imgur.com/NdmszFZ.png)
