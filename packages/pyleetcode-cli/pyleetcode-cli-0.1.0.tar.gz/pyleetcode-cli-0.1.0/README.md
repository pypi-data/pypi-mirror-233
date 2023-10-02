# Leetcode CLI
Get your Leetcode account into the terminal. Search for problems, solve them and submit.

## Installation
#### Windows
```
pip install pyleetcode-cli
```

#### Linux
```
sudo pip install pyleetcode-cli
```

## Configuration
For this software to work you need to be logged into your Leetcode account. Your Leetcode `session_id` (can be found in cookies) is required for client initialization.
#### Chrome / Edge
``` chrome://settings/cookies/detail?site=leetcode.com ```
After you get your `session_id` you can either paste it into the right place in `config.yaml` file or use the CLI for the configuration:
``` 
leet config session_id YOUR_SESSION_ID
```

## Usage
```
Leet CLI

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

Commands:
  {config,stats,list,problem,today,submission,submit}
    config              Configure the CLI
    stats               Display statistics
    list                Display problem list
    problem             Display problem
    today               Display today's problem.
    submission          Download submission code
    submit              Submit code answer
```
