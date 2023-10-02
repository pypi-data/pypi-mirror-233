# Platitude Terminal
## by Platitude.ai
Natural language AI suggestions and completions for the command line!

Platitude.ai Terminal 

- translates natural language requests into valid bash syntax without ever leaving your terminal!
- explains any command it generates, before you run it
- copies the command to your input buffer upon exit so that it's ready for you to edit and use right away!

## Installation

To install from PyPi into a new Python virtual env (recommended):

```
python3 -m venv myenv      # create new virtual env
source myenv/bin/activate  # For macOS and Linux
myenv\Scripts\activate     # For Windows

pip3 install PlatitudeTerminal   # install
```

To install from PyPi directly into default install directory, skip the venv commands then make sure to add the install script location to PATH. Look for yellow text that says something like "WARNING: The script ai is installed in '/../Python/3.8/bin' which is not on PATH." Then: 

`export PATH=$PATH:/../Python/3.8/bin`

---

## Usage


### - `ai how` (do I accomplish this task?)

`ai how "<task description in english>"`

`ai how "test ssl using tls1.2"`

---

### - `ai chat` (talk to ChatGPT in your terminal)

`ai chat "<query>"`

`ai chat "write a haiku about basketball"`

---

### - `ai what` (does this command do?)

`ai what "<command text>"`

`ai what "openssl s_client -connect google.com:443 -tls1_2"`

----

### - `ai alternatives` (suggest other tools that might accomplish a similar goal)

`ai alternatives "openssl s_client -connect google.com:443 -tls1_2"`

----

### Disclaimer

DO NOT run queries suggested by this tool without doing your own research on their usage. The results of AI translations are NOT deterministic, so always understand each command you run. DO NOT ask for commands that may be desctructive or illegal to run. This tool is intended to be a quick way to find the most likely command that may achieve your stated goal, but may not have access to the most up-to-date documentation, and does not necessarily understand the usage of any specific command line tool.
