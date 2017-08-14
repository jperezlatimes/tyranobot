Tyranobot
===================
![Python versions](https://img.shields.io/badge/python-2.7-blue.svg)

An easily customizable Slackbot built on the SlackClient python library

Installation
------------
Install the tricerabot module from [Pypi](https://pypi.python.org/pypi/tricerabot)
```bash
pip install tricerabot
```

Usage
-------
Extend the class


Reply Types
-------
Passive:

Active:


Reply Actions
-------
Message:

Random:

Function:


Adding Replies
-------
add_passive_reply

add_active_reply

add_replies


```
{
  "type": "passive|active",
  "pattern": "(.*?)regex|pattern(.*?)",
  "response": "string|array|function name",
  "action": "message|random|function"
}
```
