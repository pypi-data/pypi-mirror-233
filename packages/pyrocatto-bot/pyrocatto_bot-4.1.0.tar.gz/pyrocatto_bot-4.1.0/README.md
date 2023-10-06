# Pyrocatto
> A multiclient bot that leverages pyrogram's smart plugins system.
<br />

# Installation
### With optional speedups (Installs packages like TgCrypto for Pyrogram):
- `pip install pyrocatto_bot[speedups]`
### Without optional speedups:
- `pip install pyrocatto_bot`
<br />

# Usage:
> after setting up sessions and writing the configuration
### Make sure to be in the directory the plugins are located in!
- `python -m pyrocatto_bot --session-dir <session_dir> --config <config_file>`
### For debugging:
- `python -m pyrocatto_bot --session-dir <session_dir> --config <config_file> --debug`
<br />

# Setting up sessions to use in configs:
### For User account:
- `python -m pyrocatto_sg create-user-session --session-dir <session_dir>`
### For Bot account:
- `python -m pyrocatto_sg create-bot-session --session-dir <session_dir>`
<br />

# Example configuration:
```
user: &user
  plugins:
    root: 'plugins.user_plugins'
    include: Null
    exclude: Null

  addons:
    wheel_userids:
      - 1698923450

sessions: # name: {options}
  cattobot: {<<: *user}
```
<br />

### Your own client sets:
```
#custom: &custom
  <<: *default # This line ensures non recursive inheritance from default client set
  plugins:
    root:
      - 'plugins.extra_plugins'
    include:
      - 'extra_plugin'
    exclude:
      - 'unwanted'

  addons:
    wheel_userids:
      - 12312421
      - 25235423
      - 21424111
      - ...

sessions:
  something: {<<: *custom}
```
<br />

### A single value to modify:
```
extra_plugins: &extra_plugins
  root: 'extra_plugins'

sessions:
  something: {<<: *default, *extra_plugins}
  anotherthing: {<<: *default, plugins: {root: 'extra_plugins'}}
```
