# Premium Bonds Prize Checker

A simple CLI tool to check whether you have won anything for the current month in the UK's Premium Bonds.

# Install

The recommended way to install is to use `pipx`:

`pipx install premium-bonds-prize-checker`

# Usage

`premium-bonds-prize-checker [holders_numbers]`

Multiple holders numbers can be checked by specifying them with commas, e.g. `123456,987654`.

If the holders number is omitted then a config will be loaded from `~/.config/premium-bonds/config.json` which has the format:

```
{"comment or name": "<holders-number>"}
```
