Tyranobot
===================
![Python versions](https://img.shields.io/badge/python-2.7-blue.svg)

An easily customizable Slackbot built on the SlackClient python library.

Installation
------------
Install the Tyranobot module from [Pypi](https://pypi.python.org/pypi/tyranobot)
```bash
pip install tyranobot
```

Usage
-------
Tyranobot is meant to be extended and customized like so:
```python
import os
import re
from random import randint
from tyranobot import TyranoBot

class MyBot(TroncBot):

    def __init__(self, bot_data, *args, **kwargs):
        # Call TroncBot's initialization function
        TyranoBot.__init__(self, bot_data, *args, **kwargs)

        # Add a passive message reply
        reply = {
          "type": "passive",
          "pattern": "h[ello|i].*mybot.*",
          "response": "Hello human!",
          "action": "message"
        }
        self.add_passive_reply(reply);

        # Add an active random reply
        reply = {
          "type": "active",
          "pattern": "tell\s*(me)*\s*a*\s*joke",
          "response": [
            "https://www.youtube.com/watch?v=kTcRRaXV-fg",
            "https://www.youtube.com/watch?v=Mdqv5xIsFLM",
            "Q: Where do orcas hear music? A: Orca-stras!",
            "Q: What do you call a blind dinosaur? A: Do-you-think-he-saurus"
          ],
          "action": "random"
        }
        self.add_active_reply(reply)

        # Add an active function reply
        reply = {
          "type": "active",
          "pattern": "(?:R|roll\\s)*([1-9]*)(d|D)([1-9].*)",
          "response": "roll_dice",
          "action": "function"
        }
        self.add_active_reply(reply)

    def roll_dice(self, msg):
        """
        This is an example of a function response. When MyBot hears @MyBot Roll X dY,
        MyBot will roll X number of Y sided dice and send the result back as a Slack message.
        """
        dice = re.match(r"(?:R|roll\s)*([1-9]*)(d|D)([1-9].*)", msg)

        num_rolls = 1
        sides = dice.group(3)
        reply = ""

        # Make sure the dice has a correct number of sides
        if sides in ['4', '6', '8', '10', '20']:
            reply = ":game_die: You rolled: "
            total = 0
            # How many dice should we roll?
            if dice.group(1) and dice.group(1) != '':
                num_rolls = int(dice.group(1))

            # Roll as many dice as indicated, recording each result in reply
            this_roll = 1
            while (this_roll <= num_rolls):
                roll = randint(1, int(sides))
                total = total + roll
                reply = reply + str(roll) + ', '
                this_roll = this_roll + 1

            # Stri the last comman and add the total roll to the end o the reply
            reply = reply.strip(', ')
            reply = reply + ". Total roll: " + str(total)
        else:
            reply = "I don't have a dice like that"

        return reply
```

Reply Objects
-------
Tyranobot responds to messages via a list of reply objects. A reply object is a dictionary with the following structure:
```python
{
  "type": "passive|active",
  "pattern": "(.*?)a regex pattern(.*?)",
  "response": "string|array|function name",
  "action": "message|random|function"
}
```
Key | Value
------------ | -------------
`type` |The type of reply this is. Expected values are "passive" or "active". See Reply Types below for details.
`pattern` | A regular expression string that Tyranobot should use to identify messages it should respond to. Tyranobot automatically converts incoming messages to lowercase to make regex matching simpler.
`response`| Tyranobot's response to any messages that match the `pattern`. Can be a string, list(array), or the name of a callable function depending on the value of  `action`.
`action`| The action that Tyranobot is making to reply. Expected values are "message", "random", or "function". See Reply Actions below for more details.


Reply Types
-------
Tyranobot has two reply types:

Passive: Passive replies are replies Tyranobot can use to reply to any incidental chatter in whatever channel(s) it has been invited too. 

Active: Active replies are replies that Tyranobot can use to reply to targets @tyranobot messages.


Reply Actions
-------
Message: A simple message reply. Tyranobot will reply to the received message with a simple string message. 

Random: Tyranobot will reply to the received message by randomly selecting one of a list of possible replies

Function (Advanced): Tyranobot will reply to the received message with the output of the named function. Tyranobot will pass the received message as arguments to the named function for processing.

(Coming soon: Attachments)


Adding Replies
-------
Tyranobot has 3 options for adding replies to it's repotoire. 

`add_passive_reply(reply dict)`: Adds a single passive reply to Tyranobot's list. The `type` key can be omitted from the passed reply dict.

`add_active_reply(reply dict)`: Adds a single active reply to Tyranobot's list. The `type` key can be omitted from the passed reply dict.

`add_replies(reply list)`: Adds a list of replies to Tyranobot. Most useful during the initializatio process. Accepts a list(array) of reply dicts as an argument. Can even be used to load a list of replies from an external file like so:

```python
 # Load list of replies from a json file
filepath = os.path.dirname(os.path.realpath(__file__)) + "/replies.json"
self.add_replies(filepath)
```
