# douglog

A simple command line program that quickly creates and opens single log files with a date in a semi-organized way. Use tools like `fzf` or `ripgrep` to search through the generated logs.

## Example Config

Default location is `~/.config/dlog.toml`.

```
editor = "nvim"
home = "~/dlogs"
logs = ["homelab", "work"]
```

`home` is where you want to store your logs. `logs` is a list of your logs (to organize separate logging). `editor` sets your editor.

## Usage

```
$ dlog log <log-name>
```
